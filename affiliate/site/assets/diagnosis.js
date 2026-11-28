/* 工数診断の計算（決裁シートの数字）。DOM には触らない。ブラウザでは window.AffDiag、node では require で使う。
 * 料金・残る工数の前提は PLANS だけで決まる（PM が決める数字。2026-11-28 時点は仮に現行の月5万円）。
 * 係数は knowledge/workload-benchmarks.md の実データ（重い運用で月80時間）に合うように置いた目安。 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.AffDiag = api;
})(typeof self !== 'undefined' ? self : this, function () {
  var ASP = [1, 2.5, 5, 8], MEDIA = [15, 60, 200, 400], CV = [30, 120, 350, 700];

  // プラン。covers が 'all' なら全作業を任せ、残るのは remainHours（週1回の確認など）だけ。
  // 一部だけ任せるプランは covers に作業名を並べる（任せない作業の時間は、そのまま残る）。
  var PLANS = [
    { id: 'full', name: 'まるごと', fee: 50000, remainHours: 4, covers: 'all', remainNote: '週1回のまとめの確認と、範囲を超える判断' }
  ];
  var ASSUMPTIONS = { fee: PLANS[0].fee, remainHours: PLANS[0].remainHours };

  function calc(a) {
    var asp = ASP[a.asp], media = MEDIA[a.media], cv = CV[a.cv];
    var t = {
      'ASP担当とのやり取り': asp * 1.8,
      'メディア対応・掲載確認': media * 0.02 + 0.5,
      '成果の承認': a.approve === 'auto' ? cv * 0.002 + 0.5 : a.approve === 'manual' ? cv * 0.017 + 0.5 : 0,
      '表記チェック': a.check === 'regular' ? media * 0.015 + 1 : a.check === 'sometimes' ? 2 : 0,
      '新規開拓・提携手続き': a.dev === 'regular' ? Math.min(10, 3 + media * 0.02) : a.dev === 'sometimes' ? 3 : 0,
      '素材・キャンペーン': asp * 0.8 + 1,
      'レポート・社内報告': a.report === 'full' ? asp * 1.2 + 4 : a.report === 'sum' ? asp * 0.8 + 1 : 1,
      '請求・予算管理': asp * 0.5
    };
    var total = 0;
    Object.keys(t).forEach(function (k) { t[k] = Math.round(t[k] * 2) / 2; total += t[k]; });
    var alerts = [];
    if (a.approve === 'none') alerts.push('承認をほとんど見ていない場合、重複やキャンセルなど、本来は否認すべき成果にも支払っている可能性があります。');
    if (a.check === 'none') alerts.push('表記チェックをしていない場合、PR表記のない記事や誤解を招く表現が残っている可能性があります。ステマ規制の責任は広告主にあります。');
    if (a.dev === 'none') alerts.push('新規メディアの開拓をしていない場合、競合が載っていて御社が載っていない記事が残っている可能性があります。');
    return { tasks: t, total: Math.round(total), alerts: alerts };
  }

  function money(hoursNow, hoursAfter, wage, fee) {
    var saved = Math.max(0, hoursNow - hoursAfter);
    var labor = Math.round(saved * wage);
    return { hoursNow: hoursNow, hoursAfter: hoursAfter, hoursSaved: saved, laborSaved: labor, fee: fee,
      netMonth: labor - fee, netYear: (labor - fee) * 12 };
  }

  function roi(total, wage, a) {
    a = a || ASSUMPTIONS;
    return money(total, Math.min(a.remainHours, total), wage, a.fee);
  }

  function plan(c, wage, p) {
    if (p.covers === 'all') return roi(c.total, wage, p);
    var left = 0;
    Object.keys(c.tasks).forEach(function (k) { if (p.covers.indexOf(k) < 0) left += c.tasks[k]; });
    return money(c.total, Math.min(c.total, left + p.remainHours), wage, p.fee);
  }

  // 共有リンク用の短い文字列（8文字）。回答の値だけを入れ、個人情報は入れない。
  var CODES = { approve: ['auto', 'a', 'manual', 'm', 'none', 'n'], check: ['regular', 'r', 'sometimes', 's', 'none', 'n'],
    dev: ['regular', 'r', 'sometimes', 's', 'none', 'n'], report: ['view', 'v', 'sum', 's', 'full', 'f'] };
  var ORDER = ['approve', 'check', 'dev', 'report'];
  function pick(list, v, toCode) {
    for (var i = 0; i < list.length; i += 2) if ((toCode ? list[i] : list[i + 1]) === v) return list[toCode ? i + 1 : i];
    return null;
  }
  function encode(a) {
    return '' + a.asp + a.media + a.cv + ORDER.map(function (k) { return pick(CODES[k], a[k], true); }).join('') + (a.wage / 1000);
  }
  function decode(s) {
    if (typeof s !== 'string' || !/^[0-3]{3}[amn][rsn][rsn][vsf][345]$/.test(s)) return null;
    var a = { asp: +s[0], media: +s[1], cv: +s[2] };
    ORDER.forEach(function (k, i) { a[k] = pick(CODES[k], s[3 + i], false); });
    a.wage = +s[7] * 1000;
    return a;
  }

  return { calc: calc, roi: roi, plan: plan, encode: encode, decode: decode, PLANS: PLANS, ASSUMPTIONS: ASSUMPTIONS };
});
