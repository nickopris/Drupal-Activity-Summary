from __future__ import annotations

import re
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
import yaml

from issue_analysis_tool.models import (
    Commit,
    Config,
    MergeRequest,
    ModuleIssue,
    ModuleIssueComment,
    ModuleResult,
)

USER_AGENT = "Drupal Issue Analysis/1.0"
PROJECT_TYPES = [
    "project_module",
    "project_drupalorg",
    "project_theme",
    "project_distribution",
    "project_core",
    "project_profile",
    "project_general",
    "project_theme_engine",
    "project_translation",
]


def load_modules(modules_file: Path) -> list[str]:
    with modules_file.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or []
    if not isinstance(data, list) or not all(isinstance(item, str) and item for item in data):
        msg = f"Invalid modules file: {modules_file}"
        raise ValueError(msg)
    return data


def period_to_date_range(period: str) -> tuple[datetime, datetime]:
    until = datetime.now(UTC)
    match period:
        case "24h":
            since = until - timedelta(hours=24)
        case "7d":
            since = until - timedelta(days=7)
        case "30d":
            since = until - timedelta(days=30)
        case _:
            msg = f"Unknown period '{period}'. Use: 24h, 7d, 30d."
            raise ValueError(msg)
    return since, until


class NewsletterDataFetcher:
    def __init__(self, config: Config, client: httpx.Client | None = None) -> None:
        self.config = config
        self.client = client or httpx.Client(timeout=config.request_timeout, follow_redirects=True)

    def close(self) -> None:
        self.client.close()

    def fetch_all_modules_data(
        self, module: str | None, since: datetime, until: datetime
    ) -> list[ModuleResult]:
        machine_names = [module] if module else load_modules(self.config.modules_file)
        results: list[ModuleResult] = []
        for machine_name in machine_names:
            title = self.fetch_drupal_project_title(machine_name) or machine_name
            results.append(self.fetch_module_data(machine_name, since, until, title))
            time.sleep(0.5)
        return results

    def fetch_module_data(
        self, machine_name: str, since: datetime, until: datetime, title: str = ""
    ) -> ModuleResult:
        result = ModuleResult(
            machine_name=machine_name,
            title=title or machine_name,
            since=since.isoformat(),
            until=until.isoformat(),
        )
        result.issues = self.fetch_gitlab_issues(machine_name, since, until, result.errors)
        result.merge_requests = self.fetch_gitlab_merge_requests(
            machine_name,
            since,
            until,
            result.errors,
        )
        result.commits = self.fetch_gitlab_commits(machine_name, since, until, result.errors)
        return result

    def fetch_drupal_project_title(self, machine_name: str) -> str | None:
        for project_type in PROJECT_TYPES:
            try:
                response = self.client.get(
                    "https://www.drupal.org/api-d7/node.json",
                    params={
                        "field_project_machine_name": machine_name,
                        "type": project_type,
                    },
                    headers=self.default_headers(),
                )
                response.raise_for_status()
                payload = response.json()
            except httpx.HTTPError:
                continue
            if payload.get("list") and payload["list"][0].get("title"):
                return str(payload["list"][0]["title"])
        return None

    def default_headers(self) -> dict[str, str]:
        headers = {"User-Agent": USER_AGENT}
        if self.config.gitlab_token:
            headers["PRIVATE-TOKEN"] = self.config.gitlab_token
        return headers

    def fetch_gitlab_issues(
        self, project: str, since: datetime, until: datetime, errors: list[str]
    ) -> list[ModuleIssue]:
        issues: list[ModuleIssue] = []
        page = 1
        url = f"https://git.drupalcode.org/api/v4/projects/project%2F{project}/issues"
        while True:
            try:
                response = self.client.get(
                    url,
                    params={
                        "updated_after": since.isoformat(),
                        "updated_before": until.isoformat(),
                        "per_page": 50,
                        "page": page,
                        "order_by": "updated_at",
                        "sort": "desc",
                    },
                    headers=self.default_headers(),
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError as exc:
                errors.append(f"GitLab issues fetch failed for '{project}' (page {page}): {exc}")
                break

            if not isinstance(data, list) or not data:
                break

            for issue in data:
                assignees_raw = issue.get("assignees") or (
                    [issue["assignee"]] if issue.get("assignee") else []
                )
                assignees = [assignee.get("username", "") for assignee in assignees_raw if assignee]
                project_id = int(issue.get("project_id") or 0)
                iid = int(issue["iid"])
                description = self.absolutify_gitlab_urls(
                    issue.get("description", ""), issue.get("web_url", ""), project_id
                )
                drupal_issue_number = self.extract_drupal_issue_number(issue.get("description", ""))
                comments = self.fetch_gitlab_issue_notes(project_id, iid) if project_id else []
                issues.append(
                    ModuleIssue(
                        iid=iid,
                        confidential=bool(issue.get("confidential", False)),
                        title=issue.get("title", ""),
                        state=issue.get("state", ""),
                        author=issue.get("author", {}).get("username", ""),
                        assignees=[item for item in assignees if item],
                        created_at=issue.get("created_at", ""),
                        updated_at=issue.get("updated_at", ""),
                        closed_at=issue.get("closed_at"),
                        labels=issue.get("labels", []),
                        web_url=issue.get("web_url", ""),
                        drupal_issue_number=drupal_issue_number,
                        drupal_url=(
                            f"https://www.drupal.org/node/{drupal_issue_number}"
                            if drupal_issue_number
                            else None
                        ),
                        description=description,
                        comment_count=int(issue.get("user_notes_count") or 0),
                        mr_count=int(issue.get("merge_requests_count") or 0),
                        comments=[
                            ModuleIssueComment(
                                author=comment["author"],
                                created_at=comment["created_at"],
                                body=self.absolutify_gitlab_urls(
                                    comment["body"], issue.get("web_url", ""), project_id
                                ),
                            )
                            for comment in comments
                        ],
                    )
                )

            next_page = response.headers.get("x-next-page", "")
            if not next_page or len(data) < 50:
                break
            page += 1
            time.sleep(0.3)
        return issues

    def fetch_gitlab_merge_requests(
        self, project: str, since: datetime, until: datetime, errors: list[str]
    ) -> list[MergeRequest]:
        merge_requests: list[MergeRequest] = []
        page = 1
        url = f"https://git.drupalcode.org/api/v4/projects/project%2F{project}/merge_requests"
        while True:
            try:
                response = self.client.get(
                    url,
                    params={
                        "updated_after": since.isoformat(),
                        "updated_before": until.isoformat(),
                        "per_page": 50,
                        "page": page,
                        "order_by": "updated_at",
                        "sort": "desc",
                    },
                    headers=self.default_headers(),
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError as exc:
                errors.append(f"GitLab MR fetch failed for '{project}': {exc}")
                break

            if not isinstance(data, list) or not data:
                break

            for mr in data:
                assignees_raw = mr.get("assignees") or (
                    [mr["assignee"]] if mr.get("assignee") else []
                )
                assignees = [assignee.get("username", "") for assignee in assignees_raw if assignee]
                merge_requests.append(
                    MergeRequest(
                        iid=int(mr["iid"]),
                        title=mr.get("title", ""),
                        state=mr.get("state", ""),
                        author=mr.get("author", {}).get("username", ""),
                        assignees=[item for item in assignees if item],
                        created_at=mr.get("created_at", ""),
                        updated_at=mr.get("updated_at", ""),
                        merged_at=mr.get("merged_at"),
                        source_branch=mr.get("source_branch", ""),
                        web_url=mr.get("web_url", ""),
                        labels=mr.get("labels", []),
                        description=mr.get("description", ""),
                        diff_lines=self.fetch_gitlab_mr_diff_line_count(project, int(mr["iid"])),
                    )
                )

            next_page = response.headers.get("x-next-page", "")
            if not next_page or len(data) < 50:
                break
            page += 1
            time.sleep(0.3)
        return merge_requests

    def fetch_gitlab_commits(
        self, project: str, since: datetime, until: datetime, errors: list[str]
    ) -> list[Commit]:
        commits: list[Commit] = []
        page = 1
        url = f"https://git.drupalcode.org/api/v4/projects/project%2F{project}/repository/commits"
        while True:
            try:
                response = self.client.get(
                    url,
                    params={
                        "since": since.isoformat(),
                        "until": until.isoformat(),
                        "per_page": 50,
                        "page": page,
                    },
                    headers=self.default_headers(),
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError as exc:
                errors.append(f"GitLab commits fetch failed for '{project}': {exc}")
                break

            if not isinstance(data, list) or not data:
                break

            for commit in data:
                commits.append(
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

            next_page = response.headers.get("x-next-page", "")
            if not next_page or len(data) < 50:
                break
            page += 1
            time.sleep(0.3)
        return commits

    def fetch_gitlab_mr_diff_line_count(self, project: str, iid: int) -> int:
        url = f"https://git.drupalcode.org/project/{project}/-/merge_requests/{iid}.diff"
        try:
            response = self.client.get(url, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
        except httpx.HTTPError:
            return 0
        return response.text.count("\n")

    def fetch_gitlab_issue_notes(self, project_id: int, iid: int) -> list[dict[str, str]]:
        if not self.config.gitlab_token:
            return []

        notes: list[dict[str, str]] = []
        page = 1
        url = f"https://git.drupalcode.org/api/v4/projects/{project_id}/issues/{iid}/notes"
        while True:
            try:
                response = self.client.get(
                    url,
                    params={"per_page": 50, "page": page, "sort": "asc"},
                    headers=self.default_headers(),
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError:
                break

            if not isinstance(data, list) or not data:
                break

            for note in data:
                if note.get("system"):
                    continue
                if note.get("author", {}).get("username") == "drupalbot":
                    continue
                notes.append(
                    {
                        "author": note.get("author", {}).get("username", ""),
                        "created_at": note.get("created_at", ""),
                        "body": note.get("body", ""),
                    }
                )

            next_page = response.headers.get("x-next-page", "")
            if not next_page or len(data) < 50:
                break
            page += 1
            time.sleep(0.2)
        return notes

    @staticmethod
    def absolutify_gitlab_urls(text: str, project_web_url: str, project_id: int = 0) -> str:
        if not text:
            return text

        base = f"https://git.drupalcode.org/-/project/{project_id}" if project_id else ""
        if not base and project_web_url:
            base = re.sub(r"/-/.*$", "", project_web_url)
        if not base:
            return text

        text = re.sub(r'(\(|")(/uploads/)', rf"\1{base}\2", text)

        def replace_image(match: re.Match[str]) -> str:
            alt, url, width, height = match.groups()
            escaped_alt = (
                alt.replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            return f'<img src="{url}" alt="{escaped_alt}" width="{width}" height="{height}">'

        return re.sub(
            r"!\[([^\]]*)\]\(([^)]+)\)\{width=(\d+)\s+height=(\d+)\}",
            replace_image,
            text,
        )

    @staticmethod
    def extract_drupal_issue_number(description: str) -> str | None:
        match = re.search(r"Migrated from issue #(\d+)", description)
        return match.group(1) if match else None
