from typing import TYPE_CHECKING, ClassVar, final

from aspy_dependency_injection.service_lookup.call_site_visitor import CallSiteVisitor

if TYPE_CHECKING:
    from aspy_dependency_injection.service_lookup.service_call_site import (
        ServiceCallSite,
    )
    from aspy_dependency_injection.service_provider_engine_scope import (
        ServiceProviderEngineScope,
    )


@final
class CallSiteRuntimeResolver(CallSiteVisitor[None, None]):
    INSTANCE: ClassVar[CallSiteRuntimeResolver]

    def resolve(
        self, call_site: ServiceCallSite, scope: ServiceProviderEngineScope
    ) -> object | None:
        raise NotImplementedError
