# Drupal AI Activity Newsletter

_Period: 2026-04-23 to 2026-04-24_

## TL;DR

1. In the `ai` module, MR !1495 merged global guardrails support (#3584851), enabling guardrail checks across every AI request globally, with a follow-on issue (#3585690) already tracking guardrails integration specifically within AI Automators.
2. In the `ai` module, MR !1353 fixed HTML encoding of special characters and trailing spaces in the CKEditor selected text preview (#3540608), closing two long-standing competing MRs (!1264, !821).
3. In `canvas`, Wim Leers merged !962 introducing `ComponentInstanceInputsConfigSchemaGeneratorInterface` (#3586342) as the first step toward symmetrically translatable component trees, and landed ADR !624 formalizing a new "entity reference" prop type for code components.
4. In `canvas`, Ben Mullins merged fixes for UI flickering in multi-value props (!959), failure to remove values from the preview pane on deletion (!964), and a flaky Cypress test (!967), alongside a Redux-integrated field widgets refactor (!774).
5. In the `tool` module, MR !76 proposes a fix for context data being lost after tool execution in the AI Connector submodule (#3576586), but remains unmerged and awaiting maintainer review.

---

### ai_context

#### Status

No merge requests or commits landed in the 24-hour window ending 2026-04-24T12:38:03+00:00. Activity was limited to issue tracker discussion as the module works toward an rc1 release.

#### Pre-RC1 UX Work

The most active thread is a lightweight UX review of the Collaborative Context Configuration (CCC) interface (#3573715, 21 comments), led by aidanfoster. This review is a stated prerequisite for tagging rc1 and covers the full CCC workflow. A related issue calls for improvements to the Context Items list view, likely addressing layout or usability gaps surfaced during that review.

#### Contributor Access

kepol opened a housekeeping issue to add regular CCC contributors as GitLab Reporter members, which would give them triage and issue management permissions. This has two comments but no resolution yet, meaning some active contributors may still lack the access needed to manage their own work items.

#### Blockers

The UX review ticket is the primary gate for rc1. Until that review concludes and any identified changes are implemented, no release candidate work is expected to land. The absence of any MRs or commits suggests the team is in a planning and feedback phase rather than active implementation.

### ai_dashboard

#### Shipped

MR !17, authored by brtamas (Tamas Bruckner), was merged into the `1.0.x` branch on 2026-04-24, closing issue #3580675. The change adds a menu item that surfaces the AI Dashboard under the `admin/config` overview page, making it discoverable alongside other configuration sections without requiring direct URL access. The single commit (`1c9a7978`) covers this addition.

#### Notes

No API changes or bug fixes were included in this window. There are no open blockers reported against the module in this period. The work was tagged under the AI Initiative Sprint and AI Product Development categories, suggesting it is part of coordinated roadmap progress rather than an ad hoc patch.

### ai_initiative

#### Repository Infrastructure

The only code activity in this window came from jjchinquist, who landed all three open merge requests against the `ai_initiative` repository within a few hours on 2026-04-24. MR!1 introduced a Marketing Generic issue template, MR!2 documented branch naming and template conventions in the README and cleaned up that generic template, and MR!3 added four sub-topic issue templates (covering the marketing workstreams) alongside a contribution workflow section in the README. The work closes #3581782 (issue template creation) and #3582480 (GitLab workflow and board setup), both of which are now marked closed. A companion issue (#3586382) documenting the contribution workflow for new marketing contributors was opened but has minimal discussion so far.

#### Coordination and Process

The period saw heavy organisational activity rather than product code. A podcast series, "Drupal AI in Practice," was formally bootstrapped by jmsaunders and domidc under #3586383, with a full breakdown of foundation, infrastructure, content framework, guest pipeline, and Episode 1 tasks filed as individual issues. Sprint 2 planning (#3585830) is underway, and migration of marketing contributors from Drupal.org issues to GitLab (#3586381) is in `needsReview`.

#### Blockers

GitLab membership gaps are flagged in an unlinked issue opened by kepol: several AI Initiative issue maintainers are not yet added as GitLab members, which risks blocking triage and MR review as the workflow migration completes.

### ai

#### Merged

Two MRs landed in the past 24 hours. Marcus Johansson's MR !1495 merged global guardrails support into the core module (#3584851), providing a mechanism to apply guardrail checks to every AI request globally. Separately, Hrishikesh Dalal's MR !1353 merged a fix for HTML encoding in the AI CKEditor selected text preview (#3540608), resolving a long-standing issue where special characters and trailing spaces were incorrectly HTML-encoded; this closes out two earlier competing MRs (!1264, !821) that had been open for some time.

#### Active Work

`AgentRunner.php` is missing configuration injection, covered by #3586385. Marcus Johansson has two MRs open against it (!1533 closed in favour of !1534), so one active MR remains under review. A.dmitriiev opened MR !1532 to correct the config schema for the `ai.provider_config` form element (#3586384, tagged `needsReview`), which currently does not reflect the structure the form element actually returns.

Cadence96 has an open MR (!1531) to hide `field_connections` in AI Automators until a workflow is selected, improving UX. A follow-on issue (#3585690) is tracking guardrails support specifically within AI Automators, building on the global guardrails work just merged.

#### Blockers

The `MDXEditor` extension set error (#3584676) and the `RestrictToTopic` semantic matching feature (#3584977) remain unassigned and unresolved.

### canvas

#### Merged this period

Six MRs landed in the 24-hour window. Ben Mullins (bnjmnm) shipped three fixes: UI flickering when adding or removing items in multi-value props (!959, #3579026), a failure to remove values from the preview pane on deletion (!964, #3586289), and a flaky `pattern.cy.js` Cypress test (!967, #3586137). His !774 refactor (#3578635) also merged, shifting linker and component patch responsibilities within the Redux-integrated field widgets layer.

Wim Leers merged two significant pieces: an ADR (!624, #3573831) documenting a new "entity reference" prop type for code components enabling view-mode combinations of multiple entities with static inputs, and !962 (#3586342) which introduces `ComponentInstanceInputsConfigSchemaGeneratorInterface` as step one toward symmetrically translatable component trees. Christian Lopez Espinola (penyaskito) merged a PHPCS config update (!969, #3586535) aligning with Drupal 11 rules, selectively complying with `Drupal.Arrays.Array.LongLineDeclaration`. mglaman fixed an assertion failure in component update when a required prop already exists in both old and new versions (!692, #3577603).

#### In progress and blocking work

Ongoing flakiness in multivalue Playwright tests (#3586288) is actively blocking progress, with a separate effort to consolidate module installs in Playwright (!978) and another to avoid wasteful Playwright runs in CI (!977, wimleers, draft). florenttorregrosa's `ComponentPluginManager` decorator contrib-compatibility MR (!961) and the React Hook Form integration (!489) remain open without resolution.

### minikanban

#### Documentation

The only activity in this period was documentation-focused. Two merge requests from contributor **orkut** relate to onboarding content: MR !18 (branch `3451057-how-to-use`, resolving issue #3451057) was closed, while MR !19 (branch `1.0.x`) was opened, proposing a `README.md` with tutorial content covering basic module usage.

The closure of MR !18 alongside the opening of MR !19 suggests the README approach was reconsidered and resubmitted against the `1.0.x` branch directly rather than a dedicated feature branch. No commits landed in this window, so the README has not yet been merged into the codebase.

#### Status

No code changes, bug fixes, or API modifications occurred during this period. There are no updated issues on record. Progress on the documentation MR (!19) is pending review; until it merges, the module ships with no user-facing guidance. No blocking technical issues were flagged.

### tool

#### Bug Fixes in Progress

The primary activity in the last 24 hours centres on a bug affecting the AI Connector submodule. Issue [#3576586](https://www.drupal.org/node/3576586) identifies that context data is lost after tool execution, with the root cause being that parent context data is not being set alongside the input. MR !76 by `b_sharpe` (branch `3576586-ai-connector--`) proposes a fix and is currently in `needs review`. No commits have landed yet, so this remains unmerged.

#### New Proposals

`michaellander` opened a proof-of-concept issue proposing that Tool API tools be callable directly via Symfony's tool caller, which would improve interoperability with the Symfony AI stack. This is early-stage with no MR attached yet.

#### What is Blocking Progress

MR !76 is awaiting review and has generated discussion (4 comments on the issue) but no maintainer sign-off. The context data regression is categorised as normal priority, so it is not blocking a release, but it does affect AI Connector workflows where tool execution discards parent context.

No API changes or new releases shipped during this period.

### ai_vdb_provider_postgres

#### Open Merge Requests

Two merge requests are currently open but no commits landed in the past 24 hours, meaning nothing has been shipped to the codebase in this period.

**MR !21** from ezeedub targets schema bloat reduction (issue #3576852). The branch `3576852-reduce-schema-bloat` suggests work to trim unnecessary schema definitions, likely addressing over-provisioned table structures or redundant index declarations in the module's vector database integration layer. No details on specific schema changes are visible without inspecting the diff, but this could affect how collection tables are registered with Drupal's database abstraction layer.

**MR !17** from garvitasakhrani addresses an undeclared module dependency (issue #3568148). The branch `3568148-undeclared-dependency-on` indicates the module is missing a formal dependency declaration in its `.info.yml`, which would cause silent failures if a required module is absent. This is a correctness fix rather than a feature change, but it blocks reliable installation in automated environments.

#### Blockers and Status

Neither MR has been merged, and there is no maintainer review activity visible in this window. Both patches are waiting on review. The undeclared dependency issue in MR !17 is worth prioritising as it represents a hard correctness problem for any downstream module relying on this provider.

