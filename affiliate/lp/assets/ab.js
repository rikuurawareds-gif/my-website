// A/Bテストの出し分け。
// 使い方: <section data-experiment="exp-001" data-variant="A">…</section>
//         <section data-experiment="exp-001" data-variant="B" hidden>…</section>
// 同じ訪問者には常に同じバリアントを出す。?variant=B で強制表示できる。
(function () {
  var groups = {};
  document.querySelectorAll('[data-experiment][data-variant]').forEach(function (el) {
    var exp = el.getAttribute('data-experiment');
    (groups[exp] = groups[exp] || []).push(el);
  });

  Object.keys(groups).forEach(function (exp) {
    var els = groups[exp];
    var variants = [];
    els.forEach(function (el) {
      var v = el.getAttribute('data-variant');
      if (variants.indexOf(v) === -1) variants.push(v);
    });
    variants.sort();

    var key = 'aff_ab_' + exp;
    var forced = (location.search.match(/[?&]variant=([^&]+)/) || [])[1];
    var chosen = null;
    try { chosen = localStorage.getItem(key); } catch (e) {}
    if (forced && variants.indexOf(forced) !== -1) chosen = forced;
    if (!chosen || variants.indexOf(chosen) === -1) {
      chosen = variants[Math.floor(Math.random() * variants.length)];
    }
    try { localStorage.setItem(key, chosen); } catch (e) {}

    els.forEach(function (el) {
      el.hidden = el.getAttribute('data-variant') !== chosen;
    });
    if (window.affTrack) window.affTrack('experiment_view', { experiment_id: exp, variant: chosen });
  });
})();
