// Вариант 4: брусок геля с лункой сверху (как кубик льда) в подвесном держателе на ободке.
// Между смывами в лунке и на мокрых гранях стоит вода, краситель диффундирует в неё,
// следующий смыв её уносит. Пока вода в лунке остаётся разбавленной (≪ концентрации в геле),
// мокрые поверхности — сток (C ≈ 0), и выход задаётся диффузией внутри геля, как в вариантах 1–3.
// Трёхмерная модель Фика с растворением (C = min(m, Cs)), шаг сетки 1 мм.
// Запуск: node rim_model.js

const DAY = 86400;
const FLUSHES_PER_DAY = 10;
const D_20C = 2.6e-10; // м²/с: у ободка воздух комнатный, гель ~18–20 °C (теплее, чем вода в бачке)
const CS = 200;        // г/л

// design (всё в мм): bar {x, y, z} — брусок; well {x, y, depth} — лунка по центру сверху;
// layers [{from, to, load}] — загрузка красителя (г/л) по высоте от дна;
// cup: true — брусок стоит в стакане-картридже (дно и бока закрыты); false — открытая решётка, мокнут все грани.
// lid: true — сверху крышка с окном только над лункой: мокнет одна лунка.
function simulate(design, { D = D_20C, storeDays = 3, days = 60, dx = 1 } = {}) {
  const nx = Math.round(design.bar.x / dx), ny = Math.round(design.bar.y / dx), nz = Math.round(design.bar.z / dx);
  const N = nx * ny * nz, idx = (i, j, k) => (k * ny + j) * nx + i;
  const wx0 = Math.round((design.bar.x - design.well.x) / 2 / dx), wx1 = wx0 + Math.round(design.well.x / dx);
  const wy0 = Math.round((design.bar.y - design.well.y) / 2 / dx), wy1 = wy0 + Math.round(design.well.y / dx);
  const wz0 = nz - Math.round(design.well.depth / dx);
  const gel = new Uint8Array(N), m = new Float64Array(N), C = new Float64Array(N);
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const inWell = i >= wx0 && i < wx1 && j >= wy0 && j < wy1 && k >= wz0;
    if (inWell) continue;
    const n = idx(i, j, k); gel[n] = 1;
    for (const L of design.layers) if (k * dx >= L.from && k * dx < L.to) m[n] = L.load;
  }
  // число мокрых граней у каждой ячейки
  const wet = new Uint8Array(N);
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const n = idx(i, j, k); if (!gel[n]) continue;
    const nb = [[i - 1, j, k], [i + 1, j, k], [i, j - 1, k], [i, j + 1, k], [i, j, k - 1], [i, j, k + 1]];
    let w = 0;
    for (const [a, b, c] of nb) {
      const outside = a < 0 || a >= nx || b < 0 || b >= ny || c < 0 || c >= nz;
      if (outside) { if (c >= nz ? !design.lid : !design.cup) w++; } // верх мокнет без крышки, бока и дно — без стакана
      else if (!gel[idx(a, b, c)]) w++;                  // стенка лунки
    }
    wet[n] = w;
  }
  const cellV = (dx / 1000) ** 3;
  const steps = Math.ceil(DAY / (0.9 * (dx / 1000) ** 2 / (6 * D)));
  const g = D * (DAY / steps) / ((dx / 1000) ** 2);
  const daily = [];
  for (let d = 0; d < storeDays + days; d++) {
    const open = d >= storeDays; let rel = 0;
    for (let s = 0; s < steps; s++) {
      for (let n = 0; n < N; n++) C[n] = m[n] < CS ? m[n] : CS;
      for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const n = idx(i, j, k); if (!gel[n]) continue;
        const c = C[n]; let dm = 0;
        if (i > 0 && gel[n - 1]) dm += g * (C[n - 1] - c);
        if (i < nx - 1 && gel[n + 1]) dm += g * (C[n + 1] - c);
        if (j > 0 && gel[n - nx]) dm += g * (C[n - nx] - c);
        if (j < ny - 1 && gel[n + nx]) dm += g * (C[n + nx] - c);
        if (k > 0 && gel[n - nx * ny]) dm += g * (C[n - nx * ny] - c);
        if (k < nz - 1 && gel[n + nx * ny]) dm += g * (C[n + nx * ny] - c);
        if (open && wet[n]) { const l = 2 * g * c * wet[n]; dm -= l; rel += l * cellV; }
        m[n] += dm;
      }
    }
    if (open) daily.push(rel * 1e6); // мг/сутки (г/л = кг/м³)
  }
  let dye = 0; for (let n = 0; n < N; n++) dye += m[n] * cellV * 1000;
  return { daily, leftG: dye };
}

function report(title, design, opts) {
  const { daily, leftG } = simulate(design, opts);
  const show = [1, 2, 3, 7, 14, 30, 45, 60];
  const tail = daily.slice(1), total = daily.reduce((a, b) => a + b, 0);
  console.log(`\n${title}`);
  console.log('  день       ' + show.map((d) => String(d).padStart(7)).join(''));
  console.log('  мг/сутки   ' + show.map((d) => daily[d - 1].toFixed(1).padStart(7)).join(''));
  console.log('  мг/смыв    ' + show.map((d) => (daily[d - 1] / FLUSHES_PER_DAY).toFixed(1).padStart(7)).join(''));
  console.log(`  вышло ${(total / 1000).toFixed(2)} г, осталось ${leftG.toFixed(2)} г; разброс дни 2–60: ` +
    `${(Math.max(...tail) / Math.min(...tail)).toFixed(2)}×`);
}

module.exports = { simulate };

if (require.main === module) {
  const bar = { x: 60, y: 40, z: 40 };
  const core = [{ from: 0, to: 20, load: 150 }]; // нижние 20 мм — гель с E133 150 г/л, верхние 20 мм — чистый
  report('4A. Исходная идея: краситель 150 г/л по всему бруску, большая лунка 30×20×10 мм, открытая решётка',
    { bar, well: { x: 30, y: 20, depth: 10 }, cup: false, lid: false, layers: [{ from: 0, to: 40, load: 150 }] });
  report('4B. Двухслойный брусок в стакане, но без крышки (мокнет весь верх)',
    { bar, well: { x: 10, y: 10, depth: 6 }, cup: true, lid: false, layers: core });
  const rec = { bar, well: { x: 10, y: 10, depth: 6 }, cup: true, lid: true, layers: core };
  report('4C. Картридж: стакан + крышка с окном над лункой 10×10×6 мм, под лункой 14 мм чистого геля (рекомендуемый)', rec);
  report('4C после хранения 14 дней', rec, { storeDays: 14 });
  report('4C зимой (в туалете ~15 °C)', rec, { D: 2.3e-10 });
}
