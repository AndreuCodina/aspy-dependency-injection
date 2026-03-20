from typing import Final, final, override

from wirio.settings.aws_secrets_manager.aws_secrets_manager_settings_provider import (
    AwsSecretsManagerSettingsProvider,
)
from wirio.settings.settings_builder import SettingsBuilder
from wirio.settings.settings_provider import SettingsProvider
from wirio.settings.settings_source import SettingsSource


@final
class AwsSecretsManagerSettingsSource(SettingsSource):
    _secret_id: Final[str]
    _region: Final[str | None]
    _url: Final[str | None]

    def __init__(
        self, secret_id: str, region: str | None = None, url: str | None = None
    ) -> None:
        self._secret_id = secret_id
        self._region = region
        self._url = url

    @override
    def build(self, builder: SettingsBuilder) -> SettingsProvider:
        return AwsSecretsManagerSettingsProvider(
            secret_id=self._secret_id, region=self._region, url=self._url
        )
