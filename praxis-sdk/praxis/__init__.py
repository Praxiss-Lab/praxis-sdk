"""Praxis public namespace with identity-preserving legacy import compatibility.

The implementation retains historical module names so existing serialized
classes and imports continue to resolve. Canonical imports share those same
module objects rather than registering duplicate models or tools.
"""

import importlib
import importlib.abc
import importlib.util
import sys


class _CompatibilityLoader(importlib.abc.Loader):
    def __init__(self, legacy_name: str):
        self.legacy_name = legacy_name

    def create_module(self, spec):  # noqa: ARG002 - Loader callback signature
        return importlib.import_module(self.legacy_name)

    def exec_module(self, module):  # noqa: ARG002 - Loader callback signature
        # create_module already imported and initialized the implementation.
        pass

    def get_code(self, _fullname):
        spec = importlib.util.find_spec(self.legacy_name)
        if spec is None or spec.loader is None:
            return None
        if isinstance(spec.loader, importlib.abc.InspectLoader):
            return spec.loader.get_code(self.legacy_name)
        return None


class _CompatibilityFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, _path=None, _target=None):
        if not fullname.startswith("praxis."):
            return None
        component = fullname.split(".", 2)[1]
        if component not in {"sdk", "tools", "workspace", "agent_server"}:
            return None
        legacy_name = "openhands." + fullname.removeprefix("praxis.")
        spec = importlib.util.find_spec(legacy_name)
        if spec is None:
            return None
        return importlib.util.spec_from_loader(
            fullname,
            _CompatibilityLoader(legacy_name),
            origin=spec.origin,
            is_package=spec.submodule_search_locations is not None,
        )


if not any(isinstance(finder, _CompatibilityFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, _CompatibilityFinder())
