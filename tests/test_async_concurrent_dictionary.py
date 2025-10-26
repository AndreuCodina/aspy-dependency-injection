import asyncio

from aspy_dependency_injection._async_concurrent_dictionary import (
    AsyncConcurrentDictionary,
)

_run_count = 0


class TestConcurrentDictionary:
    async def test_get_or_add_should_execute_value_factory_only_once(
        self,
    ) -> None:
        expected_value_factory_executions = 1
        competing_tasks = 10
        dictionary = AsyncConcurrentDictionary[str, str]()

        async def value_factory(value_to_print: str) -> str:
            global _run_count  # noqa: PLW0603
            _run_count += 1
            await asyncio.sleep(1)
            return value_to_print

        async def _create_value_factory(value_to_print: str) -> str:
            return await value_factory(value_to_print)

        async def print_value(value_to_print: str) -> None:
            value_found = await dictionary.get_or_add(
                "key", lambda _: _create_value_factory(value_to_print)
            )
            print(value_found)  # noqa: T201

        tasks = [print_value(f"Task {i + 1}") for i in range(competing_tasks)]
        await asyncio.gather(*tasks)

        assert _run_count == expected_value_factory_executions
