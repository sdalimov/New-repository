// Модель выхода красителя (E133, Brilliant Blue FCF) в бачок унитаза.
// Сравнивает три конструкции:
//   A — сплошной брикет силикагеля (гидрогель), краситель распределён по объёму;
//   B — то же, но высушенный ксерогель (оптимистичная оценка: диффузия в 10 раз медленнее);
//   C — капсула-резервуар: насыщенный раствор + избыток сухого красителя
//       за «окном» из силикагеля (рекомендуемый вариант).
// Задержка первого выхода (~h²/6D ≈ 20 ч для окна 10 мм) в модели не учтена.
// Запуск: node release_model.js

const DAY = 86400; // с

// --- условия эксплуатации ---
const CISTERN_L = 6;        // объём бачка, л
const FLUSHES_PER_DAY = 10; // смывов в сутки
const TARGET_MG_L = 1;      // желаемая концентрация в воде смыва, мг/л

// Коэффициент диффузии E133 в воде ~4.5e-10 м²/с (25 °C).
// В гидрогеле SiO2 (~94 % воды) с учётом извилистости пор берём ~3e-10,
// для холодной воды бачка (~12 °C) — ~2.2e-10.
const D_GEL_25C = 3.0e-10;
const D_GEL_12C = 2.2e-10;

// Растворимость E133 ~200 г/л (= кг/м³) при 20–25 °C; в холодной воде меньше.
const SOLUBILITY = 200;

// Доля красителя, оставшаяся в пластине полутолщиной L (м) через t (с),
// решение уравнения Фика рядом Фурье.
function slabRemaining(D, L, t) {
  let sum = 0;
  for (let n = 0; n < 200; n++) {
    const k = 2 * n + 1;
    sum += (8 / (k * k * Math.PI * Math.PI)) *
      Math.exp(-D * k * k * Math.PI * Math.PI * t / (4 * L * L));
  }
  return Math.min(1, sum);
}

// Прямоугольный брикет a×b×c (м): остаток = произведение решений по трём осям.
function brickRemaining(D, [a, b, c], t) {
  return slabRemaining(D, a / 2, t) * slabRemaining(D, b / 2, t) * slabRemaining(D, c / 2, t);
}

function brickDailyRelease(D, dims, dyeMg, days) {
  const out = [];
  for (let d = 1; d <= days; d++) {
    const before = brickRemaining(D, dims, (d - 1) * DAY);
    const after = brickRemaining(D, dims, d * DAY);
    out.push(dyeMg * (before - after));
  }
  return out;
}

// Капсула: поток J = D·A·Cs/h, пока в резервуаре есть нерастворённый краситель;
// затем концентрация падает экспоненциально (dC/dt = -D·A·C/(h·V)).
function capsuleDailyRelease(D, { windowDiameterM, gelThicknessM, dyeG, waterMl }, days) {
  const A = Math.PI * windowDiameterM * windowDiameterM / 4;
  const V = waterMl * 1e-6; // м³
  let solidKg = Math.max(0, dyeG / 1000 - SOLUBILITY * V);
  let C = Math.min(SOLUBILITY, (dyeG / 1000) / V);
  const dt = 600; // шаг 10 мин
  const out = [];
  for (let d = 1; d <= days; d++) {
    let releasedKg = 0;
    for (let t = 0; t < DAY; t += dt) {
      const flux = D * A * C / gelThicknessM * dt; // кг за шаг
      releasedKg += flux;
      if (solidKg > 0) {
        solidKg -= flux; // растворяется твёрдый запас, C остаётся = Cs
        if (solidKg < 0) { C += solidKg / V; solidKg = 0; }
      } else {
        C -= flux / V;
      }
    }
    out.push(releasedKg * 1e6);
  }
  return out;
}

function report(title, daily) {
  const show = [1, 2, 3, 5, 7, 14, 21, 30, 45, 60];
  const perL = (mg) => mg / (CISTERN_L * FLUSHES_PER_DAY);
  const total = daily.reduce((s, x) => s + x, 0);
  const goodDays = daily.filter((mg) => perL(mg) >= 0.5 * TARGET_MG_L).length;
  console.log(`\n${title}`);
  console.log('  день | мг/сутки | мг/л в смыве');
  for (const d of show) {
    if (d <= daily.length) {
      console.log(`  ${String(d).padStart(4)} | ${daily[d - 1].toFixed(1).padStart(8)} | ${perL(daily[d - 1]).toFixed(2).padStart(6)}`);
    }
  }
  console.log(`  всего вышло за ${daily.length} дн.: ${(total / 1000).toFixed(2)} г; ` +
    `дней с цветом ≥ ${0.5 * TARGET_MG_L} мг/л: ${goodDays}`);
}

const DAYS = 60;
const needMgPerDay = TARGET_MG_L * CISTERN_L * FLUSHES_PER_DAY;
console.log(`Цель: ~${TARGET_MG_L} мг/л в смыве → ~${needMgPerDay} мг красителя в сутки, ` +
  `~${(needMgPerDay * DAYS / 1000).toFixed(1)} г за ${DAYS} дней.`);

const brick = [0.06, 0.04, 0.025]; // 6×4×2.5 см
report('A. Брикет-гидрогель 6×4×2.5 см, 5 г E133, 12 °C',
  brickDailyRelease(D_GEL_12C, brick, 5000, DAYS));
report('B. Брикет-ксерогель 6×4×2.5 см, 5 г E133, D в 10 раз меньше (оптимистично, без растрескивания)',
  brickDailyRelease(D_GEL_12C / 10, brick, 5000, DAYS));

// Рекомендуемая капсула: банка ~45 мл, 12 г E133, окно Ø14 мм с гелем толщиной 10 мм.
const capsule = { windowDiameterM: 0.014, gelThicknessM: 0.010, dyeG: 12, waterMl: 45 };
report('C. Капсула: окно Ø14 мм, гель 10 мм, 12 г E133 + 45 мл воды, 12 °C (обычный бачок)',
  capsuleDailyRelease(D_GEL_12C, capsule, DAYS));
report('C. Та же капсула при 25 °C (тёплое помещение, растворимость принята той же)',
  capsuleDailyRelease(D_GEL_25C, capsule, DAYS));
