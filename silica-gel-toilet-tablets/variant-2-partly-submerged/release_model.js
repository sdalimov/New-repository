// Вариант 2: брикет силикагеля, погружённый в воду бачка на 1/4 высоты.
// Трёхмерная модель диффузии с растворением (Фик + твёрдый запас красителя):
//   — в каждой ячейке геля хранится краситель m (кг/м³); в растворе C = min(m, Cs),
//     остальное — нерастворённые кристаллы;
//   — краситель движется только диффузией (осмос в силикагеле не работает: гель не
//     полупроницаем, а конвекцию в порах подавляет сам гель);
//   — грани ниже уровня воды отдают краситель в бачок (C = 0 на поверхности),
//     грани в воздухе (влажный закрытый бачок) — непроницаемы.
// Запуск: node release_model.js

const DAY = 86400;
const CISTERN_L = 6;
const FLUSHES_PER_DAY = 10;
const D = 2.2e-10;     // м²/с, E133 в гидрогеле SiO2 при ~12 °C
const CS = 200;        // кг/м³, растворимость E133
const DX_DEFAULT = 0.002; // шаг сетки 2 мм

// design: {x, y, z} — размеры брикета (м), submerged — погружённая высота (м),
// zones — [{from, to, dyeG}] — сколько граммов красителя заложено в слой по высоте (м, от низа).
function simulate(design, days = 60) {
  const DX = design.dx || DX_DEFAULT;
  const nx = Math.round(design.x / DX), ny = Math.round(design.y / DX), nz = Math.round(design.z / DX);
  const nWet = Math.round(design.submerged / DX);
  const idx = (i, j, k) => (k * ny + j) * nx + i;
  const m = new Float64Array(nx * ny * nz);
  const cellV = DX * DX * DX;
  for (const zone of design.zones) {
    const k0 = Math.round(zone.from / DX), k1 = Math.round(zone.to / DX);
    const per = (zone.dyeG / 1000) / ((k1 - k0) * nx * ny * cellV);
    for (let k = k0; k < k1; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) m[idx(i, j, k)] += per;
  }
  const dt = 0.9 * DX * DX / (6 * D);
  const stepsPerDay = Math.ceil(DAY / dt);
  const h = DAY / stepsPerDay;
  const g = D * h / (DX * DX);   // межъячеечный обмен
  const gb = 2 * g;              // ячейка ↔ поверхность (полшага)
  const C = new Float64Array(m.length);
  const daily = [];
  const zRelease = new Float64Array(nz); // где по высоте выходит краситель
  for (let d = 0; d < days; d++) {
    let out = 0;
    for (let s = 0; s < stepsPerDay; s++) {
      for (let n = 0; n < m.length; n++) C[n] = m[n] < CS ? m[n] : CS;
      for (let k = 0; k < nz; k++) {
        const wet = k < nWet;
        for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
          const n = idx(i, j, k), c = C[n];
          let dm = 0;
          if (i > 0) dm += g * (C[n - 1] - c);
          if (i < nx - 1) dm += g * (C[n + 1] - c);
          if (j > 0) dm += g * (C[n - nx] - c);
          if (j < ny - 1) dm += g * (C[n + nx] - c);
          if (k > 0) dm += g * (C[n - nx * ny] - c);
          if (k < nz - 1) dm += g * (C[n + nx * ny] - c);
          if (wet) {
            let faces = (i === 0) + (i === nx - 1) + (j === 0) + (j === ny - 1) + (k === 0);
            if (faces) {
              const loss = gb * c * faces;
              dm -= loss;
              out += loss * cellV;
              zRelease[k] += loss * cellV;
            }
          }
          m[n] += dm;
        }
      }
    }
    daily.push(out * 1e6); // мг
  }
  let left = 0;
  for (let n = 0; n < m.length; n++) left += m[n] * cellV;
  return { daily, leftG: left * 1000, zRelease, nWet };
}

function report(title, design) {
  const { daily, leftG } = simulate(design);
  const perL = (mg) => mg / (CISTERN_L * FLUSHES_PER_DAY);
  const total = daily.reduce((a, b) => a + b, 0);
  console.log(`\n${title}`);
  console.log('  день | мг/сутки | мг/л в смыве');
  for (const d of [1, 2, 3, 5, 7, 14, 21, 30, 45, 60]) {
    console.log(`  ${String(d).padStart(4)} | ${daily[d - 1].toFixed(1).padStart(8)} | ${perL(daily[d - 1]).toFixed(2).padStart(6)}`);
  }
  const good = daily.filter((mg) => perL(mg) >= 0.5 && perL(mg) <= 3).length;
  console.log(`  вышло ${(total / 1000).toFixed(2)} г, осталось ${leftG.toFixed(2)} г; ` +
    `дней с цветом 0.5–3 мг/л: ${good}, макс/мин за 2–60 дни: ` +
    `${(Math.max(...daily.slice(1)) / Math.min(...daily.slice(1))).toFixed(1)}×`);
}

module.exports = { simulate };

if (require.main === module) {
  const brick = { x: 0.04, y: 0.06, z: 0.10, submerged: 0.025 };
  report('2A. Брикет 6×4×10 см, погружён 2.5 см, 12 г E133 равномерно',
    { ...brick, zones: [{ from: 0, to: 0.10, dyeG: 12 }] });
  report('2B. То же, но нижняя (подводная) четверть без красителя, 12 г в верхних 7.5 см',
    { ...brick, zones: [{ from: 0.025, to: 0.10, dyeG: 12 }] });
  // Рекомендуемый: 3 см без красителя (2.5 см под водой + 0.5 см запаса), 2 см слой с 2 г,
  // 5 см верхний слой с 10 г. Надводная часть закрыта стаканом-гильзой (грани непроницаемы).
  const layered = [{ from: 0.03, to: 0.05, dyeG: 2 }, { from: 0.05, to: 0.10, dyeG: 10 }];
  report('2C. Послойный брикет в гильзе: 0–3 см пусто, 3–5 см 2 г, 5–10 см 10 г (рекомендуемый)',
    { ...brick, zones: layered });
  report('2C при заниженной воде: под водой только 1.5 см из 2.5 см «пенька»',
    { ...brick, submerged: 0.015, zones: layered });
}
