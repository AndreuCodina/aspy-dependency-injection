from abc import ABC
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from aspy_dependency_injection.service_lookup.constructor_call_site import (
        ConstructorCallSite,
    )

TArgument = TypeVar("TArgument")
TResult = TypeVar("TResult")


class CallSiteVisitor[TArgument, TResult](ABC):  # noqa: B024
    def _visit_call_site(self, call_site: TArgument, argument: TArgument) -> TResult:
        return self._visit_no_cache(call_site, argument)

    def _visit_no_cache(self, call_site: TArgument, argument: TArgument) -> TResult:
        return self._visit_call_site_main(call_site, argument)

    def _visit_call_site_main(
        self, call_site: TArgument, argument: TArgument
    ) -> TResult:
        # return self._visit_constructor((ConstructorCallSite)call_site, argument)
        raise NotImplementedError

    def _visit_constructor(
        self, constructor_call_site: ConstructorCallSite, argument: TArgument
    ) -> TResult:
        raise NotImplementedError
