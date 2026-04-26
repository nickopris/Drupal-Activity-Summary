# Drupal AI Activity Newsletter

_Period: 2026-04-25 to 2026-04-26_
_Generated: 2026-04-26 19:45 GMT_

## TL;DR

### Shipped

1. **CCC: Programmatic Context API** `getResult()` and `getRenderedContext()` added directly to `AiContextRepository` via MR !122 (issue #3584838), including a fix for token-limit metadata inconsistency in the renamed `getResult()` method.
2. **CCC: Optional Subcontext Feature** MR !120 (issue #3586120) landed after fixing three kernel failures in `AiContextSubcontextDisabledTest` caused by duplicate `taxonomy_vocabulary` creation, and replaced static `\Drupal::config()` usage in `AiContextAgentForm`.
3. **AI Initiative: Monthly Funding Template** MRs !5, !7, !8, and !9 delivered a reusable GitLab issue template for monthly funding tracking, after which domidc opened fourteen historical and forward-looking issues spanning May 2025 through July 2026.
4. **Drupal Canvas: JSX Transform and Metadata Validation Fixes** MR !989 resolved inconsistent React JSX transform application in CLI preview-build exports, and MR !988 added validation of image prop example URLs in Code Component metadata files.
5. **AI Initiative: Partner Onboarding and Cleanup** Drupal Forge silver partner onboarding (#3583297) moved back to Active after contract signing, and GitLab membership cleanup (#3586380) closed after maintainers were added to the repository.

### Ongoing

1. **AI: Symfony AI 0.8.0 Architecture Rethink** Issue #3574187 is blocked on reconciling prototype MRs !1250 and !1259 with Symfony AI 0.8.0's new provider abstractions, requiring a revised design around the proposed `AiPlatformProviderInterface` and config entity approach before work can progress.
2. **CCC: Scope Index Table** MR !117 (issue #3574905) adds a denormalized scope index to replace SQL `LIKE` queries on serialized data and is tagged as a stable blocker, with `prefilterItemIdsByScope()` wired into `AiContextSelector` but not yet merged.
3. **CCC: Batched Cron Pruning and Usage Indexes** MR !119 (issue #3574907) adds `ai_context_usage` indexes and batched pruning, but is blocked pending planned integration with `ai_observability` and has a hook-renumber conflict with MR !120.
4. **Drupal Canvas: Component Path Sync** MR !990 from lauriii proposes storing and syncing the code component folder path in `component.yml` in a 1073-line diff, indicating a significant structural change not yet reviewed.
5. **AI: PHPStan Fixes on api-2.0.x** MR !1074 from danrod targets PHPStan issues in #3563396 with a 1232-line diff against the `api-2.0.x` branch, but no commits landed in the current window.

---

## Modules

- [Context Control Center (CCC)](#context-control-center-ccc-)
- [Drupal AI Initiative](#drupal-ai-initiative)
- [AI (Artificial Intelligence)](#ai-artificial-intelligence-)
- [Drupal Canvas](#drupal-canvas)

---

### Context Control Center (CCC)

_[View issues data](/1d-data?id=context-control-center-ccc-)_

#### Merged This Period

Two MRs landed in the past 24 hours. MR !122 (issue #3584838) ships a new convenience API for programmatic context retrieval without an agent. Rather than adding another service to an already crowded service layer, the methods `getResult()` and `getRenderedContext()` were added directly to `AiContextRepository`. A late fix from scottfalconer addressed a token-limit metadata inconsistency where `retrieve()` with no selected items exposed the selector's default budget instead of the caller-supplied `tokenLimit`. The method was also renamed from `retrieve()` to `getResult()` for clarity before merge. MR !120 (issue #3586120) makes the subcontext feature optional. Testing by scottfalconer caught three kernel failures in `AiContextSubcontextDisabledTest` caused by a duplicate `taxonomy_vocabulary` creation; the fix removed the manual `Vocabulary::create()` call. Additional cleanup addressed static `\Drupal::config()` usage in `AiContextAgentForm`, replaced with `$this->configFactory->get()`. Note that both #3586120 and #3574907 introduced `ai_context_update_10002()`; kepol flagged that whichever lands second will need a hook renumber.

#### Open and In Progress

MR !117 (issue #3574905) adds a denormalized scope index table to replace SQL `LIKE` queries on serialized scope data. scottfalconer's latest push wires `AiContextSelector` to call `prefilterItemIdsByScope()` when scope subscriptions are present. MR !119 (issue #3574907) adds batched cron pruning and usage indexes; scottfalconer added the missing `ai_context_update_10002()` for `ai_context_usage` indexes that were intentionally deferred pending planned integration with `ai_observability`. Both remain open and are tagged as stable blockers.

#### Blocking Progress

The UX review issue (#3573715) is active but lacks a second reviewer with emma-horrell away. Terminology is unsettled, particularly the distinction between "context item" and "context source." The scheduler submodule split (#3577429) is blocked upstream on `scheduler` issue #3355087 (non-bundle entity type support).

### Drupal AI Initiative

_[View issues data](/1d-data?id=drupal-ai-initiative)_

#### Merged

All four merged MRs this period (MR!5, MR!7, MR!8, MR!9) came from kepol and focused on a single deliverable: a reusable monthly funding issue template for the `ai_initiative` GitLab project (#3586427). The work required several iterations to get label metadata and assignee fields correctly applied in the template format, with MR!6 abandoned before a working approach landed. Once the template was in place, domidc opened fourteen historical and forward-looking monthly funding tracking issues spanning May 2025 through July 2026.

#### Partner and Contributor Management

The Drupal Forge silver partner onboarding (#3583297) unblocked after a contract signing, moving the issue from Postponed back to Active. The partner agreement review (#3583337) also closed, with kepol's feedback incorporated into contract templates now in active use. The AI Partners block copy on d.o/ai (#3572736) was updated, replacing "AI Maker" with "AI Partner" and revising the partner description for clarity.

The GitLab membership cleanup task (#3586380) closed after kepol added initiative maintainers to the repository, though one contributor (davidlynch62) remains absent due to unaccepted platform terms and conditions.

#### Still Open

The AI partner/contributor offboarding checklist (#3570461) is drafted and out for team review but not yet closed. The funding issue template still has unresolved label and assignee automation, with kepol awaiting input from the infrastructure team.

### AI (Artificial Intelligence)

_[View issues data](/1d-data?id=ai-artificial-intelligence-)_

#### Symfony AI 0.8.0 Integration Requires Architecture Rethink

The dominant activity this period centres on #3574187, the long-running effort to replace the existing AI provider system with Symfony AI's Platform component. The issue received a significant architecture proposal from mxr576 on 2026-04-26 outlining integration with Symfony AI 0.8.0, which introduced its own provider abstractions. The proposed design introduces an `AiPlatformProviderInterface` extending both `ProviderInterface` and `PluginInspectionInterface`, backed by a config entity to give vendor connections a stable machine name and make them storable and referenceable. This represents a course correction from earlier prototype MRs (MR !1250 and MR !1259 from fago), which predated the 0.8.0 release. The team now needs to reconcile those prototypes with the upstream changes before work can progress.

The BC impact analysis completed earlier in the issue thread, led by fago, found that existing configurations and recipes are largely unaffected by provider-layer changes, which is an encouraging baseline for the refactor.

#### PHPStan Fixes

MR !1074 from danrod was opened against the `api-2.0.x` branch, targeting #3563396 to resolve PHPStan issues. The diff is substantial at 1,232 lines but no commits landed in the 24-hour window.

#### Blockers

Progress on the Symfony AI integration is blocked pending a revised architecture plan compatible with Symfony AI 0.8.0+. MR reviews have been acknowledged as delayed by mxr576.

### Drupal Canvas

_[View issues data](/1d-data?id=drupal-canvas)_

#### Merged

Two CLI Tool improvements landed on 2026-04-26, both authored by balintbrews (Balint Kleri).

MR !989 (d7e56bd7) fixes inconsistent application of the React JSX transform in Workbench preview-build exports, resolving issue #3586971. MR !988 (d20871a7) adds validation of image prop example URLs inside Code Component metadata files, resolving issue #3586959. The latter is a 409-line addition and represents a meaningful expansion of metadata validation coverage.

#### Open and In Progress

lauriii opened MR !990 to store and sync the code component folder path in `component.yml`, a 1073-line diff that suggests a significant structural change to how component paths are tracked and persisted.

jptaranto's MR !523 for state-managed WASM file loading (718 lines, issue #3518306) remains open and appears to be a longer-running effort.

#### Drafts and Blockers

bnjmnm has three draft MRs open. MR !981 and MR !985 both address issue #3586589 via different approaches -- one targeting a CI popover staging problem (2397 lines) and one covering an entity reference/entity form variant (2489 lines). MR !987 is a small 26-line baseline control probe. The duplication across !981 and !985 suggests the fix strategy for #3586589 is still being worked out.

