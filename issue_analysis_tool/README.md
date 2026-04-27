# Issue Analysis Tool

Standalone Python implementation of the Drupal `issue_analysis` digest pipeline.

## Purpose

This tool runs on GitHub Actions without requiring a Drupal site. It fetches GitLab and drupal.org activity for configured projects, generates newsletter-style summaries via an OpenAI-compatible LLM API, and updates the existing docsify files in the repository root.

## Configuration

Environment variables:

- `ISSUE_ANALYSIS_LLM_BASE_URL`
- `ISSUE_ANALYSIS_LLM_API_KEY`
- `ISSUE_ANALYSIS_LLM_MODEL`
- `GITLAB_TOKEN` (optional, but required for issue comments and confidential issue access)

## Commands

```bash
python -m issue_analysis_tool.cli list-modules
python -m issue_analysis_tool.cli fetch 24h
python -m issue_analysis_tool.cli summarise issue_analysis_tool/out/issues-digest/24h_2026-04-27.json
python -m issue_analysis_tool.cli daily-digest
```

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
pytest
```
