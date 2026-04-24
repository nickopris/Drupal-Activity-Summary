# Drupal AI Activity Newsletter

_Period: 2026-04-23 to 2026-04-24_

## TL;DR

### Shipped

1. **AI Dashboard Admin Menu Link** The AI Dashboard is now discoverable at `admin/config/ai/dashboard` after MR !17 added a missing menu item to the standard configuration UI.
2. **Global Guardrails Feature (AI module)** MR !1495 ships globally applied guardrail sets across every AI request, including ordering support, an update hook, and automated tests.
3. **AI CKEditor HTML Encoding Fix** MR !1353 corrects raw HTML entities being exposed in the selected-text textarea preview before submission in the CKEditor integration.
4. **AgentRunner.php Configuration Fix** MR !1534 resolves incorrect configuration handling in `AgentRunner.php`, a same-day turnaround fix tracked in #3586385.
5. **Drupal Canvas `dataDependencies.entityFields` Schema** MR !929 extends the `JavaScriptComponent` config schema to allow JavaScript components to declare entity field dependencies, a notable data model addition.

### Ongoing

1. **AI Automators Guardrails API Review** MR !1528 introducing `InputInterface::setGuardrailSet()` is under review with two pending suggestions from AkhilBabu before it can merge.
2. **Assistant API Session Persistence Bug** MR !978 addressing `session_one_thread` breakage after the first message (#3554797) remains blocked by permission issues preventing a status change from RTBC.
3. **Tool API Context Loss Bug** MR !76 proposes preserving parent context data across `execute()` calls in the AI Connector integration (#3576586), but unresolved edge cases around the token-based context mechanism are blocking merge.
4. **Postgres VDB Schema Bloat Refactor** MR !21 from ezeedub carries a 1,591-line diff restructuring the module's database schema (#3576852) and is stalled awaiting maintainer review.
5. **Canvas React Hook Form Integration** MR !489 (6768 diff lines) from bnjmnm remains open and is likely blocking downstream form-handling work in Drupal Canvas.

---

### AI Dashboard

#### Merged

MR !17 (issue #3580675) landed on the `1.0.x` branch on 2026-04-24, contributed by Tamás Brückner (brtamas) and reviewed by robloach. The change adds a menu item so that the AI Dashboard is reachable from the `admin/config` overview under the "AI" section, routed at `/admin/config/ai/dashboard`. Previously, no link existed on that page, leaving the dashboard effectively undiscoverable from the standard configuration UI. The patch is small (33 diff lines) and a.dmitriiev confirmed the merge.

#### No Blocking Issues

Activity in the window was limited to this single task. No open regressions, failing tests, or API changes were recorded. No deprecations or hook/service interface changes are introduced by this commit.

#### Contributors

brtamas (patch), robloach (review), a.dmitriiev (merge).

### ai_initiative

#### Merged

Three MRs from jjchinquist landed on `main` within the 24h window, all closing out work tracked in #3581782. MR !1 added the `AI Marketing Initiative - Generic` issue template (74 diff lines); MR !2 documented branch-naming and template conventions in the README and cleaned up the Generic template (68 lines); MR !3 added four sub-topic templates -- Blog Entry, Video, Case Study, and Webinar -- and embedded contribution-workflow documentation in the README (369 lines). All five templates are now live on `main` (commits 38ca7233, b51ab860, 89c291be, a90e2498). Issue #3582480 (GitLab board and label setup) was closed simultaneously, with jjchinquist confirming scoped `state::*` labels are distinct from the built-in State field and do not affect non-marketing work in the queue.

#### Security

mxr576 posted a long-overdue update on #3559052 (credential storage hardening): Drupal CMS 2.1.0 ships the `easy_encryption` module as default protection for plaintext provider credentials. Contrib modules and recipes can now treat it as a standard dependency for secrets at rest.

#### Blocked / Needs Action

The `glab api` CLI skill (#3586406) has a documented data-corruption trap: `@file` syntax for the `-f` flag is silently unsupported on drupalcode.org. The YouTube channel manager access (#3584835) is stalled pending pdjohnson confirming acceptance with hestenet. The d.o CKEditor media-embed feature (#3567516, needed for content creation on the initiative site) is in review but deploy timing is uncertain due to ongoing DDoS mitigation load.

### AI (Artificial Intelligence)

#### Merged

Three MRs landed in this period. MR!1495 (by Marcus_Johansson) ships the global guardrails feature (#3584851), adding a globally applied guardrail set to every AI request, with ordering support, an update hook, and automated tests. MR!1353 (by hrishikesh-dalal) fixes HTML encoding in the AI CKEditor selected-text preview (#3540608), correcting raw HTML entities being exposed in the textarea before submission. MR!1534 (by Marcus_Johansson) is a small fix ensuring `AgentRunner.php` correctly sets configuration (#3586385, 12 diff lines).

#### In Progress

`InputInterface::setGuardrailSet()` is the new API surface introduced for Guardrails support in AI Automators (#3585690, MR!1528), currently in review with two suggestions pending from AkhilBabu. The `ai.provider_config` config schema fix (MR!1532, #3586384) is at RTBC and close to merge.

The assistant API session bug (#3554797, MR!978) remains blocked: scottfalconer identified a regression where `session_one_thread` persistence breaks after the first message, and MR!978 has been updated to address it, but permission issues are preventing a status change from RTBC.

The queue worker exception rethrow (#3571498, MR!1535) is newly opened by scottfalconer; the core problem is that caught exceptions are not reraised, preventing queue runners from observing failures.

#### Also Notable

A fork was created for the MDXEditor `[object Object]` extension error (#3584676), and valthebald filed #3586385 for `AgentRunner.php` configuration handling, which was resolved same-day.

### Drupal Canvas

#### Merged This Period

Six MRs landed in the 24-hour window. The most significant is MR !929 (penyaskito), which adds `dataDependencies.entityFields` to the `JavaScriptComponent` config schema -- a data model extension that enables JavaScript components to declare entity field dependencies. MR !774 (bnjmnm) shipped a refactor titled "Simplify args," shifting linker and component patch responsibilities within Redux-integrated field widgets. MR !692 (mglaman) fixed an assertion failure in component update logic when a required prop already exists in both the old and new component versions. On the tooling side, MR !978 (justafish) consolidates module installs across Playwright tests, MR !950 (penyaskito) resolves flaky `multivalue-form-design*.cy.js` Cypress tests by intercepting a race condition, and MR !969 updates the PHPCS config to selectively comply with `Drupal.Arrays.Array.LongLineDeclaration` for Drupal 11.

#### Open Work of Note

CI overhead is a theme: MR !977 (wimleers) proposes avoiding unnecessary E2E jobs, MR !976 (justafish) adds additional GitLab CI caching, and a draft PoC (MR !974, isholgueras) explores Playwright snapshot-based testing. MR !961 (florenttorregrosa) addresses `ComponentPluginManager` decorator compatibility for contrib. The large React Hook Form integration (MR !489, bnjmnm, 6768 diff lines) and the "symmetric content inputs" draft (MR !882, tedbow) remain open and are likely blocking downstream form-handling work. MR !638 (lauriii) fixing static contextual panel width on left sidebar toggle also awaits review.

### Tool API

#### In Progress

The primary active work centres on issue #3576586, a bug where context data is lost after `execute()` in the AI Connector integration. MR !76, authored by b_sharpe, proposes setting parent context data alongside input to preserve state across calls. The MR is open and under review, with 13 diff lines changed. michaellander noted some uncertainty around whether a prior fix was actually merged during the GitLab migration, and flagged that even with the proposed solution there may be edge cases where failures occur, particularly around the existing token-based context mechanism. No commits landed in this window.

#### New Proposals

michaellander opened a proof-of-concept issue proposing that Tool API tools be callable directly via Symfony's tool caller interface. No code or MR is attached yet, and the issue has no comments, so it is early exploration.

#### Blockers and Notes

Nothing was merged or shipped in this 24-hour period. The main blocker on #3576586 is the unresolved question from michaellander about potential failures even after the fix is applied, which needs testing before the MR can advance. The GitLab migration appears to have introduced some tracking ambiguity around previously attempted fixes.

### Postgres VDB Provider

#### In Progress

The only activity in this period is an open merge request from contributor **ezeedub** addressing schema bloat (MR !21, resolving issue #3576852). The branch `3576852-reduce-schema-bloat` carries a substantial diff of 1,591 lines, suggesting a significant refactor of how the module manages its database schema structure. No commits landed in the 24-hour window, meaning nothing has been merged or shipped yet.

#### Blockers

Progress is effectively paused pending review of MR !21. The size of the diff warrants careful attention from maintainers, as schema changes in a vector database provider can have downstream implications for sites using pgvector indexes or relying on the module's table layout for custom queries. No other issues or merge requests were active in this period.

