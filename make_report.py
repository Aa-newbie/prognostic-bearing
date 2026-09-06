"""
make_report.py
--------------
Generate the whole HTML report from outputs/comparison_results.json.

    page1.html   ภาพรวมโปรเจกต์
    page2.html   CNN-LSTM
    page3.html   LSTM
    page4.html   BiLSTM
    page5.html   Transformer
    page6.html   เปรียบเทียบทุกโมเดล

Every number on every page is read from the training run, so after re-running
compare_models.py just run this and the whole report stays in sync.

Usage:
    python make_report.py
"""

import os
import json

from report_config import MODEL_ORDER, COLORS, ARCH, CSS
from report_overview import OVERVIEW_BODY

RESULTS_PATH = os.path.join("outputs", "comparison_results.json")

# (filename, nav label) — built in main()
PAGES = []


# ════════════════════════════ Shell ════════════════════════════

def nav_html(active_file, accent):
    items = "".join(
        '  <a href="%s"%s>%s</a>\n' % (fn, ' class="active"' if fn == active_file else "", label)
        for fn, label in PAGES
    )
    return ('<nav style="--nav-active:%s">\n'
            '  <span class="logo">⚙️ Bearing RUL</span>\n%s</nav>') % (accent, items)


PAGE_TMPL = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>__CSS__</style>
</head>
<body>

__NAV__

<div class="hero" style="--hero-a:__HERO_A__;--hero-b:__HERO_B__">
  <div class="eyebrow">__EYEBROW__</div>
  <h1>__H1__</h1>
  <p>__SUB__</p>
</div>

<main>
__BODY__
</main>

<footer>
__FOOTER__
</footer>

<script>
__JS__
</script>

</body>
</html>
"""


def shell(filename, title, eyebrow, h1, sub, body, footer,
          accent="var(--accent1)", hero_a="var(--accent1)", hero_b="var(--accent4)", js=""):
    out = PAGE_TMPL
    for key, val in [
        ("__TITLE__", title),
        ("__CSS__", CSS),
        ("__NAV__", nav_html(filename, accent)),
        ("__HERO_A__", hero_a),
        ("__HERO_B__", hero_b),
        ("__EYEBROW__", eyebrow),
        ("__H1__", h1),
        ("__SUB__", sub),
        ("__BODY__", body),
        ("__FOOTER__", footer),
        ("__JS__", js),
    ]:
        out = out.replace(key, val)
    return out


CHART_SETUP = """
Chart.defaults.color = '#8892b0';
Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
"""


# ════════════════════════════ Helpers ════════════════════════════

def rank_badge(rank):
    return {0: "🥇", 1: "🥈", 2: "🥉"}.get(rank, "#%d" % (rank + 1))


def baseline(targets):
    """
    Naive reference: always predict the mean of the test labels.

    This is the least-squares-optimal constant predictor, so its RMSE equals the
    standard deviation of the labels. Any model has to beat it to be worth
    anything, and because the Health Index is heavily concentrated it is a much
    stronger reference than the raw RMSE suggests.
    """
    n = len(targets)
    mean_t = sum(targets) / n
    med = sorted(targets)[n // 2]
    rmse = (sum((mean_t - t) ** 2 for t in targets) / n) ** 0.5
    mae = sum(abs(mean_t - t) for t in targets) / n
    near = sum(1 for t in targets if abs(t - med) <= 0.02)
    return {"rmse": rmse, "mae": mae, "mean": mean_t,
            "concentration": near / n * 100}


def derived(r):
    """Stats not stored by the training script, computed from stored predictions."""
    preds, targets = r["test_preds"], r["test_targets"]
    n = len(targets)
    errs = sorted(abs(p - t) for p, t in zip(preds, targets))
    mean_t = sum(targets) / n
    ss_res = sum((p - t) ** 2 for p, t in zip(preds, targets))
    ss_tot = sum((t - mean_t) ** 2 for t in targets)
    hi_range = max(targets) - min(targets)
    base = baseline(targets)
    return {
        "n": n,
        "r2": 1 - ss_res / ss_tot if ss_tot > 0 else 0.0,
        "max_err": errs[-1],
        "p50": errs[n // 2],
        "p90": errs[min(n - 1, int(n * 0.90))],
        "p95": errs[min(n - 1, int(n * 0.95))],
        "bias": sum(p - t for p, t in zip(preds, targets)) / n,
        "rmse_pct": r["rmse"] / hi_range * 100 if hi_range > 0 else 0.0,
        "hi_range": hi_range,
        "base_rmse": base["rmse"],
        "base_mae": base["mae"],
        "vs_base": (base["rmse"] - r["rmse"]) / base["rmse"] * 100 if base["rmse"] > 0 else 0.0,
        "concentration": base["concentration"],
    }


def pager(prev, nxt):
    """prev / nxt are (href, label) or None."""
    left = ('<a href="%s"><div class="plbl">← ก่อนหน้า</div><div class="pname">%s</div></a>'
            % prev) if prev else '<div style="flex:1;min-width:210px"></div>'
    right = ('<a href="%s" class="next"><div class="plbl">ถัดไป →</div><div class="pname">%s</div></a>'
             % nxt) if nxt else '<div style="flex:1;min-width:210px"></div>'
    return '<section><div class="pager">%s%s</div></section>' % (left, right)


FOOTER_NOTE = ('<br><span style="font-size:0.72rem">หน้านี้สร้างอัตโนมัติจาก '
               '<code>outputs/comparison_results.json</code> ด้วย <code>make_report.py</code></span>')


# ════════════════════════════ Page 1 — Overview ════════════════════════════

def build_overview(results, order):
    by_rmse = sorted(order, key=lambda n: results[n]["rmse"])
    best = by_rmse[0]
    b = results[best]
    n_test = len(b["test_targets"])
    total_time = sum(results[n]["train_time_sec"] for n in order)

    cards = []
    for i, name in enumerate(order):
        r = results[name]
        c = COLORS[name]
        rank = by_rmse.index(name)
        page = "page%d.html" % (i + 2)
        cards.append(
            '  <a class="model-link" href="%s" style="border-color:%s33">\n'
            '    <div class="mtop"><span style="font-size:1.4rem">%s</span>'
            '<span class="mname" style="color:%s">%s</span>'
            '<span class="mrank">%s</span></div>\n'
            '    <div class="mrmse" style="color:%s">%.4f</div>\n'
            '    <div class="mlbl">RMSE บน test set</div>\n'
            '    <div class="mlbl" style="margin-top:8px">r = %.4f &nbsp;·&nbsp; %s params</div>\n'
            '    <div class="mgo" style="color:%s">ดูผลแบบละเอียด →</div>\n'
            '  </a>'
            % (page, c, ARCH[name]["icon"], c, name, rank_badge(rank), c, r["rmse"],
               r["pearson_r"], "{:,}".format(r["params"]), c)
        )
    model_cards = "\n".join(cards)

    body = OVERVIEW_BODY

    base = baseline(b["test_targets"])
    gains = [(base["rmse"] - results[n]["rmse"]) / base["rmse"] * 100 for n in order]

    body = (body
            .replace("__MODEL_CARDS__", model_cards)
            .replace("__BEST_COLOR__", COLORS[best])
            .replace("__BEST_RMSE__", "%.4f" % b["rmse"])
            .replace("__BEST_GAIN__", "%.0f" % ((base["rmse"] - b["rmse"]) / base["rmse"] * 100))
            .replace("__BEST_R__", "%.4f" % b["pearson_r"])
            .replace("__BEST__", best)
            .replace("__TOTAL_TIME__", "%.0f" % total_time)
            .replace("__CONC__", "%.0f" % base["concentration"])
            .replace("__BASERMSE__", "%.4f" % base["rmse"])
            .replace("__MINGAIN__", "%.0f" % min(gains))
            .replace("__MAXGAIN__", "%.0f" % max(gains))
            .replace("__NTEST__", str(n_test))
            .replace("__CMPPAGE__", str(len(order) + 2)))

    js = CHART_SETUP + """
const OV = __OV__;
new Chart(document.getElementById('overviewChart'), {
  type: 'bar',
  data: {
    labels: OV.names,
    datasets: [
      { label: 'RMSE', data: OV.rmse, backgroundColor: OV.colors.map(c => c + 'cc'), borderRadius: 6 },
      { label: 'MAE',  data: OV.mae,  backgroundColor: OV.colors.map(c => c + '55'), borderRadius: 6 },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    scales: { y: { beginAtZero: true, title: { display: true, text: 'Error (หน่วยของ Health Index)' } } },
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } },
      tooltip: { callbacks: { label: c => c.dataset.label + ': ' + c.parsed.y.toFixed(4) } },
    },
  },
});
""".replace("__OV__", json.dumps({
        "names": order,
        "colors": [COLORS[n] for n in order],
        "rmse": [results[n]["rmse"] for n in order],
        "mae": [results[n]["mae"] for n in order],
    }))

    footer = ('Bearing RUL Prediction &nbsp;·&nbsp; หน้า 1 จาก %d &nbsp;·&nbsp; '
              '<a href="page2.html">เริ่มดูผลรายโมเดล: %s →</a>%s'
              % (len(PAGES), order[0], FOOTER_NOTE))

    return shell(
        filename="page1.html",
        title="ภาพรวมโปรเจกต์ | Bearing RUL Prediction",
        eyebrow="Prognostics & Health Management",
        h1="ทำนายสภาพลูกปืนด้วย Deep Learning",
        sub="อ่านสัญญาณสั่นสะเทือนจากลูกปืนที่เดินจนพังจริง แล้วเรียนรู้ที่จะบอกสุขภาพที่เหลืออยู่<br>"
            "เปรียบเทียบ 4 สถาปัตยกรรมบนข้อมูลชุดเดียวกัน",
        body=body, footer=footer, js=js,
    )


# ════════════════════════════ Pages 2-5 — one per model ════════════════════════════

def build_model_page(name, results, order, page_index):
    r = results[name]
    d = derived(r)
    a = ARCH[name]
    c = COLORS[name]
    by_rmse = sorted(order, key=lambda n: results[n]["rmse"])
    rank = by_rmse.index(name)
    filename = "page%d.html" % page_index

    # layer stack
    rows = []
    for i, (lname, shape, note) in enumerate(a["layers"]):
        if i:
            rows.append('    <div class="layer-sep">↓</div>')
        rows.append(
            '    <div class="layer-row" style="border-color:%s33">\n'
            '      <span class="lname">%s</span><span class="lshape">%s</span>\n'
            '      <span class="lnote">%s</span>\n'
            '    </div>' % (c, lname, shape, note)
        )
    layer_stack = "\n".join(rows)

    pros = "".join('<li>%s</li>' % p for p in a["pros"])
    cons = "".join('<li>%s</li>' % p for p in a["cons"])

    # ranking table against the others
    rank_rows = []
    for i, n in enumerate(by_rmse):
        rr = results[n]
        here = n == name
        style = ' style="background:%s14"' % c if here else ""
        label = ('<strong style="color:%s">%s ← หน้านี้</strong>' % (c, n)) if here else \
                ('<a href="page%d.html" style="color:%s;text-decoration:none">%s</a>'
                 % (order.index(n) + 2, COLORS[n], n))
        rank_rows.append(
            '          <tr%s><td>%s</td><td>%s</td><td><strong>%.4f</strong></td>'
            '<td>%.4f</td><td>%.4f</td></tr>'
            % (style, rank_badge(i), label, rr["rmse"], rr["mae"], rr["pearson_r"])
        )
    rank_table = "\n".join(rank_rows)

    diff_note = ""
    if rank > 0:
        top = results[by_rmse[0]]
        pct = (r["rmse"] - top["rmse"]) / top["rmse"] * 100
        diff_note = ('RMSE สูงกว่าอันดับ 1 (<strong>%s</strong>) อยู่ <strong>%.1f%%</strong>'
                     % (by_rmse[0], pct))
    else:
        second = results[by_rmse[1]]
        pct = (second["rmse"] - r["rmse"]) / second["rmse"] * 100
        diff_note = ('RMSE ต่ำกว่าอันดับ 2 (<strong>%s</strong>) อยู่ <strong>%.1f%%</strong>'
                     % (by_rmse[1], pct))

    body = """
<!-- 1. สรุปผล -->
<section>
  <div class="section-title">1 &nbsp; ผลของโมเดลนี้</div>
  <div class="card" style="border-color:__C__33">
    <h3><span style="font-size:1.2em">__ICON__</span> __NAME__
      <span class="pill" style="background:__C__22;color:__C__">__TAG__</span>
      <span style="margin-left:auto;font-size:1.3rem">__BADGE__ อันดับ __RANK__ จาก __NMODELS__</span>
    </h3>
    <div class="mini-metrics">
      <div class="mini-metric"><div class="num" style="color:__C__">__RMSE__</div><div class="lbl">RMSE ↓</div></div>
      <div class="mini-metric"><div class="num" style="color:__C__">__MAE__</div><div class="lbl">MAE ↓</div></div>
      <div class="mini-metric"><div class="num" style="color:__C__">__R__</div><div class="lbl">Pearson r ↑</div></div>
      <div class="mini-metric"><div class="num" style="color:__C__">__R2__</div><div class="lbl">R² ↑</div></div>
      <div class="mini-metric"><div class="num" style="color:__C__">__PARAMS__</div><div class="lbl">Parameters</div></div>
      <div class="mini-metric"><div class="num" style="color:__C__">__EPOCHS__</div><div class="lbl">Epochs ที่เทรนจริง</div></div>
    </div>
    <div class="info-block" style="margin-top:18px;border-color:__C__33">
      <span style="color:var(--muted);font-size:0.85rem">
        วัดบน test set __NTEST__ ตัวอย่างที่โมเดลไม่เคยเห็น &nbsp;·&nbsp; __DIFF__<br>
        RMSE คิดเป็น <strong style="color:var(--text)">__RMSEPCT__%</strong> ของช่วง Health Index ทั้งหมด (__HIRANGE__)
      </span>
    </div>

    <div class="info-block orange" style="margin-top:12px">
      <strong>🧪 เทียบกับ baseline ที่ไม่ต้องเรียนรู้อะไรเลย</strong><br>
      <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
        Health Index ใน test set กระจุกตัวสูงมาก — <strong style="color:var(--text)">__CONC__%</strong>
        ของตัวอย่างอยู่ในช่วง ±0.02 รอบค่ากลาง ดังนั้นแค่
        <strong style="color:var(--text)">ทายค่าเฉลี่ยเท่ากันทุกครั้ง</strong> ก็ได้ RMSE
        <strong style="color:var(--text)">__BASERMSE__</strong> แล้ว<br>
        โมเดลนี้ทำได้ <strong style="color:__C__">__RMSE__</strong> —
        ดีกว่า baseline อยู่ <strong style="color:__C__">__VSBASE__%</strong>
        <span style="opacity:0.8">(ตรงกับค่า R² = __R2__)</span><br>
        <span style="font-size:0.95em;opacity:0.85">
          ตัวเลข RMSE ที่ดูน้อยมากจึงต้องอ่านคู่กับบรรทัดนี้เสมอ ไม่ใช่อ่านลอย ๆ
        </span>
      </span>
    </div>
  </div>
</section>

<!-- 2. สถาปัตยกรรม -->
<section>
  <div class="section-title">2 &nbsp; สถาปัตยกรรม</div>
  <div class="row-2">
    <div class="card">
      <h3>🧱 โครงสร้างทีละชั้น</h3>
      <div class="layer-stack">
__LAYERS__
      </div>
    </div>
    <div class="card">
      <h3>💡 แนวคิดเบื้องหลัง</h3>
      <p style="color:var(--muted);font-size:0.87rem;line-height:1.95">__IDEA__</p>

      <div class="info-block green" style="margin-top:18px">
        <strong>✅ ข้อดี</strong>
        <ul style="color:var(--muted);font-size:0.83rem;padding-left:20px;line-height:1.9;margin-top:6px">__PROS__</ul>
      </div>
      <div class="info-block orange" style="margin-top:12px">
        <strong>⚠️ ข้อจำกัด</strong>
        <ul style="color:var(--muted);font-size:0.83rem;padding-left:20px;line-height:1.9;margin-top:6px">__CONS__</ul>
      </div>
    </div>
  </div>
</section>

<!-- 3. การเทรน -->
<section>
  <div class="section-title">3 &nbsp; การเทรน</div>
  <div class="row-2">
    <div class="card">
      <h3>📉 Loss ต่อ epoch</h3>
      <div class="chart-box"><canvas id="lossChart"></canvas></div>
      <div class="info-block" style="margin-top:14px;padding:12px 16px;border-color:__C__33">
        <span style="color:var(--muted);font-size:0.8rem">
          แกน Y เป็น log scale — ถ้าเส้น train ลงเรื่อย ๆ แต่ val เริ่มเชิดขึ้น แปลว่าเริ่ม overfit
        </span>
      </div>
    </div>
    <div class="card">
      <h3>⚙️ รายละเอียดการเทรน</h3>
      <table>
        <thead><tr><th>รายการ</th><th>ค่า</th></tr></thead>
        <tbody>
          <tr><td>Epochs ที่เทรนจริง</td><td><strong>__EPOCHS__</strong> (สูงสุด 100)</td></tr>
          <tr><td>หยุดด้วย Early stopping</td><td><strong>__EARLY__</strong></td></tr>
          <tr><td>Val loss ต่ำสุด</td><td><strong>__BESTVAL__</strong></td></tr>
          <tr><td>เวลาเทรนรวม</td><td><strong>__TIME__ วินาที</strong></td></tr>
          <tr><td>เวลาต่อ epoch</td><td><strong>__SPE__ วินาที</strong></td></tr>
          <tr><td>จำนวนพารามิเตอร์</td><td><strong>__PARAMSFULL__</strong></td></tr>
          <tr><td>Loss function</td><td>MSE</td></tr>
          <tr><td>Optimizer</td><td>AdamW (lr 5e-4, wd 1e-4)</td></tr>
          <tr><td>LR schedule</td><td>CosineAnnealing → 1e-5</td></tr>
          <tr><td>Gradient clipping</td><td>max_norm = 1.0</td></tr>
        </tbody>
      </table>
      <div class="info-block purple" style="margin-top:14px">
        <span style="color:var(--muted);font-size:0.82rem">
          เก็บ checkpoint ที่ <strong style="color:var(--text)">val loss ต่ำสุด</strong> แล้วโหลดกลับมาวัดผลบน test set
          → ตัวเลข test ไม่เคยถูกใช้เลือกโมเดล
        </span>
      </div>
    </div>
  </div>
</section>

<!-- 4. ผลทำนาย -->
<section>
  <div class="section-title">4 &nbsp; ผลการทำนายบน Test Set</div>
  <div class="card">
    <h3>📈 ค่าจริง vs ค่าที่ทำนาย</h3>
    <div class="chart-box tall"><canvas id="lineChart"></canvas></div>
    <div class="info-block" style="margin-top:14px;padding:12px 16px;border-color:__C__33">
      <span style="color:var(--muted);font-size:0.8rem">
        เรียงตัวอย่างตามค่า Health Index จริงจากมากไปน้อย (เพราะ test set ถูกสุ่มลำดับ)
        เส้นทำนายยิ่งทาบเส้นจริงยิ่งดี
      </span>
    </div>
  </div>

  <div class="row-2" style="margin-top:20px">
    <div class="card">
      <h3>🎯 Scatter: จริง vs ทำนาย</h3>
      <div class="chart-box"><canvas id="scatterChart"></canvas></div>
    </div>
    <div class="card">
      <h3>📊 การกระจายของ Error</h3>
      <div class="chart-box"><canvas id="histChart"></canvas></div>
    </div>
  </div>

  <div class="card" style="margin-top:20px">
    <h3>🔎 ดู error ละเอียด</h3>
    <div class="row-2">
      <table>
        <thead><tr><th>สถิติของ |error|</th><th>ค่า</th><th>ความหมาย</th></tr></thead>
        <tbody>
          <tr><td>Median (P50)</td><td><strong>__P50__</strong></td><td>ครึ่งหนึ่งของตัวอย่างพลาดน้อยกว่านี้</td></tr>
          <tr><td>P90</td><td><strong>__P90__</strong></td><td>90% พลาดน้อยกว่านี้</td></tr>
          <tr><td>P95</td><td><strong>__P95__</strong></td><td>95% พลาดน้อยกว่านี้</td></tr>
          <tr><td>Max</td><td><strong>__MAXERR__</strong></td><td>ตัวอย่างที่พลาดหนักที่สุด</td></tr>
          <tr><td>Bias เฉลี่ย</td><td><strong>__BIAS__</strong></td><td>__BIASNOTE__</td></tr>
        </tbody>
      </table>
      <div>
        <div class="info-block green">
          <strong>อ่านยังไง</strong><br>
          <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
            ถ้า <strong style="color:var(--text)">RMSE (__RMSE__)</strong> สูงกว่า
            <strong style="color:var(--text)">MAE (__MAE__)</strong> มาก
            แปลว่ามีตัวอย่างส่วนน้อยที่พลาดหนักและดึงค่าเฉลี่ยขึ้น —
            ดูได้จากหางขวาของกราฟการกระจาย error
          </span>
        </div>
        <div class="info-block purple" style="margin-top:12px">
          <strong>Bias บอกอะไร</strong><br>
          <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
            ค่าบวก = โมเดลมองโลกในแง่ดีเกินจริง (ทำนายว่าสุขภาพดีกว่าความเป็นจริง)
            ซึ่งอันตรายกว่าในงานบำรุงรักษา เพราะอาจพลาดสัญญาณเตือน
          </span>
        </div>
      </div>
    </div>
  </div>

  <div class="img-card" style="margin-top:20px">
    <div class="img-card-header" style="color:__C__">🖼️ กราฟจากสคริปต์เทรน (matplotlib)</div>
    <img src="outputs/__NAME___prediction.png" alt="__NAME__ prediction" onerror="this.parentElement.style.display='none'">
    <div class="img-card-footer">ลำดับตามดัชนีเดิมของ test set — RMSE __RMSE__ &nbsp;·&nbsp; MAE __MAE__ &nbsp;·&nbsp; r __R__</div>
  </div>
</section>

<!-- 5. เทียบกับโมเดลอื่น -->
<section>
  <div class="section-title">5 &nbsp; ยืนอยู่ตรงไหนเทียบกับโมเดลอื่น</div>
  <div class="card">
    <h3>🏁 อันดับทั้งหมด</h3>
    <table>
      <thead><tr><th>อันดับ</th><th>Model</th><th>RMSE ↓</th><th>MAE ↓</th><th>Pearson r ↑</th></tr></thead>
      <tbody>
__RANKTABLE__
      </tbody>
    </table>
    <div class="info-block" style="margin-top:16px;border-color:__C__33">
      <span style="color:var(--muted);font-size:0.84rem">__DIFF__ &nbsp;·&nbsp;
        <a href="page__CMPPAGE__.html" style="color:__C__;text-decoration:none">ดูหน้าเปรียบเทียบเต็ม →</a>
      </span>
    </div>
  </div>
</section>
"""

    early = "ใช่ (val loss ไม่ดีขึ้นติดกัน 15 epoch)" if r["epochs_trained"] < 100 else "ไม่ (ครบ 100 epoch)"
    bias_note = ("ทำนายสูงกว่าค่าจริงโดยเฉลี่ย" if d["bias"] > 0
                 else "ทำนายต่ำกว่าค่าจริงโดยเฉลี่ย")

    for key, val in [
        ("__LAYERS__", layer_stack),
        ("__RANKTABLE__", rank_table),
        ("__ICON__", a["icon"]),
        ("__TAG__", a["tag"]),
        ("__IDEA__", a["idea"]),
        ("__PROS__", pros),
        ("__CONS__", cons),
        ("__BADGE__", rank_badge(rank)),
        ("__RANK__", str(rank + 1)),
        ("__NMODELS__", str(len(order))),
        ("__RMSEPCT__", "%.1f" % d["rmse_pct"]),
        ("__HIRANGE__", "%.3f" % d["hi_range"]),
        ("__CONC__", "%.0f" % d["concentration"]),
        ("__BASERMSE__", "%.4f" % d["base_rmse"]),
        ("__VSBASE__", "%.0f" % d["vs_base"]),
        ("__RMSE__", "%.4f" % r["rmse"]),
        ("__MAE__", "%.4f" % r["mae"]),
        ("__R2__", "%.4f" % d["r2"]),
        ("__R__", "%.4f" % r["pearson_r"]),
        ("__PARAMSFULL__", "{:,}".format(r["params"])),
        ("__PARAMS__", "%.0fK" % (r["params"] / 1000)),
        ("__EPOCHS__", str(r["epochs_trained"])),
        ("__EARLY__", early),
        ("__BESTVAL__", "%.6f" % r["best_val_loss"]),
        ("__TIME__", "%.1f" % r["train_time_sec"]),
        ("__SPE__", "%.2f" % r["sec_per_epoch"]),
        ("__NTEST__", str(d["n"])),
        ("__DIFF__", diff_note),
        ("__P50__", "%.4f" % d["p50"]),
        ("__P90__", "%.4f" % d["p90"]),
        ("__P95__", "%.4f" % d["p95"]),
        ("__MAXERR__", "%.4f" % d["max_err"]),
        ("__BIASNOTE__", bias_note),
        ("__BIAS__", "%+.5f" % d["bias"]),
        ("__CMPPAGE__", str(len(order) + 2)),
        ("__NAME__", name),
        ("__C__", c),
    ]:
        body = body.replace(key, val)

    js = CHART_SETUP + """
const M = __M__;
const idx = M.targets.map((t, i) => i).sort((a, b) => M.targets[b] - M.targets[a]);

new Chart(document.getElementById('lossChart'), {
  type: 'line',
  data: {
    labels: M.train.map((_, i) => i + 1),
    datasets: [
      { label: 'Train loss', data: M.train, borderColor: '#8892b0', borderWidth: 2, pointRadius: 0, tension: 0.25 },
      { label: 'Val loss',   data: M.val,   borderColor: M.color,  borderWidth: 2.4, pointRadius: 0, tension: 0.25 },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    scales: {
      y: { type: 'logarithmic', title: { display: true, text: 'MSE Loss (log)' } },
      x: { title: { display: true, text: 'Epoch' }, ticks: { maxTicksLimit: 12 } },
    },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } } },
  },
});

new Chart(document.getElementById('lineChart'), {
  type: 'line',
  data: {
    labels: idx.map((_, i) => i + 1),
    datasets: [
      { label: 'Health Index จริง', data: idx.map(i => M.targets[i]),
        borderColor: '#e8eaf6', borderWidth: 2.4, pointRadius: 0, tension: 0.1 },
      { label: 'ทำนายโดย ' + M.name, data: idx.map(i => M.preds[i]),
        borderColor: M.color, backgroundColor: M.color + '22',
        borderWidth: 1.6, pointRadius: 1.5, tension: 0.1, fill: true },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    scales: {
      y: { title: { display: true, text: 'Health Index' } },
      x: { title: { display: true, text: 'ตัวอย่างใน test set (เรียงตามค่าจริง มาก → น้อย)' },
           ticks: { maxTicksLimit: 15 } },
    },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } } },
  },
});

const lo = Math.min(...M.targets), hi = Math.max(...M.targets);
new Chart(document.getElementById('scatterChart'), {
  type: 'scatter',
  data: {
    datasets: [
      { label: M.name, data: M.targets.map((t, i) => ({ x: t, y: M.preds[i] })),
        backgroundColor: M.color + 'aa', pointRadius: 3.5 },
      { label: 'ทำนายสมบูรณ์แบบ', type: 'line',
        data: [{ x: lo, y: lo }, { x: hi, y: hi }],
        borderColor: '#8892b0', borderWidth: 1.5, borderDash: [6, 4], pointRadius: 0, fill: false },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: 'Health Index จริง' } },
      y: { title: { display: true, text: 'Health Index ที่ทำนาย' } },
    },
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } },
      tooltip: { callbacks: { label: c => 'จริง ' + c.parsed.x.toFixed(4) + ' → ทำนาย ' + c.parsed.y.toFixed(4) } },
    },
  },
});

const errs = M.targets.map((t, i) => Math.abs(M.preds[i] - t));
const maxE = Math.max(...errs), NB = 20;
const bins = new Array(NB).fill(0);
errs.forEach(e => { bins[Math.min(NB - 1, Math.floor(e / maxE * NB))]++; });
new Chart(document.getElementById('histChart'), {
  type: 'bar',
  data: {
    labels: bins.map((_, i) => (maxE / NB * i).toFixed(3)),
    datasets: [{ label: 'จำนวนตัวอย่าง', data: bins, backgroundColor: M.color + 'bb', borderRadius: 3 }],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    scales: {
      y: { beginAtZero: true, title: { display: true, text: 'จำนวนตัวอย่าง' } },
      x: { title: { display: true, text: '|error| (absolute error)' }, ticks: { maxTicksLimit: 10 } },
    },
    plugins: { legend: { display: false } },
  },
});
""".replace("__M__", json.dumps({
        "name": name,
        "color": c,
        "train": r["train_loss_history"],
        "val": r["val_loss_history"],
        "preds": r["test_preds"],
        "targets": r["test_targets"],
    }))

    prev = ("page1.html", "ภาพรวมโปรเจกต์") if page_index == 2 else \
           ("page%d.html" % (page_index - 1), order[page_index - 3])
    nxt = ("page%d.html" % (page_index + 1),
           order[page_index - 1] if page_index - 1 < len(order) else "เปรียบเทียบทุกโมเดล")

    body += "\n" + pager(prev, nxt)

    footer = ('Bearing RUL Prediction &nbsp;·&nbsp; หน้า %d จาก %d &nbsp;·&nbsp; %s%s'
              % (page_index, len(PAGES), name, FOOTER_NOTE))

    return filename, shell(
        filename=filename,
        title="%s | Bearing RUL Prediction" % name,
        eyebrow="โมเดลที่ %d จาก %d — %s" % (order.index(name) + 1, len(order), a["tag"]),
        h1="%s %s" % (a["icon"], name),
        sub=a["idea"],
        body=body, footer=footer, js=js,
        accent=c, hero_a=c, hero_b="var(--accent2)",
    )


# ════════════════════════════ Last page — comparison ════════════════════════════

def build_comparison(results, order, page_index):
    filename = "page%d.html" % page_index
    by_rmse = sorted(order, key=lambda n: results[n]["rmse"])
    best, worst = by_rmse[0], by_rmse[-1]
    b = results[best]
    gap = (results[worst]["rmse"] - b["rmse"]) / results[worst]["rmse"] * 100

    rows = []
    for i, n in enumerate(by_rmse):
        r = results[n]
        d = derived(r)
        style = ' style="background:rgba(74,222,128,0.07)"' if i == 0 else ""
        rows.append(
            '          <tr%s>\n'
            '            <td>%s</td>\n'
            '            <td><a href="page%d.html" style="color:%s;font-weight:700;text-decoration:none">%s →</a></td>\n'
            '            <td><strong>%.4f</strong></td><td>%.4f</td><td>%.4f</td><td>%.4f</td>\n'
            '            <td>%s</td><td>%d</td><td>%.0fs</td>\n'
            '          </tr>'
            % (style, rank_badge(i), order.index(n) + 2, COLORS[n], n,
               r["rmse"], r["mae"], r["pearson_r"], d["r2"],
               "{:,}".format(r["params"]), r["epochs_trained"], r["train_time_sec"])
        )
    table_rows = "\n".join(rows)

    body = """
<!-- 1. ผู้ชนะ -->
<section>
  <div class="section-title">1 &nbsp; สรุปผลการแข่ง</div>
  <div class="winner">
    <div class="trophy">🏆</div>
    <div style="flex:1;min-width:250px">
      <div style="font-size:1.5rem;font-weight:800;color:__BESTC__">__BEST__</div>
      <div style="color:var(--muted);font-size:0.86rem">
        RMSE ต่ำสุดที่ <strong style="color:var(--good)">__BESTRMSE__</strong>
        — ดีกว่าโมเดลอันดับสุดท้าย (__WORST__) อยู่ <strong style="color:var(--good)">__GAP__%</strong>
      </div>
      <div style="margin-top:8px">
        <a href="page__BESTPAGE__.html" style="color:__BESTC__;text-decoration:none;font-size:0.83rem;font-weight:600">
          ดูผลของ __BEST__ แบบละเอียด →
        </a>
      </div>
    </div>
    <div class="mini-metrics" style="flex:2;min-width:320px">
      <div class="mini-metric"><div class="num" style="color:var(--good)">__BESTRMSE__</div><div class="lbl">RMSE</div></div>
      <div class="mini-metric"><div class="num" style="color:var(--good)">__BESTMAE__</div><div class="lbl">MAE</div></div>
      <div class="mini-metric"><div class="num" style="color:var(--good)">__BESTR__</div><div class="lbl">Pearson r</div></div>
      <div class="mini-metric"><div class="num" style="color:var(--good)">__BESTEP__</div><div class="lbl">Epochs</div></div>
    </div>
  </div>
</section>

<!-- 2. ควบคุมตัวแปร -->
<section>
  <div class="section-title">2 &nbsp; เงื่อนไขที่ควบคุมให้เท่ากัน</div>
  <div class="row-2">
    <div class="card">
      <h3>⚖️ ตัวแปรที่ล็อกไว้เหมือนกันทุกโมเดล</h3>
      <div class="info-block">
        <span style="font-size:0.85rem;line-height:2.05">
          ✅ <strong>ข้อมูลชุดเดียวกัน</strong> — train/val/test split เดียว (seed = 42)<br>
          ✅ <strong>Label เดียวกัน</strong> — Health Index (rolling window = 7)<br>
          ✅ <strong>Scaler เดียวกัน</strong> — fit บน train windows เท่านั้น<br>
          ✅ <strong>Input เดียวกัน</strong> — (B, 20, 56)<br>
          ✅ <strong>Output เดียวกัน</strong> — Sigmoid → HI ∈ (0, 1)<br>
          ✅ <strong>Seed เดียวกัน</strong> — reset ก่อนสร้างทุกโมเดล<br>
          ✅ <strong>Training recipe เดียวกัน</strong> — MSE + AdamW + Cosine + early stopping
        </span>
      </div>
      <div class="info-block orange" style="margin-top:12px">
        <span style="color:var(--muted);font-size:0.82rem">
          <strong style="color:var(--text)">สิ่งเดียวที่ต่างกันคือสถาปัตยกรรม</strong>
          ผลที่ออกมาจึงเทียบกันได้ตรง ๆ
        </span>
      </div>
    </div>
    <div class="card">
      <h3>⚙️ Hyperparameters</h3>
      <table>
        <thead><tr><th>พารามิเตอร์</th><th>ค่า</th><th>เหตุผล</th></tr></thead>
        <tbody>
          <tr><td>Loss</td><td><strong>MSE</strong></td><td>ปัญหา regression ค่าต่อเนื่อง</td></tr>
          <tr><td>Optimizer</td><td><strong>AdamW</strong></td><td>weight decay แยกจาก gradient</td></tr>
          <tr><td>Learning rate</td><td><strong>5e-4</strong></td><td>เสถียรกับ LSTM</td></tr>
          <tr><td>LR schedule</td><td><strong>Cosine</strong></td><td>ลดถึง 1e-5 ตอนท้าย</td></tr>
          <tr><td>Weight decay</td><td><strong>1e-4</strong></td><td>กัน overfit</td></tr>
          <tr><td>Grad clipping</td><td><strong>1.0</strong></td><td>กัน exploding gradient</td></tr>
          <tr><td>Batch size</td><td><strong>32</strong></td><td>สมดุลกับ 675 train windows</td></tr>
          <tr><td>Max epochs</td><td><strong>100</strong></td><td>คู่กับ early stopping</td></tr>
          <tr><td>Early stopping</td><td><strong>patience 15</strong></td><td>หยุดเมื่อ val loss ไม่ดีขึ้น</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- 3. leaderboard -->
<section>
  <div class="section-title">3 &nbsp; ตารางผลรวม</div>
  <div class="card">
    <h3>📋 Leaderboard — เรียงตาม RMSE (น้อย = ดี)</h3>
    <table>
      <thead>
        <tr><th>อันดับ</th><th>Model</th><th>RMSE ↓</th><th>MAE ↓</th>
            <th>Pearson r ↑</th><th>R² ↑</th><th>Params</th><th>Epochs</th><th>เวลาเทรน</th></tr>
      </thead>
      <tbody>
__TABLEROWS__
      </tbody>
    </table>
    <div class="info-block purple" style="margin-top:18px">
      <strong>📖 อ่านค่ายังไง</strong><br>
      <span style="color:var(--muted);font-size:0.82rem;line-height:1.9">
        <strong style="color:var(--text)">RMSE / MAE</strong> — ค่าคลาดเคลื่อนเฉลี่ยบนสเกลของ Health Index ยิ่งน้อยยิ่งดี<br>
        <strong style="color:var(--text)">Pearson r</strong> — ทิศทางของ predicted กับ actual ไปด้วยกันแค่ไหน ใกล้ 1 ยิ่งดี<br>
        <strong style="color:var(--text)">R²</strong> — โมเดลอธิบายความแปรปรวนของ Health Index ได้กี่ %<br>
        <strong style="color:var(--text)">Epochs</strong> — จำนวนรอบที่เทรนจริงก่อน early stopping จะตัด
      </span>
    </div>
  </div>
</section>

<!-- 3b. sanity check -->
<section>
  <div class="section-title">4 &nbsp; Sanity check — ตัวเลขนี้ดีจริงหรือแค่ดูดี</div>
  <div class="card" style="border-color:rgba(249,115,22,0.35)">
    <h3>🧪 เทียบกับ baseline ที่ไม่ต้องเรียนรู้อะไรเลย</h3>
    <p style="color:var(--muted);font-size:0.88rem;line-height:1.9">
      RMSE ระดับ 0.00x ดูน่าประทับใจ แต่ต้องดูก่อนว่า
      <strong style="color:var(--text)">ค่าที่ต้องทายมันกระจายกว้างแค่ไหน</strong> —
      ใน test set ชุดนี้ <strong style="color:var(--accent3)">__CONC__%</strong>
      ของตัวอย่างมี Health Index อยู่ในช่วง ±0.02 รอบค่ากลาง
      แปลว่าแค่ทายค่าเดิมทุกครั้งก็ได้คะแนนไม่เลวแล้ว
      จึงต้องเทียบกับ baseline เพื่อดูว่าโมเดลเรียนรู้อะไรเพิ่มขึ้นมาจริง
    </p>

    <table style="margin-top:16px">
      <thead>
        <tr><th>วิธีทำนาย</th><th>RMSE ↓</th><th>MAE ↓</th><th>ดีกว่า baseline</th></tr>
      </thead>
      <tbody>
        <tr style="background:rgba(249,115,22,0.07)">
          <td><strong style="color:var(--accent3)">Baseline — ทายค่าเฉลี่ยเสมอ</strong></td>
          <td><strong>__BASERMSE__</strong></td>
          <td>__BASEMAE__</td>
          <td style="color:var(--muted)">—</td>
        </tr>
__BASEROWS__
      </tbody>
    </table>

    <div class="info-block green" style="margin-top:18px">
      <strong>✅ สรุป</strong><br>
      <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
        ทุกโมเดลชนะ baseline อย่างชัดเจน (ดีขึ้น __MINGAIN__–__MAXGAIN__%)
        แปลว่าโมเดลจับสัญญาณการเสื่อมได้จริง ไม่ได้แค่ทายค่ากลาง<br>
        แต่ตัวเลข RMSE ดิบ <strong style="color:var(--text)">ไม่ควรนำไปเทียบกับงานวิจัยอื่นตรง ๆ</strong>
        เพราะสเกลของ label ต่างกัน — ควรอ้างอิง R² หรือ % ที่ดีกว่า baseline แทน
      </span>
    </div>
  </div>
</section>

<!-- 4. กราฟ -->
<section>
  <div class="section-title">5 &nbsp; กราฟเปรียบเทียบ</div>
  <div class="row-2">
    <div class="card">
      <h3>📉 Validation loss ทุกโมเดล</h3>
      <div class="chart-box"><canvas id="lossChart"></canvas></div>
      <div class="info-block" style="margin-top:14px;padding:12px 16px">
        <span style="color:var(--muted);font-size:0.8rem">
          เส้นที่ลงต่ำและนิ่งเร็ว = ลู่เข้าได้ดี — ความยาวเส้นต่างกันเพราะ early stopping ตัดคนละ epoch
        </span>
      </div>
    </div>
    <div class="card">
      <h3>📊 RMSE เทียบ MAE</h3>
      <div class="chart-box"><canvas id="barChart"></canvas></div>
      <div class="info-block" style="margin-top:14px;padding:12px 16px">
        <span style="color:var(--muted);font-size:0.8rem">
          RMSE ลงโทษ error ก้อนใหญ่หนักกว่า MAE — ถ้าสองค่าห่างกันมาก แปลว่ามีตัวอย่างที่พลาดหนักอยู่
        </span>
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:20px">
    <h3>🎯 Predicted vs Actual ทุกโมเดลซ้อนกัน</h3>
    <div class="chart-box tall"><canvas id="scatterChart"></canvas></div>
    <div class="info-block green" style="margin-top:14px;padding:12px 16px">
      <span style="color:var(--muted);font-size:0.8rem">
        เส้นประคือการทำนายที่สมบูรณ์แบบ — คลิกชื่อโมเดลใน legend เพื่อซ่อน/แสดงทีละตัว
      </span>
    </div>
  </div>

  <div class="img-card" style="margin-top:20px">
    <div class="img-card-header">🖼️ ทุกโมเดลบนแกนเวลาเดียวกัน</div>
    <img src="outputs/all_models_prediction.png" alt="All models" onerror="this.parentElement.style.display='none'">
    <div class="img-card-footer">เส้นดำคือ Health Index จริง เส้นสีคือค่าที่แต่ละโมเดลทำนาย</div>
  </div>
</section>

<!-- 5. วิเคราะห์ -->
<section>
  <div class="section-title">6 &nbsp; วิเคราะห์ผล</div>
  <div class="row-2">
    <div class="card">
      <h3>🔍 อ่านผลได้ว่าอย่างไร</h3>
      <div class="info-block green">
        <strong>1. ขนาดโมเดลไม่ได้ตัดสินผล</strong><br>
        <span style="color:var(--muted);font-size:0.83rem">
          โมเดลที่พารามิเตอร์มากที่สุดไม่ได้ชนะ — บนข้อมูลขนาดนี้ (675 train windows)
          โมเดลใหญ่มีแนวโน้ม overfit มากกว่าจะได้เปรียบ
        </span>
      </div>
      <div class="info-block" style="margin-top:12px">
        <strong>2. Temporal resolution สำคัญ</strong><br>
        <span style="color:var(--muted);font-size:0.83rem">
          สถาปัตยกรรมที่เก็บครบทั้ง 20 timestep ทำได้ดีกว่าตัวที่ pooling จนเหลือ 5 timestep
          เพราะการเสื่อมของลูกปืนอยู่ในรายละเอียดของแนวโน้ม ไม่ใช่ค่าเฉลี่ยหยาบ ๆ
        </span>
      </div>
      <div class="info-block purple" style="margin-top:12px">
        <strong>3. Transformer ยังไม่ได้เปรียบที่สเกลนี้</strong><br>
        <span style="color:var(--muted);font-size:0.83rem">
          sequence ยาวแค่ 20 step และข้อมูลเทรนไม่ถึงพันตัวอย่าง ซึ่งน้อยเกินกว่าที่ self-attention
          จะแสดงข้อได้เปรียบเหนือ RNN
        </span>
      </div>
    </div>
    <div class="card">
      <h3>⚠️ ข้อจำกัดของการทดลอง</h3>
      <div class="info-block pink">
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.95">
          <strong style="color:var(--text)">1. Label สร้างขึ้นเอง</strong><br>
          Health Index คำนวณจาก feature ชุดเดียวกับที่ป้อนเข้าโมเดล ตัวเลขจึงสูงกว่างานที่มี ground-truth RUL จริง<br><br>
          <strong style="color:var(--text)">2. หน้าต่างซ้อนทับกัน</strong><br>
          window ที่ติดกันใช้ข้อมูลร่วมกัน เมื่อ shuffle แล้วแบ่ง test set จึงไม่เป็นอิสระจาก train เต็มที่<br><br>
          <strong style="color:var(--text)">3. รันครั้งเดียวต่อโมเดล</strong><br>
          ยังไม่ได้ทำ multi-seed เพื่อดูว่าความต่างที่เห็นเกินความผันผวนจากการสุ่มหรือไม่<br><br>
          <strong style="color:var(--text)">4. BiLSTM ใช้ข้อมูลอนาคต</strong><br>
          เหมาะกับการวิเคราะห์ย้อนหลัง ไม่ใช่การทำนายแบบ real-time
        </span>
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:20px">
    <h3>🚀 ขั้นต่อไป</h3>
    <div class="row-3">
      <div class="info-block">
        <strong>รันหลาย seed</strong><br>
        <span style="color:var(--muted);font-size:0.8rem">
          เทรนซ้ำ 5 seed แล้วรายงานค่าเฉลี่ย ± ส่วนเบี่ยงเบน เพื่อยืนยันว่าอันดับไม่ได้มาจากความบังเอิญ
        </span>
      </div>
      <div class="info-block orange">
        <strong>ทดสอบข้าม dataset</strong><br>
        <span style="color:var(--muted);font-size:0.8rem">
          เทรนบน 2nd_test แล้ววัดผลบน 1st/3rd_test เพื่อดู generalization จริง
        </span>
      </div>
      <div class="info-block purple">
        <strong>Sequential split</strong><br>
        <span style="color:var(--muted);font-size:0.8rem">
          แบ่งตามเวลาแทน shuffle เพื่อจำลองสถานการณ์ทำนายอนาคตจริง
        </span>
      </div>
    </div>
  </div>
</section>
"""

    # Baseline comparison: how much better than always predicting the mean
    base = baseline(b["test_targets"])
    base_rows = []
    for n in by_rmse:
        r = results[n]
        gain = (base["rmse"] - r["rmse"]) / base["rmse"] * 100
        base_rows.append(
            '        <tr><td style="color:%s;font-weight:700">%s</td>'
            '<td><strong>%.4f</strong></td><td>%.4f</td>'
            '<td style="color:var(--good);font-weight:700">-%.0f%%</td></tr>'
            % (COLORS[n], n, r["rmse"], r["mae"], gain)
        )
    gains = [(base["rmse"] - results[n]["rmse"]) / base["rmse"] * 100 for n in order]

    for key, val in [
        ("__TABLEROWS__", table_rows),
        ("__BASEROWS__", "\n".join(base_rows)),
        ("__BASERMSE__", "%.4f" % base["rmse"]),
        ("__BASEMAE__", "%.4f" % base["mae"]),
        ("__CONC__", "%.0f" % base["concentration"]),
        ("__MINGAIN__", "%.0f" % min(gains)),
        ("__MAXGAIN__", "%.0f" % max(gains)),
        ("__BESTC__", COLORS[best]),
        ("__BESTRMSE__", "%.4f" % b["rmse"]),
        ("__BESTMAE__", "%.4f" % b["mae"]),
        ("__BESTR__", "%.4f" % b["pearson_r"]),
        ("__BESTEP__", str(b["epochs_trained"])),
        ("__BESTPAGE__", str(order.index(best) + 2)),
        ("__BEST__", best),
        ("__WORST__", worst),
        ("__GAP__", "%.1f" % gap),
    ]:
        body = body.replace(key, val)

    body += "\n" + pager(("page%d.html" % (page_index - 1), order[-1]), ("page1.html", "กลับหน้าภาพรวม"))

    js = CHART_SETUP + """
const D = __D__;

new Chart(document.getElementById('lossChart'), {
  type: 'line',
  data: {
    labels: Array.from({ length: Math.max(...D.names.map(n => D.val[n].length)) }, (_, i) => i + 1),
    datasets: D.names.map(n => ({
      label: n, data: D.val[n], borderColor: D.colors[n],
      borderWidth: 2, pointRadius: 0, tension: 0.25,
    })),
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    scales: {
      y: { type: 'logarithmic', title: { display: true, text: 'Val loss (MSE, log)' } },
      x: { title: { display: true, text: 'Epoch' }, ticks: { maxTicksLimit: 12 } },
    },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } } },
  },
});

new Chart(document.getElementById('barChart'), {
  type: 'bar',
  data: {
    labels: D.names,
    datasets: [
      { label: 'RMSE', data: D.names.map(n => D.rmse[n]),
        backgroundColor: D.names.map(n => D.colors[n] + 'cc'), borderRadius: 6 },
      { label: 'MAE', data: D.names.map(n => D.mae[n]),
        backgroundColor: D.names.map(n => D.colors[n] + '55'), borderRadius: 6 },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    scales: { y: { beginAtZero: true, title: { display: true, text: 'Error (หน่วยของ Health Index)' } } },
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } },
      tooltip: { callbacks: { label: c => c.dataset.label + ': ' + c.parsed.y.toFixed(4) } },
    },
  },
});

const lo = Math.min(...D.targets), hi = Math.max(...D.targets);
new Chart(document.getElementById('scatterChart'), {
  type: 'scatter',
  data: {
    datasets: [
      ...D.names.map(n => ({
        label: n, data: D.targets.map((t, i) => ({ x: t, y: D.preds[n][i] })),
        backgroundColor: D.colors[n] + 'aa', pointRadius: 3,
      })),
      { label: 'ทำนายสมบูรณ์แบบ', type: 'line',
        data: [{ x: lo, y: lo }, { x: hi, y: hi }],
        borderColor: '#8892b0', borderWidth: 1.5, borderDash: [6, 4], pointRadius: 0, fill: false },
    ],
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: 'Health Index จริง' } },
      y: { title: { display: true, text: 'Health Index ที่ทำนาย' } },
    },
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 12, usePointStyle: true } },
      tooltip: { callbacks: { label: c => c.dataset.label + ': จริง ' + c.parsed.x.toFixed(4) + ' → ทำนาย ' + c.parsed.y.toFixed(4) } },
    },
  },
});
""".replace("__D__", json.dumps({
        "names": order,
        "colors": {n: COLORS[n] for n in order},
        "val": {n: results[n]["val_loss_history"] for n in order},
        "rmse": {n: results[n]["rmse"] for n in order},
        "mae": {n: results[n]["mae"] for n in order},
        "preds": {n: results[n]["test_preds"] for n in order},
        "targets": results[best]["test_targets"],
    }))

    footer = ('Bearing RUL Prediction &nbsp;·&nbsp; หน้า %d จาก %d &nbsp;·&nbsp; '
              '<a href="page1.html">← กลับหน้าภาพรวม</a>%s' % (page_index, len(PAGES), FOOTER_NOTE))

    return filename, shell(
        filename=filename,
        title="เปรียบเทียบทุกโมเดล | Bearing RUL Prediction",
        eyebrow="หน้าสุดท้าย — สรุปการแข่งขัน",
        h1="เปรียบเทียบทุกโมเดล",
        sub="วางผลของทั้ง %d สถาปัตยกรรมไว้บนกราฟและตารางเดียวกัน<br>"
            "เพื่อดูว่าอะไรทำให้โมเดลหนึ่งดีกว่าอีกโมเดลหนึ่ง" % len(order),
        body=body, footer=footer, js=js,
        accent="var(--good)", hero_a="var(--good)", hero_b="var(--accent1)",
    )


# ════════════════════════════ Main ════════════════════════════

def main():
    if not os.path.exists(RESULTS_PATH):
        raise SystemExit("[ERROR] %s not found. Run: python compare_models.py" % RESULTS_PATH)

    with open(RESULTS_PATH, encoding="utf-8") as f:
        results = json.load(f)
    if not results:
        raise SystemExit("[ERROR] %s is empty." % RESULTS_PATH)

    # Keep the configured order, but only for models that were actually trained
    order = [n for n in MODEL_ORDER if n in results]
    order += [n for n in results if n not in order]

    PAGES.clear()
    PAGES.append(("page1.html", "🏠 ภาพรวม"))
    for i, name in enumerate(order):
        PAGES.append(("page%d.html" % (i + 2), "%s %s" % (ARCH.get(name, {}).get("icon", "📈"), name)))
    PAGES.append(("page%d.html" % (len(order) + 2), "🏁 เปรียบเทียบ"))

    written = []

    html = build_overview(results, order)
    with open("page1.html", "w", encoding="utf-8") as f:
        f.write(html)
    written.append(("page1.html", "overview", len(html)))

    for i, name in enumerate(order):
        fn, html = build_model_page(name, results, order, i + 2)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((fn, name, len(html)))

    fn, html = build_comparison(results, order, len(order) + 2)
    with open(fn, "w", encoding="utf-8") as f:
        f.write(html)
    written.append((fn, "comparison", len(html)))

    print("[OK] Generated %d pages from %d models" % (len(written), len(order)))
    for fn, label, size in written:
        print("     %-12s %-14s %7d bytes" % (fn, label, size))


if __name__ == "__main__":
    main()
