import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "reaccent_file", HERE / "reaccent_file.py"
)


def load_module():
    module = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(module)
    return module


def test_reaccent_file_writes_only_when_text_changes(tmp_path, monkeypatch):
    module = load_module()
    article = tmp_path / "article.md"
    article.write_text("Les salaries sont formes.\n", encoding="utf-8")
    monkeypatch.setattr(
        module,
        "reaccent_text",
        lambda text, **_: text.replace("salaries", "salariés").replace("formes", "formés"),
    )

    assert module.reaccent_file(article) is True
    assert article.read_text(encoding="utf-8") == "Les salariés sont formés.\n"


def test_guard_uses_repository_local_reaccenter():
    guard = (HERE.parent / "site" / "scripts" / "guard-content.sh").read_text(
        encoding="utf-8"
    )

    assert 'REPO_ROOT=' in guard
    assert 'blog-auto/reaccent_file.py' in guard
    assert 'MISTRAL_API_KEY' in guard
    assert '$HOME/stack-2026/scripts/reaccent_gemini.py' not in guard


def test_reaccent_file_chunks_long_articles(tmp_path, monkeypatch):
    module = load_module()
    article = tmp_path / "long.md"
    article.write_text("ligne sans accents\n" * 20, encoding="utf-8")
    calls = []

    def fake_reaccent(text, **_):
        calls.append(text)
        return text.replace("accents", "accénts")

    monkeypatch.setattr(module, "MAX_CHUNK_CHARS", 60)
    monkeypatch.setattr(module, "reaccent_text", fake_reaccent)

    assert module.reaccent_file(article) is True
    assert len(calls) > 1
    assert "".join(calls) == "ligne sans accents\n" * 20


def test_reaccent_falls_back_to_mistral_when_gemini_is_noop(monkeypatch):
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import reaccent_lib

    original = "Les salaries sont formes a l IA."
    corrected = "Les salariés sont formés à l IA."
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-stub")
    monkeypatch.setenv("MISTRAL_API_KEY", "mistral-stub")
    monkeypatch.setattr(reaccent_lib, "_is_folded_french", lambda _: True)
    monkeypatch.setattr(reaccent_lib, "_call_gemini", lambda *_: original)
    monkeypatch.setattr(reaccent_lib, "_call_mistral", lambda *_: corrected)

    assert reaccent_lib.reaccent_text(original) == corrected
