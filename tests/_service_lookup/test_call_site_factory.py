import pytest

from tests.utils.services import ServiceWithNoDependencies
from wirio._service_lookup._call_site_chain import CallSiteChain
from wirio._service_lookup._call_site_factory import CallSiteFactory
from wirio._service_lookup._constant_call_site import ConstantCallSite
from wirio._service_lookup._service_identifier import ServiceIdentifier
from wirio._service_lookup._typed_type import TypedType
from wirio.exceptions import ServiceDescriptorDoesNotExistError
from wirio.service_descriptor import ServiceDescriptor
from wirio.service_lifetime import ServiceLifetime


class TestCallSiteFactory:
    async def test_fail_when_service_descriptor_instance_does_not_exist(self) -> None:
        existing_descriptor = ServiceDescriptor.from_implementation_type(
            service_type=ServiceWithNoDependencies,
            implementation_type=ServiceWithNoDependencies,
            service_key=None,
            lifetime=ServiceLifetime.SINGLETON,
            auto_activate=False,
        )
        call_site_factory = CallSiteFactory([existing_descriptor])
        missing_descriptor = ServiceDescriptor.from_implementation_type(
            service_type=ServiceWithNoDependencies,
            implementation_type=ServiceWithNoDependencies,
            service_key=None,
            lifetime=ServiceLifetime.SINGLETON,
            auto_activate=False,
        )

        with pytest.raises(ServiceDescriptorDoesNotExistError):
            await call_site_factory.get_call_site_from_service_descriptor(
                missing_descriptor,
                CallSiteChain(),
            )

    async def test_return_overridden_call_site_when_override_exists(self) -> None:
        service_identifier = ServiceIdentifier.from_service_type(
            service_type=TypedType.from_type(ServiceWithNoDependencies)
        )
        call_site_factory = CallSiteFactory([])
        override_instance = ServiceWithNoDependencies()
        call_site_chain = CallSiteChain()

        with call_site_factory.override_service(
            service_identifier=service_identifier,
            implementation_instance=override_instance,
        ):
            call_site = await call_site_factory.get_call_site_from_service_identifier(
                service_identifier=service_identifier,
                call_site_chain=call_site_chain,
            )

        assert isinstance(call_site, ConstantCallSite)
        assert call_site.default_value is override_instance

    async def test_return_none_when_descriptor_not_registered(self) -> None:
        missing_descriptor = ServiceDescriptor.from_implementation_type(
            service_type=ServiceWithNoDependencies,
            implementation_type=ServiceWithNoDependencies,
            service_key=None,
            lifetime=ServiceLifetime.SINGLETON,
            auto_activate=False,
        )
        call_site_factory = CallSiteFactory([])

        call_site = await call_site_factory.get_call_site_from_service_descriptor(
            missing_descriptor,
            CallSiteChain(),
        )

        assert call_site is None
