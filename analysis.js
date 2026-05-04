(() => {
  // ---------------------------------------------------------------------------
  // Data loading — resolve latest JSON from the digest folder
  // ---------------------------------------------------------------------------

  // The JSON is written to the same directory as this page (issue_analysis/).
  // A stable copy named `latest.json` is written on each digest run.
  async function findLatestJson() {
    try {
      const res = await fetch('latest.json', { method: 'HEAD' });
      if (res.ok) return 'latest.json';
    } catch (_) {}
    return null;
  }

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function fmtDate(iso) {
    if (!iso) return '';
    const [y, m, d] = iso.slice(0, 10).split('-');
    return `${d}-${m}-${y}`;
  }

  // ---------------------------------------------------------------------------
  // Flatten JSON into a uniform items array
  // ---------------------------------------------------------------------------

  function flattenData(json) {
    const items = [];

    for (const mod of json.modules) {
      const module = mod.title || mod.machine_name;

      for (const issue of mod.issues || []) {
        items.push({
          type: 'issue',
          module,
          id: `${mod.machine_name}-issue-${issue.iid}`,
          title: issue.title,
          state: issue.state,
          url: issue.web_url,
          drupalUrl: issue.drupal_url,
          drupalNumber: issue.drupal_issue_number,
          labels: issue.labels || [],
          author: issue.author,
          assignees: issue.assignees || [],
          commentCount: issue.comment_count,
          mrCount: issue.mr_count,
          createdAt: issue.created_at,
          updatedAt: issue.updated_at,
          confidential: issue.confidential,
        });
      }

      for (const mr of mod.merge_requests || []) {
        items.push({
          type: 'mr',
          module,
          id: `${mod.machine_name}-mr-${mr.iid}`,
          title: mr.title,
          state: mr.merged_at ? 'merged' : mr.state,
          url: mr.web_url,
          labels: mr.labels || [],
          author: mr.author,
          assignees: mr.assignees || [],
          branch: mr.source_branch,
          diffLines: mr.diff_lines,
          createdAt: mr.created_at,
          updatedAt: mr.updated_at,
        });
      }

      for (const commit of mod.commits || []) {
        items.push({
          type: 'commit',
          module,
          id: `${mod.machine_name}-commit-${commit.short_id}`,
          title: commit.title,
          state: null,
          url: commit.web_url,
          labels: [],
          author: commit.author_name,
          assignees: [],
          shortId: commit.short_id,
          updatedAt: commit.authored_date,
        });
      }
    }

    return items;
  }

  // ---------------------------------------------------------------------------
  // Populate filter dropdowns from data
  // ---------------------------------------------------------------------------

  const BOT_USERS = new Set(['drupalbot']);

  function populateFilters(items, json) {
    const modules = [...new Set(items.map(i => i.module))].sort();
    const states  = [...new Set(items.map(i => i.state).filter(Boolean))].sort();
    const labels  = [...new Set(items.flatMap(i => i.labels))].sort();
    const users   = [...new Set(items.flatMap(i => {
      const u = [];
      if (i.author && !BOT_USERS.has(i.author)) u.push(i.author);
      u.push(...i.assignees.filter(a => !BOT_USERS.has(a)));
      return u;
    }).filter(Boolean))].sort();

    fill('filter-module', modules);
    fill('filter-state',  states);
    fill('filter-label',  labels);
    fill('filter-user',   users);

    const since = json.since ? json.since.slice(0, 10) : '';
    const until = json.until ? json.until.slice(0, 10) : '';
    document.getElementById('period-label').textContent =
      since && until ? `${since} → ${until}` : '';
  }

  function fill(id, values) {
    const sel = document.getElementById(id);
    for (const v of values) {
      const opt = document.createElement('option');
      opt.value = v;
      opt.textContent = v;
      sel.appendChild(opt);
    }
  }

  // ---------------------------------------------------------------------------
  // Card rendering
  // ---------------------------------------------------------------------------

  const TYPE_LABELS = { issue: 'Issue', mr: 'MR', commit: 'Commit' };
  const TYPE_CLASS  = { issue: 'type-issue', mr: 'type-mr', commit: 'type-commit' };

  function labelClass(label) {
    const l = label.toLowerCase();
    if (l.startsWith('category::bug'))     return 'label-bug';
    if (l.startsWith('category::feat'))    return 'label-feat';
    if (l.startsWith('category::task'))    return 'label-task';
    if (l.startsWith('state::'))           return 'label-state';
    if (l.startsWith('priority::'))        return 'label-pri';
    return 'label-other';
  }

  function renderCard(item) {
    const card = document.createElement('article');
    card.className = 'card bg-white rounded-lg border border-gray-200 shadow-sm p-4 flex flex-col gap-2';
    card.dataset.id = item.id;

    // Header row
    const header = document.createElement('div');
    header.className = 'flex items-start gap-2';

    const typeBadge = document.createElement('span');
    typeBadge.className = `type-badge ${TYPE_CLASS[item.type]} text-xs font-semibold px-2 py-0.5 rounded shrink-0 mt-0.5`;
    typeBadge.textContent = TYPE_LABELS[item.type];

    const titleEl = document.createElement('a');
    titleEl.href = item.url;
    titleEl.target = '_blank';
    titleEl.rel = 'noopener';
    titleEl.className = 'text-sm font-medium text-drupal-blue hover:underline leading-snug';
    titleEl.textContent = item.title;

    header.append(typeBadge, titleEl);
    card.appendChild(header);

    // Module + state row
    const meta = document.createElement('div');
    meta.className = 'flex flex-wrap gap-2 items-center text-xs text-gray-500';

    const moduleEl = document.createElement('span');
    moduleEl.className = 'font-medium text-gray-700';
    moduleEl.textContent = item.module;
    meta.appendChild(moduleEl);

    if (item.state) {
      const stateEl = document.createElement('span');
      stateEl.className = 'bg-gray-100 rounded px-2 py-0.5';
      stateEl.textContent = item.state;
      meta.appendChild(stateEl);
    }

    if (item.type === 'issue' && item.commentCount > 0) {
      const cEl = document.createElement('span');
      cEl.textContent = `💬 ${item.commentCount}`;
      meta.appendChild(cEl);
    }

    if (item.type === 'mr' && item.diffLines) {
      const dEl = document.createElement('span');
      dEl.textContent = `±${item.diffLines} lines`;
      meta.appendChild(dEl);
    }

    if (item.type === 'commit' && item.shortId) {
      const sEl = document.createElement('span');
      sEl.className = 'font-mono bg-gray-100 px-1 rounded';
      sEl.textContent = item.shortId;
      meta.appendChild(sEl);
    }

    if (item.drupalNumber) {
      const dEl = document.createElement('a');
      dEl.href = item.drupalUrl;
      dEl.target = '_blank';
      dEl.rel = 'noopener';
      dEl.className = 'text-gray-400 hover:text-drupal-blue';
      dEl.textContent = `d.o #${item.drupalNumber}`;
      meta.appendChild(dEl);
    }

    card.appendChild(meta);

    // Labels
    if (item.labels.length) {
      const labelsEl = document.createElement('div');
      labelsEl.className = 'flex flex-wrap gap-1';
      for (const label of item.labels) {
        const pill = document.createElement('span');
        pill.className = `label-pill ${labelClass(label)}`;
        pill.textContent = label;
        labelsEl.appendChild(pill);
      }
      card.appendChild(labelsEl);
    }

    // Author / assignees
    const people = document.createElement('div');
    people.className = 'flex flex-wrap gap-1 mt-auto pt-1';

    const allUsers = [];
    if (item.author && !BOT_USERS.has(item.author)) allUsers.push({ name: item.author, role: 'author' });
    for (const a of item.assignees) {
      if (!BOT_USERS.has(a)) allUsers.push({ name: a, role: 'assignee' });
    }

    for (const u of allUsers) {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.title = u.role;
      chip.textContent = (u.role === 'assignee' ? '→ ' : '') + u.name;
      people.appendChild(chip);
    }

    if (allUsers.length) card.appendChild(people);

    // Dates
    if (item.createdAt || item.updatedAt) {
      const dateEl = document.createElement('div');
      dateEl.className = 'text-xs text-gray-400 flex gap-3 justify-end pt-1';
      if (item.createdAt) {
        const s = document.createElement('span');
        s.title = 'Opened';
        s.textContent = 'Opened: ' + fmtDate(item.createdAt);
        dateEl.appendChild(s);
      }
      if (item.updatedAt) {
        const s = document.createElement('span');
        s.title = 'Updated';
        s.textContent = 'Updated: ' + fmtDate(item.updatedAt);
        dateEl.appendChild(s);
      }
      card.appendChild(dateEl);
    }

    return card;
  }

  // ---------------------------------------------------------------------------
  // Filtering logic
  // ---------------------------------------------------------------------------

  let allItems = [];

  function getFilters() {
    return {
      search:  document.getElementById('search').value.trim().toLowerCase(),
      module:  document.getElementById('filter-module').value,
      type:    document.getElementById('filter-type').value,
      state:   document.getElementById('filter-state').value,
      label:   document.getElementById('filter-label').value,
      user:    document.getElementById('filter-user').value,
    };
  }

  function itemMatchesFilters(item, f) {
    if (f.module && item.module !== f.module) return false;
    if (f.type   && item.type   !== f.type)   return false;
    if (f.state  && item.state  !== f.state)   return false;
    if (f.label  && !item.labels.includes(f.label)) return false;
    if (f.user) {
      const users = [item.author, ...item.assignees].filter(Boolean);
      if (!users.includes(f.user)) return false;
    }
    if (f.search) {
      const haystack = [
        item.title,
        item.module,
        item.author,
        ...item.assignees,
        ...item.labels,
        item.state,
        item.branch,
        item.shortId,
      ].filter(Boolean).join(' ').toLowerCase();
      if (!haystack.includes(f.search)) return false;
    }
    return true;
  }

  function applyFilters() {
    const f = getFilters();
    const results = document.getElementById('results');
    const empty   = document.getElementById('empty-state');
    const count   = document.getElementById('result-count');

    let visible = 0;
    for (const card of results.querySelectorAll('.card')) {
      const item = allItems.find(i => i.id === card.dataset.id);
      const show = item && itemMatchesFilters(item, f);
      card.classList.toggle('hidden', !show);
      if (show) visible++;
    }

    count.textContent = `${visible} item${visible !== 1 ? 's' : ''}`;
    empty.classList.toggle('hidden', visible > 0);
    empty.classList.toggle('flex',   visible === 0);
  }

  // ---------------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------------

  async function boot() {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const errEl   = document.getElementById('load-error');

    const url = await findLatestJson();
    if (!url) {
      loading.classList.add('hidden');
      errEl.classList.remove('hidden');
      errEl.textContent = 'No digest data found (latest.json missing). Run `drush ia-daily` first.';
      return;
    }

    let json;
    try {
      const res = await fetch(url);
      json = await res.json();
    } catch (e) {
      loading.classList.add('hidden');
      errEl.classList.remove('hidden');
      errEl.textContent = `Failed to load ${url}: ${e.message}`;
      return;
    }

    allItems = flattenData(json);
    populateFilters(allItems, json);

    // Render all cards once
    for (const item of allItems) {
      results.appendChild(renderCard(item));
    }

    loading.classList.add('hidden');
    results.classList.remove('hidden');
    applyFilters();

    // Wire up filter controls
    for (const id of ['search', 'filter-module', 'filter-type', 'filter-state', 'filter-label', 'filter-user']) {
      const el = document.getElementById(id);
      el.addEventListener(el.tagName === 'INPUT' ? 'input' : 'change', applyFilters);
    }

    document.getElementById('reset-filters').addEventListener('click', () => {
      document.getElementById('search').value = '';
      for (const id of ['filter-module', 'filter-type', 'filter-state', 'filter-label', 'filter-user']) {
        document.getElementById(id).value = '';
      }
      applyFilters();
    });
  }

  boot();
})();
