from threading import RLock
from typing import TYPE_CHECKING, ClassVar, final

from aspy_dependency_injection._concurrent_dictionary import ConcurrentDictionary
from aspy_dependency_injection.service_identifier import ServiceIdentifier
from aspy_dependency_injection.service_lookup.constructor_call_site import (
    ConstructorCallSite,
)

if TYPE_CHECKING:
    from aspy_dependency_injection.service_collection import ServiceCollection
    from aspy_dependency_injection.service_descriptor import ServiceDescriptor
    from aspy_dependency_injection.service_lookup.call_site_chain import CallSiteChain
    from aspy_dependency_injection.service_lookup.service_call_site import (
        ServiceCallSite,
    )


@final
class CallSiteFactory:
    _DEFAULT_SLOT: ClassVar[int] = 0

    _call_site_locks: ConcurrentDictionary[ServiceIdentifier, RLock]
    _descriptor_lookup: dict[ServiceIdentifier, _ServiceDescriptorCacheItem]
    _descriptors: list[ServiceDescriptor]

    def __init__(self, services: ServiceCollection) -> None:
        self._call_site_locks = ConcurrentDictionary[ServiceIdentifier, RLock]()
        self._descriptor_lookup = {}
        self._descriptors = services.descriptors.copy()
        self._populate()

    def _populate(self) -> None:
        for descriptor in self._descriptors:
            cache_key = ServiceIdentifier.from_descriptor(descriptor)
            cache_item = self._descriptor_lookup.get(
                cache_key, _ServiceDescriptorCacheItem()
            )
            self._descriptor_lookup[cache_key] = cache_item.add(descriptor)

    def get_call_site(
        self, service_identifier: ServiceIdentifier, call_site_chain: CallSiteChain
    ) -> ServiceCallSite | None:
        return self._create_call_site(
            service_identifier=service_identifier, call_site_chain=call_site_chain
        )

    def _create_call_site(
        self, service_identifier: ServiceIdentifier, call_site_chain: CallSiteChain
    ) -> ServiceCallSite | None:
        call_site_lock = self._call_site_locks.get_or_add(
            service_identifier, lambda _: RLock()
        )

        with call_site_lock:
            return self._try_create_exact_from_service_identifier(
                service_identifier, call_site_chain
            )

    def _try_create_exact_from_service_identifier(
        self, service_identifier: ServiceIdentifier, call_site_chain: CallSiteChain
    ) -> ServiceCallSite | None:
        service_descriptor_cache_item = self._descriptor_lookup.get(
            service_identifier, None
        )

        if service_descriptor_cache_item is not None:
            return self._try_create_exact_from_service_descriptor(
                service_descriptor_cache_item.last,
                service_identifier,
                call_site_chain,
                self._DEFAULT_SLOT,
            )

        return None

    def _try_create_exact_from_service_descriptor(
        self,
        service_descriptor: ServiceDescriptor,
        service_identifier: ServiceIdentifier,
        call_site_chain: CallSiteChain,
        slot: int,
    ) -> ServiceCallSite | None:
        if not self._should_create_exact(
            service_descriptor.service_type, service_identifier.service_type
        ):
            return None

        return self._create_exact(
            service_descriptor, service_identifier, call_site_chain, slot
        )

    def _should_create_exact(self, descriptor_type: type, service_type: type) -> bool:
        return descriptor_type == service_type

    def _create_exact(
        self,
        service_descriptor: ServiceDescriptor,
        service_identifier: ServiceIdentifier,
        call_site_chain: CallSiteChain,
        slot: int,  # noqa: ARG002
    ) -> ServiceCallSite:
        if service_descriptor.has_implementation_type():
            assert service_descriptor.implementation_type is not None
            return self._create_constructor_call_site(
                service_identifier,
                service_descriptor.implementation_type,
                call_site_chain,
            )
        error_message = "Invalid service descriptor"
        raise RuntimeError(error_message)

    def _create_constructor_call_site(
        self,
        service_identifier: ServiceIdentifier,
        implementation_type: type,  # noqa: ARG002
        call_site_chain: CallSiteChain,  # noqa: ARG002
    ) -> ServiceCallSite:
        return ConstructorCallSite(service_identifier.service_type)


class _ServiceDescriptorCacheItem:
    _item: ServiceDescriptor | None
    _items: list[ServiceDescriptor] | None

    def __init__(self) -> None:
        self._item = None
        self._items = None

    @property
    def last(self) -> ServiceDescriptor:
        if self._items is not None and len(self._items) > 0:
            return self._items[len(self._items) - 1]

        assert self._item is not None
        return self._item

    def add(self, descriptor: ServiceDescriptor) -> _ServiceDescriptorCacheItem:
        new_cache_item = _ServiceDescriptorCacheItem()

        if self._item is None:
            new_cache_item._item = descriptor
        else:
            new_cache_item._item = self._item
            new_cache_item._items = self._items if self._items is not None else []
            new_cache_item._items.append(descriptor)

        return new_cache_item
