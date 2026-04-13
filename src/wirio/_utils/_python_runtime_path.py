import sys
from pathlib import Path
from typing import final


@final
class PythonRuntimePath:
    """Provide helpers to identify paths that belong to the active Python runtime."""

    @staticmethod
    def is_python_runtime_path(resolved_path: Path) -> bool:
        """Return true when the provided path is within Python runtime directories."""
        runtime_prefixes = {
            Path(sys.prefix).resolve(),
            Path(sys.exec_prefix).resolve(),
            Path(sys.base_prefix).resolve(),
            Path(sys.base_exec_prefix).resolve(),
        }

        return any(
            runtime_prefix == resolved_path or runtime_prefix in resolved_path.parents
            for runtime_prefix in runtime_prefixes
        )
