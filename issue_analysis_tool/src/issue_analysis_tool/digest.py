from __future__ import annotations

import json
from datetime import UTC, datetime

from issue_analysis_tool.fetchers import NewsletterDataFetcher, period_to_date_range
from issue_analysis_tool.llm import LlmSummariser
from issue_analysis_tool.models import DigestPayload, ModuleResult
from issue_analysis_tool.render import assemble_newsletter, build_data_markdown


class DigestService:
    def __init__(self, fetcher: NewsletterDataFetcher, summariser: LlmSummariser) -> None:
        self.fetcher = fetcher
        self.summariser = summariser

    def run(
        self,
        module: str | None = None,
        period: str = "24h",
    ) -> tuple[DigestPayload, dict[str, str]]:
        since, until = period_to_date_range(period)
        generated_at = datetime.now(UTC)
        results = self.fetcher.fetch_all_modules_data(module, since, until)
        payload = DigestPayload(
            period=period,
            since=since.isoformat(),
            until=until.isoformat(),
            generated_at=generated_at.isoformat(),
            modules=results,
        )
        generated_line = f"_Generated: {generated_at.strftime('%Y-%m-%d %H:%M')} GMT_"
        data_markdown = build_data_markdown(
            results,
            period,
            payload.since,
            payload.until,
            generated_line,
        )

        documents: dict[str, str] = {
            "json": json.dumps(payload.to_dict(), indent=2, ensure_ascii=False) + "\n",
            "data": data_markdown + "\n",
        }

        for persona in ("developer", "executive"):
            sections = self.summarise_modules(
                results,
                period,
                payload.since,
                payload.until,
                persona,
            )
            tldr = self.generate_tldr(sections, period, persona)
            documents[persona] = (
                assemble_newsletter(
                    sections,
                    tldr,
                    period,
                    payload.since,
                    payload.until,
                    generated_line,
                )
                + "\n"
            )

        return payload, documents

    def summarise_modules(
        self,
        results: list[ModuleResult],
        period: str,
        since: str,
        until: str,
        persona: str,
    ) -> dict[str, str]:
        sections: dict[str, str] = {}
        for module in results:
            if not module.issues and not module.merge_requests and not module.commits:
                continue
            try:
                sections[module.machine_name] = self.summarise_module(
                    module,
                    period,
                    since,
                    until,
                    persona,
                )
            except RuntimeError as exc:
                sections[module.machine_name] = f"_Summarisation failed: {exc}_"
        return sections

    def summarise_module(
        self, module: ModuleResult, period: str, since: str, until: str, persona: str
    ) -> str:
        machine_name = module.machine_name
        title = module.title or machine_name
        confidential_count = 0
        issue_lines: list[str] = []

        for issue in module.issues:
            if issue.confidential:
                confidential_count += 1
                continue
            assignees = ", ".join(issue.assignees) if issue.assignees else "unassigned"
            labels = ", ".join(issue.labels[:4]) if issue.labels else ""
            drupal_ref = (
                f" [#{issue.drupal_issue_number}]({issue.drupal_url})"
                if issue.drupal_issue_number
                else ""
            )
            issue_lines.append(
                f"- [{issue.title}]({issue.web_url}){drupal_ref} | {issue.state} | {assignees} | "
                f"comments: {issue.comment_count} | {labels}"
            )
            for comment in issue.comments:
                issue_lines.append(
                    f"  [{comment.author} {comment.created_at[:10]}]: {comment.body.strip()[:300]}"
                )

        mr_lines = []
        for mr in module.merge_requests:
            merged = f"merged {mr.merged_at[:10]}" if mr.merged_at else mr.state
            diff_note = f" | {mr.diff_lines} diff lines" if mr.diff_lines > 0 else ""
            mr_lines.append(
                f"- [{mr.title}]({mr.web_url}) by {mr.author} | {merged} | branch: "
                f"{mr.source_branch}{diff_note}"
            )

        commit_lines = [
            f"- [{commit.short_id}]({commit.web_url}) {commit.title} - {commit.author_name} "
            f"({commit.authored_date})"
            for commit in module.commits
        ]

        format_instruction = (
            f'Format your response as Markdown. Start with the exact heading "### {title}" '
            "then use subsections as needed."
        )

        if persona == "executive":
            persona_instruction = (
                "You are writing for a non-technical executive audience "
                "(CEO/leadership level).\n"
                "Focus on: business impact, strategic progress, risks, and what is being "
                "delivered.\n"
                "Avoid technical jargon. Do not mention branch names, function names, "
                "or API details.\n"
                "Explain what each piece of work means for users or the project's goals."
            )
            help_instruction = (
                "After the project summary prose, add a single subsection titled "
                '"#### How can I help on this project?" aimed at a non-technical executive. '
                "Suggest 2-3 concrete, high-level ways a leader could support or unblock progress "
                "(e.g. resourcing, stakeholder alignment, decision-making, funding, advocacy). "
                "Keep it under 60 words. Do not add any other 'How can I help' text anywhere else "
                "in the section."
            )
        else:
            persona_instruction = (
                "You are writing for a technical developer audience.\n"
                "Focus on: what was merged or shipped, specific bugs fixed, APIs changed, "
                "contributors, and what is blocking progress.\n"
                "Be specific - mention function names, module names, and MR references "
                "where relevant."
            )
            help_instruction = (
                "After the project summary prose, add a single subsection titled "
                '"#### How can I help on this project?" aimed at a developer. Suggest 2-3 '
                "concrete technical actions a contributor could take right now (e.g. reviewing a "
                "specific MR, picking up an unassigned issue, writing a test, or investigating "
                "a blocker). Keep it under 60 words. Do not add any other 'How can I help' text "
                "anywhere else in the section."
            )

        confidential_note = (
            f"Note: {confidential_count} confidential issue(s) existed in this period but "
            "have been "
            "excluded from the data below. Mention briefly at the end of your section that "
            f"{confidential_count} confidential issue(s) were not included in this analysis."
            if confidential_count > 0
            else ""
        )

        prompt = f"""You are a technical writer producing a newsletter section about recent
Drupal module activity.

Module: {title} (machine name: {machine_name})
Period: {period} ({since} to {until})

{persona_instruction}

Do not list every issue/MR individually - synthesise into prose. Keep it under 200 words.
Do not use emoticons or mdashes.
{confidential_note}
{format_instruction}

{help_instruction}

--- ISSUES UPDATED ({period}) ---
{chr(10).join(issue_lines) if issue_lines else "(none)"}

--- MERGE REQUESTS ({period}) ---
{chr(10).join(mr_lines) if mr_lines else "(none)"}

--- COMMITS ({period}) ---
{chr(10).join(commit_lines) if commit_lines else "(none)"}
"""

        return self.summariser.complete(prompt, ["newsletter_summarise"])

    def generate_tldr(self, sections: dict[str, str], period: str, persona: str) -> str | None:
        if not sections:
            return None
        persona_instruction = (
            "You are writing for a non-technical executive audience. Focus on business impact, "
            "strategic progress, and delivery milestones. Avoid all technical jargon."
            if persona == "executive"
            else "You are writing for a technical developer audience. Be specific - name "
            "modules, merged features, and critical bugs."
        )
        prompt = f"""You are an editor distilling a Drupal AI project newsletter into its most
important highlights.

{persona_instruction}

Read all the module summaries below. Separate the highlights into two categories:
- SHIPPED: things that were merged, fixed, released, or completed during this period.
- ONGOING: things that are actively in progress, under review, or blocked.

Be specific - name the module, what happened, and why it matters.
Do not use emoticons or mdashes. Do not include any text outside the two sections.

Format as two Markdown sections:

### Shipped
A numbered list of items that were completed, merged, or released. Each item must start
with a bold title on the same line as the number, followed by one sentence of explanation.

### Ongoing
A numbered list of the most significant in-progress items. Same format.

Use up to 5 items per section. Do not include any other text or headings.

--- MODULE SUMMARIES ---
{chr(10).join(sections.values())}
"""
        return self.summariser.complete(prompt, ["newsletter_tldr"])
