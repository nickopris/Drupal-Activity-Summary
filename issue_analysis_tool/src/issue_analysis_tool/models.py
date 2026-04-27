from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class Config:
    repo_root: Path
    output_dir: Path
    modules_file: Path
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    gitlab_token: str = ""
    request_timeout: float = 30.0


@dataclass(slots=True)
class ModuleIssueComment:
    author: str
    created_at: str
    body: str


@dataclass(slots=True)
class ModuleIssue:
    iid: int
    confidential: bool
    title: str
    state: str
    author: str
    assignees: list[str]
    created_at: str
    updated_at: str
    closed_at: str | None
    labels: list[str]
    web_url: str
    drupal_issue_number: str | None
    drupal_url: str | None
    description: str
    comment_count: int
    mr_count: int
    comments: list[ModuleIssueComment] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "iid": self.iid,
            "confidential": self.confidential,
            "title": self.title,
            "state": self.state,
            "author": self.author,
            "assignees": self.assignees,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            "labels": self.labels,
            "web_url": self.web_url,
            "drupal_issue_number": self.drupal_issue_number,
            "drupal_url": self.drupal_url,
            "description": self.description,
            "comment_count": self.comment_count,
            "mr_count": self.mr_count,
            "comments": [
                {
                    "author": comment.author,
                    "created_at": comment.created_at,
                    "body": comment.body,
                }
                for comment in self.comments
            ],
        }


@dataclass(slots=True)
class MergeRequest:
    iid: int
    title: str
    state: str
    author: str
    assignees: list[str]
    created_at: str
    updated_at: str
    merged_at: str | None
    source_branch: str
    web_url: str
    labels: list[str]
    description: str
    diff_lines: int

    def to_dict(self) -> dict[str, object]:
        return {
            "iid": self.iid,
            "title": self.title,
            "state": self.state,
            "author": self.author,
            "assignees": self.assignees,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "merged_at": self.merged_at,
            "source_branch": self.source_branch,
            "web_url": self.web_url,
            "labels": self.labels,
            "description": self.description,
            "diff_lines": self.diff_lines,
        }


@dataclass(slots=True)
class Commit:
    commit_id: str
    short_id: str
    title: str
    author_name: str
    authored_date: str
    committed_date: str
    message: str
    web_url: str

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.commit_id,
            "short_id": self.short_id,
            "title": self.title,
            "author_name": self.author_name,
            "authored_date": self.authored_date,
            "committed_date": self.committed_date,
            "message": self.message,
            "web_url": self.web_url,
        }


@dataclass(slots=True)
class ModuleResult:
    machine_name: str
    title: str
    since: str
    until: str
    issues: list[ModuleIssue] = field(default_factory=list)
    merge_requests: list[MergeRequest] = field(default_factory=list)
    commits: list[Commit] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "machine_name": self.machine_name,
            "title": self.title,
            "since": self.since,
            "until": self.until,
            "issues": [item.to_dict() for item in self.issues],
            "merge_requests": [item.to_dict() for item in self.merge_requests],
            "commits": [item.to_dict() for item in self.commits],
            "errors": self.errors,
        }


@dataclass(slots=True)
class DigestPayload:
    period: str
    since: str
    until: str
    generated_at: str
    modules: list[ModuleResult]

    def to_dict(self) -> dict[str, object]:
        return {
            "period": self.period,
            "since": self.since,
            "until": self.until,
            "generated_at": self.generated_at,
            "modules": [module.to_dict() for module in self.modules],
        }


def now_utc() -> datetime:
    return datetime.now().astimezone().astimezone(tz=None)
