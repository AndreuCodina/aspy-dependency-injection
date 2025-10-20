import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, final, get_type_hints, override

from aspy_dependency_injection.service_lookup.call_site_visitor import CallSiteVisitor

if TYPE_CHECKING:
    from aspy_dependency_injection.service_lookup.constructor_call_site import (
        ConstructorCallSite,
    )
    from aspy_dependency_injection.service_lookup.service_call_site import (
        ServiceCallSite,
    )
    from aspy_dependency_injection.service_provider_engine_scope import (
        ServiceProviderEngineScope,
    )


@dataclass
class _RuntimeResolverContext:
    scope: ServiceProviderEngineScope


@final
class CallSiteRuntimeResolver(CallSiteVisitor[_RuntimeResolverContext, object | None]):
    INSTANCE: ClassVar[CallSiteRuntimeResolver]

    def resolve(
        self, call_site: ServiceCallSite, scope: ServiceProviderEngineScope
    ) -> object | None:
        return self._visit_call_site(call_site, _RuntimeResolverContext(scope=scope))

    @override
    def _visit_constructor(
        self,
        constructor_call_site: ConstructorCallSite,
        argument: _RuntimeResolverContext,
    ) -> object:
        return self._create_instance(constructor_call_site.service_type)

    def _create_instance(self, service_type: type) -> object:
        """Recursively create an instance of the service type."""
        init_method = service_type.__init__
        init_signature = inspect.signature(init_method)
        init_type_hints = get_type_hints(init_method)
        parameter_names = init_signature.parameters.keys()
        arguments: dict[str, object] = {}

        for parameter_name in parameter_names:  # init_signature.parameters.items()
            if parameter_name in ["self", "args", "kwargs"]:
                continue

            parameter_type = init_type_hints[parameter_name]
            arguments[parameter_name] = self._create_instance(parameter_type)

        if len(arguments) == 0:
            return service_type()

        return service_type(**arguments)


CallSiteRuntimeResolver.INSTANCE = CallSiteRuntimeResolver()
