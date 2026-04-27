from __future__ import annotations

import json

import httpx

from issue_analysis_tool.models import Config


class LlmSummariser:
    def __init__(self, config: Config, client: httpx.Client | None = None) -> None:
        self.config = config
        self.client = client or httpx.Client(timeout=config.request_timeout)

    def close(self) -> None:
        self.client.close()

    def complete(self, prompt: str, tags: list[str] | None = None) -> str:
        if not self.config.llm_api_key:
            msg = "ISSUE_ANALYSIS_LLM_API_KEY is not configured."
            raise RuntimeError(msg)
        if not self.config.llm_model:
            msg = "ISSUE_ANALYSIS_LLM_MODEL is not configured."
            raise RuntimeError(msg)

        response = self.client.post(
            f"{self.config.llm_base_url}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.config.llm_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.config.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "extra_body": {"tags": tags or []},
            },
        )
        response.raise_for_status()
        payload = response.json()
        text = payload["choices"][0]["message"]["content"].strip()
        text = text.removeprefix("```json").removeprefix("```markdown").removeprefix("```text")
        text = text.removeprefix("```").removesuffix("```").strip()
        return text

    def complete_json(self, prompt: str, tags: list[str] | None = None) -> dict[str, object]:
        text = self.complete(prompt, tags)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            msg = f"LLM returned invalid JSON: {text}"
            raise RuntimeError(msg) from exc
        if not isinstance(data, dict):
            msg = f"LLM returned invalid JSON object: {text}"
            raise RuntimeError(msg)
        return data
