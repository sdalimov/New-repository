// Генератор схемы порядка работы варианта 3: node make_workflow_svg.js [workflow.svg]
const fs = require('fs');
const W = 1200, H = 1710;
const C = {
  ink: '#1d2733', muted: '#5b6773', line: '#c9d2db', panel: '#f7f9fb', bg: '#ffffff',
  clear: '#dff1f5', clearStroke: '#9ccbd6', dye: '#1778d4', dyeDark: '#0f5aa3',
  wax: '#f1dc9f', waxStroke: '#c9ad5c', plug: '#4a4f57', acid: '#e8eef5', ok: '#2e8b57', bad: '#c0392b',
  water: '#d6ecfa', accent: '#1778d4', warn: '#b35c00',
};
let out = [];
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const t = (x, y, s, o = {}) => out.push(`<text x="${x}" y="${y}" font-size="${o.size || 14}" fill="${o.fill || C.ink}"` +
  `${o.weight ? ` font-weight="${o.weight}"` : ''}${o.anchor ? ` text-anchor="${o.anchor}"` : ''}>${esc(s)}</text>`);
const lines = (x, y, arr, o = {}) => arr.forEach((s, i) => t(x, y + i * (o.lh || 19), s, o));
const r = (x, y, w, h, o = {}) => out.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}"${o.rx ? ` rx="${o.rx}"` : ''} fill="${o.fill || 'none'}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`);
const p = (d, o = {}) => out.push(`<path d="${d}" fill="${o.fill || 'none'}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}${o.dash ? ` stroke-dasharray="${o.dash}"` : ''} stroke-linecap="round" stroke-linejoin="round"${o.opacity ? ` opacity="${o.opacity}"` : ''}${o.marker ? ` marker-end="url(#arrow)"` : ''}/>`);
const circ = (x, y, rr, o = {}) => out.push(`<circle cx="${x}" cy="${y}" r="${rr}" fill="${o.fill || 'none'}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 1.5}"` : ''}/>`);

// Трубка: x — левый край, yb — низ трубки (над пробкой), mm → px.
// layers: {barrier, dye(верх слоя красителя, мм), wax(bool)}, marks: [мм]
function tube(x, yb, o = {}) {
  const k = o.k || 2.0, w = o.w || 30, hTube = 90 * k;
  const y = (mm) => yb - mm * k;
  if (o.barrier) r(x, y(o.barrier), w, o.barrier * k, { fill: C.clear });
  if (o.dye) r(x, y(o.dye), w, (o.dye - (o.barrier || 0)) * k, { fill: C.dye });
  if (o.wax) {
    r(x, y(90), w, 10 * k, { fill: C.wax });
    p(`M${x + w / 2} ${y(84)} C ${x + w / 2 - 14} ${y(100)}, ${x + w / 2 + 14} ${y(108)}, ${x + w / 2} ${y(96)}`, { stroke: C.muted, sw: 1.3 });
    p(`M${x + w / 2} ${y(84)} L${x + w / 2} ${y(96)}`, { stroke: C.muted, sw: 1.3 });
  }
  r(x, y(90), w, hTube, { stroke: '#7d8a96', sw: 2, rx: 2 });
  if (o.plug !== false) r(x - 3, yb, w + 6, 12, { fill: C.plug, rx: 3 });
  for (const mm of o.marks || []) {
    p(`M${x + w} ${y(mm)} L${x + w + 8} ${y(mm)}`, { stroke: C.muted, sw: 1.2 });
    t(x + w + 11, y(mm) + 4, String(mm), { size: 11, fill: C.muted });
  }
  if (o.label) t(x + w / 2, yb + 30, o.label, { size: 13, weight: 600, anchor: 'middle' });
}
function beaker(x, y, w, h, fill, label, o = {}) {
  r(x + 2, y + h * 0.35, w - 4, h * 0.65 - 2, { fill });
  p(`M${x} ${y} L${x} ${y + h} L${x + w} ${y + h} L${x + w} ${y}`, { stroke: '#7d8a96', sw: 2 });
  lines(x + w / 2, y + h + 18, label.split('\n'), { size: 12, anchor: 'middle', fill: C.muted, lh: 15 });
}
function clock(x, y, label) {
  circ(x, y, 22, { stroke: C.ink, sw: 2, fill: '#fff' });
  p(`M${x} ${y} L${x} ${y - 14} M${x} ${y} L${x + 10} ${y + 4}`, { stroke: C.ink, sw: 2 });
  t(x, y + 42, label, { size: 14, weight: 700, anchor: 'middle' });
}
function wrap(s, n) {
  const words = s.split(' '); const res = []; let cur = '';
  for (const wd of words) { if ((cur + ' ' + wd).trim().length > n) { res.push(cur); cur = wd; } else cur = (cur + ' ' + wd).trim(); }
  if (cur) res.push(cur); return res;
}

out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif">`);
out.push(`<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${C.ink}"/></marker></defs>`);
r(0, 0, W, H, { fill: C.bg });

// --- заголовок и легенда ---
t(30, 48, 'Вариант 3. Палочки Ø15×90 мм — порядок работы', { size: 28, weight: 700 });
t(30, 76, 'Партия 12 палочек (6 А + 6 Б = 2 набора). Силикагель из жидкого стекла и H₂SO₄, краситель E133.', { size: 15, fill: C.muted });
const lg = [[C.clear, 'чистый гель (барьер)'], [C.dye, 'гель + E133 150 г/л'], [C.wax, 'воск'], [C.plug, 'пробка']];
lg.forEach(([f, s], i) => { const lx = 840 + (i % 2) * 175, ly = 34 + Math.floor(i / 2) * 26; r(lx, ly, 18, 14, { fill: f, stroke: '#7d8a96', sw: 1 }); t(lx + 26, ly + 12, s, { size: 13 }); });

// --- полоса разработки рецептуры ---
const ry = 105;
r(20, ry, W - 40, 150, { fill: '#eef5fc', rx: 14 });
t(40, ry + 30, 'А. Разработка рецептуры — один раз, до производства', { size: 17, weight: 700 });
const stages = [
  ['0', 'Сырьё', 'плотности,', 'эталон E133', '1 день'],
  ['1', 'Гель', 'SiO₂ 5–7 %,', 'pH 3–5', '1–2 дня'],
  ['2', 'Краситель', 'макс. загрузка', 'без осадка', '1 день'],
  ['3', 'Стенка', 'нет «языков»', 'у стенки', '2 дня'],
  ['4', 'Замер', '1 палочка в 1 л,', 'fit модели', '10–14 дней'],
  ['5', 'Хранение', '3/7/14/30 дн', 'в упаковке', 'до 30 дней'],
  ['6', 'Бачок', 'набор 3А+3Б', 'в работе', '60 дней'],
  ['7', 'Карта', 'рецептура', 'утверждена', '—'],
];
const cw = 138;
stages.forEach(([n, title, a, b, dur], i) => {
  const x = 40 + i * (cw + 4), y = ry + 46;
  const tip = i < stages.length - 1 ? 14 : 0;
  p(`M${x} ${y} L${x + cw - tip} ${y} L${x + cw} ${y + 40} L${x + cw - tip} ${y + 80} L${x} ${y + 80} ${i ? `L${x + 14} ${y + 40} Z` : 'Z'}`, { fill: '#fff', stroke: C.accent, sw: 1.5 });
  t(x + (i ? 24 : 12), y + 22, `${n}. ${title}`, { size: 14, weight: 700, fill: C.dyeDark });
  t(x + (i ? 24 : 12), y + 41, a, { size: 12, fill: C.muted });
  t(x + (i ? 24 : 12), y + 56, b, { size: 12, fill: C.muted });
  t(x + (i ? 24 : 12), y + 73, dur, { size: 12, weight: 600 });
});

// --- панели производства ---
t(30, 300, 'Б. Изготовление партии', { size: 17, weight: 700 });
const PW = 370, PH = 380, X0 = 25, Y0 = 315, G = 20;
const panels = [];
function panel(i, title, caption, draw) {
  const col = i % 3, row = Math.floor(i / 3);
  const x = X0 + col * (PW + G), y = Y0 + row * (PH + G);
  r(x, y, PW, PH, { fill: C.panel, stroke: C.line, rx: 14 });
  circ(x + 26, y + 28, 15, { fill: C.accent });
  t(x + 26, y + 33, String(i + 1), { size: 15, weight: 700, fill: '#fff', anchor: 'middle' });
  t(x + 50, y + 34, title, { size: 17, weight: 700 });
  draw(x, y);
  lines(x + 18, y + PH - 70, wrap(caption, 47), { size: 13.5, fill: C.ink });
  if (i % 3 < 2 && i < 8) p(`M${x + PW + 3} ${y + 140} L${x + PW + G - 3} ${y + 140}`, { stroke: C.ink, sw: 2, marker: true });
}

panel(0, 'Подготовка трубок', 'Нарезать по 90 мм, зашкурить изнутри, нанести метки 15 мм (А) / 30 мм (Б) и 80 мм, вставить нижние пробки.', (x, y) => {
  tube(x + 95, y + 250, { marks: [15, 80], label: 'А' });
  tube(x + 175, y + 250, { marks: [30, 80], label: 'Б' });
  t(x + 250, y + 120, '90 мм', { size: 12, fill: C.muted });
  p(`M${x + 238} ${y + 70} L${x + 238} ${y + 250}`, { stroke: C.muted, sw: 1, dash: '3 3' });
  t(x + 250, y + 262, '← пробка', { size: 12, fill: C.muted });
  // наждачка
  r(x + 278, y + 150, 46, 30, { fill: '#e2c99a', stroke: '#b8975c', sw: 1, rx: 3 });
  t(x + 301, y + 198, 'шкурка', { size: 12, fill: C.muted, anchor: 'middle' });
});

panel(1, 'Бесцветный золь → барьер', '15 г жидкого стекла + 30 мл воды медленно влить В КИСЛОТУ (~21 мл 10 %), pH 3–4. Залить до 15 мм (А) и 30 мм (Б).', (x, y) => {
  beaker(x + 25, y + 90, 60, 70, '#eceff2', 'силикат\n+ вода');
  beaker(x + 120, y + 150, 64, 76, C.acid, 'кислота\n10 %');
  p(`M${x + 75} ${y + 92} C ${x + 110} ${y + 70}, ${x + 140} ${y + 100}, ${x + 150} ${y + 140}`, { stroke: C.ink, sw: 2, marker: true });
  r(x + 118, y + 100, 66, 22, { fill: '#fff', stroke: C.warn, sw: 1.3, rx: 11 });
  t(x + 151, y + 115, 'pH 3–4', { size: 12, weight: 700, fill: C.warn, anchor: 'middle' });
  tube(x + 235, y + 250, { barrier: 15, marks: [15], label: 'А' });
  tube(x + 300, y + 250, { barrier: 30, marks: [30], label: 'Б' });
});

panel(2, 'Схватывание', 'Наклонить контрольный стаканчик на 45°: гель не течёт. Обычно 10–20 мин. Второй слой — не позже чем через 2 ч.', (x, y) => {
  out.push(`<g transform="rotate(-45 ${x + 120} ${y + 190})">`);
  beaker(x + 90, y + 140, 60, 80, C.clear, '');
  out.push('</g>');
  t(x + 92, y + 268, 'не течёт ✓', { size: 13, weight: 600, fill: C.ok });
  clock(x + 270, y + 120, '10–20 мин');
  r(x + 222, y + 200, 98, 26, { fill: '#fff4e5', stroke: C.warn, sw: 1.3, rx: 13 });
  t(x + 271, y + 218, 'макс. 2 ч', { size: 13, weight: 700, fill: C.warn, anchor: 'middle' });
});

panel(3, 'Окрашенный золь → запас', '35 г жидкого стекла в 70 мл воды с 12,6 г E133 влить в ~49 мл кислоты с 8,8 г E133 (≈150 г/л). Трубку шприца — почти до барьера, залить до 80 мм.', (x, y) => {
  beaker(x + 22, y + 80, 60, 70, '#5aa2e6', 'вода + E133\n+ силикат');
  beaker(x + 110, y + 150, 64, 76, '#5aa2e6', 'кислота\n+ E133');
  p(`M${x + 72} ${y + 82} C ${x + 105} ${y + 62}, ${x + 130} ${y + 95}, ${x + 140} ${y + 140}`, { stroke: C.ink, sw: 2, marker: true });
  tube(x + 235, y + 250, { barrier: 15, dye: 80, marks: [80], label: 'А' });
  tube(x + 300, y + 250, { barrier: 30, dye: 80, marks: [80], label: 'Б' });
  // шприц
  r(x + 190, y + 58, 16, 60, { fill: '#fff', stroke: '#7d8a96', sw: 1.5, rx: 2 });
  p(`M${x + 198} ${y + 118} C ${x + 205} ${y + 150}, ${x + 245} ${y + 130}, ${x + 250} ${y + 200}`, { stroke: '#7d8a96', sw: 2 });
});

panel(4, 'Воск и подвес', 'Через 30 мин: воск (~60 °C, водяная баня) слоем 8–10 мм прямо на гель, без воздуха. Утопить петлю лески.', (x, y) => {
  tube(x + 110, y + 260, { barrier: 15, dye: 80, wax: true, k: 2.1, w: 34 });
  const yy = (mm) => y + 260 - mm * 2.1;
  [[90, 'воск + петля, 10 мм'], [47, 'запас: 65 мм (А) / 50 мм (Б)'], [7.5, 'барьер: 15 мм (А) / 30 мм (Б)']].forEach(([mm, s]) => {
    p(`M${x + 150} ${yy(mm) + (mm === 90 ? 10 : 0)} L${x + 175} ${yy(mm) + (mm === 90 ? 10 : 0)}`, { stroke: C.muted, sw: 1 });
    t(x + 180, yy(mm) + (mm === 90 ? 14 : 4), s, { size: 12.5 });
  });
  t(x + 180, y + 274, 'пробка — до установки', { size: 12.5 });
  p(`M${x + 150} ${y + 266} L${x + 175} ${y + 270}`, { stroke: C.muted, sw: 1 });
});

panel(5, 'Созревание 48 ч', '48 ч в штативе при комнатной температуре, в темноте (E133 выцветает на свету). Пробки не снимать.', (x, y) => {
  r(x + 30, y + 236, 230, 18, { fill: '#c9a77a', rx: 3 });
  for (let i = 0; i < 6; i++) tube(x + 42 + i * 36, y + 236, { barrier: i < 3 ? 15 : 30, dye: 80, wax: true, k: 1.65, w: 22, plug: false });
  t(x + 90, y + 274, '3 × А', { size: 13, weight: 600, anchor: 'middle' });
  t(x + 200, y + 274, '3 × Б', { size: 13, weight: 600, anchor: 'middle' });
  clock(x + 315, y + 105, '48 ч');
  p(`M${x + 322} ${y + 175} a 16 16 0 1 0 14 22 a 12 12 0 1 1 -14 -22 z`, { fill: '#55606c' });
});

panel(6, 'Контроль качества', 'Через 24 и 48 ч: фронт красителя ровный, без пузырей, трещин и зазора у стенки. Брак не исправляется.', (x, y) => {
  // годно
  const g1 = x + 80, g2 = x + 230, top = y + 70, hh = 170, ww = 60;
  r(g1, top, ww, hh * 0.45, { fill: C.dye });
  r(g1, top + hh * 0.45, ww, hh * 0.55, { fill: C.clear });
  r(g1, top + hh * 0.45, ww, 14, { fill: '#7fb7ea' });
  r(g1, top, ww, hh, { stroke: '#7d8a96', sw: 2 });
  t(g1 + ww / 2, top + hh + 26, '✓ годно', { size: 15, weight: 700, fill: C.ok, anchor: 'middle' });
  t(g1 + ww / 2, top + hh + 44, 'ровный фронт', { size: 12, fill: C.muted, anchor: 'middle' });
  // брак
  r(g2, top, ww, hh * 0.45, { fill: C.dye });
  r(g2, top + hh * 0.45, ww, hh * 0.55, { fill: C.clear });
  r(g2, top + hh * 0.45, ww, 14, { fill: '#7fb7ea' });
  p(`M${g2} ${top + hh * 0.45} L${g2} ${top + hh - 8} L${g2 + 7} ${top + hh * 0.5} Z`, { fill: C.dye });
  p(`M${g2 + ww} ${top + hh * 0.45} L${g2 + ww} ${top + hh - 25} L${g2 + ww - 7} ${top + hh * 0.5} Z`, { fill: C.dye });
  r(g2, top, ww, hh, { stroke: '#7d8a96', sw: 2 });
  t(g2 + ww / 2, top + hh + 26, '✗ брак', { size: 15, weight: 700, fill: C.bad, anchor: 'middle' });
  t(g2 + ww / 2, top + hh + 44, '«языки» у стенки', { size: 12, fill: C.muted, anchor: 'middle' });
});

panel(7, 'Упаковка и хранение', 'Мягкий вакуум или зип-пакет. 5–15 °C, темно, не замораживать. Поставить в бачок в течение 7 дней от заливки.', (x, y) => {
  r(x + 40, y + 70, 170, 190, { fill: '#eef3f7', stroke: '#9aa7b3', sw: 1.5, rx: 18, dash: '6 4' });
  for (let i = 0; i < 6; i++) tube(x + 62 + i * 22, y + 230, { barrier: i < 3 ? 15 : 30, dye: 80, wax: true, k: 1.6, w: 16 });
  r(x + 228, y + 80, 124, 92, { fill: '#fff', stroke: C.ink, sw: 1.3, rx: 6 });
  lines(x + 238, y + 100, ['Партия № 07', 'Залито: 01.11', 'А ×3   Б ×3', 'Годен до: 08.11'], { size: 12.5, lh: 19 });
  r(x + 228, y + 188, 124, 62, { fill: '#fff4e5', stroke: C.warn, sw: 1.3, rx: 6 });
  lines(x + 238, y + 207, ['> 7 дн → замочить', '14 дн → 1 сутки', '30 дн → 2 суток'], { size: 12, lh: 17, fill: C.warn });
});

panel(8, 'Установка в бачок', 'Снять пробки, связать пучок 3А + 3Б, повесить торцами вниз под воду, подальше от поплавка и клапана. Замена через 60 дней.', (x, y) => {
  const bx = x + 30, by = y + 60, bw = 310, bh = 210;
  r(bx, by + 50, bw, bh - 50, { fill: C.water });
  p(`M${bx} ${by} L${bx} ${by + bh} L${bx + bw} ${by + bh} L${bx + bw} ${by}`, { stroke: '#7d8a96', sw: 3 });
  r(bx - 6, by - 8, bw + 12, 10, { fill: '#7d8a96', rx: 3 });
  p(`M${bx} ${by + 50} L${bx + bw} ${by + 50}`, { stroke: '#4d93c9', sw: 1.5, dash: '6 4' });
  t(bx + 150, by + 44, 'уровень воды', { size: 11, fill: '#3a78a8' });
  // поплавок и клапан
  r(bx + 232, by + 38, 44, 26, { fill: '#e6e9ec', stroke: '#7d8a96', sw: 1.3, rx: 10 });
  r(bx + 248, by + 64, 10, 110, { fill: '#e6e9ec', stroke: '#7d8a96', sw: 1.3 });
  r(bx + 225, by + bh - 22, 56, 22, { fill: '#e6e9ec', stroke: '#7d8a96', sw: 1.3, rx: 4 });
  t(bx + 253, by + bh - 28, 'клапан', { size: 11, fill: C.muted, anchor: 'middle' });
  // пучок
  p(`M${bx + 2} ${by - 2} C ${bx + 30} ${by + 10}, ${bx + 60} ${by + 10}, ${bx + 82} ${by + 32}`, { stroke: C.muted, sw: 1.3 });
  for (let i = 0; i < 6; i++) tube(x + 92 + i * 13, y + 210, { barrier: i < 3 ? 15 : 30, dye: 80, wax: true, k: 1.25, w: 11, plug: false });
  r(x + 89, y + 130, 84, 6, { fill: '#c0392b', rx: 2 });
  // шлейф красителя из торцов
  out.push(`<ellipse cx="${x + 130}" cy="${y + 255}" rx="62" ry="16" fill="${C.dye}" opacity="0.18"/>`);
  for (let i = 0; i < 6; i++) {
    const sx = x + 97.5 + i * 13, sy = y + 212;
    p(`M${sx} ${sy} C ${sx - 8} ${sy + 15}, ${sx + 8} ${sy + 28}, ${sx + (i - 2.5) * 6} ${sy + 46}`, { stroke: C.dye, sw: 3, opacity: 0.55 });
  }
});

// --- шкала времени ---
const ty = Y0 + 3 * (PH + G) + 10;
r(20, ty, W - 40, 145, { fill: '#eef5fc', rx: 14 });
t(40, ty + 30, 'В. Сроки одной партии', { size: 17, weight: 700 });
const tl = [[0, 'День 0', 'заливка, шаги 1–5'], [2, 'День 2', 'контроль, упаковка'], [7, '≤ День 7', 'установка в бачок'], [67, 'День 67', 'замена набора (60 дней работы)']];
const tx = (d) => 90 + (d <= 7 ? d * 70 : 7 * 70 + (d - 7) * 8.3);
p(`M${tx(0)} ${ty + 75} L${tx(67) + 10} ${ty + 75}`, { stroke: C.ink, sw: 3 });
r(tx(0), ty + 69, tx(2) - tx(0), 12, { fill: '#9ccbd6' });
r(tx(2), ty + 69, tx(7) - tx(2), 12, { fill: C.wax });
r(tx(7), ty + 69, tx(67) - tx(7), 12, { fill: C.dye });
tl.forEach(([d, a, b]) => { circ(tx(d), ty + 75, 8, { fill: '#fff', stroke: C.ink, sw: 2.5 });
  t(tx(d), ty + 106, a, { size: 14, weight: 700, anchor: d === 67 ? 'end' : 'middle' });
  t(d === 67 ? tx(d) : tx(d), ty + 125, b, { size: 12.5, fill: C.muted, anchor: d === 67 ? 'end' : 'middle' }); });
t((tx(0) + tx(2)) / 2, ty + 60, 'созревание', { size: 12, fill: C.muted, anchor: 'middle' });
t((tx(2) + tx(7)) / 2, ty + 60, 'хранение', { size: 12, fill: C.muted, anchor: 'middle' });
t((tx(7) + tx(67)) / 2, ty + 60, 'работа: ~1 мг/л в смыве, к 60-му дню ~0,7 мг/л', { size: 12, fill: C.muted, anchor: 'middle' });

t(30, H - 14, 'Очки и перчатки обязательны · кислоту — в воду, силикат — в кислоту · воск — только на водяной бане', { size: 13, fill: C.warn, weight: 600 });
out.push('</svg>');
fs.writeFileSync(process.argv[2] || require('path').join(__dirname, 'workflow.svg'), out.join('\n'));
