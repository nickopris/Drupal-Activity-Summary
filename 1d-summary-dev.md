# Drupal AI Activity Newsletter

_Period: 2026-04-23 to 2026-04-24_
_Generated: 2026-04-24T21:56 GMT_

## TL;DR

### Shipped

1. **AI Module: Global Guardrails Feature** The global guardrails MR!1495 was merged by Marcus Johansson, adding a sortable guardrail set applied to every AI request with an update hook and test coverage.
2. **AI Module: CKEditor HTML Encoding Fix** MR!1353 resolved raw HTML entities appearing in the selected-text preview textarea and was backported to the 1.4.x branch.
3. **AI Dashboard: Admin Menu Entry** MR!17 added a missing menu link registering the dashboard at `/admin/config/ai/dashboard`, making it discoverable from the standard Drupal config UI.
4. **AI Module: AgentRunner Configuration Fix** MR!1534 fixed `AgentRunner.php` failing to set configuration, a small but blocking correctness bug.
5. **Drupal Canvas: Contextual Panel Layout Fix** MR!638 resolved a long-standing regression where the contextual panel width shifted incorrectly when the left sidebar was toggled.

### Ongoing

1. **AI Module: Deferred Assistant API Session Creation** MR!978 is stalled at RTBC with a regression where `session_one_thread` persistence breaks after the first interaction, and the contributor lacks permission to change the issue state.
2. **AWS Bedrock Provider: Inference Profile Support** MR!17 adds routing via profile ARNs instead of direct model IDs but has not yet received review activity or landed any commits.
3. **Postgres VDB Provider: Schema Bloat Reduction** MR!21 carries a 1,591-line diff targeting structural schema rework but has no reviewer activity and remains unmerged.
4. **Context Control Center: RC1 UX Review** Issue #3573715 covers naming conventions and UI changes targeting RC1, but the review is incomplete because co-reviewer emma-horrell is unavailable.
5. **AI Module: Guardrail Support for AI Automators** MR!1528 adds guardrail integration via `InputInterface::setGuardrailSet()` and is awaiting review feedback before it can progress.

---

## Modules

- [Context Control Center (CCC)](#context-control-center-ccc-)
- [AI Dashboard](#ai-dashboard)
- [Drupal AI Initiative](#drupal-ai-initiative)
- [AI (Artificial Intelligence)](#ai-artificial-intelligence-)
- [Drupal Canvas](#drupal-canvas)
- [AWS Bedrock Provider](#aws-bedrock-provider)
- [Tool API](#tool-api)
- [Postgres VDB Provider](#postgres-vdb-provider)

---

### Context Control Center (CCC)

_[View issues data](/1d-data?id=context-control-center-ccc-)_

#### UX Push Toward RC1

The bulk of activity this period was UX-focused, with no commits or merge requests landing in the 24-hour window.

aidanfoster posted a substantial UX review (#3573715) covering naming conventions, terminology, and UI improvements targeting the RC1 milestone. Key recommendations include retaining "Context Item" as the unit noun and a series of UI changes now being broken into child issues for incremental implementation. kepol and emma-horrell are co-reviewers, though emma-horrell is currently unavailable, leaving the review incomplete.

Two companion design issues were opened by aidanfoster: one for the Context Item single entity view and one for the Context Items list view. The list view mockup proposes renaming "Target" to "Scope", adding search filters, type icons with tooltips, and a shortened label display with tooltip fallback for use cases. kepol requested the single entity view issue be split to handle connected context separately, and both designs are queued for the Monday UX call.

#### Pending Feature

The issue for dynamically generating local tasks for scopes (#3585041) reached RTBC status after review by mglaman, who noted potential cache rebuild nuances. kepol intends to merge it but no commit landed within this window.

#### Housekeeping

kepol opened an issue to add regular contributors as GitLab reporter members, unblocking their ability to interact with the repository directly.

### AI Dashboard

_[View issues data](/1d-data?id=ai-dashboard)_

#### Merged

MR !17 (issue #3580675) landed on the `1.0.x` branch, adding a missing menu entry so the AI Dashboard is now discoverable from the `admin/config` overview page under the "AI" section. The fix registers a new route at `/admin/config/ai/dashboard` and wires up the corresponding menu link. The change is small (33 diff lines) and was committed by Tamas Bruckner (brtamas), with review from robloach and final merge sign-off from a.dmitriiev.

#### Context

The dashboard had been functional but invisible to site administrators navigating the standard configuration UI, which made it effectively inaccessible without knowing the direct path. No API changes or hook modifications were introduced; this was purely a routing and menu link definition fix.

#### Status

No open blockers were noted at the close of this period. The `1.0.x` branch remains the active development target. No issues were opened during this window beyond the one resolved above.

### Drupal AI Initiative

_[View issues data](/1d-data?id=drupal-ai-initiative)_

#### Merged This Period

Three MRs from jjchinquist landed on `main` (MR !1, !2, !3), closing out issue #3581782. The work ships five GitLab issue templates under `.gitlab/issue_templates/`: a generic marketing template, plus four sub-topic variants covering Blog Entry, Video, Case Study, and Webinar. MR !2 added branch and template naming conventions to the README; MR !3 added the four sub-topic templates and documented the contribution workflow in a README section. Commits 89c291be and b51ab860 cover the bulk of the 511 diff lines across the three MRs.

Alongside the template work, issue #3582480 (GitLab workflows and board for the Marketing Initiative) was closed by jjchinquist. Delivered items include three scoped `state::*` labels, a marketing board, Reporter role granted to 11 new members, and contribution workflow documentation split into #3586382.

#### Security: Credential Storage

The long-running meta issue #3559052 (AI and VDB provider credential storage) received a closing update from mxr576 noting that Drupal CMS 2.1.0 now ships Easy Encryption as the default protection for plaintext credentials. Other recipes and contrib modules can adopt the same pattern.

#### Infrastructure Blockers

YouTube channel manager access for the marketing team (#3584835) is awaiting confirmation from hestenet before proceeding. The `d.o` editor request for YouTube embed support (#3567516) is in review but deployment is delayed by ongoing DDoS mitigation work, per B_man.

#### Upcoming Work

Marketing Sprint #2 (April 27 to May 11, #3585830) is open. A full task breakdown for a DB Schenker webinar has been filed across planning, content, production, and post-event issues, all currently unassigned. The "Drupal AI in Practice" podcast launch meta (#3586383) has spawned a parallel set of infrastructure and Episode 1 production tasks, led by jmsaunders and domidc.

### AI (Artificial Intelligence)

_[View issues data](/1d-data?id=ai-artificial-intelligence-)_

#### Merged

Three MRs landed in the past 24 hours. The global guardrails feature (MR!1495, #3584851) was merged by Marcus Johansson, adding a sortable global guardrail set applied to every AI request, including an update hook and test coverage added after review feedback from Ahmad-Khader. The HTML encoding fix for the CKEditor selected-text preview (MR!1353, #3540608) was merged, resolving raw HTML entities appearing in the textarea; this was backported to 1.4.x. A small but necessary fix for `AgentRunner.php` failing to set configuration (MR!1534, #3586385) was also merged.

#### Open and In Progress

MR!978 (#3554797), which defers AI assistant API session creation until after the first message, is stalled. scottfalconer identified a regression where `session_one_thread` persistence breaks after the first interaction and updated the MR to address it, but lacks permission to move the issue out of RTBC state.

MR!1535 (#3571498) proposes rethrowing exceptions from the queue worker so callers can observe failures; currently exceptions are silently swallowed after marking the entity failed.

MR!1528 (#3585690) adds guardrail support to AI Automators via `InputInterface::setGuardrailSet()` and is awaiting review feedback from AkhilBabu. The `ai.provider_config` config schema fix (MR!1532) is state::rtbc and close to merge.

### Drupal Canvas

_[View issues data](/1d-data?id=drupal-canvas)_

#### Merged

Six MRs landed in the 24-hour window. The most notable is MR !638 (lauriii), which keeps the contextual panel width static when the left sidebar is toggled, resolving a long-standing layout regression (#3574994). MR !950 (penyaskito) eliminated race conditions and magic sleeps in the `multivalue-form-design*` Cypress tests, and MR !967 (bnjmnm) patched flakiness in `pattern.cy.js`. On the data model side, MR !929 (penyaskito) adds `dataDependencies.entityFields` to the `JavaScriptComponent` config schema. The CLI tool gained support for omitted props in Workbench page specs and component mocks via MR !979 (balintbrews). MR !978 (justafish) consolidates module installs across Playwright tests, and MR !969 (penyaskito) updated the PHPCS config to selectively comply with `Drupal.Arrays.Array.LongLineDeclaration` against Drupal 11 rules.

#### Open Work of Note

lauriii opened MR !982 to fix a fatal error when clearing a required formatted text field, and MR !971 targeting iframe height not updating on dynamic content changes. The large Draft pair MR !981 and MR !973 (bnjmnm, ~4600 combined diff lines) is tackling popover staging and immediate change propagation (#3586589). florenttorregrosa's MR !961 proposes a `ComponentPluginManager` decorator for contrib compatibility. justafish opened MR !976 to add GitLab CI caching and wimleers opened MR !977 to skip unnecessary E2E jobs, both aimed at reducing pipeline overhead.

#### Blockers

No issues were updated in the period. The popover staging work remains draft and split across two large MRs, suggesting architectural decisions are still unresolved there.

### AWS Bedrock Provider

_[View issues data](/1d-data?id=aws-bedrock-provider)_

#### In Progress

The only notable activity in this period is an open merge request from contributor RatNeurons adding support for inference profiles (MR !17, branch `3586773-inference-profiles-arent`, 105 diff lines). Inference profiles in AWS Bedrock allow routing requests across regions and model variants using a profile ARN rather than a direct model ID, so this change likely touches model resolution logic within the provider's API integration layer. No commits have landed yet, and the MR remains unmerged.

#### What Is Blocking Progress

No issues were updated and no commits landed in the 24-hour window, suggesting this work is either awaiting review or still being refined. There is no indication of a corresponding issue update to track feedback or blockers. Developers monitoring this module should watch MR !17 for review activity, particularly around how inference profile ARNs are validated and passed through to the Bedrock API client.

#### Summary

Quiet period overall. The inference profiles feature is the sole area of active development and represents a meaningful capability gap being addressed, but nothing has shipped yet.

### Tool API

_[View issues data](/1d-data?id=tool-api)_

#### Active Development

The primary shipping activity in this 24-hour window is a new merge request against the `LogMessage` tool bug (#3554285). Contributor scottfalconer opened MR !84 (`3554285-fix-logmessage-tool`, 350 diff lines), addressing a defect in the `LogMessage` tool implementation. No commits landed in the period, so this fix is pending review.

#### Issues in Progress

Three feature and bug issues saw discussion. The context data loss bug (#3576586) -- where `ContextData` is missing after `execute()` in the AI Connector -- moved to "Needs Review" but was then unassigned from b_sharpe. michaellander noted the fix may have been overlooked during the GitLab migration and flagged a concern that the token-based context solution could still produce failures in some call paths; this needs targeted testing before it can close.

A proof-of-concept issue (no number assigned yet) opened by michaellander proposes allowing Tool API tools to be called directly via Symfony's tool caller interface, which would tighten integration with the Symfony AI component stack.

The feature request to control tool return format (#3582933) remains open and unassigned under the AI Initiative Sprint tag.

#### Blockers

No MRs merged. The GitLab migration appears to have disrupted issue tracking continuity, contributing to at least one regression being overlooked (#3576586).

### Postgres VDB Provider

_[View issues data](/1d-data?id=postgres-vdb-provider)_

#### Active Work

The only activity in this period is an open merge request from contributor **ezeedub** targeting schema bloat reduction (MR !21, issue #3576852). The branch `3576852-reduce-schema-bloat` carries a substantial diff of 1,591 lines, suggesting a significant structural rework of how the module manages its Postgres schema rather than a minor cleanup.

No details on the specific changes are available from the MR metadata alone, but given the scope, this likely touches table definitions, index strategies, or vector column provisioning logic within the VDB provider layer.

#### Blocking / Status

No commits have landed in this period and no issues were updated, meaning MR !21 is open but not yet merged. There is no visible reviewer activity or blocking label information. The size of the diff may be a factor in review turnaround.

Developers integrating this module against a production Postgres vector database should monitor MR !21 before upgrading, as a schema-level change of this magnitude could require a migration step or manual schema reconciliation depending on what lands.

