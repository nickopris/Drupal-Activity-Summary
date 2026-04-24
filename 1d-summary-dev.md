# Drupal AI Activity Newsletter

_Period: 2026-04-23 to 2026-04-24_

## TL;DR

### Shipped

1. **AI module global guardrails** MR !1495 merged support for site-wide guardrail checks applied to every AI request in the core `ai` module.
2. **AI CKEditor HTML-encoding bug fixed** MR !1353 resolved a long-standing bug where special characters and trailing spaces were incorrectly HTML-encoded in the CKEditor selected text preview.
3. **AI Dashboard admin menu entry** MR !17 in `ai_dashboard` added a menu link surfacing the dashboard under `admin/config`, fixing a discoverability problem.
4. **Canvas multi-value prop fixes and architecture** Six MRs merged in `canvas` including UI flicker fixes, removed-value preview corrections, a new `entity reference` prop type ADR, and the `ComponentInstanceInputsConfigSchemaGeneratorInterface` interface for translatable component trees.
5. **AI initiative repository templates** Three MRs landed in `ai_initiative` adding issue templates, branch naming conventions, and a contribution workflow section to the README.

### Ongoing

1. **AI context CCC UX review blocking rc1** Issue #3573715 in `ai_context` has 21 comments and no consensus, stalling all code progress toward the rc1 release candidate.
2. **AI module config schema and AgentRunner fixes** MR !1532 corrects `ai.provider_config` schema mismatch and MR !1534 fixes missing configuration on `AgentRunner` instantiation, both awaiting merge.
3. **Tool API context data loss after execution** MR !76 in `tool` proposes a fix for AI Connector losing parent context data after a tool executes, currently in `needsReview`.
4. **ai_vdb_provider_postgres undeclared dependency** MR !17 addresses a missing `.info.yml` dependency entry that can cause silent installation failures, blocked on maintainer review.
5. **Canvas CI overhead and downstream stabilisation** MRs !977 and !978 target wasteful Playwright runs, while symmetric content inputs (MR !882) and React Hook Form integration (MR !489) remain open and are likely blocking downstream work.

---

### ai_context

#### Status

No merge requests or commits landed in the 24-hour window ending 2026-04-24T12:38:03+00:00. Activity was limited to issue tracking and planning work.

#### Planning and UX

The bulk of discussion is centred on the upcoming rc1 milestone. Issue #3573715, a comprehensive UX review of the Configurable Context Collections (CCC) interface, accumulated 21 comments and remains open with a "Needs UX review" tag. A companion issue was opened to improve the Context Items list view, suggesting the CCC management UI is a known weak point ahead of the release candidate.

#### Housekeeping

A separate issue was opened by kepol to add regular CCC contributors as GitLab reporter members, indicating the project is formalising its contributor access model as it approaches rc1.

#### Blockers

No code is moving until the UX review on #3573715 reaches consensus. With no MRs or commits in the window, the module appears to be in a holding pattern pending decisions on interface design. Developers interested in contributing should focus review effort on the CCC UX thread to unblock forward progress.

### ai_dashboard

#### Merged This Period

One merge request landed in the `1.0.x` branch over this period. MR !17, authored by brtamas (Tamas Bruckner), resolves issue #3580675 by adding a menu item that surfaces the AI Dashboard under the `admin/config` overview page. The commit `1c9a7978` carries the change. Previously the dashboard had no entry point in the standard Drupal configuration section, making it difficult to discover without knowing the direct path.

#### What Changed

The fix is a routing or menu link configuration addition rather than an API change, so no backwards-incompatible changes are expected for modules depending on `ai_dashboard`. No hook or service interface modifications were noted.

#### Blockers and Open Work

No blocking issues were flagged in the period reviewed. The issue closed cleanly after the merge with ten comments indicating reasonable review activity before landing.

#### Contributors

- brtamas (Tamas Bruckner) -- patch author and committer

### ai_initiative

#### Repository Infrastructure

The only code activity in this window was a burst of GitLab repository housekeeping by jjchinquist. Three MRs landed on 2026-04-24: MR!1 added a Marketing Generic issue template, MR!2 documented branch and template naming conventions in the README and cleaned up that generic template, and MR!3 added four sub-topic issue templates alongside a contribution workflow section in the README. All three were merged the same day across four commits (38ca7233, b51ab860, 89c291be, a90e2498). The closed issues #3581782 and #3582480 correspond directly to this work. A follow-on issue is open to finalise the state-label workflow for the new templates (acceptance criteria 1 and 4 from #3582480), which remains unassigned.

#### Marketing Sprint Activity

Sprint 1 (April 13-27, #3583465) is closing out. Several deliverables were resolved: LinkedIn posts for industry guides (#3578729), NYC Summit featured session posts (#3585907), DrupalCon Chicago social media (#3578732), and the Southwark Council webinar setup (#3586060) and process document (#3586051) were all closed. Sprint 2 meta (#3585830) is open and being structured.

A significant new workstream opened: jmsaunders and domidc bootstrapped a "Drupal AI in Practice" podcast initiative (#3586383) with roughly 15 child issues covering infrastructure (RSS feed, directory submission, YouTube channel access), content framework, guest pipeline, and Episode 1 production. Most tasks are unassigned, indicating this is in early planning.

#### Product Development

No code changes landed for the AI Product Development workstream. Active tracked items include the AI CMS Demo System (#3575135), AI Content Review Workflow (#3545606), and the Chicago Driesnote DrupalForge demo (#3583361), all of which remain open without resolution in this period.

#### Blockers

The migration of marketing contributors from Drupal.org issues to GitLab (#3586381) is in `needsReview` and is a prerequisite for normalising the new contribution workflow. Adding missing issue maintainers as GitLab members (#3586380) is also unresolved and likely gates participation for several contributors.

### ai

#### Merged

Two notable MRs landed in the past 24 hours. Marcus Johansson's MR !1495 merged global guardrails support into the core AI module (#3584851), providing a mechanism to apply guardrail checks to every AI request site-wide. Separately, MR !1353 by Hrishikesh Dalal (commit `6f727f06`) fixed a long-standing bug (#3540608) in the AI CKEditor integration where special characters and trailing spaces were incorrectly HTML-encoded in the selected text preview; two earlier competing MRs (!1264, !821) were closed in favour of this resolution.

#### Open Work

Config schema correctness is getting attention: a.dmitriiev opened MR !1532 to fix `ai.provider_config` so its schema matches the actual structure returned by the form element (#3586384). In `AgentRunner.php`, configuration is not being set on instantiation (#3586385); Marcus Johansson has an open MR !1534 addressing this, with a duplicate MR !1533 already closed.

Additional open MRs include a UX improvement to `ai_automators` hiding `field_connections` until a workflow is selected (cadence96, MR !1531) and per-entity content suggestion settings (Ahmad-Khader, MR !1486).

#### Pending and Blocked

Semantic topic matching for the `RestrictToTopic` guardrail (#3584977) is flagged as needing manual testing. The `MDXEditor` extension set error (#3584676) remains triaged but unassigned.

### canvas

#### Merged This Period

Six MRs landed in the 24-hour window. bnjmnm merged three fixes targeting multi-value prop behaviour: MR!959 eliminates UI flickering when adding or removing items (`#3579026`), MR!964 corrects the preview pane not reflecting removed date values (`#3586289`), and MR!967 resolves flakiness in `pattern.cy.js` (`#3586137`). MR!774 (`#3578635`, also bnjmnm) refactors linker and component patch responsibilities in the Redux-integrated field widgets layer. penyaskito landed MR!969 updating the PHPCS config to selectively comply with `Drupal.Arrays.Array.LongLineDeclaration` for Drupal 11 compatibility. wimleers merged two architecture pieces: MR!624 adds ADR #11 documenting a new `entity reference` prop type for code components enabling multi-entity view modes with static inputs, and MR!962 introduces `ComponentInstanceInputsConfigSchemaGeneratorInterface` as step one toward symmetrically translatable component trees (`#3586342`). mglaman's MR!692 fixed an assertion failure in component update when a required prop already exists in both old and new versions.

#### Open Work of Note

CI overhead is a recurring theme: wimleers (MR!977) and justafish (MR!978) are independently attacking wasteful Playwright runs and fragmented module installs. MR!956 addresses a 500 error when clearing a required `uri-reference` link prop. florenttorregrosa's MR!961 targets `ComponentPluginManager` decorator compatibility for contrib modules. Several drafts around symmetric content inputs (MR!882, tedbow) and React Hook Form integration (MR!489, bnjmnm) remain open and are likely blocking downstream stabilisation work.

### minikanban

#### Documentation Activity

The only activity in this 24-hour window was documentation-related, with no code commits or issue updates recorded.

Contributor **orkut** submitted two merge requests around the same topic: MR !18, opened against a feature branch tied to issue #3451057 ("How to use"), was closed, while MR !19 against the `1.0.x` branch remains open and proposes the creation of a `README.md` file with introductory tutorial content. The closure of !18 in favour of !19 suggests the work was rebased or redirected onto the stable branch rather than merged through a topic branch.

#### Status and Blockers

No functional code, API changes, or bug fixes landed in this period. The module appears to lack end-user and developer documentation entirely, and that gap is what is being addressed. MR !19 is still open and awaiting review, so the README has not yet shipped. No other contributors are active, and there are no open issues driving functional work. Progress on documentation is blocked solely on review and merge of !19.

### tool

#### Bug Fixes in Progress

A notable bug is under review affecting the AI Connector submodule: context data is lost after a tool executes (issue #3576586). MR !76, authored by b_sharpe, proposes a fix by setting parent context data alongside input rather than input alone. The branch `3576586-ai-connector--` is open and awaiting review; no commits have landed yet. The issue carries a normal priority and is currently in `state::needsReview`.

#### New API Proposal

michaellander opened a proof-of-concept issue proposing that Tool API tools be callable directly from Symfony's tool caller, which would allow tighter integration with the Symfony AI component layer. No MR is attached yet and the discussion is just getting started.

#### Blockers and Status

No commits were merged in this period. Progress on the context data bug is gated on review of MR !76. The Symfony integration proposal is exploratory and has no assignee or implementation work attached. Developers working with `ToolInterface` implementations or the AI Connector should watch MR !76 closely, as the missing parent context data regression can silently drop state between chained tool calls.

### ai_vdb_provider_postgres

#### Open Work

Two merge requests are currently open against the module with no commits landing in the review window.

MR !21, opened by ezeedub against branch `3576852-reduce-schema-bloat`, targets issue #3576852 and aims to reduce schema bloat. This is likely addressing unnecessary table or column definitions accumulating in the module's database schema declarations, which can cause overhead during schema comparisons and updates.

MR !17, opened by garvitasakhrani against branch `3568148-undeclared-dependency-on`, addresses issue #3568148, which flags an undeclared dependency on another module. Without an explicit entry in the module's `.info.yml` `dependencies` key, installations that lack the required module will fail silently or produce runtime errors rather than a clean dependency resolution error.

#### Status

No commits were merged during this period, so neither fix is in a released state. Progress is blocked on review and approval for both MRs. The undeclared dependency issue (MR !17) is worth prioritising, as it represents a correctness problem that can affect any installation. The schema bloat work (MR !21) is a quality and performance improvement but lower urgency. Maintainers are the current bottleneck.

