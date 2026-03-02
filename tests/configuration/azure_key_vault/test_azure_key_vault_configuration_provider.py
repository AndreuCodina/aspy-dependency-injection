from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

import pytest
from pytest_mock import MockerFixture

from wirio._utils._extra_dependencies import ExtraDependencies
from wirio.configuration.convention_changer import ConventionChanger

if TYPE_CHECKING:
    from azure.identity.aio import DefaultAzureCredential
    from azure.keyvault.secrets import KeyVaultSecret, SecretProperties
    from azure.keyvault.secrets.aio import SecretClient

    from wirio.configuration.azure_key_vault.azure_key_vault_configuration_provider import (
        AzureKeyVaultConfigurationProvider,
    )
else:
    DefaultAzureCredential = Any
    KeyVaultSecret = Any
    SecretProperties = Any
    SecretClient = Any
    AzureKeyVaultConfigurationProvider = Any

try:
    from azure.identity.aio import DefaultAzureCredential
    from azure.keyvault.secrets import KeyVaultSecret, SecretProperties
    from azure.keyvault.secrets.aio import SecretClient

    from wirio.configuration.azure_key_vault.azure_key_vault_configuration_provider import (
        AzureKeyVaultConfigurationProvider,
    )
except ImportError:
    pass


@pytest.mark.skipif(
    not ExtraDependencies.is_azure_key_vault_installed(),
    reason=ExtraDependencies.AZURE_KEY_VAULT_NOT_INSTALLED_ERROR_MESSAGE,
)
class TestAzureKeyVaultConfigurationProvider:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.vault_url = "https://example.vault.azure.net"

    async def test_load_enabled_secrets(self, mocker: MockerFixture) -> None:
        credential = mocker.create_autospec(DefaultAzureCredential, instance=True)
        credential.__aenter__.return_value = credential
        credential.__aexit__.return_value = None

        enabled_secret_name = "EnabledSecretName"  # noqa: S105
        enabled_secret_value = "SecretValue"  # noqa: S105
        disabled_secret_name = "DisabledSecretName"  # noqa: S105

        enabled_secret_properties = mocker.create_autospec(
            SecretProperties,
            instance=True,
        )
        enabled_secret_properties.name = enabled_secret_name
        enabled_secret_properties.enabled = True

        disabled_secret_properties = mocker.create_autospec(
            SecretProperties,
            instance=True,
        )
        disabled_secret_properties.name = disabled_secret_name
        disabled_secret_properties.enabled = False

        async def list_properties_of_secrets() -> AsyncIterator[SecretProperties]:
            yield enabled_secret_properties
            yield disabled_secret_properties

        secret_client = mocker.create_autospec(SecretClient, instance=True)
        secret_client.__aenter__.return_value = secret_client
        secret_client.__aexit__.return_value = None
        secret_client.list_properties_of_secrets.return_value = (
            list_properties_of_secrets()
        )

        key_vault_secret_mock = mocker.create_autospec(
            KeyVaultSecret,
            instance=True,
        )
        key_vault_secret_mock.value = enabled_secret_value

        secret_client.get_secret.return_value = key_vault_secret_mock
        secret_client_patch = mocker.patch(
            f"{AzureKeyVaultConfigurationProvider.__module__}.{SecretClient.__qualname__}",
            autospec=True,
            return_value=secret_client,
        )
        provider = AzureKeyVaultConfigurationProvider(
            url=self.vault_url,
            credential=credential,
        )

        await provider.load()

        assert provider.data == {
            ConventionChanger.to_snake_case(enabled_secret_name): enabled_secret_value
        }
        secret_client.get_secret.assert_called_once_with(enabled_secret_name)
        secret_client_patch.assert_called_once_with(
            vault_url=self.vault_url,
            credential=credential,
        )

    async def test_use_default_azure_credential_when_none_is_passed(
        self, mocker: MockerFixture
    ) -> None:
        default_credential = mocker.create_autospec(
            DefaultAzureCredential, instance=True
        )
        default_credential.__aenter__.return_value = default_credential
        default_credential.__aexit__.return_value = None

        async def iterate_secret_properties() -> AsyncIterator[Any]:
            if False:
                secret_properties = mocker.create_autospec(
                    SecretProperties,
                    instance=True,
                )
                secret_properties.name = None
                secret_properties.enabled = False
                yield secret_properties

        secret_client = mocker.create_autospec(SecretClient, instance=True)
        secret_client.__aenter__.return_value = secret_client
        secret_client.__aexit__.return_value = None
        secret_client.list_properties_of_secrets.return_value = (
            iterate_secret_properties()
        )

        default_credential_patch = mocker.patch(
            f"{AzureKeyVaultConfigurationProvider.__module__}.{DefaultAzureCredential.__qualname__}",
            autospec=True,
            return_value=default_credential,
        )
        secret_client_patch = mocker.patch(
            f"{AzureKeyVaultConfigurationProvider.__module__}.{SecretClient.__qualname__}",
            autospec=True,
            return_value=secret_client,
        )
        provider = AzureKeyVaultConfigurationProvider(url=self.vault_url)

        await provider.load()

        default_credential_patch.assert_called_once_with()
        secret_client_patch.assert_called_once_with(
            vault_url=self.vault_url,
            credential=default_credential,
        )

    async def test_skip_secret_without_name(self, mocker: MockerFixture) -> None:
        credential = mocker.create_autospec(DefaultAzureCredential, instance=True)
        credential.__aenter__.return_value = credential
        credential.__aexit__.return_value = None

        unnamed_secret_properties = mocker.create_autospec(
            SecretProperties,
            instance=True,
        )
        unnamed_secret_properties.name = None
        unnamed_secret_properties.enabled = True

        async def list_properties_of_secrets() -> AsyncIterator[SecretProperties]:
            yield unnamed_secret_properties

        secret_client = mocker.create_autospec(SecretClient, instance=True)
        secret_client.__aenter__.return_value = secret_client
        secret_client.__aexit__.return_value = None
        secret_client.list_properties_of_secrets.return_value = (
            list_properties_of_secrets()
        )

        mocker.patch(
            f"{AzureKeyVaultConfigurationProvider.__module__}.{SecretClient.__qualname__}",
            autospec=True,
            return_value=secret_client,
        )
        provider = AzureKeyVaultConfigurationProvider(
            url=self.vault_url,
            credential=credential,
        )

        await provider.load()

        assert provider.data == {}
        secret_client.get_secret.assert_not_called()
