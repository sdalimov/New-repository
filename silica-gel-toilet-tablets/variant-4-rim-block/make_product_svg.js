// Генератор иллюстрации варианта 4 (картридж на ободке): node make_product_svg.js [product.svg]
const fs = require('fs');
const W = 1200, H = 1660;
const C = {
  ink: '#1d2733', muted: '#5b6773', line: '#c9d2db', panel: '#f7f9fb', bg: '#ffffff',
  clear: '#dff1f5', dye: '#1778d4', dyeDark: '#0f5aa3', water: '#d6ecfa', waterStroke: '#4d93c9',
  plastic: '#e6e9ec', plasticStroke: '#7d8a96', lid: '#5d6873', porcelain: '#f2f4f6',
  ok: '#2e8b57', bad: '#c0392b', warn: '#b35c00', accent: '#1778d4',
  s1: '#2a78d6', s2: '#eb6834', band: '#e3f1e8',
};
const out = [];
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const t = (x, y, s, o = {}) => out.push(`<text x="${x}" y="${y}" font-size="${o.size || 14}" fill="${o.fill || C.ink}"` +
  `${o.weight ? ` font-weight="${o.weight}"` : ''}${o.anchor ? ` text-anchor="${o.anchor}"` : ''}${o.italic ? ' font-style="italic"' : ''}>${esc(s)}</text>`);
const lines = (x, y, arr, o = {}) => arr.forEach((s, i) => t(x, y + i * (o.lh || 18), s, o));
const r = (x, y, w, h, o = {}) => out.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}"${o.rx ? ` rx="${o.rx}"` : ''} fill="${o.fill || 'none'}"` +
  `${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}${o.opacity ? ` opacity="${o.opacity}"` : ''}/>`);
const p = (d, o = {}) => out.push(`<path d="${d}" fill="${o.fill || 'none'}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}` +
  `${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}${o.opacity ? ` opacity="${o.opacity}"` : ''} stroke-linecap="round" stroke-linejoin="round"${o.marker ? ` marker-end="url(#${o.marker})"` : ''}/>`);
const circ = (x, y, rr, o = {}) => out.push(`<circle cx="${x}" cy="${y}" r="${rr}" fill="${o.fill || 'none'}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}/>`);
const leader = (x1, y1, x2, y2) => { p(`M${x1} ${y1} L${x2} ${y2}`, { stroke: C.muted, sw: 1 }); circ(x1, y1, 2.5, { fill: C.muted }); };
function wrap(s, n) {
  const res = []; let cur = '';
  for (const wd of s.split(' ')) { if ((cur + ' ' + wd).trim().length > n) { res.push(cur); cur = wd; } else cur = (cur + ' ' + wd).trim(); }
  if (cur) res.push(cur); return res;
}
function panel(x, y, w, h, num, title) {
  r(x, y, w, h, { fill: C.panel, stroke: C.line, rx: 14 });
  circ(x + 26, y + 28, 15, { fill: C.accent });
  t(x + 26, y + 33, num, { size: 15, weight: 700, fill: '#fff', anchor: 'middle' });
  t(x + 50, y + 34, title, { size: 18, weight: 700 });
}

// Разрез картриджа: x, y — левый верх стакана, k — px/мм; wellFill: 0..1 — насыщенность воды в лунке;
// diffusion — показать стрелки диффузии; empty — лунка пустая; flush — струя сверху.
function cartridge(x, y, k, o = {}) {
  const w = 60 * k, h = 40 * k, wellW = 11 * k, wellD = 6 * k, wx = x + w / 2 - wellW / 2;
  const grad = o.grad ? 'url(#barrierGrad)' : C.clear;
  r(x, y, w, h / 2, { fill: grad });
  r(x, y + h / 2, w, h / 2, { fill: C.dye });
  // лунка
  r(wx, y, wellW, wellD, { fill: o.empty ? '#ffffff' : C.water });
  if (!o.empty && o.wellFill) r(wx, y, wellW, wellD, { fill: C.dye, opacity: o.wellFill });
  p(`M${wx} ${y} L${wx} ${y + wellD} L${wx + wellW} ${y + wellD} L${wx + wellW} ${y}`, { stroke: C.plasticStroke, sw: 1 });
  // стакан
  p(`M${x} ${y - 2} L${x} ${y + h} L${x + w} ${y + h} L${x + w} ${y - 2}`, { stroke: C.plasticStroke, sw: 2.5 });
  // крышка с окном
  const lt = 2.2 * k;
  r(x - 4, y - lt, wx - x + 4, lt, { fill: C.lid, rx: 2 });
  r(wx + wellW, y - lt, x + w + 4 - wx - wellW, lt, { fill: C.lid, rx: 2 });
  if (o.diffusion) {
    for (const dx of [-0.9, 0, 0.9]) {
      const ax = x + w / 2 + dx * wellW;
      p(`M${ax} ${y + h / 2 + 4} L${ax + dx * -4} ${y + wellD + 8}`, { stroke: C.dyeDark, sw: 2, marker: 'arrowBlue', dash: '4 4' });
    }
  }
}

out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif">`);
out.push(`<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${C.ink}"/></marker>
<marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${C.dyeDark}"/></marker>
<marker id="arrowWater" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${C.waterStroke}"/></marker>
<linearGradient id="barrierGrad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7fb7ea"/><stop offset="0.55" stop-color="${C.clear}"/><stop offset="1" stop-color="${C.clear}"/></linearGradient>
</defs>`);
r(0, 0, W, H, { fill: C.bg });

// ---------- заголовок ----------
t(30, 48, 'Вариант 4. Синий картридж на ободке унитаза', { size: 28, weight: 700 });
t(30, 76, 'Гель силикагеля с красителем E133 в стаканчике с крышкой. Вода из лунки окрашивает каждый смыв — ровно 60 дней.', { size: 15, fill: C.muted });

// ---------- 1. Где стоит ----------
panel(20, 100, 560, 500, '1', 'Где стоит и что видно');
{
  const X = 20, Y = 40; // рисунок сдвинут вверх внутри панели (панель начинается с y=100)
  // унитаз в разрезе
  p(`M${X + 95} ${Y + 175} C ${X + 110} ${Y + 330}, ${X + 200} ${Y + 420}, ${X + 255} ${Y + 440} L${X + 345} ${Y + 440} C ${X + 420} ${Y + 420}, ${X + 495} ${Y + 330}, ${X + 505} ${Y + 175}`,
    { fill: C.porcelain, stroke: C.plasticStroke, sw: 3 });
  p(`M${X + 170} ${Y + 380} C ${X + 205} ${Y + 418}, ${X + 235} ${Y + 432}, ${X + 255} ${Y + 437} L${X + 345} ${Y + 437} C ${X + 375} ${Y + 430}, ${X + 400} ${Y + 415}, ${X + 432} ${Y + 380} Z`,
    { fill: '#bcdcf5' });
  p(`M${X + 170} ${Y + 380} L${X + 432} ${Y + 380}`, { stroke: C.waterStroke, sw: 1.5, dash: '5 4' });
  // ободок
  r(X + 60, Y + 160, 60, 26, { fill: C.porcelain, stroke: C.plasticStroke, sw: 2.5, rx: 10 });
  r(X + 480, Y + 160, 60, 26, { fill: C.porcelain, stroke: C.plasticStroke, sw: 2.5, rx: 10 });
  t(X + 510, Y + 150, 'ободок', { size: 12, fill: C.muted, anchor: 'middle' });
  // держатель: крючок
  p(`M${X + 70} ${Y + 205} L${X + 70} ${Y + 150} Q ${X + 70} ${Y + 142}, ${X + 80} ${Y + 142} L${X + 120} ${Y + 142} Q ${X + 132} ${Y + 142}, ${X + 132} ${Y + 154} L${X + 132} ${Y + 214}`,
    { stroke: '#3d4752', sw: 4 });
  // корзинка с картриджем
  r(X + 120, Y + 214, 92, 70, { fill: '#fff', stroke: '#3d4752', sw: 2.5, rx: 5 });
  for (let i = 1; i < 4; i++) p(`M${X + 120 + i * 23} ${Y + 262} L${X + 120 + i * 23} ${Y + 284}`, { stroke: '#3d4752', sw: 1 });
  cartridge(X + 131, Y + 232, 1.15, { wellFill: 0.8 });
  // козырёк-воронка
  p(`M${X + 118} ${Y + 214} L${X + 140} ${Y + 200} L${X + 214} ${Y + 196}`, { stroke: '#3d4752', sw: 2.5 });
  // струя из-под ободка
  p(`M${X + 118} ${Y + 190} C ${X + 135} ${Y + 192}, ${X + 155} ${Y + 200}, ${X + 163} ${Y + 222}`, { stroke: C.waterStroke, sw: 2.5, marker: 'arrowWater' });
  p(`M${X + 122} ${Y + 196} C ${X + 145} ${Y + 196}, ${X + 160} ${Y + 210}, ${X + 172} ${Y + 222}`, { stroke: C.waterStroke, sw: 2.5, marker: 'arrowWater' });
  // синяя струя по стенке
  p(`M${X + 200} ${Y + 286} C ${X + 205} ${Y + 330}, ${X + 225} ${Y + 380}, ${X + 265} ${Y + 420}`, { stroke: C.dye, sw: 7, opacity: 0.75 });
  p(`M${X + 212} ${Y + 286} C ${X + 222} ${Y + 330}, ${X + 245} ${Y + 375}, ${X + 290} ${Y + 412}`, { stroke: C.dye, sw: 4, opacity: 0.45 });
  // подписи
  leader(X + 72, Y + 196, X + 30, Y + 230); lines(X + 34, Y + 248, ['крючок', 'с защёлкой'], { size: 12.5, anchor: 'start' });
  leader(X + 205, Y + 240, X + 290, Y + 225); lines(X + 296, Y + 220, ['картридж в корзинке'], { size: 13.5, weight: 600 });
  t(X + 296, Y + 239, '60×40×40 мм, ~120 г', { size: 12.5, fill: C.muted });
  leader(X + 145, Y + 194, X + 290, Y + 160); lines(X + 296, Y + 156, ['струя из-под ободка', 'попадает в окно крышки'], { size: 12.5 });
  leader(X + 228, Y + 360, X + 330, Y + 315); lines(X + 336, Y + 304, ['синяя струя при смыве', '~6 мг красителя'], { size: 13.5, weight: 600, fill: C.dyeDark, lh: 18 });
  leader(X + 330, Y + 410, X + 400, Y + 465); t(X + 330, Y + 482, 'вода в колене слегка голубая (~1 мг/л)', { size: 12.5 });
  lines(X + 24, Y + 512, wrap('Картридж висит под ободком там, где сильнее всего бьёт вода. Каждый смыв промывает лунку — и синяя вода уходит в чашу.', 70), { size: 13.5, lh: 19 });
}

// ---------- 2. Что внутри ----------
panel(600, 100, 580, 500, '2', 'Что внутри картриджа (разрез)');
{
  const X = 600, Y = 100, k = 5, cx = X + 95, cy = Y + 150; // стакан 300×200 px
  cartridge(cx, cy, k, { wellFill: 0.75, grad: false });
  // размеры
  const dimV = (x, y1, y2, s) => { p(`M${x} ${y1} L${x} ${y2}`, { stroke: C.muted, sw: 1, marker: 'arrow' }); p(`M${x} ${y2} L${x} ${y1}`, { stroke: C.muted, sw: 1, marker: 'arrow' }); t(x - 6, (y1 + y2) / 2 + 4, s, { size: 12, fill: C.muted, anchor: 'end' }); };
  dimV(cx - 12, cy, cy + 100, '20 мм');
  dimV(cx - 12, cy + 100, cy + 200, '20 мм');
  p(`M${cx} ${cy + 218} L${cx + 300} ${cy + 218}`, { stroke: C.muted, sw: 1, marker: 'arrow' }); p(`M${cx + 300} ${cy + 218} L${cx} ${cy + 218}`, { stroke: C.muted, sw: 1, marker: 'arrow' });
  t(cx + 150, cy + 236, '60 мм (глубина 40 мм)', { size: 12, fill: C.muted, anchor: 'middle' });
  // 14 мм под лункой
  p(`M${cx + 150} ${cy + 32} L${cx + 150} ${cy + 98}`, { stroke: C.ink, sw: 1.3, marker: 'arrow' }); p(`M${cx + 150} ${cy + 98} L${cx + 150} ${cy + 32}`, { stroke: C.ink, sw: 1.3, marker: 'arrow' });
  t(cx + 158, cy + 70, '14 мм', { size: 12.5, weight: 700 });
  // Ø11
  t(cx + 150, cy - 26, 'окно Ø11 мм', { size: 12.5, weight: 700, anchor: 'middle' });
  p(`M${cx + 150} ${cy - 20} L${cx + 150} ${cy - 4}`, { stroke: C.ink, sw: 1.3, marker: 'arrow' });
  // подписи справа
  const lx = cx + 322;
  leader(cx + 290, cy - 6, lx, cy - 18); lines(lx + 6, cy - 22, ['крышка — плотно', 'лежит на геле'], { size: 12.5, lh: 16 });
  leader(cx + 170, cy + 14, lx, cy + 22); lines(lx + 6, cy + 18, ['лунка 0,6 мл —', 'тут копится синяя', 'вода'], { size: 12.5, lh: 16 });
  leader(cx + 260, cy + 70, lx, cy + 80); lines(lx + 6, cy + 76, ['чистый гель —', 'барьер, задаёт', 'скорость'], { size: 12.5, lh: 16 });
  leader(cx + 260, cy + 150, lx, cy + 150); lines(lx + 6, cy + 146, ['гель + E133', '150 г/л (7,2 г) —', 'запас на 60 дней'], { size: 12.5, lh: 16, fill: C.dyeDark, weight: 600 });
  leader(cx + 300, cy + 196, lx, cy + 206); lines(lx + 6, cy + 210, ['пищевой стакан ПП'], { size: 12.5 });
  lines(X + 24, Y + 420, wrap('Краситель лежит внизу, далеко от воды. До лунки он идёт через 14 мм чистого геля — медленно и ровно. Мокнет только лунка: бока, дно и верх закрыты, гель не сохнет и не вымывается.', 72), { size: 13.5, lh: 19 });
}

// ---------- 3. Цикл ----------
panel(20, 620, 1160, 420, '3', 'Как работает: один цикл между смывами (повторяется ~10 раз в сутки)');
{
  const X = 20, Y = 620, sw = 262;
  const steps = [
    ['Смыв', 'Струя заходит в окно и вымывает синюю воду из лунки в чашу.', { wellFill: 0, empty: false, flush: true }],
    ['Сразу после', 'В лунке осталось 0,6 мл чистой воды.', { wellFill: 0 }],
    ['Через 1–2 часа', 'Краситель медленно идёт из запаса через барьер в воду лунки.', { wellFill: 0.35, diffusion: true, grad: true }],
    ['Перед следующим смывом', 'Вода в лунке синяя: ~6 мг красителя (~10 г/л). Смыв — и всё сначала.', { wellFill: 0.85, grad: true }],
  ];
  steps.forEach(([title, cap, o], i) => {
    const sx = X + 30 + i * (sw + 18), sy = Y + 66;
    r(sx, sy, sw, 290, { fill: '#fff', stroke: C.line, rx: 10 });
    circ(sx + 22, sy + 24, 13, { fill: '#fff', stroke: C.accent, sw: 2 });
    t(sx + 22, sy + 29, String.fromCharCode(0x2460 + i).replace(/./, String(i + 1)), { size: 13, weight: 700, fill: C.accent, anchor: 'middle' });
    t(sx + 42, sy + 29, title, { size: 15, weight: 700 });
    cartridge(sx + 45, sy + 85, 3, o);
    if (o.flush) {
      p(`M${sx + 110} ${sy + 50} C ${sx + 125} ${sy + 55}, ${sx + 132} ${sy + 62}, ${sx + 134} ${sy + 80}`, { stroke: C.waterStroke, sw: 3, marker: 'arrowWater' });
      p(`M${sx + 125} ${sy + 82} C ${sx + 150} ${sy + 60}, ${sx + 185} ${sy + 62}, ${sx + 222} ${sy + 92}`, { stroke: C.dye, sw: 4, marker: 'arrowBlue', opacity: 0.85 });
      t(sx + 180, sy + 62, 'в чашу', { size: 12, fill: C.dyeDark, weight: 600 });
    }
    lines(sx + 16, sy + 238, wrap(cap, 33), { size: 13, lh: 18 });
    if (i < 3) p(`M${sx + sw + 2} ${sy + 150} L${sx + sw + 16} ${sy + 150}`, { stroke: C.ink, sw: 2, marker: 'arrow' });
  });
  // возврат к шагу 1
  const ry = Y + 384, x1 = X + 30 + sw / 2, x4 = X + 30 + 3 * (sw + 18) + sw / 2;
  p(`M${x4} ${Y + 358} L${x4} ${ry} L${x1} ${ry} L${x1} ${Y + 362}`, { stroke: C.muted, sw: 1.5, dash: '5 5', marker: 'arrow' });
  r(X + 520, ry - 10, 120, 20, { fill: C.panel });
  t(X + 580, ry + 4, 'следующий смыв', { size: 12, fill: C.muted, anchor: 'middle' });
}

// ---------- 4. График ----------
panel(20, 1060, 680, 420, '4', 'Почему именно так: краситель за смыв, мг');
{
  const X = 20, Y = 1060, px = X + 70, py = Y + 80, pw = 560, ph = 230, yMax = 20;
  const sx = (d) => px + (d / 60) * pw, sy = (v) => py + ph - (Math.min(v, yMax) / yMax) * ph;
  // целевая зона 4–8 мг
  r(px, sy(8), pw, sy(4) - sy(8), { fill: C.band });
  t(px + pw - 6, sy(8) + 14, 'нужно: ~4–8 мг', { size: 12, fill: C.ok, anchor: 'end', weight: 600 });
  // сетка и оси
  for (const v of [0, 5, 10, 15, 20]) { p(`M${px} ${sy(v)} L${px + pw} ${sy(v)}`, { stroke: '#e3e7eb', sw: 1 }); t(px - 8, sy(v) + 4, String(v), { size: 12, fill: C.muted, anchor: 'end' }); }
  for (const d of [0, 7, 14, 30, 45, 60]) t(sx(d), py + ph + 18, String(d), { size: 12, fill: C.muted, anchor: 'middle' });
  t(px + pw / 2, py + ph + 38, 'дни', { size: 12, fill: C.muted, anchor: 'middle' });
  p(`M${px} ${py + ph} L${px + pw} ${py + ph}`, { stroke: C.plasticStroke, sw: 1.2 });
  // ряд 2: открытый брусок
  const a = [[1, 853], [2, 206], [3, 110], [7, 17], [14, 0.8], [30, 0], [45, 0], [60, 0]];
  const pts = (arr) => arr.map(([d, v]) => `${sx(d).toFixed(1)} ${sy(v).toFixed(1)}`);
  p(`M${sx(1)} ${py} L${pts(a.slice(3)).join(' L')}`, { stroke: C.s2, sw: 2 });
  p(`M${sx(1)} ${py - 4} L${sx(1)} ${py}`, { stroke: C.s2, sw: 2 });
  a.slice(3).forEach(([d, v]) => circ(sx(d), sy(v), 4, { fill: C.s2, stroke: '#fff', sw: 2 }));
  t(sx(1) + 6, py - 10, '▲ 1-й день: 853 мг — выше шкалы, вода «чернильная»', { size: 12, fill: C.ink });
  t(sx(14) + 12, sy(0) - 12, 'открытый брусок: к 14-му дню почти пусто', { size: 12.5, weight: 600 });
  // ряд 1: картридж
  const c4 = [[1, 6.2], [2, 5.6], [3, 6.1], [7, 7.5], [14, 8.0], [30, 6.9], [45, 5.6], [60, 4.6]];
  p(`M${pts(c4).join(' L')}`, { stroke: C.s1, sw: 2 });
  c4.forEach(([d, v]) => circ(sx(d), sy(v), 4, { fill: C.s1, stroke: '#fff', sw: 2 }));
  t(sx(30), sy(6.9) - 12, 'картридж: 4,6–8 мг все 60 дней', { size: 12.5, weight: 600, anchor: 'middle' });
  // легенда
  const ly = Y + 376;
  r(px, ly - 9, 18, 3, { fill: C.s1 }); circ(px + 9, ly - 7.5, 4, { fill: C.s1, stroke: '#fff', sw: 2 });
  t(px + 26, ly - 3, 'картридж (стакан + крышка + барьер)', { size: 12.5 });
  r(px + 300, ly - 9, 18, 3, { fill: C.s2 }); circ(px + 309, ly - 7.5, 4, { fill: C.s2, stroke: '#fff', sw: 2 });
  t(px + 326, ly - 3, 'брусок с красителем везде, открыт', { size: 12.5 });
  t(px, ly + 22, 'Расчёт по модели rim_model.js: брусок 60×40×40 мм, E133 150 г/л, 10 смывов в сутки, ~20 °C.', { size: 11.5, fill: C.muted });
}

// ---------- 5. Правила ----------
panel(720, 1060, 460, 420, '5', 'Как пользоваться');
{
  const X = 720, Y = 1060;
  const items = [
    ['1', 'Снять скотч с окна, вставить картридж в держатель до щелчка, повесить окном вверх.'],
    ['2', 'Первый смыв наполнит лунку, через 1–2 ч вода в ней посинеет.'],
    ['3', 'Уезжаете больше чем на 3 дня — заклейте окно скотчем.'],
    ['4', 'Менять через 60 дней (можно держать до ~90, цвет слабее).'],
    ['5', 'До установки: не дольше 7 дней от заливки, в темноте, окно заклеено.'],
  ];
  items.forEach(([n, s], i) => {
    const iy = Y + 80 + i * 66;
    circ(X + 40, iy, 13, { fill: '#eef5fc', stroke: C.accent, sw: 1.5 });
    t(X + 40, iy + 5, n, { size: 13, weight: 700, fill: C.accent, anchor: 'middle' });
    lines(X + 64, iy + 5, wrap(s, 46), { size: 13.5, lh: 18 });
  });
}

// ---------- подвал ----------
r(20, 1500, 1160, 130, { fill: '#eef5fc', rx: 14 });
t(40, 1532, 'Главная идея', { size: 17, weight: 700 });
lines(40, 1560, [
  'Скорость задаёт не лунка, а слой чистого геля между запасом красителя и водой. Лунка — только «ведёрко»,',
  'в которое краситель собирается между смывами. Ночью вода в лунке насыщается, и выход сам замедляется —',
  'поэтому утром нет «чернильного» смыва.',
], { size: 14, lh: 21 });
t(30, H - 10, 'Изготовление: силикат — в кислоту, кислоту — в воду, очки и перчатки. Подробности — README варианта 4.', { size: 12.5, fill: C.warn, weight: 600 });

out.push('</svg>');
fs.writeFileSync(process.argv[2] || require('path').join(__dirname, 'product.svg'), out.join('\n'));
