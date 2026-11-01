import importlib.util
from pathlib import Path


class Translator:
    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], dict[str, str]] = {}

    def _load_group(self, locale: str, group: str) -> dict[str, str]:
        cache_key = (locale, group)
        if cache_key in self._cache:
            return self._cache[cache_key]

        target_file = Path(__file__).resolve().parent.parent.parent / "lang" / locale / f"{group}.py"
        spec = importlib.util.spec_from_file_location(f"lang_{locale}_{group}", str(target_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self._cache[cache_key] = module.translations
        return self._cache[cache_key]

    def trans(self, key: str, locale: str = "es") -> str:
        group, item = key.split(".", 1)
        return self._load_group(locale, group)[item]


translator = Translator()
trans = translator.trans
__ = translator.trans
