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

  // ── Renderer registry ─────────────────────────────────────────────────

  var _renderers = { '/home': renderHome, '/decisions': renderDecisions };

  // Sort button delegation (event fires before re-render rebuilds DOM)
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
