from __future__ import annotations

import argparse
import json
from pathlib import Path

from issue_analysis_tool.config import load_config
from issue_analysis_tool.digest import DigestService
from issue_analysis_tool.fetchers import NewsletterDataFetcher, load_modules, period_to_date_range
from issue_analysis_tool.llm import LlmSummariser
from issue_analysis_tool.models import (
    Commit,
    DigestPayload,
    MergeRequest,
    ModuleIssue,
    ModuleIssueComment,
    ModuleResult,
)
from issue_analysis_tool.render import assemble_newsletter
from issue_analysis_tool.writer import resolve_output_path, write_digest_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="issue-analysis-tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-modules")

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("period", nargs="?", default="7d")
    fetch_parser.add_argument("--module")

    summarise_parser = subparsers.add_parser("summarise")
    summarise_parser.add_argument("input_file")
    summarise_parser.add_argument(
        "--persona",
        choices=["developer", "executive"],
        default="developer",
    )
    summarise_parser.add_argument("--module")

    digest_parser = subparsers.add_parser("daily-digest")
    digest_parser.add_argument("--module")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config()

    if args.command == "list-modules":
        for module in load_modules(config.modules_file):
            print(module)
        return 0

    fetcher = NewsletterDataFetcher(config)
    summariser = LlmSummariser(config)
    digest_service = DigestService(fetcher, summariser)

    try:
        if args.command == "fetch":
            since, until = period_to_date_range(args.period)
            results = fetcher.fetch_all_modules_data(args.module, since, until)
            payload = DigestPayload(
                period=args.period,
                since=since.isoformat(),
                until=until.isoformat(),
                generated_at=until.isoformat(),
                modules=results,
            )
            path = resolve_output_path(config.output_dir, payload.period, payload.since, "json")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(payload.to_dict(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(path)
            return 0

        if args.command == "summarise":
            payload = load_payload(Path(args.input_file))
            results = payload.modules
            if args.module:
                results = [module for module in results if module.machine_name == args.module]
            sections = digest_service.summarise_modules(
                results, payload.period, payload.since, payload.until, args.persona
            )
            tldr = digest_service.generate_tldr(sections, payload.period, args.persona)
            print(assemble_newsletter(sections, tldr, payload.period, payload.since, payload.until))
            return 0

        if args.command == "daily-digest":
            payload, documents = digest_service.run(args.module)
            written = write_digest_outputs(config, payload, documents)
            for path in written:
                print(path)
            return 0

        return 1
    finally:
        fetcher.close()
        summariser.close()


def load_payload(path: Path) -> DigestPayload:
    raw = json.loads(path.read_text(encoding="utf-8"))
    modules: list[ModuleResult] = []
    for module in raw.get("modules", []):
        module_result = ModuleResult(
            machine_name=module["machine_name"],
            title=module.get("title", module["machine_name"]),
            since=module["since"],
            until=module["until"],
            issues=[],
            merge_requests=[],
            commits=[],
            errors=module.get("errors", []),
        )
        for issue in module.get("issues", []):
            module_result.issues.append(
                ModuleIssue(
                    iid=issue["iid"],
                    confidential=issue.get("confidential", False),
                    title=issue.get("title", ""),
                    state=issue.get("state", ""),
                    author=issue.get("author", ""),
                    assignees=issue.get("assignees", []),
                    created_at=issue.get("created_at", ""),
                    updated_at=issue.get("updated_at", ""),
                    closed_at=issue.get("closed_at"),
                    labels=issue.get("labels", []),
                    web_url=issue.get("web_url", ""),
                    drupal_issue_number=issue.get("drupal_issue_number"),
                    drupal_url=issue.get("drupal_url"),
                    description=issue.get("description", ""),
                    comment_count=issue.get("comment_count", 0),
                    mr_count=issue.get("mr_count", 0),
                    comments=[
                        ModuleIssueComment(
                            author=comment.get("author", ""),
                            created_at=comment.get("created_at", ""),
                            body=comment.get("body", ""),
                        )
                        for comment in issue.get("comments", [])
                    ],
                )
            )
        for mr in module.get("merge_requests", []):
            module_result.merge_requests.append(
                MergeRequest(
                    iid=mr["iid"],
                    title=mr.get("title", ""),
                    state=mr.get("state", ""),
                    author=mr.get("author", ""),
                    assignees=mr.get("assignees", []),
                    created_at=mr.get("created_at", ""),
                    updated_at=mr.get("updated_at", ""),
                    merged_at=mr.get("merged_at"),
                    source_branch=mr.get("source_branch", ""),
                    web_url=mr.get("web_url", ""),
                    labels=mr.get("labels", []),
                    description=mr.get("description", ""),
                    diff_lines=mr.get("diff_lines", 0),
                )
            )
        for commit in module.get("commits", []):
            module_result.commits.append(
                Commit(
                    commit_id=commit.get("id", ""),
                    short_id=commit.get("short_id", ""),
                    title=commit.get("title", ""),
                    author_name=commit.get("author_name", ""),
                    authored_date=commit.get("authored_date", ""),
                    committed_date=commit.get("committed_date", ""),
                    message=commit.get("message", ""),
                    web_url=commit.get("web_url", ""),
                )
            )
        modules.append(module_result)
    return DigestPayload(
        period=raw["period"],
        since=raw["since"],
        until=raw["until"],
        generated_at=raw.get("generated_at", raw["until"]),
        modules=modules,
    )


if __name__ == "__main__":
    raise SystemExit(main())
