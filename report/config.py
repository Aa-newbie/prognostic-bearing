"""
report_config.py
----------------
Static content for the HTML report: colours, architecture descriptions,
and the shared stylesheet. Numbers never live here — they come from
outputs/comparison_results.json at generation time.
"""

# Page order: overview, one page per model, comparison
MODEL_ORDER = ["CNN-LSTM", "LSTM", "BiLSTM", "Transformer"]

COLORS = {
    "CNN-LSTM":    "#4f8ef7",
    "LSTM":        "#f97316",
    "BiLSTM":      "#a78bfa",
    "Transformer": "#f472b6",
}

ARCH = {
    "CNN-LSTM": {
        "icon": "🧬",
        "tag": "Hybrid CNN + RNN",
        "layers": [
            ("Input", "(B, 20, 56)", "20 timestep x 56 features"),
            ("Conv1D(64, k=7) + BN + ReLU", "(B, 64, 20)", "สกัด local pattern ข้าม feature"),
            ("MaxPool(2)", "(B, 64, 10)", "ลดความยาวลงครึ่งหนึ่ง"),
            ("Conv1D(128, k=5) + BN + ReLU", "(B, 128, 10)", "สกัด pattern ที่ซับซ้อนขึ้น"),
            ("MaxPool(2)", "(B, 128, 5)", "เหลือ 5 timestep"),
            ("LSTM(128) + Dropout(0.3)", "(B, 5, 128)", "เรียนรู้ลำดับเวลา"),
            ("LSTM(64) + Dropout(0.3)", "(B, 5, 64)", "บีบให้กระชับ"),
            ("Last timestep → FC(32) → FC(1) → Sigmoid", "(B,)", "Health Index ∈ (0, 1)"),
        ],
        "idea": "แนวคิดคือให้ CNN ทำหน้าที่อ่าน &quot;รูปร่าง&quot; ของสัญญาณในช่วงสั้น ๆ ก่อน "
                "แล้วส่งผลลัพธ์ที่กลั่นแล้วให้ LSTM เรียนรู้แนวโน้มระยะยาว "
                "เป็นสถาปัตยกรรมที่ถูกใช้บ่อยที่สุดในงาน RUL prediction",
        "pros": [
            "จับได้ทั้ง local shape และ temporal trend ในโมเดลเดียว",
            "BatchNorm ทำให้ training เสถียร ไม่ค่อยมีปัญหา gradient",
        ],
        "cons": [
            "พารามิเตอร์เยอะที่สุดในการทดลองนี้",
            "MaxPool 2 ชั้นบีบ sequence จาก 20 เหลือ 5 → เสีย temporal resolution",
            "มี hyperparameter ให้ tune เยอะ (kernel size, pool size, channel)",
        ],
    },
    "LSTM": {
        "icon": "🔁",
        "tag": "Baseline RNN",
        "layers": [
            ("Input", "(B, 20, 56)", "20 timestep x 56 features"),
            ("LSTM(128)", "(B, 20, 128)", "อ่านลำดับเวลาตรง ๆ"),
            ("LSTM(64)", "(B, 20, 64)", "ชั้นที่สอง"),
            ("Last timestep", "(B, 64)", "ใช้ hidden state ตัวสุดท้าย"),
            ("FC(32) → ReLU → FC(1) → Sigmoid", "(B,)", "Health Index ∈ (0, 1)"),
        ],
        "idea": "ป้อน 56 features ทั้ง 20 timestep เข้า LSTM ตรง ๆ โดยไม่มีการสกัด feature ก่อน "
                "ใช้เป็น baseline เพื่อดูว่าการเพิ่ม CNN หรือ attention เข้ามาคุ้มค่าจริงหรือไม่",
        "pros": [
            "เรียบง่ายที่สุด ตีความง่าย เหมาะเป็นจุดอ้างอิง",
            "เทรนเร็วที่สุดในการทดลองนี้",
            "รักษา temporal resolution ครบทั้ง 20 timestep ไม่มี pooling",
        ],
        "cons": [
            "ไม่มี local feature extraction — ต้องเรียนรู้ทุกอย่างเอง",
            "เห็นเฉพาะ context ย้อนหลัง ไม่เห็นข้างหน้า",
        ],
    },
    "BiLSTM": {
        "icon": "↔️",
        "tag": "Bidirectional RNN",
        "layers": [
            ("Input", "(B, 20, 56)", "20 timestep x 56 features"),
            ("BiLSTM(64 x 2 ทิศทาง)", "(B, 20, 128)", "อ่านไปข้างหน้า + ย้อนกลับ"),
            ("BiLSTM(32 x 2 ทิศทาง)", "(B, 20, 64)", "ชั้นที่สอง"),
            ("Last timestep", "(B, 64)", "รวม forward + backward"),
            ("FC(32) → ReLU → FC(1) → Sigmoid", "(B,)", "Health Index ∈ (0, 1)"),
        ],
        "idea": "อ่าน sequence ทั้งสองทิศทาง ทำให้ทุก timestep เห็น context ทั้งก่อนและหลัง "
                "ภายในหน้าต่าง 20 timestep เหมาะกับการประเมินสภาพย้อนหลังจากข้อมูลที่บันทึกไว้แล้ว",
        "pros": [
            "เห็น context สองทิศทางภายในหน้าต่างเดียวกัน",
            "hidden size เล็กแต่ได้ representation กว้าง",
            "รักษา temporal resolution ครบ ไม่มี pooling",
        ],
        "cons": [
            "ใช้ข้อมูลอนาคตภายในหน้าต่าง → ทำ real-time forecasting ตรง ๆ ไม่ได้",
            "เทรนช้ากว่า LSTM ธรรมดาเพราะคำนวณสองทิศทาง",
        ],
    },
    "Transformer": {
        "icon": "🎯",
        "tag": "Self-Attention",
        "layers": [
            ("Input", "(B, 20, 56)", "20 timestep x 56 features"),
            ("Positional Encoding (sin/cos)", "(B, 20, 56)", "ใส่ข้อมูลลำดับเข้าไป"),
            ("TransformerEncoder x2 (nhead=4, ff=128)", "(B, 20, 56)", "self-attention ทุก timestep"),
            ("Mean Pooling", "(B, 56)", "เฉลี่ยข้าม 20 timestep"),
            ("FC(32) → ReLU → FC(1) → Sigmoid", "(B,)", "Health Index ∈ (0, 1)"),
        ],
        "idea": "ใช้ self-attention ให้ทุก timestep มองเห็นกันได้ทั้งหมดพร้อมกัน แทนการไล่ทีละ step "
                "แบบ recurrent เป็นสถาปัตยกรรมที่ครองงาน NLP และเริ่มถูกนำมาใช้กับ time series",
        "pros": [
            "พารามิเตอร์น้อยที่สุดในการทดลองนี้",
            "คำนวณขนานได้เต็มที่ ไม่ต้องไล่ตามลำดับ",
            "attention บอกได้ว่า timestep ไหนมีน้ำหนักต่อการทำนาย",
        ],
        "cons": [
            "d_model ถูกล็อกไว้ที่ 56 ตามจำนวน feature เพราะไม่มี input projection",
            "Transformer มักต้องการข้อมูลมากกว่านี้จึงจะเหนือกว่า RNN",
            "sequence ยาวแค่ 20 step ทำให้ข้อได้เปรียบของ attention ไม่เด่น",
        ],
    },
}

CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:       #0f1117;
    --surface:  #1a1d27;
    --card:     #21263a;
    --border:   #2e3450;
    --accent1:  #4f8ef7;
    --accent2:  #6ee7b7;
    --accent3:  #f97316;
    --accent4:  #a78bfa;
    --accent5:  #f472b6;
    --text:     #e8eaf6;
    --muted:    #8892b0;
    --good:     #4ade80;
    --radius:   14px;
  }

  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.65;
  }

  /* Nav */
  nav {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; flex-wrap: wrap;
    padding: 0 26px; min-height: 54px;
    position: sticky; top: 0; z-index: 100;
  }
  nav .logo { font-weight: 800; font-size: 0.95rem; color: #fff; margin-right: 24px; }
  nav a {
    color: var(--muted); text-decoration: none;
    font-size: 0.82rem; font-weight: 600;
    padding: 15px 13px; border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s; white-space: nowrap;
  }
  nav a:hover { color: var(--text); }
  nav a.active { color: var(--nav-active); border-bottom-color: var(--nav-active); }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #1a1f35 0%, #0f1117 60%);
    border-bottom: 1px solid var(--border);
    padding: 50px 40px 46px; text-align: center;
  }
  .hero .eyebrow {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 8px;
  }
  .hero h1 {
    font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(135deg, var(--hero-a) 0%, var(--hero-b) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 10px;
  }
  .hero p { color: var(--muted); font-size: 1rem; max-width: 680px; margin: 0 auto; }

  /* Layout */
  main { max-width: 1180px; margin: 0 auto; padding: 40px 24px; display: flex; flex-direction: column; gap: 44px; }

  .section-title {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--accent1); margin-bottom: 18px;
    display: flex; align-items: center; gap: 8px;
  }
  .section-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }

  .card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 28px;
  }
  .card h3 { font-size: 1.05rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }

  .row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
  @media (max-width: 860px) { .row-2, .row-3 { grid-template-columns: 1fr; } }

  /* Info blocks */
  .info-block {
    background: rgba(79,142,247,0.06);
    border: 1px solid rgba(79,142,247,0.2);
    border-radius: 12px; padding: 18px 22px; margin-top: 12px;
  }
  .info-block.purple { background: rgba(167,139,250,0.06); border-color: rgba(167,139,250,0.2); }
  .info-block.green  { background: rgba(74,222,128,0.06);  border-color: rgba(74,222,128,0.2); }
  .info-block.orange { background: rgba(249,115,22,0.06);  border-color: rgba(249,115,22,0.2); }
  .info-block.pink   { background: rgba(244,114,182,0.06); border-color: rgba(244,114,182,0.2); }

  /* Step indicators */
  .step-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 30px; height: 30px; border-radius: 50%;
    background: var(--accent1); color: #fff;
    font-size: 0.8rem; font-weight: 800; flex-shrink: 0;
  }
  .step-num.purple { background: var(--accent4); }
  .step-num.green  { background: var(--accent2); color: #0f1117; }
  .step-num.orange { background: var(--accent3); }
  .step-num.pink   { background: var(--accent5); }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  thead th {
    background: rgba(255,255,255,0.04);
    padding: 10px 14px; text-align: left;
    font-size: 0.7rem; letter-spacing: 0.06em;
    text-transform: uppercase; color: var(--muted);
    border-bottom: 1px solid var(--border);
  }
  tbody td { padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.04); }
  tbody tr:hover td { background: rgba(255,255,255,0.02); }
  .pill {
    display: inline-block; padding: 2px 10px; border-radius: 100px;
    font-size: 0.7rem; font-weight: 600;
  }
  .pill.time { background: rgba(167,139,250,0.18); color: var(--accent4); }
  .pill.freq { background: rgba(79,142,247,0.18);  color: var(--accent1); }

  /* Image cards */
  .img-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); overflow: hidden;
  }
  .img-card-header {
    padding: 14px 20px; border-bottom: 1px solid var(--border);
    font-size: 0.88rem; font-weight: 700;
    display: flex; align-items: center; gap: 8px;
  }
  .img-card img { width: 100%; display: block; }
  .img-card-footer { padding: 10px 20px; font-size: 0.76rem; color: var(--muted); border-top: 1px solid var(--border); }

  /* Metric tiles */
  .mini-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; }
  .mini-metric {
    background: rgba(255,255,255,0.03); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px; text-align: center;
  }
  .mini-metric .num { font-size: 1.5rem; font-weight: 800; color: var(--accent1); }
  .mini-metric .lbl { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }

  /* Code block */
  pre.code-block {
    background: rgba(0,0,0,0.35); border-radius: 10px; padding: 18px 22px;
    font-size: 0.8rem; line-height: 1.7; overflow-x: auto;
    color: #c9d1d9; font-family: 'Consolas', 'Courier New', monospace;
    border: 1px solid var(--border);
  }
  pre.code-block .cmt { color: #6a9955; }
  pre.code-block .kw  { color: #c586c0; }
  pre.code-block .fn  { color: #dcdcaa; }
  pre.code-block .num { color: #b5cea8; }

  /* Flow diagram */
  .flow { display: flex; flex-direction: column; align-items: center; }
  .flow-step {
    display: flex; align-items: center; gap: 14px;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 22px; width: 100%; max-width: 620px;
  }
  .flow-step .title { font-weight: 700; font-size: 0.88rem; }
  .flow-step .desc { font-size: 0.78rem; color: var(--muted); }
  .flow-arrow { color: var(--muted); font-size: 1.4rem; padding: 2px 0; }

  /* Layer stack */
  .layer-stack { display: flex; flex-direction: column; }
  .layer-row {
    display: grid; grid-template-columns: 1fr auto; gap: 10px 14px; align-items: center;
    background: rgba(0,0,0,0.28); border: 1px solid var(--border);
    border-radius: 9px; padding: 11px 16px;
  }
  .layer-row .lname  { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.78rem; color: #c9d1d9; }
  .layer-row .lshape { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.73rem; color: var(--muted); white-space: nowrap; }
  .layer-row .lnote  { grid-column: 1 / -1; font-size: 0.74rem; color: var(--muted); }
  .layer-sep { text-align: center; color: var(--muted); font-size: 0.85rem; line-height: 1.6; opacity: 0.5; }

  /* Model link cards */
  .model-links { display: grid; grid-template-columns: repeat(auto-fit, minmax(235px, 1fr)); gap: 16px; }
  .model-link {
    display: block; text-decoration: none; color: inherit;
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 22px;
    transition: transform 0.15s, border-color 0.15s;
  }
  .model-link:hover { transform: translateY(-3px); }
  .model-link .mtop  { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
  .model-link .mname { font-weight: 800; font-size: 1.05rem; }
  .model-link .mrank { margin-left: auto; font-size: 1.15rem; }
  .model-link .mrmse { font-size: 1.7rem; font-weight: 800; line-height: 1.2; }
  .model-link .mlbl  { font-size: 0.72rem; color: var(--muted); }
  .model-link .mgo   { margin-top: 14px; font-size: 0.78rem; font-weight: 600; }

  /* Charts */
  .chart-box { position: relative; height: 330px; }
  .chart-box.tall { height: 420px; }

  /* Collapsible detail */
  details.more {
    margin-top: 16px; border: 1px solid var(--border);
    border-radius: 12px; background: rgba(0,0,0,0.16);
  }
  details.more > summary {
    cursor: pointer; padding: 13px 20px; list-style: none;
    font-size: 0.84rem; font-weight: 700; color: var(--accent1);
    display: flex; align-items: center; gap: 8px;
  }
  details.more > summary::-webkit-details-marker { display: none; }
  details.more > summary::before { content: '▸'; font-size: 0.9em; transition: transform 0.15s; }
  details.more[open] > summary::before { transform: rotate(90deg); }
  details.more > summary:hover { color: var(--text); }
  details.more .more-body { padding: 4px 20px 20px; }

  /* Winner banner */
  .winner {
    background: linear-gradient(135deg, rgba(74,222,128,0.12), rgba(79,142,247,0.08));
    border: 1px solid rgba(74,222,128,0.35);
    border-radius: var(--radius); padding: 26px 30px;
    display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
  }
  .winner .trophy { font-size: 2.6rem; }

  /* Prev / next pager */
  .pager { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .pager a {
    flex: 1; min-width: 210px; text-decoration: none; color: inherit;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; transition: border-color 0.15s;
  }
  .pager a:hover { border-color: var(--accent1); }
  .pager .plbl  { font-size: 0.72rem; color: var(--muted); }
  .pager .pname { font-weight: 700; font-size: 0.92rem; }
  .pager .next  { text-align: right; }

  /* Footer */
  footer {
    text-align: center; color: var(--muted); font-size: 0.78rem;
    padding: 32px; border-top: 1px solid var(--border);
  }
  footer a { color: var(--accent1); text-decoration: none; }
"""
