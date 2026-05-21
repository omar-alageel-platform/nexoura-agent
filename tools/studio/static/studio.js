/**
 * NEXOURA Studio — SSE client + view router (B3)
 *
 * Routes: #/home (default), #/decisions
 * SSE: subscribes to /api/events on load; fetches /api/state on every
 *      state-changed event and re-renders the active view.
 */
(function () {
  'use strict';

  var _state = null;
  var _route = '/home';
  var _es = null;
  var _sortMode = 'oldest';

  // Stage short codes for the timeline strip
  var STAGE_LABELS = ['REQ','FEAS','BRAND','ARCH','BUILD','GTM','OPS','GATE','LIVE'];

  function $(sel) { return document.querySelector(sel); }

  function esc(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // ── SSE status indicator ───────────────────────────────────────────────

  function setSseStatus(s) {
    var dot = $('#nx-sse-dot'), lbl = $('#nx-sse-label');
    if (!dot || !lbl) return;
    dot.className = 'nx-sse-dot' + (s === 'live' ? ' nx-sse-dot--live' : s === 'error' ? ' nx-sse-dot--error' : '');
    lbl.textContent = s === 'live' ? 'Live' : s === 'error' ? 'Offline' : 'Connecting';
  }

  // ── Routing ───────────────────────────────────────────────────────────

  function parseRoute() {
    var m = (window.location.hash || '#/home').match(/^#\/?(.*)$/);
    return '/' + (m ? (m[1] || 'home') : 'home');
  }

  function setActiveNav(route) {
    document.querySelectorAll('.nx-nav-link').forEach(function (a) {
      var matches = (a.getAttribute('href') || '') === '#' + route;
      a.classList.toggle('nx-nav-link--active', matches);
    });
  }

  function renderView() {
    var app = $('#app');
    if (!app) return;
    var renderer = _renderers[_route];
    app.innerHTML = renderer ? renderer(_state || {}) : '<p class="nx-empty">View not found.</p>';
    attachApproveListeners();
  }

  function navigate(route) {
    _route = route;
    setActiveNav(route);
    renderView();
  }

  window.addEventListener('hashchange', function () { navigate(parseRoute()); });

  // ── API ───────────────────────────────────────────────────────────────

  function fetchState() {
    fetch('/api/state', {credentials:'same-origin'})
      .then(function (r) { return r.json(); })
      .then(function (d) { _state = d; renderView(); })
      .catch(function (e) { console.warn('[studio] /api/state error:', e); });
  }

  // ── SSE ───────────────────────────────────────────────────────────────

  function connectSSE() {
    if (_es) _es.close();
    setSseStatus('connecting');
    try { _es = new EventSource('/api/events'); } catch(e) { setSseStatus('error'); return; }
    _es.addEventListener('open', function () { setSseStatus('live'); });
    _es.addEventListener('state-changed', function () { setSseStatus('live'); fetchState(); });
    _es.addEventListener('error', function () {
      setSseStatus('error');
      setTimeout(function () { if (_es && _es.readyState === EventSource.CLOSED) connectSSE(); }, 5000);
    });
  }

  // ── Approve handler ───────────────────────────────────────────────────

  function attachApproveListeners() {
    document.querySelectorAll('.nx-btn-approve').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var card = btn.closest('.nx-decision-card');
        if (card) card.classList.add('nx-decision-card--approved');
        var badge = document.createElement('span');
        badge.className = 'nx-approved-badge';
        badge.textContent = 'Approved';
        btn.parentNode.replaceChild(badge, btn);
      });
    });
  }

  // ── HOME renderer ─────────────────────────────────────────────────────

  function renderHome(state) {
    var engs  = (state.engagements && state.engagements.data) || [];
    var decs  = (state.decisions   && state.decisions.data)   || [];
    var prs   = (state.prs         && state.prs.data)         || [];
    var eng   = engs[0] || null;
    var prsOpen = prs.filter(function (p) { return p.state === 'open'; }).length;

    var directors = ['Product Director','Design Director','Brand Director','Tech Director','Strategy Director'];

    // Activity feed: up to 10 items from PRs + commits
    var activity = [];
    prs.forEach(function (pr) {
      activity.push({ text: 'PR #'+esc(pr.number)+' '+esc(pr.state)+' — '+esc(pr.title), age: esc(pr.age) });
    });
    engs.forEach(function (e) {
      (e.commits||[]).forEach(function (c) { activity.push({ text: esc(c.message), age: esc(c.age) }); });
    });
    activity = activity.slice(0, 10);

    var h = '';
    h += '<div class="nx-view-title">Home</div>';
    h += '<div class="nx-view-subtitle">Live view of your platform. Updates automatically.</div>';

    // Metric tiles
    h += '<div class="nx-metrics">';
    h += '<div class="nx-tile"><div class="nx-tile__label">Dispatches</div><div class="nx-tile__value">'+engs.length+'</div></div>';
    h += '<div class="nx-tile"><div class="nx-tile__label">Decisions</div><div class="nx-tile__value">'+decs.length+'</div></div>';
    h += '<div class="nx-tile"><div class="nx-tile__label">PRs Open</div><div class="nx-tile__value">'+prsOpen+'</div></div>';
    // Cost runway — never fabricate (Locked Decision #1)
    h += '<div class="nx-tile nx-tile--accent"><div class="nx-tile__label">Cost Runway</div>'
       + '<div class="nx-tile__value--unknown">Cost data not available yet.</div></div>';
    h += '</div>';

    // Directors
    h += '<div class="nx-section-heading">Directors</div><div class="nx-directors">';
    directors.forEach(function (name) {
      h += '<div class="nx-director-card"><span class="nx-dot nx-dot--gray" aria-hidden="true"></span><span>'+esc(name)+'</span></div>';
    });
    h += '</div>';

    // Two-column: engagement + decisions preview
    h += '<div class="nx-home-grid">';

    // Left: engagement
    h += '<div><div class="nx-section-heading">Active Engagement</div>';
    if (eng) {
      h += '<div class="nx-engagement"><div class="nx-engagement__name">'+esc(eng.name)+'</div><div class="nx-stages">';
      for (var i=0; i<STAGE_LABELS.length; i++) {
        var done = i < eng.stage_index, cur = i === eng.stage_index;
        var dc = done ? 'nx-stage__dot--done' : cur ? 'nx-stage__dot--current' : '';
        var lc = cur  ? 'nx-stage__label--current' : '';
        h += '<div class="nx-stage"><span class="nx-stage__dot '+dc+'" aria-hidden="true"></span>'
           + '<span class="nx-stage__label '+lc+'">'+STAGE_LABELS[i]+'</span></div>';
        if (i < STAGE_LABELS.length-1) h += '<div class="nx-stage-line'+(done?' nx-stage-line--done':'')+'" aria-hidden="true"></div>';
      }
      h += '</div></div>';
    } else {
      h += '<p class="nx-empty">No active engagements.</p>';
    }
    h += '</div>';

    // Right: decisions preview
    h += '<div><div class="nx-section-heading">Decisions Waiting</div>';
    var top3 = decs.slice(0,3);
    if (top3.length > 0) {
      h += '<div class="nx-decisions-preview">';
      top3.forEach(function (d) {
        h += '<div class="nx-decision-row"><span class="nx-decision-row__title">'+esc(d.title)+'</span>'
           + '<span class="nx-decision-row__age">'+esc(d.age)+'</span></div>';
      });
      h += '</div>';
      h += '<a href="#/decisions" class="nx-link-subtle">'+(decs.length>3?'See all '+decs.length+' decisions':'See decisions')+'</a>';
    } else {
      h += '<p class="nx-empty">No decisions waiting.</p>';
    }
    h += '</div>';

    h += '</div>'; // .nx-home-grid

    // Activity feed
    h += '<div class="nx-section-heading">Recent Activity</div>';
    if (activity.length > 0) {
      h += '<div class="nx-activity-feed">';
      activity.forEach(function (item) {
        h += '<div class="nx-activity-item"><span class="nx-activity-item__age">'+item.age+'</span>'
           + '<span class="nx-activity-item__text">'+item.text+'</span></div>';
      });
      h += '</div>';
    } else {
      h += '<p class="nx-empty">No activity in the last 24 hours.</p>';
    }

    return h;
  }

  // ── DECISIONS renderer ────────────────────────────────────────────────

  function sortDecisions(decs, mode) {
    var copy = decs.slice();
    if (mode === 'agent') {
      copy.sort(function (a,b) { var aa=(a.agent||'').toLowerCase(), bb=(b.agent||'').toLowerCase(); return aa<bb?-1:aa>bb?1:0; });
    }
    // 'oldest' = default order from cache; 'priority' = no field yet, keep order
    return copy;
  }

  function renderDecisions(state) {
    var decs = sortDecisions((state.decisions && state.decisions.data) || [], _sortMode);
    var h = '';
    h += '<div class="nx-view-title">Decisions</div>';
    h += '<div class="nx-view-subtitle">Items waiting for your approval.</div>';

    // Sort controls
    h += '<div class="nx-decisions-controls"><span class="nx-sort-label">Sort:</span>';
    [['oldest','Oldest first'],['priority','Priority'],['agent','By agent']].forEach(function (s) {
      h += '<button class="nx-sort-btn'+(_sortMode===s[0]?' nx-sort-btn--active':'')+'" data-sort="'+s[0]+'">'+esc(s[1])+'</button>';
    });
    h += '</div>';

    if (decs.length === 0) { h += '<p class="nx-empty">No decisions waiting.</p>'; return h; }

    decs.forEach(function (d) {
      h += '<div class="nx-decision-card">'
         + '<div class="nx-decision-card__header">'
         + '<div class="nx-decision-card__title">'+esc(d.title)+'</div>'
         + '<div class="nx-decision-card__age">'+esc(d.age)+'</div>'
         + '</div>';
      if (d.path) h += '<div class="nx-decision-card__context">'+esc(d.path.split('/').pop())+'</div>';
      h += '<div class="nx-decision-card__summary">'+esc(d.title)+' This item is waiting for your review.</div>';
      h += '<div><div class="nx-decision-card__rec-label">Recommendation</div>'
         + '<div class="nx-decision-card__rec">Approve, or pick an alternative below.</div></div>';
      h += '<div class="nx-decision-card__rationale">No extra rationale yet. See the decision file for details.</div>';
      h += '<div class="nx-decision-card__actions">'
         + '<button class="nx-btn-approve" type="button">Approve</button>'
         // "Pick alternative" — modal is OUT OF SCOPE (B3). Placeholder only.
         + '<a class="nx-link-alt" href="#" title="Coming soon." onclick="return false;">Pick alternative</a>'
         + '</div></div>';
    });

    return h;
  }

  // ── Relative time helper (no library — hand-rolled per spec) ─────

  var _renderers = { '/home': renderHome, '/decisions': renderDecisions, '/projects': renderProjects };

  // ── B4: PROJECTS renderer ─────────────────────────────────────────────

  // 7-stage lifecycle — Locked Decision: FULL for S1-S5, FAST-PATH for S6
  var PROJ_STAGES = [
    { key:'S1', label:'S1 Idea' },
    { key:'S2', label:'S2 Strategy' },
    { key:'S3', label:'S3 Brand' },
    { key:'S4', label:'S4 Design' },
    { key:'S5', label:'S5 Build' },
    { key:'S6', label:'S6 Operate' },
    { key:'S7', label:'S7 Sunset' },
  ];

  function renderProjects(state) {
    var engs  = (state.engagements && state.engagements.data) || [];
    var decs  = (state.decisions   && state.decisions.data)   || [];

    var h = '';
    h += '<div class="nx-view-title">Projects</div>';
    h += '<div class="nx-view-subtitle">Track each product from idea to launch.</div>';

    // Product tabs — only Supply Chain SaaS active; rest are placeholders
    h += '<div class="projects-tabs" role="tablist" aria-label="Products">';
    h += '<button class="projects-tab projects-tab--active" role="tab" aria-selected="true"'
       + ' data-product="supply-chain-saas">Supply Chain SaaS</button>';
    ['Work','One','Enterprise'].forEach(function(p) {
      h += '<button class="projects-tab projects-tab--placeholder" role="tab"'
         + ' aria-selected="false" disabled aria-disabled="true">'+esc(p)
         + ' <span class="nx-nav-badge">Not started</span></button>';
    });
    h += '</div>';

    // Empty state
    if (engs.length === 0) {
      h += '<p class="nx-empty">No projects yet. Start one to see it here.</p>';
      return h;
    }

    // Use first engagement (Supply Chain SaaS)
    var eng = engs[0];
    var stageIdx = typeof eng.stage_index === 'number' ? eng.stage_index : 0;

    // 7-stage timeline
    h += '<div class="projects-timeline" role="list" aria-label="Project stages">';
    PROJ_STAGES.forEach(function(s, i) {
      var done = i < stageIdx;
      var cur  = i === stageIdx;
      var dotC = done ? 'projects-stage__dot--done' : cur ? 'projects-stage__dot--current' : '';
      var lblC = cur  ? 'projects-stage__label--current' : '';
      var curAttr = cur ? ' aria-current="step"' : '';
      h += '<div class="projects-stage" role="listitem"'+curAttr+'>'
         + '<span class="projects-stage__dot '+dotC+'" aria-hidden="true"></span>'
         + '<span class="projects-stage__label '+lblC+'">'+esc(s.label)+'</span>'
         + '</div>';
      if (i < PROJ_STAGES.length - 1) {
        h += '<div class="projects-stage-line'+(done?' projects-stage-line--done':'')+'" aria-hidden="true"></div>';
      }
    });
    h += '</div>';

    // Deliverables grid
    h += '<div class="nx-section-heading">Deliverables</div>';
    var delivs = (eng.deliverables && eng.deliverables[eng.current_stage]) || null;
    if (!delivs) {
      h += '<p class="nx-empty">Data not yet available.</p>';
    } else {
      h += '<div class="projects-deliverables">';
      delivs.forEach(function(d) {
        var status = d.status || 'unknown';
        var pillClass = status === 'shipped' ? 'projects-pill--shipped'
          : status === 'partial'  ? 'projects-pill--partial'
          : status === 'missing'  ? 'projects-pill--missing'
          : 'projects-pill--unknown';
        var pillLabel = status === 'shipped' ? 'Shipped'
          : status === 'partial' ? 'Partial'
          : status === 'missing' ? 'Missing'
          : 'Unknown';
        h += '<div class="projects-deliverable">'
           + '<div class="projects-deliverable__title">'+esc(d.title || d.name || 'Untitled')+'</div>';
        if (d.pr_url) {
          h += '<a class="projects-deliverable__link" href="'+esc(d.pr_url)+'"'
             + ' target="_blank" rel="noopener noreferrer">View PR ↗</a>';
        }
        if (d.artifact_path) {
          h += '<a class="projects-deliverable__link" href="#" data-artifact="'+esc(d.artifact_path)
             + '" data-artifact-name="'+esc(d.title || 'Artifact')+'">View artifact</a>';
        }
        h += '<span class="projects-pill '+pillClass+'">'+esc(pillLabel)+'</span>';
        h += '</div>';
      });
      h += '</div>';
    }

    // Lower grid: team + decisions
    h += '<div class="projects-lower-grid">';

    // Team
    h += '<div><div class="nx-section-heading">Team</div>';
    var team = eng.team || [];
    if (team.length === 0) {
      h += '<p class="nx-empty">No team assigned yet.</p>';
    } else {
      h += '<div class="projects-team">';
      team.forEach(function(member) {
        h += '<div class="projects-team-member">'
           + '<span class="nx-dot nx-dot--green" aria-hidden="true"></span>'
           + '<span>'+esc(member)+'</span></div>';
      });
      h += '</div>';
    }
    h += '</div>';

    // Last 5 decisions for this engagement
    h += '<div><div class="nx-section-heading">Recent Decisions</div>';
    var engId = eng.name || '';
    var projDecs = decs.filter(function(d) {
      return d.engagement_id === engId || !d.engagement_id;
    }).slice(-5).reverse();
    if (projDecs.length === 0) {
      h += '<p class="nx-empty">No decisions yet.</p>';
    } else {
      h += '<div class="projects-decisions">';
      projDecs.forEach(function(d) {
        h += '<div class="projects-decision-row">'
           + '<span class="projects-decision-row__title">'+esc(d.title)+'</span>'
           + '<span class="projects-decision-row__age">'+esc(d.age)+'</span>'
           + '</div>';
      });
      h += '</div>';
    }
    h += '</div>';
    h += '</div>'; // .projects-lower-grid

    // Gate block — shown when gate_pending=true on current stage
    if (eng.gate_pending) {
      h += '<div class="projects-gate-block">'
         + '<div class="projects-gate-alert">'
         + '<span class="projects-gate-alert__icon" aria-hidden="true">&#9654;</span>'
         + '<span class="projects-gate-alert__text">This stage is ready for a gate review.</span>'
         + '<button class="projects-gate-btn" type="button"'
         + ' data-gate-eng="'+esc(eng.name || '')+'"'
         + ' data-gate-stage-idx="'+stageIdx+'">'
         + 'Open Gate Ceremony</button>'
         + '</div></div>';
    }

    return h;
  }

  // ── B4: Artifact viewer ───────────────────────────────────────────────

  function _ensureArtifactModal() {
    if (document.getElementById('artifact-backdrop')) return;
    var wrap = document.createElement('div');
    wrap.innerHTML = '<div class="artifact-backdrop" id="artifact-backdrop" role="dialog"'
      + ' aria-modal="true" aria-label="Artifact viewer" style="display:none">'
      + '<div class="artifact-modal">'
      + '<div class="artifact-modal__header">'
      + '<span class="artifact-modal__title" id="artifact-title">Artifact</span>'
      + '<button class="artifact-modal__close" id="artifact-close" type="button" aria-label="Close viewer">&#x2715;</button>'
      + '</div>'
      + '<div class="artifact-modal__body" id="artifact-body"><p class="nx-empty">Loading...</p></div>'
      + '</div></div>';
    document.body.appendChild(wrap.firstChild);

    document.getElementById('artifact-close').addEventListener('click', closeArtifact);
    document.getElementById('artifact-backdrop').addEventListener('click', function(e) {
      if (e.target === e.currentTarget) closeArtifact();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && document.getElementById('artifact-backdrop').style.display !== 'none') {
        closeArtifact();
      }
    });
  }

  function closeArtifact() {
    var bd = document.getElementById('artifact-backdrop');
    if (bd) bd.style.display = 'none';
    var body = document.getElementById('artifact-body');
    if (body) body.innerHTML = '<p class="nx-empty">Loading...</p>';
  }

  function openArtifact(relPath, name) {
    _ensureArtifactModal();
    var bd = document.getElementById('artifact-backdrop');
    var body = document.getElementById('artifact-body');
    var title = document.getElementById('artifact-title');
    if (title) title.textContent = name || 'Artifact';
    if (body) body.innerHTML = '<p class="nx-empty">Loading...</p>';
    bd.style.display = 'flex';

    fetch('/api/artifact?path=' + encodeURIComponent(relPath), {credentials:'same-origin'})
      .then(function(r) {
        if (!r.ok) throw new Error('Could not load artifact. Status: ' + r.status);
        var ct = r.headers.get('Content-Type') || '';
        if (ct.indexOf('image/') === 0) {
          return r.blob().then(function(blob) {
            var url = URL.createObjectURL(blob);
            body.innerHTML = '<img src="'+url+'" alt="'+esc(name)+'">';
          });
        } else if (ct.indexOf('text/html') !== -1) {
          return r.text().then(function(html) {
            var iframe = document.createElement('iframe');
            iframe.setAttribute('sandbox', '');
            iframe.srcdoc = html;
            body.innerHTML = '';
            body.appendChild(iframe);
          });
        } else {
          return r.text().then(function(txt) {
            var pre = document.createElement('pre');
            pre.textContent = txt;
            body.innerHTML = '';
            body.appendChild(pre);
          });
        }
      })
      .catch(function(err) {
        body.innerHTML = '<p class="nx-empty" style="padding:20px">Could not load artifact. Try again.</p>';
        console.warn('[studio] artifact load error:', err);
      });
  }

  // Delegate artifact link clicks in #app
  document.addEventListener('click', function(evt) {
    var link = evt.target.closest('[data-artifact]');
    if (!link) return;
    evt.preventDefault();
    openArtifact(link.dataset.artifact, link.dataset.artifactName || 'Artifact');
  });

  // Delegate gate button clicks in #app
  document.addEventListener('click', function(evt) {
    var btn = evt.target.closest('.projects-gate-btn');
    if (!btn) return;
    var engId = btn.dataset.gateEng || '';
    var stageIdx = parseInt(btn.dataset.gateStageIdx || '0', 10);
    openGateCeremony(engId, stageIdx);
  });

  // ── B4: Gate Ceremony modal ───────────────────────────────────────────

  var _gateEngId = '';
  var _gateStageIdx = 0;

  function _ensureGateModal() {
    if (document.getElementById('gate-backdrop')) return;
    var wrap = document.createElement('div');
    wrap.innerHTML = '<div class="gate-backdrop" id="gate-backdrop" role="dialog"'
      + ' aria-modal="true" aria-label="Gate Ceremony" style="display:none">'
      + '<div class="gate-modal">'
      + '<div class="gate-modal__header">'
      + '<div><div class="gate-modal__title" id="gate-title">Gate Review</div>'
      + '<div class="gate-modal__subtitle" id="gate-subtitle">Review this stage before moving on.</div></div>'
      + '<button class="gate-modal__close" id="gate-close" type="button" aria-label="Close gate ceremony">&#x2715;</button>'
      + '</div>'
      // FULL body
      + '<div id="gate-full-body">'
      + '<div class="gate-section-label">Deliverables</div>'
      + '<div class="gate-checklist" id="gate-checklist"><p class="nx-empty">No deliverables found.</p></div>'
      + '<div id="gate-scorecard-wrap" style="display:none">'
      + '<div class="gate-section-label">Scores</div>'
      + '<div class="gate-scorecard" id="gate-scorecard"></div></div>'
      + '<div class="gate-section-label">Your reason'
      + '<span class="gate-field-hint">(required, at least 20 characters)</span></div>'
      + '<textarea class="gate-rationale" id="gate-rationale" rows="4" minlength="20"'
      + ' placeholder="Explain why you are approving, requesting changes, or deferring."></textarea>'
      + '<div class="gate-rationale-error" id="gate-rationale-error" style="display:none">'
      + 'Enter at least 20 characters to continue.</div>'
      + '<div class="gate-actions" id="gate-full-actions">'
      + '<button class="gate-btn gate-btn--approve" id="gate-approve" type="button">Approve</button>'
      + '<button class="gate-btn gate-btn--changes" id="gate-changes" type="button">Request Changes</button>'
      + '<button class="gate-btn gate-btn--defer" id="gate-defer" type="button">Defer</button>'
      + '</div></div>'
      // FAST-PATH body
      + '<div id="gate-fast-body" style="display:none">'
      + '<div class="gate-section-label">Optional note</div>'
      + '<input class="gate-note" id="gate-note" type="text" maxlength="200"'
      + ' placeholder="Add a short note (optional).">'
      + '<div class="gate-actions gate-actions--fast">'
      + '<button class="gate-btn gate-btn--approve" id="gate-fast-approve" type="button">'
      + 'Approve operational stage</button>'
      + '</div></div>'
      + '</div></div>';
    document.body.appendChild(wrap.firstChild);

    // Toast element
    var toastWrap = document.createElement('div');
    toastWrap.innerHTML = '<div class="gate-toast" id="gate-toast" role="status"'
      + ' aria-live="polite" style="display:none">Gate decision recorded.</div>';
    document.body.appendChild(toastWrap.firstChild);

    document.getElementById('gate-close').addEventListener('click', closeGateCeremony);
    document.getElementById('gate-backdrop').addEventListener('click', function(e) {
      if (e.target === e.currentTarget) closeGateCeremony();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && document.getElementById('gate-backdrop').style.display !== 'none') {
        closeGateCeremony();
      }
    });
    document.getElementById('gate-approve').addEventListener('click', function() { _submitGate('approve'); });
    document.getElementById('gate-changes').addEventListener('click', function() { _submitGate('request_changes'); });
    document.getElementById('gate-defer').addEventListener('click', function() { _submitGate('defer'); });
    document.getElementById('gate-fast-approve').addEventListener('click', function() { _submitGate('approve'); });
  }

  function closeGateCeremony() {
    var bd = document.getElementById('gate-backdrop');
    if (bd) bd.style.display = 'none';
  }

  function openGateCeremony(engId, stageIdx) {
    _ensureGateModal();
    _gateEngId = engId;
    _gateStageIdx = stageIdx;

    var s = PROJ_STAGES[stageIdx] || { key:'S?', label:'Stage '+(stageIdx+1) };
    var nextS = PROJ_STAGES[stageIdx + 1] || { label:'completion' };
    var isFastPath = (s.key === 'S6'); // Locked Decision #3

    document.getElementById('gate-title').textContent = 'Gate Review — ' + s.label;
    document.getElementById('gate-subtitle').textContent =
      'Closing ' + s.label + '. Opening ' + nextS.label + '.';

    var fullBody = document.getElementById('gate-full-body');
    var fastBody = document.getElementById('gate-fast-body');
    fullBody.style.display = isFastPath ? 'none' : 'block';
    fastBody.style.display = isFastPath ? 'block' : 'none';

    if (!isFastPath) {
      // Populate deliverables checklist from cached state
      var eng = null;
      if (_state && _state.engagements && _state.engagements.data) {
        eng = _state.engagements.data.find(function(e) { return e.name === engId; })
           || _state.engagements.data[0] || null;
      }
      var delivs = (eng && eng.deliverables && eng.deliverables[eng.current_stage]) || [];
      var cl = document.getElementById('gate-checklist');
      if (delivs.length === 0) {
        cl.innerHTML = '<p class="nx-empty">No deliverables found.</p>';
      } else {
        cl.innerHTML = delivs.map(function(d) {
          var st = d.status || 'unknown';
          var icon = st === 'shipped' ? '&#10003;' : st === 'partial' ? '&#9888;' : '&#10007;';
          var iconClass = st === 'shipped' ? 'gate-check-icon--ok'
            : st === 'partial' ? 'gate-check-icon--warn' : 'gate-check-icon--miss';
          return '<div class="gate-check-row">'
            + '<span class="gate-check-icon '+iconClass+'">'+icon+'</span>'
            + '<span>'+esc(d.title || d.name || 'Untitled')+'</span>'
            + '</div>';
        }).join('');
      }

      // Validator scorecard
      var scores = (eng && eng.validator_scores) || null;
      var scoreWrap = document.getElementById('gate-scorecard-wrap');
      var scoreEl   = document.getElementById('gate-scorecard');
      if (scores && Object.keys(scores).length > 0) {
        scoreEl.innerHTML = Object.keys(scores).map(function(dim) {
          return '<div class="gate-score-cell">'
            + '<div class="gate-score-cell__dim">'+esc(dim)+'</div>'
            + '<div class="gate-score-cell__val">'+esc(String(scores[dim]))+'</div>'
            + '</div>';
        }).join('');
        scoreWrap.style.display = 'block';
      } else {
        scoreWrap.style.display = 'none';
      }

      // Reset rationale
      var rationale = document.getElementById('gate-rationale');
      if (rationale) rationale.value = '';
      var ratErr = document.getElementById('gate-rationale-error');
      if (ratErr) ratErr.style.display = 'none';
    } else {
      var noteEl = document.getElementById('gate-note');
      if (noteEl) noteEl.value = '';
    }

    document.getElementById('gate-backdrop').style.display = 'flex';
  }

  function _submitGate(decision) {
    var isFastPath = (PROJ_STAGES[_gateStageIdx] || {}).key === 'S6';
    var rationale = '';
    var note = '';

    if (!isFastPath) {
      var el = document.getElementById('gate-rationale');
      rationale = el ? el.value.trim() : '';
      if (rationale.length < 20) {
        var err = document.getElementById('gate-rationale-error');
        if (err) err.style.display = 'block';
        return;
      }
    } else {
      var noteEl2 = document.getElementById('gate-note');
      note = noteEl2 ? noteEl2.value.trim() : '';
    }

    var payload = {
      engagement_id: _gateEngId,
      stage: (PROJ_STAGES[_gateStageIdx] || {}).key || '',
      decision: decision,
      rationale: rationale,
      note: note,
    };

    fetch('/api/gate/decide', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
      credentials: 'same-origin',
    })
    .then(function(r) {
      if (!r.ok) throw new Error('Server returned ' + r.status);
      return r.json();
    })
    .then(function() {
      closeGateCeremony();
      _showGateToast();
    })
    .catch(function(err) {
      console.warn('[studio] gate/decide error:', err);
      closeGateCeremony();
      _showGateToast(); // still show toast — file may have been written
    });
  }

  function _showGateToast() {
    var toast = document.getElementById('gate-toast');
    if (!toast) return;
    toast.style.display = 'block';
    setTimeout(function() { toast.style.display = 'none'; }, 3000);
  }

  function relTime(tsRaw) {
    if (!tsRaw) return '';
    var t = typeof tsRaw === 'number' ? tsRaw * 1000 : Date.parse(tsRaw);
    if (isNaN(t)) return '';
    var secs = Math.floor((Date.now() - t) / 1000);
    if (secs < 60)  return secs + 's ago';
    if (secs < 3600) return Math.floor(secs / 60) + 'm ago';
    if (secs < 86400) return Math.floor(secs / 3600) + 'h ago';
    if (secs < 172800) return '1d ago';
    return Math.floor(secs / 86400) + 'd ago';
  }

  // ── Profile avatar color (hash slug → palette color) ─────────────

  var _PALETTE = ['#7861FF','#5B30FF','#2563FF','#00E0FF'];
  function slugColor(slug) {
    var h = 0;
    for (var i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) >>> 0;
    return _PALETTE[h % _PALETTE.length];
  }

  function slugInitials(slug) {
    return (slug || 'AG').slice(0, 2).toUpperCase();
  }

  // ── AGENTS renderer ───────────────────────────────────────────────

  function renderAgents(state) {
    var agents = (state.agents && state.agents.data) || {};
    var active    = agents.active    || [];
    var available = agents.available || [];
    var idle      = agents.idle      || [];

    var h = '';
    h += '<div class="nx-view-title">Agents</div>';
    h += '<div class="nx-view-subtitle">See which agents are running, ready, or resting.</div>';

    // Zone 1: Active Now
    h += '<div class="nx-section-heading">Active Now</div>';
    h += '<div class="agents-zone agents-zone--active">';
    if (active.length === 0) {
      h += '<p class="nx-empty">No agents running right now.</p>';
    } else {
      active.forEach(function(a) {
        var col = slugColor(a.slug || a.name || '');
        var ini = slugInitials(a.slug || a.name || 'AG');
        h += '<button class="agents-card agents-card--active" tabindex="0"'
           + ' data-slug="' + esc(a.slug) + '" aria-label="View ' + esc(a.slug) + ' profile">'
           + '<span class="agents-card__pulse"></span>'
           + '<span class="agents-avatar" style="background:' + col + '">' + esc(ini) + '</span>'
           + '<span class="agents-card__name">' + esc(a.slug) + '</span>'
           + '<span class="agents-card__role">Running</span>'
           + '</button>';
      });
    }
    h += '</div>';

    // Zone 2: Available
    h += '<div class="nx-section-heading">Available</div>';
    h += '<div class="agents-zone agents-zone--available">';
    if (available.length === 0) {
      h += '<p class="nx-empty">All agents are busy.</p>';
    } else {
      available.forEach(function(a) {
        var col = slugColor(a.slug || a.name || '');
        var ini = slugInitials(a.slug || a.name || 'AG');
        var role = esc(a.role || _slugToRole(a.slug));
        h += '<button class="agents-card agents-card--available" tabindex="0"'
           + ' data-slug="' + esc(a.slug) + '" aria-label="View ' + esc(a.slug) + ' profile">'
           + '<span class="agents-avatar" style="background:' + col + '">' + esc(ini) + '</span>'
           + '<span class="agents-card__name">' + esc(a.slug) + '</span>'
           + '<span class="agents-card__role">' + role + '</span>'
           + '</button>';
      });
    }
    h += '</div>';

    // Zone 3: Idle
    h += '<div class="nx-section-heading">Idle '
       + '<span class="agents-zone-hint">(not used in 7+ days)</span></div>';
    h += '<div class="agents-zone agents-zone--idle">';
    if (idle.length === 0) {
      h += '<p class="nx-empty">No idle agents.</p>';
    } else {
      idle.forEach(function(a) {
        var col = slugColor(a.slug || a.name || '');
        var ini = slugInitials(a.slug || a.name || 'AG');
        h += '<button class="agents-card agents-card--idle" tabindex="0"'
           + ' data-slug="' + esc(a.slug) + '" aria-label="View ' + esc(a.slug) + ' profile">'
           + '<span class="agents-avatar" style="background:' + col + '">' + esc(ini) + '</span>'
           + '<span class="agents-card__name">' + esc(a.slug) + '</span>'
           + '</button>';
      });
    }
    h += '</div>';

    // Slide-over (hidden by default)
    h += '<div class="agents-slideover" id="agents-slideover" role="dialog"'
       + ' aria-modal="true" aria-label="Agent profile" hidden>'
       + '<div class="agents-slideover__inner">'
       + '<button class="agents-slideover__close" id="agents-slideover-close"'
       + ' type="button" aria-label="Close panel">&#x2715;</button>'
       + '<div id="agents-slideover-content"><p class="nx-empty">Select an agent.</p></div>'
       + '</div></div>'
       + '<div class="agents-slideover__backdrop" id="agents-slideover-backdrop" hidden></div>';

    return h;
  }

  // Derive a one-line role from profile slug
  function _slugToRole(slug) {
    if (!slug) return '';
    var map = {
      'accessibility-reviewer':    'Accessibility review',
      'architecture-director':     'Tech architecture',
      'brand-director':            'Brand strategy',
      'brand-strategist':          'Brand research',
      'business-analyst':          'Business analysis',
      'copywriter':                'Content writing',
      'design-director':           'UX and design',
      'marketing-director':        'Go-to-market',
      'nfr-author':                'Non-functional requirements',
      'product-director':          'Product strategy',
      'product-manager':           'Product management',
      'technical-writer-bilingual':'Technical writing',
      'trademark-researcher':      'Trademark research',
      'ux-researcher':             'User research',
      'validator':                 'Quality validation',
      'visual-designer':           'Visual design',
    };
    return map[slug] || slug.replace(/-/g, ' ');
  }

  // Slide-over open/close via event delegation
  document.addEventListener('click', function(evt) {
    var card = evt.target.closest('.agents-card[data-slug]');
    if (card) { _openSlideOver(card.dataset.slug); return; }
    var closeBtn = evt.target.closest('#agents-slideover-close');
    if (closeBtn) { _closeSlideOver(); return; }
    var bd = evt.target.closest('#agents-slideover-backdrop');
    if (bd) { _closeSlideOver(); return; }
  });

  function _openSlideOver(slug) {
    var so = document.getElementById('agents-slideover');
    var bd = document.getElementById('agents-slideover-backdrop');
    var ct = document.getElementById('agents-slideover-content');
    if (!so || !ct) return;
    so.hidden = false;
    if (bd) bd.hidden = false;
    ct.innerHTML = '<p class="nx-empty">Loading...</p>';
    fetch('/api/profile/' + encodeURIComponent(slug))
      .then(function(r) { return r.json(); })
      .then(function(d) { ct.innerHTML = _renderSlideOverContent(slug, d); })
      .catch(function() { ct.innerHTML = '<p class="nx-empty">Profile not found.</p>'; });
  }

  function _closeSlideOver() {
    var so = document.getElementById('agents-slideover');
    var bd = document.getElementById('agents-slideover-backdrop');
    if (so) so.hidden = true;
    if (bd) bd.hidden = true;
  }

  function _renderSlideOverContent(slug, d) {
    var col = slugColor(slug);
    var ini = slugInitials(slug);
    var h = '';
    h += '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;padding-top:8px">'
       + '<span class="agents-avatar" style="background:' + col + ';width:48px;height:48px;font-size:16px">' + esc(ini) + '</span>'
       + '<div><div style="font-size:15px;font-weight:700;color:var(--nx-text)">' + esc(slug) + '</div>'
       + '<div style="font-size:11px;color:rgba(245,247,250,0.45)">' + esc(_slugToRole(slug)) + '</div></div>'
       + '</div>';
    if (d.soul) {
      h += '<div class="nx-section-heading" style="margin-top:0">Profile</div>'
         + '<div class="agents-soul">' + esc(d.soul) + '</div>';
    }
    var dispatches = d.dispatches || [];
    h += '<div class="nx-section-heading">Last dispatches</div>';
    if (dispatches.length === 0) {
      h += '<p class="nx-empty">No dispatches on record.</p>';
    } else {
      dispatches.forEach(function(dp) {
        h += '<div class="agents-dispatch-row">'
           + '<span class="agents-dispatch-row__age">' + esc(relTime(dp.started_at)) + '</span>'
           + '<span>' + esc(dp.id || '—') + '</span>'
           + (dp.estimated_cost_usd != null ? '<span style="color:rgba(245,247,250,0.40);margin-left:auto">$' + Number(dp.estimated_cost_usd).toFixed(3) + '</span>' : '')
           + '</div>';
      });
    }
    if (d.memory) {
      h += '<div class="nx-section-heading">Memory</div>'
         + '<div class="agents-soul" style="max-height:120px;overflow-y:auto">' + esc(d.memory) + '</div>';
    }
    return h;
  }

  // ── ACTIVITY renderer ─────────────────────────────────────────────

  var _afRange = 'today';
  var _afType  = 'all';
  var _afRepo  = 'all';

  function renderActivity(state) {
    var prs       = (state.prs       && state.prs.data)       || [];
    var decs      = (state.decisions && state.decisions.data) || [];
    var agents    = (state.agents    && state.agents.data)    || {};
    var dispatches = agents.all_sessions || [];

    var events = [];
    prs.forEach(function(pr) {
      events.push({
        type: 'prs', icon: '&#x1F500;', badge: 'PR',
        badgeClass: 'activity-row__badge--pr',
        text: 'PR #' + pr.number + ' ' + pr.state + ' \u2014 ' + (pr.title || ''),
        ts: pr.ts_ms || 0, tsRaw: pr.ts_ms,
        href: pr.url || '#', repo: pr.repo || '',
      });
    });
    decs.forEach(function(d) {
      events.push({
        type: 'decisions', icon: '&#x2713;', badge: 'Decision',
        badgeClass: 'activity-row__badge--decision',
        text: d.title || 'Untitled decision',
        ts: d.ts_ms || 0, tsRaw: d.ts_ms,
        href: d.url || d.path || '#', repo: '',
      });
    });
    dispatches.forEach(function(dp) {
      events.push({
        type: 'dispatches', icon: '&#x26A1;', badge: 'Dispatch',
        badgeClass: 'activity-row__badge--dispatch',
        text: 'Agent dispatched: ' + (dp.slug || dp.id || 'unknown'),
        ts: dp.started_at ? dp.started_at * 1000 : 0, tsRaw: dp.started_at,
        href: '#', repo: '',
      });
    });

    events.sort(function(a, b) { return b.ts - a.ts; });

    var now = Date.now();
    var cutoff = 0;
    if (_afRange === 'today') {
      var d0 = new Date(); d0.setHours(0,0,0,0); cutoff = d0.getTime();
    } else if (_afRange === 'week')  { cutoff = now - 7 * 86400000; }
    else if (_afRange === 'month') { cutoff = now - 30 * 86400000; }

    var filtered = events.filter(function(e) {
      if (_afRange !== 'all' && e.ts < cutoff) return false;
      if (_afType  !== 'all' && e.type !== _afType) return false;
      if (_afRepo  !== 'all' && e.repo && !e.repo.includes(_afRepo)) return false;
      return true;
    });

    var h = '';
    h += '<div class="nx-view-title">Activity</div>';
    h += '<div class="nx-view-subtitle">Everything that happened, newest first.</div>';

    h += '<div class="activity-filters" role="group" aria-label="Filter activity">';
    h += '<span class="nx-sort-label">When:</span>';
    [['today','Today'],['week','This week'],['month','This month'],['all','All']].forEach(function(r) {
      h += '<button class="nx-sort-btn' + (_afRange===r[0]?' nx-sort-btn--active':'') + '" data-af-range="' + r[0] + '" type="button">' + r[1] + '</button>';
    });
    h += '<span class="nx-sort-label activity-filters__sep">Type:</span>';
    [['all','All'],['prs','PRs'],['decisions','Decisions'],['dispatches','Dispatches']].forEach(function(t) {
      h += '<button class="nx-sort-btn' + (_afType===t[0]?' nx-sort-btn--active':'') + '" data-af-type="' + t[0] + '" type="button">' + t[1] + '</button>';
    });
    h += '<span class="nx-sort-label activity-filters__sep">Repo:</span>';
    [['all','All'],['supply-chain-saas','Supply Chain'],['nexoura-agent','nexoura-agent']].forEach(function(rv) {
      h += '<button class="nx-sort-btn' + (_afRepo===rv[0]?' nx-sort-btn--active':'') + '" data-af-repo="' + rv[0] + '" type="button">' + rv[1] + '</button>';
    });
    h += '</div>';

    h += '<div class="activity-feed" role="feed" aria-label="Activity timeline">';
    if (filtered.length === 0) {
      var msg = _afRange === 'today' ? 'Nothing happened yet today.' : 'No results for this filter.';
      h += '<p class="nx-empty">' + msg + '</p>';
    } else {
      filtered.forEach(function(e) {
        var hasHref = e.href && e.href !== '#';
        var tag  = hasHref ? 'a href="' + esc(e.href) + '" target="_blank" rel="noopener"' : 'div';
        var etag = hasHref ? 'a' : 'div';
        h += '<' + tag + ' class="activity-row">'
           + '<span class="activity-row__icon" aria-hidden="true">' + e.icon + '</span>'
           + '<span class="activity-row__text">' + esc(e.text) + '</span>'
           + '<span class="activity-row__badge ' + e.badgeClass + '">' + e.badge + '</span>'
           + '<span class="activity-row__age">' + esc(relTime(e.tsRaw)) + '</span>'
           + '</' + etag + '>';
      });
    }
    h += '</div>';

    return h;
  }

  // Activity filter delegation
  document.addEventListener('click', function(evt) {
    var btn = evt.target.closest('[data-af-range]');
    if (btn && btn.dataset.afRange) { _afRange = btn.dataset.afRange; if (_route === '/activity') renderView(); return; }
    btn = evt.target.closest('[data-af-type]');
    if (btn && btn.dataset.afType)  { _afType  = btn.dataset.afType;  if (_route === '/activity') renderView(); return; }
    btn = evt.target.closest('[data-af-repo]');
    if (btn && btn.dataset.afRepo)  { _afRepo  = btn.dataset.afRepo;  if (_route === '/activity') renderView(); return; }
  });

  // ── SYSTEM renderer ───────────────────────────────────────────────

  function renderSystem(state) {
    var health = (state.health && state.health.data) || {};
    var system = (state.system && state.system.data) || {};
    var logLines = system.watchdog_lines !== undefined ? system.watchdog_lines : null;
    var spend    = system.spend || {};

    var h = '';
    h += '<div class="nx-view-title">System</div>';
    h += '<div class="nx-view-subtitle">Services, logs, and costs at a glance.</div>';

    // Service health table
    h += '<div class="nx-section-heading">Service Health</div>';
    h += '<div class="system-health-table" role="table" aria-label="Service health">';
    var services = [
      {key:'gateway',  label:'Hermes gateway'},
      {key:'studio',   label:'Studio server'},
      {key:'watchdog', label:'Watchdog'},
      {key:'dashboard',label:'Dashboard'},
    ];
    var lastCheck = health.last_check || null;
    services.forEach(function(svc) {
      var info  = health[svc.key] || {};
      var status = info.status || 'Unknown';
      var color  = info.color  || 'unknown';
      var pillC  = 'system-pill--' + ({'green':'green','amber':'amber','red':'red'}[color] || 'unknown');
      var icon   = {'green':'&#x2713;','amber':'&#x26A0;','red':'&#x2717;'}[color] || '?';
      h += '<div class="system-health-row" role="row">'
         + '<span class="system-health-row__name" role="cell">' + esc(svc.label) + '</span>'
         + '<span class="system-pill ' + pillC + '" role="cell">' + icon + ' ' + esc(status) + '</span>'
         + '<span class="system-health-row__check" role="cell">'
         + (lastCheck ? 'Checked ' + esc(lastCheck) : 'Not checked yet') + '</span>'
         + '</div>';
    });
    h += '</div>';

    // Watchdog log
    h += '<div class="nx-section-heading">Watchdog Log</div>';
    h += '<div class="system-log" aria-label="Watchdog log tail">';
    if (logLines === null) {
      h += 'Watchdog log not found.';
    } else if (logLines.length === 0) {
      h += 'Log is empty.';
    } else {
      h += esc(logLines.join('\n'));
    }
    h += '</div>';

    // Token spend chart
    h += '<div class="nx-section-heading">Token Spend \u2014 Last 7 Days</div>';
    h += '<div class="system-spend" aria-label="Token spend by provider">';
    var providers = Object.keys(spend);
    if (providers.length === 0) {
      h += '<p class="nx-empty">No spend data yet.</p>';
    } else {
      var maxAmt = Math.max.apply(null, providers.map(function(p) { return spend[p] || 0; }));
      var BAR_MAX = 80;
      providers.forEach(function(p) {
        var amt  = spend[p] || 0;
        var barH = maxAmt > 0 ? Math.max(3, Math.round((amt / maxAmt) * BAR_MAX)) : 3;
        h += '<div class="system-spend__bar-wrap">'
           + '<span class="system-spend__amount">$' + amt.toFixed(2) + '</span>'
           + '<div class="system-spend__bar" style="height:' + barH + 'px" aria-label="' + esc(p) + ' $' + amt.toFixed(2) + '"></div>'
           + '<span class="system-spend__label">' + esc(p) + '</span>'
           + '</div>';
      });
    }
    h += '</div>';

    return h;
  }

  // ── Renderer registry ─────────────────────────────────────────────

  var _renderers = {
    '/home':      renderHome,
    '/decisions': renderDecisions,
    '/agents':    renderAgents,
    '/activity':  renderActivity,
    '/system':    renderSystem,
  };

  // Sort button delegation (fires before re-render rebuilds DOM)
  document.addEventListener('click', function (evt) {
    var btn = evt.target.closest('.nx-sort-btn');
    if (!btn) return;
    var mode = btn.dataset.sort;
    if (mode) { _sortMode = mode; renderView(); }
  });

  // ── Boot ──────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', function () {
    _route = parseRoute();
    setActiveNav(_route);
    fetchState();
    connectSSE();
  });

}());
