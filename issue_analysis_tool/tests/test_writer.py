from pathlib import Path

from issue_analysis_tool.models import Config, DigestPayload
from issue_analysis_tool.writer import write_digest_outputs


def test_write_digest_outputs_updates_root_files(tmp_path: Path) -> None:
    config = Config(
        repo_root=tmp_path,
        output_dir=tmp_path / "out",
        modules_file=tmp_path / "modules.yml",
        llm_base_url="https://example.com",
        llm_api_key="key",
        llm_model="model",
    )
    payload = DigestPayload(
        period="24h",
        since="2026-04-26T00:00:00+00:00",
        until="2026-04-27T00:00:00+00:00",
        generated_at="2026-04-27T08:45:00+00:00",
        modules=[],
    )
    write_digest_outputs(
        config,
        payload,
        {
            "json": "{}\n",
            "data": "data\n",
            "developer": "dev\n",
            "executive": "exec\n",
        },
    )
    assert (tmp_path / "1d-data.md").read_text(encoding="utf-8") == "data\n"
    assert (tmp_path / "1d-summary-dev.md").read_text(encoding="utf-8") == "dev\n"
    assert (tmp_path / "1d-summary-executive.md").read_text(encoding="utf-8") == "exec\n"
    assert (tmp_path / "_sidebar.md").exists()
