/* 工数診断の計算（決裁シートの数字）。DOM には触らない。ブラウザでは window.AffDiag、node では require で使う。
 * 料金・残る工数の前提は PLANS と fee だけで決まる（docs/pricing.md）。
 * 係数は knowledge/workload-benchmarks.md の実データ（重い運用で月80時間）に合うように置いた目安。 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.AffDiag = api;
})(typeof self !== 'undefined' ? self : this, function () {
  var ASP = [1, 2.5, 5, 8], MEDIA = [15, 60, 200, 400], CV = [30, 120, 350, 700];

  // プランと前提は docs/pricing.md（2026-11-28 オーナー決定）のとおり。変えるときは pricing.md が先。
  // covers が 'all' なら全作業を任せ、残るのは remainHours だけ。一部だけのプランは任せる作業名を並べる。
  // ASP の数は診断の選択肢（1社／2〜3社／4〜6社／7社以上）を 1・3・5・8 社として数える。
  var ASP_COUNT = [1, 3, 5, 8];
  var DEFAULT_WAGE = 5000;
  var PLANS = [
    { id: 'pack', name: 'まるごとパック', base: 90000, perAsp: 10000, approval: true, remainHours: 4,
      covers: ['ASP担当とのやり取り', 'メディア対応・掲載確認', '成果の承認', '表記チェック', '新規開拓・提携手続き', '素材・キャンペーン', 'レポート・社内報告'],
      remainNote: '週1回のまとめ報告の確認と、任せた範囲を超える判断、請求・予算管理（料金表に含まれないため）' },
    { id: 'contact', name: '窓口代行だけ', base: 30000, perAsp: 10000, approval: false, remainHours: 2,
      covers: ['ASP担当とのやり取り', 'メディア対応・掲載確認'],
      remainNote: '週1回のまとめ報告の確認と判断、窓口以外の作業（成果承認・表記チェック・レポートなど）' }
  ];

  // 委託費（月・税別）。ASP 3社までが基本料金。4社目から窓口 +1万円/社、パックは成果承認も 4社目3,000円・5社目から2,000円/社
  function fee(p, aspIdx) {
    var n = ASP_COUNT[aspIdx], f = p.base;
    for (var i = 4; i <= n; i++) f += p.perAsp + (p.approval ? (i === 4 ? 3000 : 2000) : 0);
    return f;
  }

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

  // a = { fee, remainHours }
  function roi(total, wage, a) {
    return money(total, Math.min(a.remainHours, total), wage, a.fee);
  }

  // c = calc の結果、ans = 診断の回答（asp・wage を使う）、p = PLANS の1つ
  function plan(c, ans, p) {
    var f = fee(p, ans.asp);
    if (p.covers === 'all') return roi(c.total, ans.wage, { fee: f, remainHours: p.remainHours });
    var left = 0;
    Object.keys(c.tasks).forEach(function (k) { if (p.covers.indexOf(k) < 0) left += c.tasks[k]; });
    return money(c.total, Math.min(c.total, left + p.remainHours), ans.wage, f);
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

  return { calc: calc, roi: roi, plan: plan, fee: fee, encode: encode, decode: decode, PLANS: PLANS, DEFAULT_WAGE: DEFAULT_WAGE, ASP_COUNT: ASP_COUNT };
});
