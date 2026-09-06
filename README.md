# Bearing RUL Prediction — เปรียบเทียบ 4 สถาปัตยกรรม Deep Learning

ทำนายสุขภาพลูกปืน (bearing) จากสัญญาณสั่นสะเทือน โดยเทียบ **CNN-LSTM / LSTM / BiLSTM / Transformer**
บนชุดข้อมูล IMS Bearing Dataset แบบ run-to-failure (เดินเครื่องจริงจนพัง)

ผลลัพธ์ออกมาเป็นรายงาน HTML 6 หน้าที่สร้างอัตโนมัติจากผลการเทรนจริง

---

## ผลลัพธ์

| อันดับ | Model | RMSE ↓ | MAE ↓ | Pearson r ↑ | R² ↑ | Params |
|---|---|---|---|---|---|---|
| 🥇 | **LSTM** | **0.0080** | 0.0062 | 0.9805 | 0.9586 | 147,009 |
| 🥈 | Transformer | **0.0085** | 0.0064 | 0.9800 | 0.9537 | 56,881 |
| 🥉 | BiLSTM | **0.0093** | 0.0069 | 0.9751 | 0.9441 | 106,049 |
| 4 | CNN-LSTM | **0.0097** | 0.0072 | 0.9744 | 0.9396 | 250,497 |

> **อ่านตัวเลขนี้อย่างระวัง** — ผลข้างบนใช้การแบ่งข้อมูลแบบสุ่มสลับ ซึ่งทำให้หน้าต่างที่ซ้อนทับกัน
> กระจายไปทั้ง train และ test ตัวเลขจึงดีเกินความเป็นจริง
> โมเดลเดียวกันได้ **R² = 0.94 เมื่อสุ่มสลับ** แต่เหลือ **R² = 0.05 เมื่อแบ่งตามเวลา**
> ([ดูการทดลองใน notebooks/08](notebooks/08_from_hi_to_rul.ipynb))
>
> ใช้ตัวเลขชุดนี้**เทียบระหว่างโมเดล**ได้ (ทุกตัวเจอเงื่อนไขเดียวกัน)
> แต่ห้ามตีความว่าเป็นความแม่นยำตอนนำไปใช้จริง
>
> Baseline (ทายค่าเฉลี่ยเสมอ) ได้ RMSE **0.0393** — ทุกโมเดลดีกว่า baseline 75–80%

ข้อสังเกต: โมเดลที่พารามิเตอร์เยอะที่สุด (CNN-LSTM, 250K) ได้อันดับสุดท้าย ส่วน Transformer
ที่เล็กที่สุด (57K) กลับได้ที่ 2 — ขนาดโมเดลไม่ได้ตัดสินผลเมื่อข้อมูลมีจำกัด

---

## การติดตั้ง

### สิ่งที่ต้องมีก่อน

- **Python 3.10 ขึ้นไป** (พัฒนาและทดสอบบน 3.12)
- **~2 GB พื้นที่ว่าง** สำหรับชุดข้อมูล
- ไม่ต้องมี GPU — เทรนครบทั้ง 4 โมเดลใช้เวลาราว **45 วินาทีบน CPU**

### 1. Clone repository

```bash
git clone https://github.com/Aa-newbie/prognostic-bearing.git
cd prognostic-bearing
```

### 2. สร้าง virtual environment แล้วติดตั้ง dependencies

<details open>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

ถ้าติด execution policy ให้รัน `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` ก่อน
</details>

<details>
<summary><b>macOS / Linux</b></summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
</details>

### 3. ดาวน์โหลดชุดข้อมูล

ชุดข้อมูล **ไม่ได้อยู่ใน repo** เพราะมีขนาดกว่า 1 GB ต้องดาวน์โหลดเอง

1. ไปที่ [NASA Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
   แล้วหา **"Bearing Data Set"** ของ IMS, University of Cincinnati
   (หรือค้นบน Kaggle ด้วยคำว่า `IMS bearing dataset` ก็มีคนอัปโหลดไว้)

2. วางไฟล์ให้ได้โครงสร้างแบบนี้:

   ```
   IMS/
   └── IMS/
       ├── 1st_test.rar
       ├── 2nd_test.rar     ← โปรเจกต์นี้ใช้แค่ตัวนี้
       └── 3rd_test.rar
   ```

3. แตกไฟล์:

   ```bash
   python scripts/extract_data.py
   ```

   สคริปต์ใช้ `rarfile` ซึ่งต้องมีตัวแตก `.rar` ในเครื่องด้วย —
   ติดตั้ง [7-Zip](https://www.7-zip.org/) (Windows), `sudo apt install unrar` (Linux)
   หรือ `brew install unrar` (macOS)

   **ถ้าสคริปต์ไม่ผ่าน ให้แตกด้วยมือ** — คลิกขวา `IMS/IMS/2nd_test.rar` → Extract to `data/2nd_test/`

4. ตรวจว่าได้ไฟล์ครบ **984 ไฟล์**:

   ```powershell
   # Windows PowerShell
   (Get-ChildItem data\2nd_test\2nd_test).Count
   ```

   ```bash
   # macOS / Linux
   ls data/2nd_test/2nd_test | wc -l
   ```

### 4. รัน

```bash
# เทรนและเปรียบเทียบทั้ง 4 โมเดล (รอบแรก ~2 นาที รวมเวลาอ่านข้อมูลดิบ)
python scripts/compare_models.py

# สร้างรายงาน HTML ทั้ง 6 หน้า
python scripts/make_report.py
```

เปิด `docs/index.html` ในเบราว์เซอร์เพื่อดูรายงาน

---

## การใช้งาน

### เทรนโมเดลเดียว (CNN-LSTM)

```bash
python scripts/train_single.py
python scripts/train_single.py --epochs 50 --batch_size 64
python scripts/train_single.py --label piecewise      # health_index | piecewise | linear
```

### เปรียบเทียบทุกโมเดล

```bash
python scripts/compare_models.py                 # ใช้ features cache ถ้ามี
python scripts/compare_models.py --epochs 50
python scripts/compare_models.py --no-cache      # บังคับอ่านข้อมูลดิบใหม่
```

รอบแรกจะอ่าน 984 ไฟล์แล้ว cache features ไว้ที่ `outputs/features_cache.npz`
รอบถัดไปจะข้ามขั้นตอนนั้นไปเลย

| ไฟล์ผลลัพธ์ | คำอธิบาย |
|---|---|
| `outputs/comparison_results.json` | metrics + loss history + test predictions ของทุกโมเดล |
| `outputs/model_comparison.png` | bar chart RMSE / MAE |
| `outputs/all_models_prediction.png` | ทุกโมเดลซ้อนกับค่าจริง |
| `outputs/<Model>_prediction.png` | กราฟทำนายรายโมเดล |
| `outputs/<Model>/best_model.pt` | checkpoint แยกตามโมเดล |
| `outputs/features_cache.npz` | features ที่สกัดแล้ว (อยู่ใน repo — บทเรียน 2–8 ใช้ตัวนี้) |

---

## รายงาน HTML

รายงานอยู่ในโฟลเดอร์ `docs/` เปิด `docs/index.html` เพื่อเริ่มอ่าน

| หน้า | เนื้อหา |
|---|---|
| `docs/index.html` | **ภาพรวมโปรเจกต์** — อธิบายตั้งแต่พื้นฐาน: ลูกปืนคืออะไร ทำไมการสั่นบอกสุขภาพได้ วิธีเตรียมข้อมูล วิธีอ่านผล + ตารางศัพท์ |
| `docs/page2.html` | CNN-LSTM — สถาปัตยกรรม, loss curve, ผลทำนาย, การกระจาย error |
| `docs/page3.html` | LSTM (โครงเดียวกัน) |
| `docs/page4.html` | BiLSTM |
| `docs/page5.html` | Transformer |
| `docs/page6.html` | เปรียบเทียบทุกโมเดล + sanity check เทียบ baseline |

> ⚠️ ทุกหน้าเป็นไฟล์ที่ **generate อัตโนมัติ** — อย่าแก้ `.html` ใน `docs/` โดยตรงเพราะจะถูกเขียนทับ
> ให้แก้ที่ `report/overview.py` (เนื้อหาหน้าภาพรวม), `scripts/make_report.py` (โครงหน้าโมเดล/เปรียบเทียบ)
> หรือ `report/config.py` (สี, CSS, คำอธิบายสถาปัตยกรรม) แล้วรัน `python scripts/make_report.py` ใหม่

ตัวเลขทุกตัวในรายงานอ่านมาจาก `outputs/comparison_results.json` ไม่มีการพิมพ์ด้วยมือ

โฟลเดอร์ชื่อ `docs/` เพราะ GitHub Pages เปิด serve จากโฟลเดอร์นี้ได้เลย
(Settings → Pages → Source: Deploy from a branch → `main` / `/docs`)

---

## บทเรียน (Jupyter Notebook)

โฟลเดอร์ [`notebooks/`](notebooks/) มีบทเรียน 8 บทที่พาไล่ตั้งแต่ "สัญญาณสั่นคืออะไร"
จนถึง "ทำนายว่าลูกปืนเหลืออีกกี่ชั่วโมง" — เขียนสำหรับคนที่ไม่เคยทำ ML มาก่อน

```bash
pip install jupyter ipykernel
jupyter notebook notebooks/
```

| บท | เนื้อหา |
|---|---|
| 1 | สัญญาณสั่นสะเทือนบอกอะไรเราได้ — พล็อตสัญญาณจริง, FFT |
| 2 | บีบ 20,480 จุด เหลือ 14 ตัวเลข — เขียน RMS/Kurtosis/Crest เอง |
| 3 | ไม่มีเฉลย แล้วจะสอนโมเดลยังไง — สร้าง Health Index |
| 4 | เตรียมข้อมูล — sliding window, แบ่ง 3 ชุด, data leakage |
| 5 | สร้างและเทรนโมเดลแรก (LSTM) |
| 6 | เทียบ 4 สถาปัตยกรรม |
| 7 | อ่านผลอย่างมีวิจารณญาณ — baseline, R², กับดักของ Pearson r |
| 8 | แล้ว RUL ล่ะ — แปลง Health Index เป็นชั่วโมงที่เหลือ |

บทที่ 1 ต้องมีข้อมูลดิบ ส่วนบทที่ 2–8 รันได้เลยเพราะใช้ `outputs/features_cache.npz` ที่อยู่ใน repo

รายละเอียดเพิ่มเติมดู [`notebooks/README.md`](notebooks/README.md)

---

## โครงสร้างโปรเจกต์

```
prognostic-bearing/
├── README.md
├── requirements.txt
│
├── scripts/                    คำสั่งที่รันจริง (รันจากที่ไหนก็ได้)
│   ├── extract_data.py           แตก 2nd_test.rar → data/
│   ├── train_single.py           เทรน CNN-LSTM ตัวเดียว
│   ├── compare_models.py         เทรนและเทียบทั้ง 4 โมเดล
│   └── make_report.py            สร้างรายงาน HTML ทั้งหมด
│
├── src/                        โค้ดหลัก (import เป็น package)
│   ├── paths.py                  ที่อยู่ของทุกโฟลเดอร์ในโปรเจกต์
│   ├── data_loader.py            อ่านไฟล์ IMS + คำนวณ label 3 แบบ
│   ├── features.py               สกัด 14 features × 4 channels = 56
│   ├── dataset.py                sliding window + split + normalize
│   ├── model.py                  CNN-LSTM
│   ├── models_extra.py           LSTM, BiLSTM, Transformer
│   └── train.py                  training loop + early stopping + metrics
│
├── report/                     เนื้อหาและสไตล์ของรายงาน
│   ├── config.py                 สี, CSS, คำอธิบายสถาปัตยกรรม
│   └── overview.py               เนื้อหาหน้าภาพรวม
│
├── docs/                       รายงาน HTML (generated + GitHub Pages root)
│   ├── index.html
│   ├── page2–6.html
│   └── assets/                   รูปที่รายงานใช้
│
├── notebooks/                  บทเรียน 8 บท (Jupyter)
│   └── 01–08_*.ipynb
│
├── outputs/                    ผลการเทรน (json, log, กราฟ, checkpoints)
├── tools/                      7-Zip / UnRAR (ไม่ขึ้น git)
├── data/                       ข้อมูลที่แตกแล้ว (ไม่ขึ้น git)
└── IMS/                        ไฟล์ .rar ต้นฉบับ (ไม่ขึ้น git)
```

**สิ่งที่ไม่ได้ขึ้น git:** ชุดข้อมูล (~2.5 GB), ไฟล์ `.exe`, model checkpoints และรูปใน `outputs/`
— ทั้งหมดสร้างใหม่ได้ ส่วนรูปที่รายงานต้องใช้ถูก copy ไปเก็บใน `docs/assets/` แล้ว
ไฟล์ `outputs/comparison_results.json` ยังอยู่ใน git จึงสั่ง `make_report.py` ได้โดยไม่ต้องเทรนใหม่

---

## วิธีการโดยย่อ

| ขั้นตอน | รายละเอียด |
|---|---|
| **ข้อมูล** | IMS 2nd_test — 984 ไฟล์ × 20,480 samples × 4 ลูกปืน, 20 kHz, บันทึกทุก 10 นาที รวม 6.8 วัน<br>ใช้จริง **982 ไฟล์** (ตัด 2 ไฟล์สุดท้ายที่บันทึกตอนเครื่องหยุดแล้ว) · ลูกปืนที่พังคือ **Bearing 1** (outer race) |
| **Features** | 14 ตัว/ลูกปืน — time domain (RMS, Peak, P2P, Crest, Kurtosis, Skewness, Shape, Impulse, Margin, Std) + frequency domain (Band Energy ต่ำ/กลาง/สูง, Spectral Centroid) |
| **Label** | Health Index จาก RMS + Kurtosis + Crest Factor เกลี่ยด้วย rolling mean (window=7) แล้วกลับด้าน |
| **Window** | sliding window 20 timestep (~3 ชม.) stride 1 → 963 หน้าต่าง |
| **Split** | shuffle แล้วแบ่ง 70/15/15 → train 674 / val 144 / test 145 |
| **Normalize** | `StandardScaler` fit เฉพาะ timestep ที่อยู่ใน train windows เท่านั้น |
| **Training** | MSE + AdamW (lr 5e-4, wd 1e-4) + CosineAnnealing + grad clip 1.0 + early stopping (patience 15) |

ทุกโมเดลใช้ split เดียวกัน label เดียวกัน seed เดียวกัน และ training recipe เดียวกัน — ต่างกันแค่สถาปัตยกรรม

---

## ข้อจำกัดที่ควรรู้

1. **Label สร้างขึ้นเอง** — Health Index คำนวณจาก features ชุดเดียวกับที่ป้อนเข้าโมเดล จึงสัมพันธ์กันอยู่ก่อนแล้วบางส่วน ตัวเลขจึงดูดีกว่างานที่มี ground-truth RUL จริง
2. **Label กระจุกตัว** — 84% ของ test set อยู่ในช่วงแคบ ทำให้ RMSE ดิบดูต่ำเกินจริง ต้องอ่านคู่กับ baseline
3. **หน้าต่างซ้อนทับ (ข้อจำกัดที่ใหญ่ที่สุด)** — window ที่ติดกันใช้ข้อมูลร่วมกัน 19 จาก 20 จุด เมื่อ shuffle แล้วแบ่ง test set จึงไม่เป็นอิสระจาก train วัดผลจริงแล้วโมเดลเดียวกันได้ R² 0.94 เมื่อ shuffle แต่เหลือ 0.05 เมื่อแบ่งตามเวลา
4. **ทดสอบบน run เดียว** — ใช้เฉพาะ 2nd_test ยังไม่ได้ยืนยันกับ 1st/3rd_test
5. **รันครั้งเดียวต่อโมเดล** — ยังไม่ได้ทำ multi-seed จึงยังบอกไม่ได้ว่าความต่างที่เห็นเกินความผันผวนจากการสุ่มหรือไม่

---

## ปัญหาที่พบบ่อย

| อาการ | วิธีแก้ |
|---|---|
| `FileNotFoundError` ตอนโหลดข้อมูล | ยังไม่ได้แตกไฟล์ข้อมูล — ดูขั้นตอนที่ 3 |
| `rarfile.RarCannotExec` | ยังไม่ได้ติดตั้ง 7-Zip / unrar ในเครื่อง หรือให้แตกไฟล์ด้วยมือแทน |
| `UnicodeEncodeError` ตอนรันสคริปต์ | คอนโซล Windows เป็น cp1252 — รัน `chcp 65001` ก่อน หรือใช้ Windows Terminal |
| กราฟในหน้า HTML ไม่ขึ้น | หน้าโหลด Chart.js จาก CDN ต้องต่ออินเทอร์เน็ต |
| รูปในหน้า HTML ไม่ขึ้น | ยังไม่ได้รัน `scripts/compare_models.py` จึงยังไม่มีรูปให้ copy เข้า `docs/assets/` |

---

## เครดิต

ชุดข้อมูล **IMS Bearing Dataset** — Center for Intelligent Maintenance Systems, University of Cincinnati
เผยแพร่ผ่าน NASA Prognostics Center of Excellence Data Repository
หากนำชุดข้อมูลไปใช้ กรุณาอ้างอิงตามเงื่อนไขของ NASA PCoE
