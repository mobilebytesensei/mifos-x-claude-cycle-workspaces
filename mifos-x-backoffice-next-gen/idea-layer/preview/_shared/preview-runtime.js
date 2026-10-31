/**
 * preview-runtime.js — byte-identical across all projects (RV-017-style).
 *
 * dashboard-roster-artifacts-flows sub-plan 04 task 4.1. The single
 * runtime every `preview/{state}.html` references; restores click→
 * navigate to LLM-rendered previews WITHOUT re-introducing a per-pattern
 * TypeScript dispatcher (RULE-PROTO-RENDER-LLM-001 stays — the HTML
 * is static, this is the thin runtime that turns declarative
 * `data-nav-to` attributes into postMessage events).
 *
 * Contract — the LLM render prompt MUST emit on every interactive
 * element whose `ui.yaml` `on_click` (or `flow.yaml` `flow_logic[].effect`
 * "Emit NavigateTo{Screen}") resolves to a known screen:
 *
 *   data-nav-to="{screenId}"          — REQUIRED (target screen id)
 *   data-nav-type="push|pop|tab|replace"  — OPTIONAL (default: push)
 *   data-action-id="{flow_logic.id}"  — OPTIONAL (carries the source id)
 *   data-nav-params='{"key":"val"}'   — OPTIONAL (JSON string)
 *
 * Resolution mirrors `tools/project-dashboard/src/lib/nav-resolve.ts`:
 *  • Strip `Screen` suffix + lowercase, e.g. `homeScreen` → `home`
 *  • Match against the known-screens set (curated at render-time)
 *  • Effects like `Emit NavigateToMovieDetail` → `moviedetail`
 *
 * The `lib/nav-resolve.ts` ↔ render-prompt parity test (sub-plan 04
 * task 4.6) keeps the TS resolver and this runtime + the prompt rule
 * in sync.
 *
 * Behaviour:
 *  1. Captures `click` on any `[data-nav-to]` element (delegated, so
 *     dynamic content works).
 *  2. preventDefault + stopPropagation on the click.
 *  3. Resolves the target window:
 *      • `window.parent !== window`        → postMessage(parent)
 *      • standalone `prototype.html?screen=` → location.search update
 *      • file://                             → console.log fallback
 *  4. Posts `{type:'proto:navigate', to, navType, actionId, params}`.
 *  5. The parent listener (dashboard / prototype.html) validates origin
 *     + source iframe per R9 before acting on it.
 *
 * Back-compat: also catches `[data-od-nav]` (legacy srcdoc-builder
 * pattern) and `[data-pdb-nav]` (dashboard) — same event shape — so
 * existing rendered previews keep working without re-render.
 *
 * Non-navigating interactions (form inputs, toggles, accordions) keep
 * working untouched — this runtime ONLY intercepts elements that
 * declare a `data-nav-to` (or alias) attribute.
 *
 * NO inline event handlers, NO TS dispatcher — this file IS the only
 * JS the static HTML pulls in.
 */

(function () {
  'use strict';

  if (window.__previewRuntimeInstalled) return;
  window.__previewRuntimeInstalled = true;

  /** Pick the first attr value among aliases (canonical first). */
  function getNavTarget(el) {
    return (
      el.getAttribute('data-nav-to') ||
      el.getAttribute('data-pdb-nav') ||
      el.getAttribute('data-od-nav') ||
      ''
    );
  }

  /**
   * Read the intra-screen state target (Phase 3 of live-prototype-bridge-e2e).
   * `data-state-to` is emitted by the renderer (SP-02) when an `on_click`
   * resolves to one of THIS screen's `states[]` rather than a cross-screen nav.
   */
  function getStateTarget(el) {
    return el.getAttribute('data-state-to') || null;
  }

  function getNavType(el) {
    var t = el.getAttribute('data-nav-type');
    if (t === 'pop' || t === 'tab' || t === 'replace' || t === 'push') return t;
    return 'push';
  }

  function getNavParams(el) {
    var raw =
      el.getAttribute('data-nav-params') ||
      el.getAttribute('data-od-params') ||
      el.getAttribute('data-pdb-params') ||
      '';
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      // Malformed — surface in console but don't break navigation.
      // eslint-disable-next-line no-console
      console.warn('[preview-runtime] data-nav-params not JSON:', raw);
      return null;
    }
  }

  function postNavigate(payload) {
    // 1) Parent frame (dashboard Screens view OR prototype.html).
    if (window.parent && window.parent !== window) {
      try {
        // Same-origin in dev → strict origin tightening when previews ever
        // serve cross-origin (they don't today; R9 keeps targetOrigin '*').
        window.parent.postMessage(payload, '*');
        return;
      } catch (e) {
        /* fall through */
      }
    }

    // 2) Standalone — set `?screen=` and reload. Used by viewers that
    // load preview HTML directly without an embedding parent.
    if (window.location && /^https?:|^file:/.test(window.location.protocol)) {
      try {
        var url = new URL(window.location.href);
        url.searchParams.set('screen', payload.to);
        if (payload.navType && payload.navType !== 'push') {
          url.searchParams.set('navType', payload.navType);
        }
        window.location.href = url.toString();
        return;
      } catch (e) {
        /* fall through */
      }
    }

    // 3) Last resort — log.
    // eslint-disable-next-line no-console
    console.log('[preview-runtime] proto:navigate', payload);
  }

  // Phase 13 T1+T2: data-action handler (non-nav clicks — state changes, toggles, etc.)
  // Posts pdb:action so the dashboard can show a toast or log it.
  // Version 1.4.0 (2026-06-27) — adds data-state-to → pdb:state emit (Phase 3 of
  //   live-prototype-bridge-e2e: intra-screen state transitions post the existing
  //   `pdb:state {newState}` contract; the dashboard onState swaps the iframe).
  // Version 1.3.0 (2026-05-20) — adds data-action support; was 1.2.0 (data-nav-to only).

  function getElPath(el) {
    var path = [];
    var cur = el;
    while (cur && cur.nodeType === 1 && cur.tagName !== 'BODY' && path.length < 5) {
      var tag = cur.tagName.toLowerCase();
      var id = cur.id ? '#' + cur.id : '';
      var cls = cur.className && typeof cur.className === 'string'
        ? '.' + cur.className.split(/\s+/).slice(0, 2).join('.')
        : '';
      path.unshift(tag + id + cls);
      cur = cur.parentElement;
    }
    return path.join(' > ');
  }

  function parseJsonAttr(str) {
    if (!str) return null;
    try { return JSON.parse(str); } catch (_) { return null; }
  }

  function postAction(actionName, params, el) {
    var payload = {
      type: 'pdb:action',
      action: actionName,
      params: params,
      el: getElPath(el),
      timestamp: Date.now(),
    };
    try {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(payload, '*');
        return;
      }
    } catch (_) { /* fall through */ }
    // eslint-disable-next-line no-console
    console.log('[preview-runtime] pdb:action', payload);
  }

  // Phase 3 of live-prototype-bridge-e2e — intra-screen state transition.
  // Modeled on postAction(): posts the EXISTING `pdb:state {newState}` contract
  // (postmessage.ts already carries the handler), so no dashboard protocol change.
  function postState(newState, el) {
    var payload = {
      kind: 'pdb:state',
      newState: newState,
      el: getElPath(el),
      timestamp: Date.now(),
    };
    try {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(payload, '*');
        return;
      }
    } catch (_) { /* fall through */ }
    // eslint-disable-next-line no-console
    console.log('[preview-runtime] pdb:state', payload);
  }

  document.addEventListener(
    'click',
    function (ev) {
      var t = ev.target;
      if (!(t instanceof Element)) return;

      // Branch 1: data-nav-to (existing behavior — navigation)
      var navEl = t.closest(
        '[data-nav-to], [data-pdb-nav], [data-od-nav]',
      );
      if (navEl) {
        var to = getNavTarget(navEl);
        if (!to) return;
        ev.preventDefault();
        ev.stopPropagation();
        var payload = {
          type: 'proto:navigate',
          to: to,
          navType: getNavType(navEl),
          actionId: navEl.getAttribute('data-action-id') || null,
          params: getNavParams(navEl),
        };
        postNavigate(payload);
        return;
      }

      // Branch 1.5: data-state-to (Phase 3 of live-prototype-bridge-e2e — intra-screen
      // state transition). Wins over data-action (state transitions are more specific);
      // loses to data-nav-to (cross-screen nav already returned at Branch 1).
      var stateEl = t.closest('[data-state-to]');
      if (stateEl) {
        var newState = getStateTarget(stateEl);
        if (!newState) return;
        ev.preventDefault();
        ev.stopPropagation();
        postState(newState, stateEl);
        return;
      }

      // Branch 2: data-action (Phase 13 T1 — non-nav clicks: state changes, toggles, etc.)
      var actionEl = t.closest('[data-action]');
      if (actionEl) {
        var actionName = actionEl.getAttribute('data-action');
        if (!actionName) return;
        var params = parseJsonAttr(actionEl.getAttribute('data-action-params'));
        ev.preventDefault();
        ev.stopPropagation();
        postAction(actionName, params, actionEl);
        return;
      }
    },
    true,
  );

  // Keyboard support — Enter / Space on focused [data-nav-to] OR [data-action] also fires.
  document.addEventListener(
    'keydown',
    function (ev) {
      if (ev.key !== 'Enter' && ev.key !== ' ') return;
      var t = ev.target;
      if (!(t instanceof Element)) return;

      var navEl = t.closest(
        '[data-nav-to], [data-pdb-nav], [data-od-nav]',
      );
      if (navEl) {
        var to = getNavTarget(navEl);
        if (!to) return;
        ev.preventDefault();
        var payload = {
          type: 'proto:navigate',
          to: to,
          navType: getNavType(navEl),
          actionId: navEl.getAttribute('data-action-id') || null,
          params: getNavParams(navEl),
        };
        postNavigate(payload);
        return;
      }

      // Branch 1.5: data-state-to keyboard parity (Phase 3 of live-prototype-bridge-e2e).
      var stateElK = t.closest('[data-state-to]');
      if (stateElK) {
        var newStateK = getStateTarget(stateElK);
        if (!newStateK) return;
        ev.preventDefault();
        postState(newStateK, stateElK);
        return;
      }

      var actionEl = t.closest('[data-action]');
      if (actionEl) {
        var actionName = actionEl.getAttribute('data-action');
        if (!actionName) return;
        var params = parseJsonAttr(actionEl.getAttribute('data-action-params'));
        ev.preventDefault();
        postAction(actionName, params, actionEl);
        return;
      }
    },
    true,
  );
})();
