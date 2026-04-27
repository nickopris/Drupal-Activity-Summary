# Drupal AI Activity Newsletter

_Period: 2026-04-26 to 2026-04-27_
_Generated: 2026-04-27 08:45 GMT_

## TL;DR

### Shipped

1. **CCC Subcontext Feature Toggle (MR !120)** Merged commit `24713d22` guarding subcontext-dependent codepaths, fixing `AiContextAgentForm` to use `$this->configFactory->get()`, removing a duplicate `Vocabulary::create()` call that broke kernel tests, and adding `ai_context_update_10002()`.
2. **Drupal Canvas React JSX Transform Fix (MR !989)** Fixed inconsistent application of the React JSX transform during Workbench preview-build exports in the CLI tool, resolving broken code component previews.
3. **Drupal Canvas Image Prop URL Validation (MR !988)** Added validation of image prop example URLs in Code Component metadata files at the CLI layer, preventing malformed entries from surfacing as runtime errors.
4. **Drupal Forge Silver Partner Onboarding Unblocked** Contract was signed after a postponement, closing the partner agreement review and offboarding checklist tasks and updating the `d.o/ai` AI Partners block copy.
5. **AI Initiative Funding Issue Template (MRs !5, !7, !8, !9)** Kepol landed four MRs on `3586427-funding-template` to introduce a monthly funding issue template with correct label metadata, though automatic label and assignee pre-population remains unresolved.

### Ongoing

1. **CCC Denormalized Scope Index Table (MR !117)** Adds a scope index table to replace SQL `LIKE` queries on serialized scope data, with `prefilterItemIdsByScope()` wired into `AiContextSelector`; remains an open stable blocker for rc1.
2. **CCC `ai_context_usage` Normalization and Cron Pruning (MR !119)** Addresses usage table normalization and batched pruning, but `ai_context_update_10002()` risks a hook number collision with the same hook added in MR !120 and needs a reroll.
3. **Symfony AI Platform Integration for `ai` Module (#3574187)** mxr576 proposed an `AiPlatformProviderInterface` extending both `ProviderInterface` and `PluginInspectionInterface`, but a naming convention dispute and the Symfony AI 0.8.0 release have stalled earlier prototype MRs !1250 and !1259.
4. **AI Module Streaming Guardrails (#3582179)** Feature using start/stop regex patterns to buffer and evaluate streamed content is cycling between review states, with the core blocker being correct separation of the evaluation buffer and the consumer-facing output buffer.
5. **Drupal Canvas `ComponentPluginManager` Decorator (MR !961)** Proposes a decorator to improve contrib module compatibility, with broad architectural implications that are holding back contrib adoption pending review.

---

## Modules

- [AI Agents](#ai-agents)
- [Context Control Center (CCC)](#context-control-center-ccc)
- [Drupal AI Initiative](#drupal-ai-initiative)
- [AI (Artificial Intelligence)](#ai-artificial-intelligence)
- [Drupal Canvas](#drupal-canvas)

---

### AI Agents

_[View issues data](1d-data?id=ai-agents)_

Activity on the AI Agents module in the last 24 hours has been limited to issue triage with no merge requests or commits landing in the period.

#### Issues

Two new issues were opened. A housekeeping "Test Issue" was filed and remains unassigned, with Marcus_Johansson indicating intent to pick it up via a `%assign-me` command in the comments. **How can I help? (Developer):** Confirm whether this is a legitimate test case or administrative noise, and close or reassign it accordingly to keep the issue queue clean.

A more substantive issue, "Create a ChatProcessor," was also filed but carries no description detail or assignee yet. A ChatProcessor would presumably introduce a new agent processing pipeline for conversational interactions, though no API shape or integration point has been proposed in the single comment so far. **How can I help? (Developer):** Review the existing agent processor interfaces in the module and post a concrete API proposal or skeleton implementation to unblock design discussion.

No code shipped this cycle.

#### How can I help on this project?

Review the existing processor plugin architecture and comment on what interface a ChatProcessor should implement. Pick up the unassigned ChatProcessor issue and draft a proof-of-concept class. If the test infrastructure is thin, write a PHPUnit or Kernel test covering an existing agent processor to establish a pattern for new work.

### Context Control Center (CCC)

_[View issues data](1d-data?id=context-control-center-ccc)_

The past 24 hours saw one merge land and two significant MRs move toward completion ahead of rc1.

#### Merged

MR !120 (commit `24713d22`) shipped the optional subcontext feature toggle (#3586120). The work involved guarding all subcontext-dependent codepaths, fixing `AiContextAgentForm` to use `$this->configFactory->get()` instead of static `\Drupal::config()`, removing a duplicate `Vocabulary::create()` call that was causing kernel test failures in `AiContextSubcontextDisabledTest`, and adding `ai_context_update_10002()`. scottfalconer flagged a hook numbering collision with #3574907 that kepol will resolve when whichever lands second requires a reroll.

#### In Review

MR !117 (#3574905) adds a denormalized scope index table to replace SQL `LIKE` queries on serialized scope data. scottfalconer pushed an update wiring `AiContextSelector` to call `prefilterItemIdsByScope()` when scope subscriptions are present, preserving broad-match fallback behaviour. This remains an open stable blocker.

MR !119 (#3574907) addresses `ai_context_usage` normalization and batched cron pruning. scottfalconer added `ai_context_update_10002()` for missing usage indexes plus an install-time helper, though kepol noted the indexes were deliberately deferred pending planned `ai_observability` integration.

#### Also Active

The rc1 UX review (#3573715) has fresh input from aidanfoster and emma-horrell, with open discussion around terminology: specifically whether "context source" and "context item" are sufficiently distinct, and how use-case scoping should be framed. This remains a stable blocker with no child issues filed yet.

**How can I help? (Developer):** Review MR !117 for correctness of the `prefilterItemIdsByScope()` integration in `AiContextSelector`, paying particular attention to fallback behaviour when no scope subscriptions are present.

**How can I help? (Developer):** Review MR !119 and confirm that `ai_context_update_10002()` does not collide with the same hook added in #3574907, and verify the install-time index helper covers fresh installs correctly.

**How can I help? (Developer):** On #3573715, pick up aidanfoster's request to open child issues for the smaller naming and labelling changes so they can be tracked and resolved independently before beta2.

---

#### How can I help on this project?

- Review MR !117 and validate the `prefilterItemIdsByScope()` wiring in `AiContextSelector` against edge cases such as items with no scope assigned.
- Audit both MR !117 and MR !119 for the `ai_context_update_10002()` hook number conflict and post a reroll on whichever lands second.
- File child issues from the #3573715 UX review for the smaller confirmed naming changes so they can be closed before rc1.

### Drupal AI Initiative

_[View issues data](1d-data?id=drupal-ai-initiative)_

#### Summary

The dominant activity in this 24-hour window was operational and governance work, with no module code shipped. Kristen Pol (kepol) drove the most technical output, landing four MRs (!5, !7, !8, !9) on branch `3586427-funding-template` and its follow-up iterations to introduce a monthly funding issue template with correct label metadata and assignee fields. A draft MR (!6) was closed after a different approach proved necessary. The template work required multiple iterations because GitLab's issue template format does not support pre-populating labels and assignees directly; kepol has escalated to the infra team for a resolution.

On the partner side, the Drupal Forge Silver AI partner onboarding (previously postponed) unblocked after contract signature. The partner agreement review and offboarding checklist tasks both closed as fixed. The `d.o/ai` AI Partners block copy was updated, replacing "AI Maker" with "AI Partner" and tightening the description. A batch of historical funding activity issues was opened by domidc covering May 2025 through July 2026.

The most technically relevant open item for developers is MR !4 on branch `3586406-marketing-cli-skill` (jjchinquist), which covers a `SKILL.md` document for using `glab` CLI against drupalcode.org, including a documented trap around the `@file` syntax in `glab api` silently discarding data. That MR is awaiting review.

GitLab member provisioning also surfaced a gap: several contributors including `davidlynch62` are absent from GitLab due to unaccepted terms, blocking role assignment.

---

#### Issue Notes

**AI skill for CLI/GitLab (work item 3586406):** MR !4 covers all acceptance criteria (AC-2 through AC-6), including `SKILL.md` setup for `glab` install paths, `GITLAB_HOST`/`GITLAB_TOKEN` env-var auth, and PAT creation. The `glab api @file` silent data-loss trap is documented. **How can I help? (Developer):** Review MR !4 on branch `3586406-marketing-cli-skill`, specifically validate the `glab api` workaround documented in commits `6c7c3df` and `471f285` against a live drupalcode.org PAT to confirm AC-1 coverage.

**DA YouTube channel manager access (work item 3584835):** Invites were sent by hestenet to pdjohnson, Will, and kepol, but pdjohnson has not received the invite and is uncertain which email address was targeted. **How can I help? (Developer):** If you have DA YouTube admin access, confirm the invite target address for pdjohnson and re-send or escalate to resolve the delivery gap.

**Create a template for monthly AI Initiative funding activities (work item 3586427):** Kepol iterated through MRs !5, !7, !8, and !9 to get label metadata correct; automatic label and assignee pre-population in GitLab issue templates remains unresolved and is pending infra team input. **How can I help? (Developer):** Investigate GitLab's `.gitlab/issue_templates` YAML schema for `labels` and `assignees` frontmatter support on drupalcode.org's GitLab instance and post findings on the issue to unblock kepol.

**Onboard Silver AI partner: Drupal Forge (work item 3583297):** Contract is now signed and the issue is unblocked after a period of postponement. **How can I help? (Developer):** Review the onboarding checklist and confirm whether any technical access provisioning steps (GitLab membership, project permissions) are needed for Drupal Forge representatives.

---

#### How can I help on this project?

- Review MR !4 (`3586406-marketing-cli-skill`) and test the `glab api` workaround against drupalcode.org to confirm the silent `@file` data-loss trap is correctly documented.
- Investigate GitLab issue template YAML frontmatter support on drupalcode.org to unblock automatic label and assignee pre-population for the funding template.
- Pick up the unassigned "Drop Initiative from issue template names" task (work item 3586447), which is a low-effort, high-visibility housekeeping change.

### AI (Artificial Intelligence)

_[View issues data](1d-data?id=ai-artificial-intelligence)_

#### Activity Overview

The past 24 hours on the `ai` module saw no merged commits land, but two merge requests are open and awaiting review. MR !1536 from petar_basic refactors field widget action dispatch by generalizing behaviour into a base class (issue #3577050), touching 3,189 diff lines on the `1.4.x` branch. MR !1074 from danrod addresses a batch of PHPStan issues against the `api-2.0.x` branch (issue #3563396), covering 1,232 diff lines.

#### Symfony AI Platform Integration (#3574187)

The largest ongoing discussion concerns replacing the existing `AiProvider` plugin type with Symfony AI's Platform component. mxr576 posted a concrete architecture proposal on 2026-04-26, centred on an `AiPlatformProviderInterface` extending both `ProviderInterface` and `PluginInspectionInterface`, backed by a config entity to give vendor connections a stable machine name. A follow-up comment on 2026-04-27 raises a naming concern: `AiPlatformProvider` is defensively named to avoid collision with the 1.x plugin type, and an alternative namespace convention modelled on `search_api`'s plugin organisation is under discussion. The Symfony AI 0.8.0 release, which ships its own provider abstractions, has forced a rethink of earlier prototype MRs (!1250 and !1259). The issue remains unassigned and open.

**How can I help? (Developer):** Review mxr576's proposed `AiPlatformProviderInterface` architecture comment from 2026-04-26 and post a concrete opinion on the naming convention question -- `AiPlatformProvider` versus a `search_api`-style module-namespaced plugin structure.

#### Streaming Guardrails (#3582179)

The streaming-aware guardrails feature, which uses start/stop regex patterns to buffer and evaluate streamed content, has been cycling between "Needs review" and "Needs work" with abhisekmazumdar driving implementation. The core blocking point raised by marcus_johansson is that the evaluation buffer and the output buffer must be kept separate. A kernel test was deferred to a follow-up issue. The MR was re-submitted as "Needs review" on 2026-04-22, and AkhilBabu self-assigned during the reporting period.

**How can I help? (Developer):** Review the current MR for correct dual-buffer separation -- confirm that the regex evaluation buffer and the consumer-facing output buffer are genuinely decoupled in the latest commits before the implementation goes another round.

#### How can I help on this project?

- Review MR !1536 (field widget base class refactor, 3,189 lines) or MR !1074 (PHPStan fixes on `api-2.0.x`) -- both are open with no reviewer assigned.
- Contribute a kernel test for the streaming guardrails buffer logic, which was explicitly deferred to a follow-up issue.
- Post a technical position on the `AiPlatformProviderInterface` naming discussion in #3574187 to unblock the architecture decision.

### Drupal Canvas

_[View issues data](1d-data?id=drupal-canvas)_

#### Activity Summary

Two MRs landed in the 24-hour window, both from Bálint Kléri (balintbrews). MR !989 fixes a bug where the React JSX transform was applied inconsistently during Workbench preview-build exports in the CLI tool, resolving breakage in code component previews. MR !988 adds validation of image prop example URLs in Code Component metadata files, catching malformed entries at the CLI tool layer before they surface as runtime errors.

A notable backlog of open MRs is accumulating. MR !961 (florenttorregrosa) proposes a `ComponentPluginManager` decorator to improve contrib compatibility, which has broad architectural implications. MR !732 (lauriii) introduces `isCanvasPreview()` so code components can detect editor context at runtime. MR !980 (longwave) drafts a content entity reference well-known type. The large MR !795 adds multi-value list text and integer prop support in the UI at nearly 2,800 diff lines and needs review. CI reliability remains a concern: MR !977 (wimleers) aims to skip unnecessary E2E jobs, and the flaky multivalue Playwright tests addressed in MR !960 were only just stabilised.

The draft Playwright snapshot-based PoC (MR !974, isholgueras) at nearly 7,000 lines suggests a significant testing infrastructure shift is under consideration.

#### How can I help on this project?

- Review MR !961 to assess whether the `ComponentPluginManager` decorator API is sound before it blocks contrib adoption.
- Test MR !795 locally against multi-value list text and integer props and leave functional feedback; it is large and needs eyes.
- Investigate the open draft MR !523 on state-managed WASM file loading, which has been open since issue #3518306 and appears stalled.

