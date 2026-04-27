from __future__ import annotations

from pathlib import Path

from issue_analysis_tool.models import Config, DigestPayload
from issue_analysis_tool.render import build_sidebar


def resolve_output_path(
    output_dir: Path,
    period: str,
    since: str,
    ext: str,
    suffix: str = "",
) -> Path:
    date = since[:10]
    return output_dir / "issues-digest" / f"{period}_{date}{suffix}.{ext}"


def write_digest_outputs(
    config: Config,
    payload: DigestPayload,
    documents: dict[str, str],
) -> list[Path]:
    output_base = config.output_dir / "issues-digest"
    output_base.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    timestamped_paths = {
        "json": resolve_output_path(config.output_dir, payload.period, payload.since, "json"),
        "data": resolve_output_path(
            config.output_dir,
            payload.period,
            payload.since,
            "md",
            "-data",
        ),
        "developer": resolve_output_path(
            config.output_dir,
            payload.period,
            payload.since,
            "md",
            "-dev",
        ),
        "executive": resolve_output_path(
            config.output_dir, payload.period, payload.since, "md", "-executive"
        ),
    }

    for key, path in timestamped_paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(documents[key], encoding="utf-8")
        written.append(path)

    stable_files = {
        config.repo_root / "1d-data.md": documents["data"],
        config.repo_root / "1d-summary-dev.md": documents["developer"],
        config.repo_root / "1d-summary-executive.md": documents["executive"],
        config.repo_root / "_sidebar.md": build_sidebar(),
    }
    for path, content in stable_files.items():
        path.write_text(content, encoding="utf-8")
        written.append(path)

    return written
