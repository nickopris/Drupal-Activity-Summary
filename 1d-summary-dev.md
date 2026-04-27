# Drupal AI Activity Newsletter

_Period: 2026-04-26 to 2026-04-27_
_Generated: 2026-04-27 10:13 GMT_

## TL;DR

### Shipped

1. **CCC Subcontext Feature Made Optional** MR !120 landed for Context Control Center, toggling taxonomy vocabulary creation at install time and fixing static `\Drupal::config()` calls with injected `configFactory->get()` in `AiContextAgentForm`.
2. **Drupal Canvas MR Template and CLI Fixes** justafish merged MR !986 adding a standardised MR template, and balintbrews shipped MR !989 fixing inconsistent React JSX transform in Workbench preview-build exports and MR !988 adding validation of image prop example URLs in code component metadata.
3. **AI Initiative Monthly Funding Template** kepol landed MRs !5, !7, and !8 to introduce a reusable monthly funding issue template in the `ai_initiative` GitLab project, after which domidc opened tracking issues covering May 2025 through July 2026.
4. **Drupal Forge Silver AI Partner Contract Confirmed** The Drupal Forge Silver AI partner contract was signed, unblocking onboarding, and `d.o/ai` partner block copy was updated replacing "AI Maker" with "AI Partner".

### Ongoing

1. **CCC Scope Index and Usage Normalization MRs Blocked** MR !117 adds `ai_context_scope_index` to replace SQL `LIKE` queries on serialized scope data, and MR !119 normalizes `ai_context_usage` with batched cron pruning; whichever merges second must renumber its `ai_context_update_10002()` hook.
2. **Symfony AI 0.8.0 Provider Architecture Redesign** Issue #3574187 proposes a new `AiPlatformProviderInterface` extending both `ProviderInterface` and `PluginInspectionInterface` after the 0.8.0 release broke the existing provider plugin design, but the issue is unassigned with no active MR.
3. **Streaming Guardrails Design Blocked on Dual-Buffer Separation** Issue #3582179 for streaming-aware guardrails with start/stop regex buffering remains unmerged because the internal evaluation buffer and output buffer are not kept separate in the current implementation.
4. **Canvas Multi-Value Prop Handling Accumulating Open MRs** MRs !958, !991, and !795 (2805 diff lines) all target multi-value prop handling bugs and UI support, with none yet merged.
5. **GitLab CLI Skill Document in Progress** MR !4 on branch `3586406-marketing-cli-skill` is completing acceptance criteria, with a critical callout that `glab api -f field=@file` silently drops data on drupalcode.org and must not be used for write operations.

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

#### Activity Summary

The 24-hour window for the `ai_agents` module was quiet in terms of shipped code, with no commits landed and no merge requests opened or merged during the period.

The only notable activity occurred on two newly opened issues. The "Test Issue" (work item 3585985) saw a significant volume of housekeeping noise, with Marcus_Johansson and arianraeesi repeatedly cycling through assignment, priority, and status commands across 29 comments. The issue currently sits at `state::needsReview` with minor priority after considerable back-and-forth. No substantive technical discussion or patch work is visible from the activity log. A separate issue, "Create a ChatProcessor" (work item 3585984), was opened with a single comment and remains unassigned and undescribed in terms of scope.

There are no blocking items reported, but the lack of MR activity and the absence of a defined specification for the ChatProcessor issue suggest both items need triage attention before development can begin.

#### How can I help on this project?

- Review and add a technical specification comment to the "Create a ChatProcessor" issue (3585984) to unblock implementation work.
- Pick up assignment on work item 3585985 and post a concrete patch or failing test to move it past the current `needsReview` stall.
- Investigate whether a `ChatProcessor` interface or base class already exists elsewhere in the codebase that could inform the new issue.

### Context Control Center (CCC)

_[View issues data](1d-data?id=context-control-center-ccc)_

#### Merged and Shipped

MR !120 (issue #3586120) landed on 2026-04-26, making the subcontext feature optional. The work involved toggling taxonomy vocabulary creation at install time, fixing inconsistent config access in `AiContextAgentForm` (replacing static `\Drupal::config()` calls with injected `configFactory->get()`), and ensuring all subcontext-gated code paths are properly guarded. scottfalconer caught and resolved a test collision where `AiContextSubcontextDisabledTest` was manually creating `ai_context_tags` after config already installed it.

#### Open and In Progress

Two stable blockers remain unmerged. MR !117 (#3574905) adds a dedicated `ai_context_scope_index` table to replace SQL `LIKE` queries on serialized scope data, with scottfalconer wiring `AiContextSelector` to use the new `prefilterItemIdsByScope()` method. MR !119 (#3574907) normalizes `ai_context_usage` and introduces batched cron pruning; scottfalconer pushed a follow-up adding `ai_context_update_10002()` indexes, though kepol notes these may be superseded by an upcoming `ai_observability` integration. A note flagged by scottfalconer: whichever of #3574905 or #3574907 merges second will need its `ai_context_update_10002()` hook renumbered.

The rc1 UX review (#3573715) is active, with aidanfoster posting a detailed pass covering naming conventions (context item, context source), scope terminology, and use-case labelling. emma-horrell has rejoined the thread to refine the item/source distinction.

#### How can I help on this project?

Review MR !117 (#3574905) focusing on `prefilterItemIdsByScope()` correctness and index coverage. Independently, MR !119 (#3574907) needs a second reviewer to confirm the update hook and batched pruning logic before merge. If you have UX instincts, chime in on the item/source/scope naming thread in #3573715 -- Emma and Aidan are actively debating it.

### Drupal AI Initiative

_[View issues data](1d-data?id=drupal-ai-initiative)_

#### Activity Summary

The main technical output this period came from kepol (Kristen Pol), who landed four MRs (!5, !7, !8, !9) to introduce a reusable monthly funding issue template in the `ai_initiative` GitLab project. The work iterated rapidly: an initial template was merged via !5 (branch `3586427-funding-template`), followed by two label-metadata fixup MRs (!7, !8) after label and assignee pre-population failed to apply correctly through the template format. A draft MR (!6) was abandoned mid-iteration. The label automation issue remains partially unresolved -- kepol has flagged it with the infrastructure team. Once the template stabilized, domidc opened a batch of monthly funding tracking issues covering May 2025 through July 2026.

On the partner and governance side, the Drupal Forge Silver AI partner contract was confirmed signed, unblocking onboarding. The AI Partner agreement review closed as fixed after kepol's feedback was incorporated into contract templates. The `d.o/ai` partners block copy was updated, replacing the old "AI Maker" terminology with "AI Partner" and tightening the description text.

A GitLab CLI skill document is in progress under MR !4 (branch `3586406-marketing-cli-skill`), with jjchinquist completing acceptance criteria AC-2 through AC-6. A notable callout in that work: the `glab api -f field=@file` syntax silently drops data on drupalcode.org and must not be used for write operations.

#### How can I help on this project?

Review MR !4 on branch `3586406-marketing-cli-skill` and verify the `glab` auth and PAT setup instructions are accurate against drupalcode.org's current GitLab configuration. Investigate the broken label and assignee pre-population in the funding issue template and report findings to the infrastructure team. Pick up the unassigned offboarding checklist issue (#3570461) and draft the checklist structure.

### AI (Artificial Intelligence)

_[View issues data](1d-data?id=ai-artificial-intelligence)_

#### Symfony AI 0.8.0 Integration Rethink

The most significant discussion in the past 24 hours centres on #3574187, which proposes replacing the existing AI provider plugin system with Symfony AI's Platform component. The integration plan was disrupted by the Symfony AI 0.8.0 release, which introduced its own provider abstractions, forcing a design reset. mxr576 posted a revised architecture proposal built around a new `AiPlatformProviderInterface` extending both `ProviderInterface` and `PluginInspectionInterface`, backed by a config entity to give vendor connections a stable machine name. An open naming question has emerged: whether `AiPlatformProvider` is too defensive a name given the `search_api`-style namespacing pattern as an alternative. The issue remains unassigned and without an active MR targeting the 0.8.0+ approach.

#### Streaming Guardrails Still in Review

Issue #3582179, adding streaming-aware guardrails with start/stop regex buffering, remains open after multiple review cycles between abhisekmazumdar and a.dmitriiev. The core blocker is a design concern: the internal evaluation buffer and the output buffer must be kept separate, which the current implementation does not fully address. Kernel tests are deferred to a follow-up issue.

#### Open MRs

Two MRs are open without merges in this period: MR 1536 from petar_basic refactors field widget action dispatch into a base class on the 1.4.x branch, and MR 1074 from danrod addresses PHPStan issues on the 2.0.x branch.

#### How can I help on this project?

Review MR 1074 against the 2.0.x PHPStan baseline and leave inline feedback. Alternatively, pick up the dual-buffer design fix in #3582179 by separating the evaluation buffer from the output buffer in the guardrail implementation. You could also review mxr576's 0.8.0+ architecture proposal on #3574187 and comment on the `AiPlatformProviderInterface` naming decision.

### Drupal Canvas

_[View issues data](1d-data?id=drupal-canvas)_

#### Activity Summary

Three MRs landed on the main branch in this window. justafish merged MR !986, adding a standardised merge request template (3a27ff3c). balintbrews shipped two CLI Tool fixes: MR !989 corrects inconsistent React JSX transform application in Workbench preview-build exports, and MR !988 introduces validation of image prop example URLs in code component metadata files (d20871a7, d7e56bd7).

A significant volume of open work is accumulating. Several MRs target multi-value prop handling: MR !958 fixes time values when adding or reordering elements, MR !991 addresses a prop limit error, and MR !795 adds UI support for multi-value list text/integer props (2805 diff lines, still open). Required-field error handling is also active, with MR !982 fixing a 500 when clearing a required formatted text field and MR !956 doing the same for URI reference props.

CI infrastructure is seeing parallel effort: MR !976 adds pipeline caching, MR !977 avoids redundant E2E jobs, and MR !845 (draft) works toward a PHPUnit testing command. The large translation-related MRs (!494, !511, !898) remain open and unresolved.

#### How can I help on this project?

Review MR !991 (multi-value prop limit error, 96 diff lines) or MR !982 (required formatted text 500 error, 294 lines) -- both are small enough for a focused pass. The draft PHPUnit setup in MR !845 needs test coverage written to prove the command works. You could also pick up MR !977 and verify the CI job-skipping logic against the pipeline configuration in MR !976.

