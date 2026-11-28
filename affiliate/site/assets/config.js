// サイトの設定。PM が書き換える。
window.AFF_CONFIG = {
  serviceName: 'アフィまかせ',          // 決定（2026-11-25）。変えるときはここだけ
  ga4MeasurementId: 'G-XXXXXXXXXX',     // GA4 の測定ID
  leadEndpoint: 'https://script.google.com/macros/s/AKfycbxre4KR-DJ37ibbvXra0Zdc_Ss4G9M44fS0HSSwk2v_tgwWcPpVJwmO0PIB2JdEzTLAmQ/exec' // リード受付（Apps Script、2026-11-28 公開）
};

// 2026-11-28: 公開先を afimakase.ixs-llc.com（合同会社IXS のサブドメイン）へ移した。
// 旧URL（*.pages.dev）で開かれたら、同じページの新URLへ移す（canonical も新URLを指している）。
(function () {
  var NEW_HOST = 'afimakase.ixs-llc.com';
  if (/\.pages\.dev$/.test(location.hostname)) {
    location.replace('https://' + NEW_HOST + location.pathname + location.search + location.hash);
  }
})();
