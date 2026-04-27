from __future__ import annotations

import re

from issue_analysis_tool.models import ModuleResult


def build_data_markdown(
    results: list[ModuleResult], period: str, since: str, until: str, generated_line: str = ""
) -> str:
    since_date = since[:10]
    until_date = until[:10]
    active = [
        module for module in results if module.issues or module.merge_requests or module.commits
    ]

    lines = [f"# Drupal AI Activity Data - {period}", "", f"_Period: {since_date} to {until_date}_"]
    if generated_line:
        lines.append(generated_line)
    lines.extend(["", "## Modules", ""])

    for module in active:
        title = module.title or module.machine_name
        anchor = anchorize(title)
        lines.append(
            f"- [{title}](#{anchor}) - {len(module.issues)} issues, "
            f"{len(module.merge_requests)} MRs, {len(module.commits)} commits"
        )

    lines.extend(["", "---", ""])

    for module in active:
        title = module.title or module.machine_name
        lines.extend([f"## {title}", ""])

        public_issues = [issue for issue in module.issues if not issue.confidential]
        confidential_count = len(module.issues) - len(public_issues)
        if public_issues:
            lines.extend(["### Issues", ""])
            for issue in public_issues:
                assignees = ", ".join(issue.assignees) if issue.assignees else "unassigned"
                drupal_ref = (
                    f" · [d.o #{issue.drupal_issue_number}]({issue.drupal_url})"
                    if issue.drupal_issue_number
                    else ""
                )
                labels = f" · {', '.join(issue.labels[:4])}" if issue.labels else ""
                lines.append(
                    f"- **[{issue.title}]({issue.web_url})**{drupal_ref} · {issue.state} · "
                    f"{assignees} · {issue.comment_count} comments{labels}"
                )
                for comment in issue.comments:
                    date = comment.created_at[:10]
                    body = comment.body.strip().replace("\n", "\n  > ")
                    lines.append(f"  > **{comment.author}** ({date}): {body}")
            if confidential_count > 0:
                lines.extend(["", f"_{confidential_count} confidential issue(s) not shown._"])
            lines.append("")
        elif confidential_count > 0:
            lines.extend(
                [
                    "### Issues",
                    "",
                    f"_{confidential_count} confidential issue(s) not shown._",
                    "",
                ]
            )

        if module.merge_requests:
            lines.extend(["### Merge Requests", ""])
            for mr in module.merge_requests:
                merged = f"merged {mr.merged_at[:10]}" if mr.merged_at else mr.state
                diff_note = f" · {mr.diff_lines} diff lines" if mr.diff_lines > 0 else ""
                lines.append(
                    f"- **[{mr.title}]({mr.web_url})** · {mr.author} · {merged} · "
                    f"`{mr.source_branch}`{diff_note}"
                )
            lines.append("")

        if module.commits:
            lines.extend(["### Commits", ""])
            for commit in module.commits:
                lines.append(
                    f"- [`{commit.short_id}`]({commit.web_url}) {commit.title} - "
                    f"{commit.author_name} ({commit.authored_date[:10]})"
                )
            lines.append("")

        lines.extend(["---", ""])

    return "\n".join(lines)


def assemble_newsletter(
    sections: dict[str, str],
    tldr: str | None,
    period: str,
    since: str,
    until: str,
    generated_line: str = "",
) -> str:
    if not sections:
        return "# Drupal AI Newsletter\n\n_No module activity found for the period._"

    since_date = since[:10]
    until_date = until[:10]
    lines = ["# Drupal AI Activity Newsletter", "", f"_Period: {since_date} to {until_date}_"]
    if generated_line:
        lines.append(generated_line)
    lines.append("")
    if tldr:
        lines.extend(["## TL;DR", "", tldr, "", "---", ""])

    lines.extend(["## Modules", ""])
    for machine_name, text in sections.items():
        title = extract_section_title(text) or machine_name
        lines.append(f"- [{title}](#{anchorize(title)})")
    lines.extend(["", "---", ""])

    for machine_name, text in sections.items():
        title = extract_section_title(text) or machine_name
        data_link = f"_[View issues data](1d-data?id={anchorize(title)})_"
        section = re.sub(r"^(###\s+.+)$", rf"\1\n\n{data_link}", text, count=1, flags=re.MULTILINE)
        lines.extend([section, ""])
    return "\n".join(lines)


def build_sidebar() -> str:
    return (
        "* [Home](/README.md)\n"
        "* [Executive audience](1d-summary-executive.md)\n"
        "* [Developer audience](1d-summary-dev.md)\n"
        "* [Data](1d-data.md)\n"
        "* [AI prompts](prompts.md)\n"
    )


def anchorize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def extract_section_title(text: str) -> str | None:
    match = re.search(r"^###\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None
