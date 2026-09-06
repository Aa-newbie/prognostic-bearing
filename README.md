# Bearing RUL Prediction — เปรียบเทียบ 4 สถาปัตยกรรม Deep Learning

ทำนายสุขภาพลูกปืน (bearing) จากสัญญาณสั่นสะเทือน โดยเทียบ **CNN-LSTM / LSTM / BiLSTM / Transformer**
บนชุดข้อมูล IMS Bearing Dataset แบบ run-to-failure (เดินเครื่องจริงจนพัง)

ผลลัพธ์ออกมาเป็นรายงาน HTML 6 หน้าที่สร้างอัตโนมัติจากผลการเทรนจริง

---

## ผลลัพธ์

| อันดับ | Model | RMSE ↓ | MAE ↓ | Pearson r ↑ | R² ↑ | Params |
|---|---|---|---|---|---|---|
| 🥇 | **BiLSTM** | **0.0079** | 0.0058 | 0.9536 | 0.9089 | 106,049 |
| 🥈 | LSTM | 0.0084 | 0.0063 | 0.9471 | 0.8983 | 147,009 |
| 🥉 | Transformer | 0.0117 | 0.0070 | 0.8993 | 0.8013 | 56,881 |
| 4 | CNN-LSTM | 0.0121 | 0.0064 | 0.8977 | 0.7876 | 250,497 |

> **อ่านตัวเลขนี้อย่างระวัง** — Health Index ใน test set กระจุกตัวมาก (84% อยู่ในช่วง ±0.02 รอบค่ากลาง)
> ถ้าทายค่าเฉลี่ยเสมอก็ได้ RMSE **0.0261** อยู่แล้ว ทุกโมเดลชนะ baseline นี้ 54–70%
> เวลาอ้างอิงผลควรใช้ **R²** หรือ **% ที่ดีกว่า baseline** ไม่ใช่ RMSE ดิบ เพราะสเกลของ label แต่ละงานไม่เท่ากัน

ข้อสังเกต: โมเดลที่พารามิเตอร์เยอะที่สุด (CNN-LSTM, 250K) กลับได้อันดับสุดท้าย —
MaxPool 2 ชั้นบีบ sequence จาก 20 เหลือ 5 timestep ทำให้เสีย temporal resolution

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
   python extract_data.py
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
python compare_models.py

# สร้างรายงาน HTML ทั้ง 6 หน้า
python make_report.py
```

เปิด `page1.html` ในเบราว์เซอร์เพื่อดูรายงาน

---

## การใช้งาน

### เทรนโมเดลเดียว (CNN-LSTM)

```bash
python main.py
python main.py --epochs 50 --batch_size 64
python main.py --label piecewise      # health_index | piecewise | linear
```

### เปรียบเทียบทุกโมเดล

```bash
python compare_models.py                 # ใช้ features cache ถ้ามี
python compare_models.py --epochs 50
python compare_models.py --no-cache      # บังคับอ่านข้อมูลดิบใหม่
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

---

## รายงาน HTML

| หน้า | เนื้อหา |
|---|---|
| `page1.html` | **ภาพรวมโปรเจกต์** — อธิบายตั้งแต่พื้นฐาน: ลูกปืนคืออะไร ทำไมการสั่นบอกสุขภาพได้ วิธีเตรียมข้อมูล วิธีอ่านผล + ตารางศัพท์ |
| `page2.html` | CNN-LSTM — สถาปัตยกรรม, loss curve, ผลทำนาย, การกระจาย error |
| `page3.html` | LSTM (โครงเดียวกัน) |
| `page4.html` | BiLSTM |
| `page5.html` | Transformer |
| `page6.html` | เปรียบเทียบทุกโมเดล + sanity check เทียบ baseline |

> ⚠️ ทุกหน้าเป็นไฟล์ที่ **generate อัตโนมัติ** — อย่าแก้ `.html` โดยตรงเพราะจะถูกเขียนทับ
> ให้แก้ที่ `report_overview.py` (เนื้อหาหน้าภาพรวม), `make_report.py` (โครงหน้าโมเดล/เปรียบเทียบ)
> หรือ `report_config.py` (สี, CSS, คำอธิบายสถาปัตยกรรม) แล้วรัน `python make_report.py` ใหม่

ตัวเลขทุกตัวในรายงานอ่านมาจาก `outputs/comparison_results.json` ไม่มีการพิมพ์ด้วยมือ

---

## โครงสร้างโปรเจกต์

```
├── src/
│   ├── data_loader.py      อ่านไฟล์ IMS + คำนวณ label 3 แบบ (linear / piecewise / health index)
│   ├── features.py         สกัด 14 features × 4 channels = 56 features
│   ├── dataset.py          sliding window + แบ่ง train/val/test + normalize
│   ├── model.py            CNN-LSTM
│   ├── models_extra.py     LSTM, BiLSTM, Transformer
│   └── train.py            training loop + early stopping + metrics + plots
│
├── main.py                 เทรน CNN-LSTM ตัวเดียว
├── compare_models.py       เทรนและเทียบทั้ง 4 โมเดล
├── extract_data.py         แตก 2nd_test.rar → data/
│
├── make_report.py          generator หลักของรายงาน HTML
├── report_config.py        สี, CSS, คำอธิบายสถาปัตยกรรม
├── report_overview.py      เนื้อหาหน้าภาพรวม (page1)
│
├── page1-6.html            รายงาน (generated)
└── outputs/                ผลการเทรน, กราฟ, checkpoints
```

---

## วิธีการโดยย่อ

| ขั้นตอน | รายละเอียด |
|---|---|
| **ข้อมูล** | IMS 2nd_test — 984 ไฟล์ × 20,480 samples × 4 ลูกปืน, 20 kHz, บันทึกทุก 10 นาที รวม 6.8 วัน |
| **Features** | 14 ตัว/ลูกปืน — time domain (RMS, Peak, P2P, Crest, Kurtosis, Skewness, Shape, Impulse, Margin, Std) + frequency domain (Band Energy ต่ำ/กลาง/สูง, Spectral Centroid) |
| **Label** | Health Index จาก RMS + Kurtosis + Crest Factor เกลี่ยด้วย rolling mean (window=7) แล้วกลับด้าน |
| **Window** | sliding window 20 timestep (~3 ชม.) stride 1 → 965 หน้าต่าง |
| **Split** | shuffle แล้วแบ่ง 70/15/15 → train 675 / val 144 / test 146 |
| **Normalize** | `StandardScaler` fit เฉพาะ timestep ที่อยู่ใน train windows เท่านั้น |
| **Training** | MSE + AdamW (lr 5e-4, wd 1e-4) + CosineAnnealing + grad clip 1.0 + early stopping (patience 15) |

ทุกโมเดลใช้ split เดียวกัน label เดียวกัน seed เดียวกัน และ training recipe เดียวกัน — ต่างกันแค่สถาปัตยกรรม

---

## ข้อจำกัดที่ควรรู้

1. **Label สร้างขึ้นเอง** — Health Index คำนวณจาก features ชุดเดียวกับที่ป้อนเข้าโมเดล จึงสัมพันธ์กันอยู่ก่อนแล้วบางส่วน ตัวเลขจึงดูดีกว่างานที่มี ground-truth RUL จริง
2. **Label กระจุกตัว** — 84% ของ test set อยู่ในช่วงแคบ ทำให้ RMSE ดิบดูต่ำเกินจริง ต้องอ่านคู่กับ baseline
3. **หน้าต่างซ้อนทับ** — window ที่ติดกันใช้ข้อมูลร่วมกัน 19 จาก 20 จุด เมื่อ shuffle แล้วแบ่ง test set จึงไม่เป็นอิสระจาก train เต็มที่
4. **ทดสอบบน run เดียว** — ใช้เฉพาะ 2nd_test ยังไม่ได้ยืนยันกับ 1st/3rd_test
5. **รันครั้งเดียวต่อโมเดล** — ยังไม่ได้ทำ multi-seed จึงยังบอกไม่ได้ว่าความต่างที่เห็นเกินความผันผวนจากการสุ่มหรือไม่

---

## ปัญหาที่พบบ่อย

| อาการ | วิธีแก้ |
|---|---|
| `FileNotFoundError: data/2nd_test/2nd_test` | ยังไม่ได้แตกไฟล์ข้อมูล — ดูขั้นตอนที่ 3 |
| `rarfile.RarCannotExec` | ยังไม่ได้ติดตั้ง 7-Zip / unrar ในเครื่อง หรือให้แตกไฟล์ด้วยมือแทน |
| `UnicodeEncodeError` ตอนรันสคริปต์ | คอนโซล Windows เป็น cp1252 — รัน `chcp 65001` ก่อน หรือใช้ Windows Terminal |
| กราฟในหน้า HTML ไม่ขึ้น | หน้าโหลด Chart.js จาก CDN ต้องต่ออินเทอร์เน็ต |
| รูปในหน้า HTML ไม่ขึ้น | ยังไม่ได้รัน `compare_models.py` จึงยังไม่มีไฟล์ใน `outputs/` |

---

## เครดิต

ชุดข้อมูล **IMS Bearing Dataset** — Center for Intelligent Maintenance Systems, University of Cincinnati
เผยแพร่ผ่าน NASA Prognostics Center of Excellence Data Repository
หากนำชุดข้อมูลไปใช้ กรุณาอ้างอิงตามเงื่อนไขของ NASA PCoE
