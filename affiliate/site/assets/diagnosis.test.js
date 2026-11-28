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

test('roi: 月48時間・時給4,000円', () => {
  const r = D.roi(48, 4000);
  assert.deepStrictEqual(r, { hoursNow: 48, hoursAfter: 4, hoursSaved: 44, laborSaved: 176000, fee: 50000, netMonth: 126000, netYear: 1512000 });
});

test('roi: 工数が残る工数より小さいとき、差し引きはマイナスのまま', () => {
  const r = D.roi(3, 4000);
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

test('plan: まるごと（全部任せる）は roi と同じ', () => {
  const c = D.calc(MID);
  const r = D.plan(c, 4000, D.PLANS[0]);
  assert.strictEqual(r.hoursAfter, 4);
  assert.strictEqual(r.netMonth, D.roi(26, 4000).netMonth);
});

test('plan: 一部だけ任せると、任せない作業の時間が残る', () => {
  const c = D.calc(MID);
  const onlyContact = { id: 'x', name: '窓口代行', fee: 30000, remainHours: 2, covers: ['ASP担当とのやり取り', 'メディア対応・掲載確認'] };
  const r = D.plan(c, 4000, onlyContact);
  assert.strictEqual(r.hoursAfter, 26 - 4.5 - 1.5 + 2);
  assert.strictEqual(r.netMonth, (26 - r.hoursAfter) * 4000 - 30000);
});
