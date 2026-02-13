import sys
from unittest.mock import patch

import pytest

from wirio._utils._extra_dependencies import ExtraDependencies


class TestExtraDependencies:
    def test_return_false_when_fastapi_cannot_be_imported(self) -> None:
        with patch.object(
            sys.modules["builtins"], "__import__", side_effect=ImportError
        ):
            assert not ExtraDependencies.is_fastapi_installed()

    def test_fail_importing_fastapi_when_it_is_not_installed(self) -> None:
        with (
            patch.object(
                sys.modules["builtins"], "__import__", side_effect=ImportError
            ),
            pytest.raises(ImportError),
        ):
            ExtraDependencies.import_fastapi()
