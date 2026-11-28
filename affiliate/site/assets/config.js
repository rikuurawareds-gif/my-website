// サイトの設定。PM が書き換える。
window.AFF_CONFIG = {
  serviceName: 'アフィまかせ',          // 決定（2026-11-25）。変えるときはここだけ
  ga4MeasurementId: 'G-XXXXXXXXXX',     // GA4 の測定ID
  leadEndpoint: ''                       // automation/lead-capture.gs を公開したURL
};

// 2026-11-28: 公開先を afimakase.ixs-llc.com（合同会社IXS のサブドメイン）へ移した。
// 旧URL（*.pages.dev）で開かれたら、同じページの新URLへ移す（canonical も新URLを指している）。
(function () {
  var NEW_HOST = 'afimakase.ixs-llc.com';
  if (/\.pages\.dev$/.test(location.hostname)) {
    location.replace('https://' + NEW_HOST + location.pathname + location.search + location.hash);
  }
})();
