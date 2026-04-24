# Drupal AI Activity Newsletter

_Period: 2026-04-23 to 2026-04-24_
_Generated: 2026-04-24T20:49 GMT_

## TL;DR

### Shipped

1. **AI Module: Global Guardrails Feature** The site-wide guardrail set (issue #3584851, MR!1495) was merged by Marcus Johansson, adding a guardrail applied to every AI request with update hook, ordering support, and a delete hook.
2. **AI Dashboard: Admin Menu Entry** MR!17 landed on `1.0.x`, adding a menu entry at `/admin/config/ai/dashboard` so the dashboard is no longer hidden from the standard configuration UI.
3. **AI Module: aiCKEditor HTML Encoding Bug Fixed** MR!1353 resolved raw HTML entities appearing in the selected-text preview inside aiCKEditor (issue #3540608).
4. **Drupal Canvas: Six MRs Merged** Fixes landed for contextual panel width reset (MR!638), two Cypress flakiness issues (MR!950, MR!967), `dataDependencies.entityFields` schema addition (MR!929), a Redux field-widget refactor (MR!774), and CLI tool prop-omission support (MR!979).
5. **Drupal AI Initiative: Issue Templates and Credential Security** Three MRs closed issue #3581782, shipping generic and sub-topic GitLab issue templates, and Drupal CMS 2.1.0 confirmed Easy Encryption as the default credential protection layer for AI providers (issue #3559052).

### Ongoing

1. **AI Module: Assistant API Session Regression** MR!978 (issue #3554797) correctly fixes the anonymous session-cookie bug but regresses `session_one_thread` persistence after the first message, leaving the fix blocked.
2. **Context Control Center: Pre-RC1 UX Audit** The "Improve Context Items List View" MR (issue #3586140) is in needs-review but blocked on token terminology clarity, unresolved moderation state visibility, and scope column rendering; no MRs have merged this period.
3. **Context Control Center: Dynamic Local Tasks** Issue #3585041 reached RTBC after mglaman's review but has not yet been merged due to potential cache-rebuild edge cases.
4. **AWS Bedrock Provider: Inference Profile Support** MR!17 adds 105-line support for routing requests via AWS inference profiles but has received no visible reviewer activity and remains unmerged.
5. **Postgres VDB Provider: Schema Bloat Refactor** MR!21 (issue #3576852) is a 1,591-line schema refactor pending review; nothing has landed and the size of the diff makes review the primary bottleneck.

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

_[View issues data](/issue_analysis/#/1d-data?id=ai-context)_

#### UX Push Toward RC1

The dominant activity this period is a pre-RC1 UX audit driven by aidanfoster (#3573715). The review covers naming conventions (confirming "Context Item" as the canonical unit noun), scope terminology, and a broad set of interaction-state improvements. Because emma-horrell is currently unavailable, the review is missing its usual two-person sign-off; kepol plans to complete a full read-over and the team is discussing whether to spin off child issues for discrete, uncontroversial changes.

A related issue, "Improve Context Items List View" (work item 3586140), is now in needs-review. aidanfoster posted mockups and a walkthrough video proposing additions to the list view: search filters, sortable columns, type icons with tooltips, and a scope column (renamed from "Target"). kepol flagged three concerns blocking merge: token terminology is opaque to content editors, moderation state visibility is unresolved, and the scope column rendering needs more consideration. Review is queued for the Monday UX call.

#### Dynamic Local Tasks

Issue #3585041, which addresses dynamically generating local tasks for scopes rather than relying on static definitions, reached RTBC after review by mglaman, with a note about potential cache-rebuild edge cases. kepol indicated intent to merge it promptly; no MR appears in the 24-hour window yet.

#### Access and Contributor Housekeeping

A new issue (work item 3586139) was opened to add regular contributors as GitLab Reporter members. Tim L is compiling the full contributor list.

**No MRs were merged and no commits landed in this period.**

### AI Dashboard

_[View issues data](/issue_analysis/#/1d-data?id=ai-dashboard)_

#### Merged

MR !17 (issue #3580675) landed on the `1.0.x` branch on 2026-04-24, contributed by Tamás Brückner (brtamas) and merged by a.dmitriiev. The change adds a menu entry at `/admin/config/ai/dashboard`, making the AI Dashboard accessible from the standard `admin/config` overview page under the "AI" section. Previously, no link existed there, leaving the dashboard effectively hidden from the configuration UI. The commit (`1c9a7978`) covers a modest 33-line diff to register the new router path and menu item.

#### Contributors

brtamas authored the patch; robloach reviewed and provided a screenshot confirming the fix; a.dmitriiev closed the issue on merge.

#### Status

Activity in this 24-hour window was limited to that single merged item. No API changes, no new hooks, and no blocking issues were noted. The module appears to be in a stabilisation phase ahead of a 1.0 release, with sprint work focused on surface-level discoverability improvements rather than core functionality changes.

### Drupal AI Initiative

_[View issues data](/issue_analysis/#/1d-data?id=ai-initiative)_

#### Merged

Three MRs from jjchinquist landed on `main` within the 24-hour window, all closing issue #3581782. !1 added the `AI Marketing Initiative - Generic` issue template, !2 documented branch-naming and template conventions in the README and cleaned up the generic template, and !3 added four sub-topic templates (`Blog Entry`, `Video`, `Case Study`, `Webinar`) alongside a contribution-workflow section in the README (commits 38ca7233, b51ab860, 89c291be, a90e2498). The companion issue #3582480 (GitLab board and label workflow) was also closed; jjchinquist confirmed that scoped `state::*` labels are distinct from the native State field, resolving a concern raised by kepol about project-wide side effects.

#### Credential Security

mxr576 confirmed on the long-running issue #3559052 that Drupal CMS 2.1.0 ships Easy Encryption as the default protection layer for plain-text AI and VDB provider credentials. The issue is effectively resolved and is pending formal closure.

#### Blockers

The `daRequest` for YouTube embed support on drupal.org (#3567516) remains unresolved; B_man noted it is in review but DDoS mitigation work at the DA is delaying deployment. The `Add DA YouTube channel managers` request (#3584835) is also stalled pending confirmation from hestenet. Promotional imagery for The AI Summit London (#3585956) is blocking the landing-page creation task (#3586408); pdjohnson has explicitly asked slawrence10 to prioritise it early in Sprint 2.

### AI (Artificial Intelligence)

_[View issues data](/issue_analysis/#/1d-data?id=ai)_

#### Merged

Three MRs landed in this period. The global guardrails feature (#3584851, MR!1495) was merged by Marcus Johansson, adding a site-wide guardrail set applied to every AI request, including an update hook, ordering support, and a delete hook. The aiCKEditor HTML encoding bug (#3540608, MR!1353) was resolved by Hrishikesh Dalal, fixing raw HTML entities appearing in the selected-text preview. A small but important fix to `AgentRunner.php` (#3586385, MR!1534) was merged by Marcus Johansson to ensure configuration is correctly set on the agent runner.

#### In Progress

The `ai.provider_config` config schema fix (#3586384, MR!1532) is at RTBC and nearly ready. Guardrails support for AI Automators (#3585690, MR!1528) is in review after joshua1234511 implemented `InputInterface::setGuardrailSet()` and reviewers from AkhilBabu added two suggestions. The `RestrictToTopic` guardrail is being extended with a semantic matching mode using a similarity threshold and surface metadata for unmatched topics.

#### Blockers and Issues

The assistant API session bug (#3554797, MR!978) remains unresolved: scottfalconer identified that while the anonymous session-cookie fix is correct, the MR regresses `session_one_thread` persistence after the first message. The queue worker exception handling (#3571498, MR!1535) is newly opened, proposing to rethrow caught exceptions so downstream processors can observe failures. An MDXEditor extension set error (#3584676) has a fork created but no patch yet.

### Drupal Canvas

_[View issues data](/issue_analysis/#/1d-data?id=canvas)_

#### Merged This Period

Six merge requests landed in the past 24 hours. lauriii's MR!638 fixes contextual panel width resetting when the left sidebar is toggled (issue #3574994). Two Cypress flakiness fixes were merged: penyaskito resolved race conditions and magic sleeps in `multivalue-form-design*` tests (MR!950, #3586022), and bnjmnm fixed `pattern.cy.js` instability (MR!967). On the data model side, penyaskito added `dataDependencies.entityFields` to the `JavaScriptComponent` config schema (MR!929, #3585298). balintbrews updated the CLI tool to allow omitted props in Workbench page specs and component mocks (MR!979). justafish consolidated module installs across Playwright tests (MR!978), and penyaskito updated the PHPCS config to selectively comply with `Drupal.Arrays.Array.LongLineDeclaration` targeting Drupal 11 (MR!969). bnjmnm also landed a Redux field-widget refactor shifting linker and component-patch responsibilities (MR!774, #3578635).

#### Open Work of Note

bnjmnm has two substantial drafts (MR!981 and MR!973, together ~4600 diff lines) targeting the absence of popover staging in CI (#3586589). longwave opened MR!980 to add a content entity reference well-known type. lauriii has open MRs targeting a 500 error on empty required formatted text fields (MR!982) and iframe height not updating on dynamic content changes (MR!971). florenttorregrosa's MR!961 addresses `ComponentPluginManager` decorator compatibility for contrib modules.

#### CI and Infrastructure

justafish (MR!976) and wimleers (MR!977) are both working to reduce wasteful CI job execution, with wimleers also proposing more selective PHPCS exclusions (MR!975). A Playwright snapshot-based proof-of-concept from isholgueras (MR!974) remains exploratory at ~3500 diff lines.

### AWS Bedrock Provider

_[View issues data](/issue_analysis/#/1d-data?id=ai-provider-aws-bedrock)_

#### In Progress

The only notable activity in this period is an open merge request from contributor RatNeurons adding support for inference profiles (MR !17, branch `3586773-inference-profiles-arent`, 105 diff lines). Inference profiles allow AWS Bedrock users to route requests across regions or use application inference profiles, and their absence had been a functional gap in the module. The MR has not yet been merged and no commits landed in the tracked window.

#### Blocking Progress

No issues were updated and no commits were recorded in the 24-hour window, suggesting the inference profile work is pending review rather than actively iterating. There is no visible reviewer activity or inline feedback on MR !17 from the available data, which may indicate the MR is waiting on a maintainer pass before it moves forward.

#### Notes

Given the lack of merged code or issue triage, the module saw minimal forward progress in this period. Developers relying on inference profile support should monitor MR !17 for merge status rather than expecting it in any immediate release.

### Tool API

_[View issues data](/issue_analysis/#/1d-data?id=tool)_

#### Active Development

No commits landed in the past 24 hours, but three merge requests are open and under active review.

scottfalconer opened MR !85 against issue #3582933, adding control over Tool return formats (330 diff lines). This is a feature addition, likely introducing new return-type configuration to the Tool plugin interface. A fork was created for the issue on 2026-04-24, suggesting active iteration. MR !84, also from scottfalconer, targets the `LogMessage` tool bug (#3554285) with a 350-line diff -- the scope suggests more than a trivial fix, possibly a refactor of how the tool structures or emits log entries.

#### Bug Fixes in Review

MR !76, authored by b_sharpe, addresses a context data loss bug in the AI Connector integration (#3576586). The fix is small (13 diff lines) and sets parent context data alongside input during tool execution. michaellander noted uncertainty about whether a related fix had already shipped during the GitLab migration, and flagged that a token-based solution may still produce failures in some call paths. This issue remains in "Needs Review" and unassigned.

#### Blockers

The context data bug (#3576586) is the most pressing open item. Confusion introduced by the GitLab migration has made it unclear what has and has not landed, which may be masking regressions.

### Postgres VDB Provider

_[View issues data](/issue_analysis/#/1d-data?id=ai-vdb-provider-postgres)_

#### Active Development

The only notable activity in this period is an open merge request (MR !21) from contributor **ezeedub**, targeting issue #3576852 under the branch `3576852-reduce-schema-bloat`. The MR is substantial at 1,591 diff lines and addresses schema bloat reduction, suggesting a significant refactor of how the module manages its PostgreSQL schema footprint. No commits landed in the 24-hour window, meaning nothing has been merged or shipped yet.

#### Blockers and Status

Progress is effectively paused pending review of MR !21. Given the size of the diff, thorough review will likely be the primary bottleneck before this work can land. No additional issues were updated during this period, and there are no parallel workstreams visible at this time.

#### What to Watch

Once merged, the schema changes introduced in this MR could affect upgrade paths or existing database configurations for sites running the module. Developers maintaining custom integrations with `ai_vdb_provider_postgres` should monitor MR !21 closely for any schema migration hooks or changes to table definitions that may require downstream adjustments.

