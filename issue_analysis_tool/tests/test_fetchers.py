from pathlib import Path

import pytest

from issue_analysis_tool.fetchers import NewsletterDataFetcher, load_modules, period_to_date_range
from issue_analysis_tool.models import Config


def test_load_modules(tmp_path: Path) -> None:
    modules_file = tmp_path / "modules.yml"
    modules_file.write_text("- ai\n- canvas\n", encoding="utf-8")
    assert load_modules(modules_file) == ["ai", "canvas"]


def test_load_modules_rejects_invalid_shape(tmp_path: Path) -> None:
    modules_file = tmp_path / "modules.yml"
    modules_file.write_text("foo: bar\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_modules(modules_file)


def test_period_to_date_range_rejects_unknown_period() -> None:
    with pytest.raises(ValueError):
        period_to_date_range("2d")


def test_absolutify_gitlab_urls_rewrites_uploads() -> None:
    text = 'See ![alt](/uploads/hash/file.png){width=100 height=200} and "(/uploads/hash/file.png"'
    rewritten = NewsletterDataFetcher.absolutify_gitlab_urls(
        text,
        "https://git.drupalcode.org/project/ai/-/issues/1",
        123,
    )
    assert "https://git.drupalcode.org/-/project/123/uploads/hash/file.png" in rewritten
    assert '<img src="/uploads/hash/file.png" alt="alt" width="100" height="200">' not in rewritten
    assert (
        '<img src="https://git.drupalcode.org/-/project/123/uploads/hash/file.png" '
        'alt="alt" width="100" height="200">' in rewritten
    )


def test_extract_drupal_issue_number() -> None:
    assert (
        NewsletterDataFetcher.extract_drupal_issue_number("Migrated from issue #12345.") == "12345"
    )
    assert NewsletterDataFetcher.extract_drupal_issue_number("No match") is None


def test_fetcher_headers_include_token(tmp_path: Path) -> None:
    config = Config(
        repo_root=tmp_path,
        output_dir=tmp_path / "out",
        modules_file=tmp_path / "modules.yml",
        llm_base_url="https://example.com",
        llm_api_key="key",
        llm_model="model",
        gitlab_token="secret",
    )
    fetcher = NewsletterDataFetcher(config)
    try:
        headers = fetcher.default_headers()
    finally:
        fetcher.close()
    assert headers["PRIVATE-TOKEN"] == "secret"
