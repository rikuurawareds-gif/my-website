// 工数診断の計算のテスト。実行: node --test site/assets/diagnosis.test.js
const test = require('node:test');
const assert = require('node:assert');
const D = require('./diagnosis.js');

const MID = { asp: 1, media: 1, cv: 1, approve: 'manual', check: 'regular', dev: 'regular', report: 'full', wage: 4000 };

test('calc: 移す前の index.html と同じ合計', () => {
  assert.strictEqual(D.calc(MID).total, 26);
  assert.strictEqual(D.calc({ ...MID, asp: 3, media: 3, cv: 3 }).total, 78);
  assert.strictEqual(D.calc({ asp: 0, media: 0, cv: 0, approve: 'auto', check: 'none', dev: 'none', report: 'view', wage: 4000 }).total, 7);
});

test('calc: 承認・表記・開拓をしていないと注意が出る', () => {
  const r = D.calc({ ...MID, approve: 'none', check: 'none', dev: 'none' });
  assert.strictEqual(r.alerts.length, 3);
});

test('roi: 月48時間・時給4,000円・委託費5万円・残り4時間', () => {
  const r = D.roi(48, 4000, { fee: 50000, remainHours: 4 });
  assert.deepStrictEqual(r, { hoursNow: 48, hoursAfter: 4, hoursSaved: 44, laborSaved: 176000, fee: 50000, netMonth: 126000, netYear: 1512000 });
});

test('roi: 工数が残る工数より小さいとき、差し引きはマイナスのまま', () => {
  const r = D.roi(3, 4000, { fee: 50000, remainHours: 4 });
  assert.strictEqual(r.hoursAfter, 3);
  assert.strictEqual(r.hoursSaved, 0);
  assert.strictEqual(r.netMonth, -50000);
  assert.strictEqual(r.netYear, -600000);
});

test('roi: 前提を差し替えられる', () => {
  const r = D.roi(20, 5000, { fee: 30000, remainHours: 2 });
  assert.strictEqual(r.netMonth, 18 * 5000 - 30000);
});

test('encode / decode: 往復で元に戻る', () => {
  const all = [];
  for (const approve of ['auto', 'manual', 'none'])
    for (const report of ['view', 'sum', 'full'])
      for (const wage of [3000, 4000, 5000])
        all.push({ asp: 3, media: 0, cv: 2, approve, check: 'sometimes', dev: 'none', report, wage });
  for (const a of all) assert.deepStrictEqual(D.decode(D.encode(a)), a);
  assert.strictEqual(D.encode(MID), '111mrrf4');
});

test('decode: 壊れた文字列は null', () => {
  for (const s of ['', 'zzz', '911mrrf4', '111mrrf9', '111mrrf4x', null, undefined, '<script>'])
    assert.strictEqual(D.decode(s), null, String(s));
});

test('fee: まるごとパックと窓口代行の委託費（ASP 4社目からの加算）', () => {
  const pack = D.PLANS.find(p => p.id === 'pack'), contact = D.PLANS.find(p => p.id === 'contact');
  assert.strictEqual(D.fee(pack, 0), 90000);           // 1社
  assert.strictEqual(D.fee(pack, 1), 90000);           // 2〜3社 → 3社
  assert.strictEqual(D.fee(pack, 2), 90000 + 2 * 10000 + 3000 + 2000); // 4〜6社 → 5社
  assert.strictEqual(D.fee(pack, 3), 90000 + 5 * 10000 + 3000 + 4 * 2000); // 7社以上 → 8社
  assert.strictEqual(D.fee(contact, 1), 30000);
  assert.strictEqual(D.fee(contact, 3), 30000 + 5 * 10000);
});

test('plan: まるごとパックは確認の月4時間＋料金表に含まれない請求・予算管理が残る', () => {
  const r = D.plan(D.calc(MID), MID, D.PLANS.find(p => p.id === 'pack'));
  assert.strictEqual(r.hoursAfter, 4 + 1.5);
  assert.strictEqual(r.fee, 90000);
  assert.strictEqual(r.netMonth, (26 - 5.5) * 4000 - 90000);
});

test('plan: 窓口代行だけは、窓口の作業以外の時間と確認の2時間が残る', () => {
  const r = D.plan(D.calc(MID), MID, D.PLANS.find(p => p.id === 'contact'));
  assert.strictEqual(r.hoursAfter, 26 - 4.5 - 1.5 + 2);
  assert.strictEqual(r.netMonth, (26 - r.hoursAfter) * 4000 - 30000);
});

test('plan: 既定はまるごとパック、時給の既定は5,000円', () => {
  assert.strictEqual(D.PLANS[0].id, 'pack');
  assert.strictEqual(D.DEFAULT_WAGE, 5000);
});
