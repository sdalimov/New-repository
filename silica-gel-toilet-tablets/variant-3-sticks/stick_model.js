// Вариант 3: палочки силикагеля Ø15 мм в трубке-гильзе, краситель выходит только
// через нижний торец. Сначала в трубке лежит чистый слой-барьер, над ним слой с красителем.
// Одномерная модель Фика с растворением (C = min(m, Cs)). Хранение (созревание, упаковка)
// моделируется как время, когда торец закрыт и краситель уже ползёт в барьер.
//
//   node stick_model.js                       — расчёт базовых конструкций и рекомендуемого набора
//   node stick_model.js fit 15 150 3 26,18,17 — подбор D по замерам одной палочки:
//        барьер (мм), загрузка (г/л), дней хранения до старта, мг/сутки по дням

const DAY = 86400;
const CS = 200;          // кг/м³ (= г/л), растворимость E133
const D_12C = 2.2e-10;   // м²/с, E133 в гидрогеле SiO2 при ~12 °C
const CISTERN_L = 6;
const FLUSHES_PER_DAY = 10;

// stick: { barrierMm, gelMm (общая высота геля), diaMm, load (г/л в слое с красителем) }
function simulate(stick, { D = D_12C, storeDays = 3, days = 60, dz = 0.0005 } = {}) {
  const n = Math.round(stick.gelMm / 1000 / dz);
  const nb = Math.round(stick.barrierMm / 1000 / dz);
  const A = Math.PI * (stick.diaMm / 1000) ** 2 / 4;
  const m = new Float64Array(n);
  for (let i = nb; i < n; i++) m[i] = stick.load;
  const dtMax = 0.4 * dz * dz / D;
  const steps = Math.ceil(DAY / dtMax);
  const g = D * (DAY / steps) / (dz * dz);
  const C = new Float64Array(n);
  const daily = [];
  for (let d = 0; d < storeDays + days; d++) {
    const open = d >= storeDays;
    let released = 0;
    for (let s = 0; s < steps; s++) {
      for (let i = 0; i < n; i++) C[i] = m[i] < CS ? m[i] : CS;
      for (let i = 0; i < n; i++) {
        let dm = 0;
        if (i > 0) dm += g * (C[i - 1] - C[i]);
        if (i < n - 1) dm += g * (C[i + 1] - C[i]);
        if (i === 0 && open) {
          const loss = 2 * g * C[0];
          dm -= loss;
          released += loss * dz * A;
        }
        m[i] += dm;
      }
    }
    if (open) daily.push(released * 1e6); // мг/сутки
  }
  return daily;
}

const dyeGrams = (s) => s.load * (s.gelMm - s.barrierMm) / 1000 * Math.PI * (s.diaMm / 1000) ** 2 / 4 * 1000;

function sumSet(set, opts) {
  let total = null;
  for (const { stick, count } of set) {
    const daily = simulate(stick, opts);
    total = total ? total.map((v, i) => v + count * daily[i]) : daily.map((v) => count * v);
  }
  return total;
}

function report(title, daily) {
  const perL = (mg) => mg / (CISTERN_L * FLUSHES_PER_DAY);
  const tail = daily.slice(1);
  console.log(`\n${title}`);
  console.log('  день     ' + [1, 2, 3, 7, 14, 30, 45, 60].map((d) => String(d).padStart(6)).join(''));
  console.log('  мг/сутки ' + [1, 2, 3, 7, 14, 30, 45, 60].map((d) => daily[d - 1].toFixed(1).padStart(6)).join(''));
  console.log('  мг/л     ' + [1, 2, 3, 7, 14, 30, 45, 60].map((d) => perL(daily[d - 1]).toFixed(2).padStart(6)).join(''));
  console.log(`  за 60 дней вышло ${(daily.reduce((a, b) => a + b, 0) / 1000).toFixed(2)} г; ` +
    `разброс дни 2–60: ${(Math.max(...tail) / Math.min(...tail)).toFixed(2)}×`);
}

// 150 г/л — реальный предел: краситель надо растворить в воде и кислоте до смешивания (≤ ~180 г/л).
// Пока краситель весь растворён, выход пропорционален загрузке.
const A = { barrierMm: 15, gelMm: 80, diaMm: 15, load: 150 }; // тип А: барьер 15 мм + 65 мм красителя
const B = { barrierMm: 30, gelMm: 80, diaMm: 15, load: 150 }; // тип Б: барьер 30 мм + 50 мм красителя
const SET = [{ stick: A, count: 3 }, { stick: B, count: 3 }];

module.exports = { simulate, sumSet, dyeGrams, A, B, SET };

if (require.main === module && process.argv[2] === 'fit') {
  const [barrierMm, load, storeDays] = process.argv.slice(3, 6).map(Number);
  const data = process.argv[6].split(',').map(Number);
  const stick = { barrierMm, gelMm: 80, diaMm: 15, load };
  let best = null;
  for (let D = 0.5e-10; D <= 6e-10; D += 0.1e-10) {
    const sim = simulate(stick, { D, storeDays, days: data.length, dz: 0.001 });
    const err = data.reduce((s, v, i) => s + (v - sim[i]) ** 2, 0);
    if (!best || err < best.err) best = { D, err, sim };
  }
  console.log(`Лучшее D = ${best.D.toExponential(2)} м²/с (принято в модели ${D_12C.toExponential(2)})`);
  console.log('  замер  ' + data.map((v) => v.toFixed(1).padStart(6)).join(''));
  console.log('  модель ' + best.sim.map((v) => v.toFixed(1).padStart(6)).join(''));
} else if (require.main === module) {
  const base = { barrierMm: 10, gelMm: 80, diaMm: 15, load: 150 };
  report(`1 палочка 10/70 мм (исходная идея), 150 г/л, ${dyeGrams(base).toFixed(1)} г E133`, simulate(base));
  report(`1 палочка тип А 15/65 мм, ${dyeGrams(A).toFixed(1)} г`, simulate(A));
  report(`1 палочка тип Б 30/50 мм, ${dyeGrams(B).toFixed(1)} г`, simulate(B));
  report('3 одинаковые палочки 10/70 мм', simulate(base).map((v) => 3 * v));
  const setDye = SET.reduce((s, x) => s + x.count * dyeGrams(x.stick), 0);
  report(`НАБОР: 3×А + 3×Б (рекомендуемый), ${setDye.toFixed(1)} г E133, хранение 3 дня`, sumSet(SET));
  for (const storeDays of [7, 14, 30]) report(`НАБОР после хранения ${storeDays} дней`, sumSet(SET, { storeDays }));
  report('НАБОР после хранения 14 дней и замачивания на 1 сутки (вода сливается)',
    sumSet(SET, { storeDays: 14, days: 61 }).slice(1));
  report('НАБОР при 25 °C', sumSet(SET, { D: 3.0e-10 }));
}
