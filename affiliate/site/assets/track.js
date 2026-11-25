// 計測スクリプト。仕様は affiliate/docs/measurement.md
(function () {
  var cfg = window.AFF_CONFIG || {};
  var id = cfg.ga4MeasurementId;
  var enabled = id && id.indexOf('XXXX') === -1;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  var internal = false;
  try {
    if (/[?&]internal=1/.test(location.search)) localStorage.setItem('aff_internal', '1');
    internal = localStorage.getItem('aff_internal') === '1';
  } catch (e) {}

  var pageId = document.body.getAttribute('data-page-id') || location.pathname;

  if (enabled) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(s);
    gtag('js', new Date());
    var params = { page_id: pageId };
    if (internal) params.traffic_type = 'internal';
    gtag('config', id, params);
  }

  function send(name, params) {
    params = params || {};
    params.page_id = pageId;
    if (enabled) gtag('event', name, params);
    else console.log('[track]', name, params);
  }
  window.affTrack = send;

  // 広告クリック
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-aff-id]');
    if (!a) return;
    send('affiliate_click', {
      aff_id: a.getAttribute('data-aff-id'),
      asp: a.getAttribute('data-asp') || '',
      program_id: a.getAttribute('data-program-id') || '',
      position: a.getAttribute('data-position') || '',
      transport_type: 'beacon'
    });
  }, true);

  // フォーム開始（最初の入力で1回だけ）
  var started = {};
  document.addEventListener('input', function (e) {
    var f = e.target.closest && e.target.closest('form[data-form-id]');
    if (!f) return;
    var fid = f.getAttribute('data-form-id');
    if (started[fid]) return;
    started[fid] = true;
    send('form_start', { form_id: fid });
  }, true);

  // ステップ進行・完了はフォーム側から呼ぶ
  window.affFormStep = function (formId, step, stepName) {
    send('form_step', { form_id: formId, step: step, step_name: stepName || '' });
  };
  window.affFormComplete = function (formId) {
    send('generate_lead', { form_id: formId });
  };
})();
