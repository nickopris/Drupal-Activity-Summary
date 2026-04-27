from __future__ import annotations

import os
from pathlib import Path

from issue_analysis_tool.models import Config


def load_config(repo_root: Path | None = None) -> Config:
    resolved_repo_root = (repo_root or Path(__file__).resolve().parents[3]).resolve()
    tool_root = resolved_repo_root / "issue_analysis_tool"

    return Config(
        repo_root=resolved_repo_root,
        output_dir=Path(os.getenv("ISSUE_ANALYSIS_OUTPUT_DIR", tool_root / "out")),
        modules_file=Path(os.getenv("ISSUE_ANALYSIS_MODULES_FILE", tool_root / "modules.yml")),
        llm_base_url=os.getenv(
            "ISSUE_ANALYSIS_LLM_BASE_URL", "https://llm.us103.amazee.ai/"
        ).rstrip("/"),
        llm_api_key=os.getenv("ISSUE_ANALYSIS_LLM_API_KEY", ""),
        llm_model=os.getenv("ISSUE_ANALYSIS_LLM_MODEL", ""),
        gitlab_token=os.getenv("GITLAB_TOKEN", ""),
        request_timeout=float(os.getenv("ISSUE_ANALYSIS_REQUEST_TIMEOUT", "30")),
    )
