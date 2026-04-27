from issue_analysis_tool.models import ModuleIssue, ModuleIssueComment, ModuleResult
from issue_analysis_tool.render import (
    anchorize,
    assemble_newsletter,
    build_data_markdown,
    build_sidebar,
)


def test_build_data_markdown_hides_confidential_issues() -> None:
    module = ModuleResult(
        machine_name="ai",
        title="AI",
        since="2026-04-26T00:00:00+00:00",
        until="2026-04-27T00:00:00+00:00",
        issues=[
            ModuleIssue(
                iid=1,
                confidential=False,
                title="Public issue",
                state="opened",
                author="alice",
                assignees=[],
                created_at="2026-04-26T00:00:00+00:00",
                updated_at="2026-04-26T00:00:00+00:00",
                closed_at=None,
                labels=["bug"],
                web_url="https://example.com/public",
                drupal_issue_number=None,
                drupal_url=None,
                description="",
                comment_count=1,
                mr_count=0,
                comments=[
                    ModuleIssueComment(
                        author="alice",
                        created_at="2026-04-26T00:00:00+00:00",
                        body="hello",
                    )
                ],
            ),
            ModuleIssue(
                iid=2,
                confidential=True,
                title="Secret issue",
                state="opened",
                author="bob",
                assignees=[],
                created_at="2026-04-26T00:00:00+00:00",
                updated_at="2026-04-26T00:00:00+00:00",
                closed_at=None,
                labels=[],
                web_url="https://example.com/secret",
                drupal_issue_number=None,
                drupal_url=None,
                description="",
                comment_count=0,
                mr_count=0,
            ),
        ],
    )
    output = build_data_markdown([module], "24h", module.since, module.until, "_Generated: now_")
    assert "Public issue" in output
    assert "Secret issue" not in output
    assert "1 confidential issue(s) not shown." in output


def test_assemble_newsletter_injects_data_links() -> None:
    output = assemble_newsletter(
        {"ai": "### AI\n\nSummary text."},
        "### Shipped\n1. **Thing** - Done.\n\n### Ongoing\n1. **Thing** - Doing.",
        "24h",
        "2026-04-26T00:00:00+00:00",
        "2026-04-27T00:00:00+00:00",
        "_Generated: now_",
    )
    assert "[AI](#ai)" in output
    assert "_[View issues data](1d-data?id=ai)_" in output


def test_anchorize() -> None:
    assert anchorize("Context Control Center (CCC)") == "context-control-center-ccc"


def test_build_sidebar() -> None:
    sidebar = build_sidebar()
    assert "Executive audience" in sidebar
    assert "AI prompts" in sidebar
