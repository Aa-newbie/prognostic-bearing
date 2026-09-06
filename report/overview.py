"""
report_overview.py
------------------
Long-form body content for the overview page (docs/index.html).

Kept separate from make_report.py because this is prose, not generator logic.
Placeholders written as __NAME__ are filled in by build_overview().
"""

OVERVIEW_BODY = """
<!-- ═══ 1. ปัญหา ═══ -->
<section>
  <div class="section-title">1 &nbsp; ปัญหาที่โปรเจกต์นี้พยายามแก้</div>

  <div class="card">
    <h3>🔩 ลูกปืน (Bearing) คืออะไร และทำไมถึงสำคัญ</h3>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95">
      ลูกปืนคือชิ้นส่วนที่อยู่ระหว่างเพลาที่หมุนกับตัวเรือนที่อยู่นิ่ง หน้าที่ของมันคือ
      <strong style="color:var(--text)">ทำให้เพลาหมุนได้ลื่นโดยแทบไม่มีแรงเสียดทาน</strong>
      ข้างในมีลูกกลิ้งหรือลูกบอลโลหะวิ่งอยู่ระหว่างวงแหวนสองวง (วงในติดกับเพลา วงนอกติดกับตัวเรือน)
    </p>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95;margin-top:12px">
      เครื่องจักรหมุนแทบทุกชนิดมีลูกปืน — มอเตอร์ ปั๊ม พัดลม กังหันลม กระปุกเกียร์ ล้อรถไฟ
      และเพราะมันต้องรับภาระตลอดเวลาที่เครื่องทำงาน
      <strong style="color:var(--text)">ลูกปืนจึงเป็นชิ้นส่วนที่พังบ่อยที่สุดในเครื่องจักรหมุน</strong>
      มีการประเมินว่าราว 40–50% ของการเสียของมอเตอร์ไฟฟ้ามีต้นเหตุมาจากลูกปืน
    </p>

    <div class="info-block orange" style="margin-top:18px">
      <strong>💥 ปัญหาคือมันพังแบบไม่บอกล่วงหน้า (ถ้าไม่มีใครฟัง)</strong><br>
      <span style="color:var(--muted);font-size:0.86rem;line-height:1.9">
        ลูกปืนไม่ได้ค่อย ๆ แย่ลงอย่างสม่ำเสมอ แต่มักทำงาน<strong style="color:var(--text)">ปกติดีเกือบตลอดอายุ</strong>
        แล้วทรุดลงอย่างรวดเร็วในช่วงท้าย เมื่อมันแตกจริง เศษโลหะจะกระจายเข้าไปทำลายชิ้นส่วนอื่น
        ทำให้ค่าซ่อมบานปลายและสายการผลิตต้องหยุดโดยไม่ได้วางแผน
      </span>
    </div>
  </div>

  <div class="card" style="margin-top:20px">
    <h3>🛠️ สามวิธีดูแลเครื่องจักร — และทำไมวิธีที่สามถึงคุ้มที่สุด</h3>
    <table style="margin-top:6px">
      <thead>
        <tr><th>กลยุทธ์</th><th>ทำอย่างไร</th><th>ข้อดี</th><th>ข้อเสีย</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong style="color:#f87171">Reactive</strong><br><span style="color:var(--muted);font-size:0.75rem">รอพังแล้วซ่อม</span></td>
          <td>ใช้จนพังแล้วค่อยเปลี่ยน</td>
          <td>ไม่ต้องลงทุนอะไรเลย</td>
          <td>เครื่องหยุดกะทันหัน ค่าเสียหายสูงสุด</td>
        </tr>
        <tr>
          <td><strong style="color:var(--accent3)">Preventive</strong><br><span style="color:var(--muted);font-size:0.75rem">เปลี่ยนตามรอบ</span></td>
          <td>เปลี่ยนทุก ๆ X ชั่วโมงตามตาราง</td>
          <td>ลดการพังกะทันหันได้มาก</td>
          <td>เปลี่ยนชิ้นส่วนที่ยังดีอยู่ทิ้ง = สิ้นเปลือง</td>
        </tr>
        <tr style="background:rgba(74,222,128,0.07)">
          <td><strong style="color:var(--good)">Predictive</strong><br><span style="color:var(--muted);font-size:0.75rem">เปลี่ยนตามสภาพจริง</span></td>
          <td>วัดสัญญาณจากตัวเครื่อง แล้วทำนายว่าจะพังเมื่อไร</td>
          <td>ใช้ชิ้นส่วนได้เต็มอายุ + วางแผนหยุดเครื่องล่วงหน้าได้</td>
          <td>ต้องมีเซ็นเซอร์ ข้อมูล และโมเดล</td>
        </tr>
      </tbody>
    </table>
    <div class="info-block green" style="margin-top:18px">
      <strong>📍 โปรเจกต์นี้อยู่ตรงไหน</strong><br>
      <span style="color:var(--muted);font-size:0.86rem;line-height:1.9">
        โปรเจกต์นี้คือชิ้นส่วน &quot;สมอง&quot; ของแนวทาง <strong style="color:var(--good)">Predictive Maintenance</strong> —
        รับสัญญาณสั่นสะเทือนที่วัดได้จริงจากลูกปืน แล้วแปลงเป็นตัวเลขบอกสุขภาพ
        สาขาวิชานี้เรียกว่า <strong style="color:var(--text)">PHM (Prognostics and Health Management)</strong>
      </span>
    </div>
  </div>
</section>

<!-- ═══ 2. ทำไมการสั่นบอกอะไรได้ ═══ -->
<section>
  <div class="section-title">2 &nbsp; ทำไม &quot;การสั่นสะเทือน&quot; ถึงบอกสุขภาพลูกปืนได้</div>
  <div class="card">
    <h3>📳 หลักการที่อยู่เบื้องหลังทั้งโปรเจกต์</h3>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95">
      ลูกปืนที่สมบูรณ์จะหมุนอย่างราบเรียบ ผิวสัมผัสเรียบสนิท การสั่นที่วัดได้จึงเป็นเพียง
      &quot;เสียงรบกวนพื้นหลัง&quot; ระดับต่ำและค่อนข้างสม่ำเสมอ
    </p>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95;margin-top:12px">
      แต่เมื่อผิวโลหะเริ่มมีรอยแตกเล็ก ๆ (จากความล้าของวัสดุ) ทุกครั้งที่ลูกกลิ้งวิ่งผ่านรอยนั้น
      จะเกิด<strong style="color:var(--text)">การกระแทกสั้น ๆ ที่คมมาก</strong>
      การกระแทกนี้ทำให้สัญญาณสั่นมี &quot;ยอดแหลม&quot; โผล่ขึ้นมาเป็นจังหวะ
      และเพราะมันเป็นการกระแทกที่สั้น พลังงานส่วนใหญ่จึงไปอยู่ที่<strong style="color:var(--text)">ย่านความถี่สูง</strong>
    </p>

    <div class="row-3" style="margin-top:20px">
      <div class="info-block green">
        <strong>ระยะที่ 1 — ปกติ</strong><br>
        <span style="color:var(--muted);font-size:0.82rem">
          สัญญาณราบเรียบ พลังงานต่ำ<br>
          ตัวชี้วัดทุกตัวนิ่ง
        </span>
      </div>
      <div class="info-block orange">
        <strong>ระยะที่ 2 — เริ่มมีรอย</strong><br>
        <span style="color:var(--muted);font-size:0.82rem">
          เริ่มมียอดแหลมเป็นจังหวะ<br>
          <strong style="color:var(--text)">Kurtosis / Crest Factor</strong> ขึ้นก่อน
          ทั้งที่พลังงานรวมยังแทบไม่เปลี่ยน
        </span>
      </div>
      <div class="info-block pink">
        <strong>ระยะที่ 3 — ใกล้พัง</strong><br>
        <span style="color:var(--muted);font-size:0.82rem">
          รอยขยายเป็นวงกว้าง<br>
          <strong style="color:var(--text)">RMS</strong> (พลังงานรวม) พุ่งขึ้นชัดเจน
        </span>
      </div>
    </div>

    <div class="info-block purple" style="margin-top:16px">
      <strong>🔑 นี่คือเหตุผลที่ต้องดูหลายตัวชี้วัดพร้อมกัน</strong><br>
      <span style="color:var(--muted);font-size:0.85rem;line-height:1.9">
        ถ้าดูแค่ &quot;แรงสั่นรวม&quot; (RMS) อย่างเดียว เราจะรู้ตัวก็ต่อเมื่อมันเข้าระยะที่ 3 ซึ่งสายเกินไป
        แต่ถ้าดูตัวชี้วัดที่จับ &quot;ความแหลม&quot; ของสัญญาณด้วย เราจะเห็นสัญญาณเตือนตั้งแต่ระยะที่ 2
        โปรเจกต์นี้จึงสกัดตัวชี้วัดออกมา 14 ตัวต่อลูกปืน แล้วให้โมเดลเรียนรู้ว่าจะรวมมันเข้าด้วยกันอย่างไร
      </span>
    </div>
  </div>
</section>

<!-- ═══ 3. เป้าหมาย ═══ -->
<section>
  <div class="section-title">3 &nbsp; โปรเจกต์นี้ทำอะไรกันแน่</div>
  <div class="card">
    <h3>🎯 สร้างโมเดลที่อ่านสัญญาณสั่น แล้วบอกคะแนนสุขภาพ</h3>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95">
      พูดให้ง่ายที่สุด: เราป้อน<strong style="color:var(--text)">ประวัติการสั่นย้อนหลังราว 3 ชั่วโมง</strong>
      เข้าไปในโมเดล แล้วให้มันตอบกลับมาเป็น<strong style="color:var(--text)">ตัวเลขตัวเดียวระหว่าง 0 ถึง 1</strong>
      ที่บอกว่าตอนนี้ลูกปืนสุขภาพดีแค่ไหน
    </p>

    <div class="row-3" style="margin-top:20px">
      <div class="info-block">
        <strong>📥 สิ่งที่ป้อนเข้าไป (Input)</strong><br>
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.85">
          ตาราง 20 แถว × 56 คอลัมน์<br>
          • 20 แถว = 20 ช่วงเวลาย้อนหลัง (~3 ชม.)<br>
          • 56 คอลัมน์ = ตัวชี้วัด 14 ตัว × ลูกปืน 4 ตัว
        </span>
      </div>
      <div class="info-block purple">
        <strong>⚙️ สิ่งที่อยู่ตรงกลาง (Model)</strong><br>
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.85">
          โครงข่ายประสาทเทียม (Neural Network)<br>
          ทดลอง 4 สถาปัตยกรรมที่ต่างกัน<br>
          เพื่อดูว่าแบบไหนเหมาะกับงานนี้ที่สุด
        </span>
      </div>
      <div class="info-block green">
        <strong>📤 สิ่งที่ได้ออกมา (Output)</strong><br>
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.85">
          Health Index ตัวเลขเดียว 0–1<br>
          • ใกล้ 1 = แข็งแรง<br>
          • ใกล้ 0 = ใกล้พัง
        </span>
      </div>
    </div>

    <div class="info-block" style="margin-top:16px">
      <strong>❓ ทำไมต้องใช้ Deep Learning ทำไมไม่ตั้งค่า threshold ธรรมดา</strong><br>
      <span style="color:var(--muted);font-size:0.86rem;line-height:1.9">
        การตั้งกฎแบบ &quot;ถ้า RMS เกิน X ให้เตือน&quot; มีปัญหาสองอย่าง —
        หนึ่ง ค่า X ที่เหมาะสมต่างกันไปตามเครื่อง ตามภาระงาน ตามความเร็วรอบ
        และสอง มันมองเห็นแค่ค่า ณ ขณะนั้น ไม่เห็น<strong style="color:var(--text)">แนวโน้ม</strong><br>
        โมเดลที่รับข้อมูลเป็นลำดับเวลาจะเห็นว่า &quot;ค่ากำลังไต่ขึ้นเรื่อย ๆ&quot;
        ซึ่งเป็นสัญญาณที่มีความหมายมากกว่าค่าดิบ ณ จุดเดียว
        และมันเรียนรู้ที่จะชั่งน้ำหนักตัวชี้วัดทั้ง 56 ตัวเองโดยที่เราไม่ต้องกำหนดกฎ
      </span>
    </div>
  </div>
</section>

<!-- ═══ 4. ข้อมูล ═══ -->
<section>
  <div class="section-title">4 &nbsp; ข้อมูลที่ใช้ — การทดลองเดินเครื่องจนพังจริง</div>
  <div class="card">
    <h3>💽 IMS Bearing Dataset (ชุด 2nd_test)</h3>
    <p style="color:var(--muted);font-size:0.9rem;line-height:1.95">
      ข้อมูลชุดนี้มาจาก <strong style="color:var(--text)">Center for Intelligent Maintenance Systems,
      University of Cincinnati</strong> เป็นชุดข้อมูลมาตรฐานที่งานวิจัยด้าน PHM ทั่วโลกใช้อ้างอิง
      จุดเด่นคือมันเป็นการทดลองแบบ <strong style="color:var(--text)">run-to-failure</strong> —
      คือเดินเครื่องจริงจนลูกปืนพังจริง ไม่ใช่การจำลอง
    </p>

    <div class="info-block" style="margin-top:16px">
      <strong>🔬 การทดลองทำอย่างไร</strong><br>
      <span style="color:var(--muted);font-size:0.86rem;line-height:1.95">
        ติดตั้งลูกปืน 4 ตัวบนเพลาเดียวกัน หมุนด้วยความเร็วคงที่ 2,000 รอบต่อนาที
        พร้อมกดภาระคงที่ประมาณ 6,000 ปอนด์ลงบนเพลา
        แล้วปล่อยให้เดินเครื่องต่อเนื่องจนกว่าจะมีลูกปืนพัง
        โดยติดเซ็นเซอร์วัดความเร่ง (accelerometer) ไว้ที่ลูกปืนแต่ละตัว
      </span>
    </div>

    <div class="mini-metrics" style="margin-top:20px">
      <div class="mini-metric"><div class="num">984</div><div class="lbl">ไฟล์ (จุดเวลา)</div></div>
      <div class="mini-metric"><div class="num">6.8 วัน</div><div class="lbl">12–19 ก.พ. 2004</div></div>
      <div class="mini-metric"><div class="num">4</div><div class="lbl">ลูกปืนที่วัด</div></div>
      <div class="mini-metric"><div class="num">20 kHz</div><div class="lbl">อัตราสุ่มสัญญาณ</div></div>
      <div class="mini-metric"><div class="num">20,480</div><div class="lbl">จุดข้อมูล / ไฟล์</div></div>
      <div class="mini-metric"><div class="num">10 นาที</div><div class="lbl">บันทึกทุก ๆ</div></div>
    </div>

    <div class="row-2" style="margin-top:20px">
      <div class="info-block purple">
        <strong>📁 หนึ่งไฟล์คืออะไร</strong><br>
        <span style="color:var(--muted);font-size:0.85rem;line-height:1.9">
          ทุก ๆ 10 นาที ระบบจะบันทึกสัญญาณสั่น<strong style="color:var(--text)">นาน 1 วินาที</strong>
          ด้วยอัตรา 20,000 ครั้งต่อวินาที<br>
          จึงได้ไฟล์ที่มี 20,480 แถว × 4 คอลัมน์ (คอลัมน์ละลูกปืน)<br>
          ชื่อไฟล์คือเวลาที่บันทึก เช่น <code style="color:var(--accent4)">2004.02.12.10.32.39</code><br><br>
          <strong style="color:var(--text)">984 ไฟล์ × 10 นาที = 6.8 วัน</strong> ของการเดินเครื่องต่อเนื่อง<br>
          <span style="opacity:0.85">
            ไฟล์แรก 12 ก.พ. 2004 เวลา 10:32 → ไฟล์สุดท้าย 19 ก.พ. 2004 เวลา 06:22
          </span>
        </span>
      </div>
      <div class="info-block pink">
        <strong>💀 สภาพลูกปืนเมื่อจบการทดลอง</strong><br>
        <span style="color:var(--muted);font-size:0.85rem;line-height:1.9">
          • <strong style="color:var(--accent1)">Bearing 1</strong> — ปกติดีตลอด<br>
          • <strong style="color:var(--accent2)">Bearing 2</strong> — ปกติดีตลอด<br>
          • <strong style="color:#f87171">Bearing 3</strong> — <strong>Outer Race Failure</strong>
            (วงแหวนรอบนอกแตก)<br>
          • <strong style="color:var(--accent3)">Bearing 4</strong> — <strong>Rolling Element Failure</strong>
            (ตัวลูกกลิ้งเสียหาย)<br><br>
          <span style="opacity:0.85">
            ตัวที่พังคือ 3 กับ 4 — กราฟด้านล่างจะเห็นสองเส้นนี้พุ่งขึ้นในช่วงท้ายอย่างชัดเจน
          </span>
        </span>
      </div>
    </div>
  </div>

  <div class="img-card" style="margin-top:20px">
    <div class="img-card-header">📉 การเสื่อมสภาพจริงที่มองเห็นได้ในข้อมูล</div>
    <img src="assets/rms_trend.png" alt="RMS trend" onerror="this.parentElement.style.display='none'">
    <div class="img-card-footer">
      <strong>กราฟบน</strong> — ค่า RMS (พลังงานการสั่นรวม) ของลูกปืนทั้ง 4 ตัวตลอด 984 จุดเวลา
      จะเห็นว่าเส้นค่อนข้างนิ่งเกือบตลอด แล้วพุ่งขึ้นเฉพาะช่วงท้าย นี่คือรูปแบบการเสื่อมที่พูดถึงในหัวข้อ 1
      &nbsp;|&nbsp;
      <strong>กราฟล่าง</strong> — Health Index ที่เราคำนวณขึ้นมาใช้เป็นคำตอบให้โมเดลเรียน (อธิบายในหัวข้อ 5.2)
    </div>
  </div>
</section>

<!-- ═══ 5. ความท้าทาย ═══ -->
<section>
  <div class="section-title">5 &nbsp; อุปสรรคสามข้อ และวิธีแก้</div>
  <p style="color:var(--muted);font-size:0.9rem;margin-bottom:20px;line-height:1.9">
    ข้อมูลดิบไม่สามารถโยนเข้าโมเดลได้ทันที มีปัญหาสามอย่างที่ต้องแก้ก่อน
    ซึ่งสามข้อนี้คือหัวใจของงาน — ส่วนการเทรนโมเดลจริง ๆ ใช้เวลาแค่ไม่กี่วินาที
  </p>

  <!-- 5.1 -->
  <div class="card">
    <h3><span class="step-num">1</span> ข้อมูลดิบใหญ่เกินไป → สกัดเป็น Features</h3>
    <p style="color:var(--muted);font-size:0.88rem;line-height:1.95">
      หนึ่งไฟล์มี 20,480 ตัวเลขต่อลูกปืน ถ้าเอาทั้ง 984 ไฟล์มากองรวมกันจะได้ตัวเลขเกือบ
      <strong style="color:var(--text)">80 ล้านตัว</strong> ซึ่งใหญ่เกินกว่าที่โมเดลลำดับเวลาจะรับไหว
      และส่วนใหญ่ก็เป็นข้อมูลซ้ำ ๆ ที่ไม่ได้ให้ข้อมูลเพิ่ม
    </p>
    <p style="color:var(--muted);font-size:0.88rem;line-height:1.95;margin-top:12px">
      ทางแก้คือ <strong style="color:var(--text)">Feature Extraction</strong> —
      บีบสัญญาณ 20,480 จุดให้เหลือตัวเลขที่สรุปลักษณะสำคัญไว้เพียง 14 ตัว
      โดยเลือกตัวที่วิศวกรรู้อยู่แล้วว่าไวต่อการเสื่อมของลูกปืน
    </p>

    <table style="margin-top:18px">
      <thead><tr><th>กลุ่ม</th><th>ตัวชี้วัด</th><th>อธิบายแบบภาษาคน</th></tr></thead>
      <tbody>
        <tr>
          <td><span class="pill time">เวลา</span></td>
          <td><strong>RMS, Peak, Peak-to-Peak, Std</strong></td>
          <td>สั่น<strong style="color:var(--text)">แรง</strong>แค่ไหน — ขึ้นชัดเจนตอนใกล้พัง</td>
        </tr>
        <tr>
          <td><span class="pill time">เวลา</span></td>
          <td><strong>Kurtosis, Crest Factor, Skewness</strong></td>
          <td>สั่น<strong style="color:var(--text)">แหลม</strong>แค่ไหน — จับการกระแทกจากรอยแตก ขึ้นก่อน RMS</td>
        </tr>
        <tr>
          <td><span class="pill time">เวลา</span></td>
          <td><strong>Shape, Impulse, Margin Factor</strong></td>
          <td>รูปร่างของคลื่นเปลี่ยนไปแค่ไหนเทียบกับตอนปกติ</td>
        </tr>
        <tr>
          <td><span class="pill freq">ความถี่</span></td>
          <td><strong>Band Energy (ต่ำ / กลาง / สูง)</strong></td>
          <td>พลังงานไปกองอยู่ที่ความถี่ไหน — ความถี่สูงเพิ่ม = มีการกระแทกโลหะ</td>
        </tr>
        <tr>
          <td><span class="pill freq">ความถี่</span></td>
          <td><strong>Spectral Centroid</strong></td>
          <td>&quot;จุดกึ่งกลาง&quot; ของความถี่ทั้งหมด — ยิ่งเสื่อมยิ่งเลื่อนไปทางสูง</td>
        </tr>
      </tbody>
    </table>

    <div class="info-block green" style="margin-top:18px">
      <span style="font-size:0.87rem;line-height:1.9">
        ผลลัพธ์: 14 ตัวชี้วัด × ลูกปืน 4 ตัว =
        <strong style="color:var(--good);font-size:1.15em">56 features</strong> ต่อหนึ่งจุดเวลา<br>
        <span style="color:var(--muted)">
          ข้อมูลถูกบีบจาก ~80 ล้านตัวเลข เหลือตาราง <code>(984, 56)</code> = 55,104 ตัวเลข
          <strong style="color:var(--text)">เล็กลงกว่า 1,400 เท่า</strong> แต่ยังเก็บข้อมูลที่จำเป็นไว้ครบ
        </span>
      </span>
    </div>

    <details class="more">
      <summary>ดูสูตรคำนวณครบทั้ง 14 features</summary>
      <div class="more-body">
        <table>
          <thead><tr><th>#</th><th>Feature</th><th>สูตร</th><th>ความหมาย</th></tr></thead>
          <tbody>
            <tr><td>1</td><td><strong>RMS</strong></td><td>√(Σx²/N)</td><td>พลังงานรวมของการสั่น</td></tr>
            <tr><td>2</td><td><strong>Peak</strong></td><td>max(|x|)</td><td>ค่าสูงสุดของแรงสั่น</td></tr>
            <tr><td>3</td><td><strong>Peak-to-Peak</strong></td><td>max − min</td><td>ช่วงกว้างของสัญญาณ</td></tr>
            <tr><td>4</td><td><strong>Crest Factor</strong></td><td>Peak / RMS</td><td>ยอดสูงกว่าค่าเฉลี่ยกี่เท่า — จับ impulsive fault</td></tr>
            <tr><td>5</td><td><strong>Kurtosis</strong></td><td>E[(x−μ)⁴]/σ⁴</td><td>ความแหลมของการกระจาย — ค่าสูง = มียอดโดดเยอะ</td></tr>
            <tr><td>6</td><td><strong>Skewness</strong></td><td>E[(x−μ)³]/σ³</td><td>ความเบ้ — สัญญาณเอียงไปทางบวกหรือลบ</td></tr>
            <tr><td>7</td><td><strong>Shape Factor</strong></td><td>RMS / mean|x|</td><td>ลักษณะรูปคลื่นโดยรวม</td></tr>
            <tr><td>8</td><td><strong>Impulse Factor</strong></td><td>Peak / mean|x|</td><td>ความรุนแรงของการกระแทก</td></tr>
            <tr><td>9</td><td><strong>Margin Factor</strong></td><td>Peak / (mean√|x|)²</td><td>ไวต่อการสึกหรอในระยะเริ่มต้น</td></tr>
            <tr><td>10</td><td><strong>Std</strong></td><td>σ(x)</td><td>ความผันแปรของสัญญาณ</td></tr>
            <tr><td>11</td><td><strong>Band Energy Low</strong></td><td>FFT 0 – 2.5 kHz</td><td>ความถี่ต่ำ (การหมุนของเพลา, ความไม่สมดุล)</td></tr>
            <tr><td>12</td><td><strong>Band Energy Mid</strong></td><td>FFT 2.5 – 7.5 kHz</td><td>ความถี่กลาง (ความผิดปกติของลูกปืน)</td></tr>
            <tr><td>13</td><td><strong>Band Energy High</strong></td><td>FFT 7.5 – 10 kHz</td><td>ความถี่สูง (โลหะกระแทกโลหะ, การสึก)</td></tr>
            <tr><td>14</td><td><strong>Spectral Centroid</strong></td><td>Σ(f·A) / ΣA</td><td>จุดศูนย์ถ่วงของสเปกตรัมความถี่</td></tr>
          </tbody>
        </table>
        <div class="info-block" style="margin-top:14px">
          <span style="color:var(--muted);font-size:0.82rem">
            10 ตัวแรกคำนวณจากสัญญาณตรง ๆ (time domain)
            ส่วน 4 ตัวหลังต้องแปลงสัญญาณเป็นสเปกตรัมความถี่ด้วย FFT ก่อน (frequency domain)
          </span>
        </div>
      </div>
    </details>
  </div>

  <!-- 5.2 -->
  <div class="card" style="margin-top:20px">
    <h3><span class="step-num purple">2</span> ไม่มีเฉลยให้โมเดลเรียน → สร้าง Health Index ขึ้นมาเอง</h3>
    <p style="color:var(--muted);font-size:0.88rem;line-height:1.95">
      การเทรนโมเดลแบบ supervised learning ต้องมี &quot;เฉลย&quot; คู่กับข้อมูลทุกตัวอย่าง
      แต่ข้อมูล IMS <strong style="color:var(--text)">ไม่ได้บอกว่าลูกปืนเหลืออายุอีกกี่ชั่วโมง</strong>
      บอกแค่ว่าเมื่อจบการทดลองแล้วตัวไหนพัง เราจึงต้องสร้างเฉลยขึ้นมาเอง
    </p>

    <p style="color:var(--muted);font-size:0.88rem;line-height:1.95;margin-top:14px">
      <strong style="color:var(--text)">มีสามทางเลือก และเราลองมาแล้วทั้งสามแบบ:</strong>
    </p>
    <table style="margin-top:12px">
      <thead><tr><th>วิธี</th><th>แนวคิด</th><th>ปัญหา</th><th>ผล</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>Linear RUL</strong></td>
          <td>สมมติสุขภาพลดลงเป็นเส้นตรงจาก 1 → 0</td>
          <td>ไม่ตรงความจริง — ลูกปืนปกติดีเกือบตลอดแล้วทรุดเร็วช่วงท้าย</td>
          <td style="color:#f87171">❌ โมเดลทำนายสวนทาง</td>
        </tr>
        <tr>
          <td><strong>Piecewise Linear</strong></td>
          <td>คงที่ที่ 1 ช่วงแรก แล้วค่อยลดลงช่วงท้าย</td>
          <td>ดีขึ้น แต่ยังต้องเดาเองว่าจุดเปลี่ยนอยู่ตรงไหน</td>
          <td style="color:var(--accent3)">⚠️ พอใช้ได้</td>
        </tr>
        <tr style="background:rgba(74,222,128,0.07)">
          <td><strong style="color:var(--good)">Health Index</strong></td>
          <td>คำนวณจากสัญญาณจริงที่วัดได้</td>
          <td>ต้องอ่านผลอย่างระวัง (ดูข้อจำกัดข้อ 1)</td>
          <td style="color:var(--good)">✅ เลือกใช้ตัวนี้</td>
        </tr>
      </tbody>
    </table>

    <div class="row-2" style="margin-top:20px">
      <div>
        <p style="color:var(--muted);font-size:0.87rem;line-height:1.95">
          <strong style="color:var(--text)">Health Index คำนวณยังไง</strong> —
          เอาตัวชี้วัดสามตัวที่ไวต่อการเสื่อมที่สุด (RMS, Kurtosis, Crest Factor)
          จากลูกปืนทั้ง 4 ตัว มาปรับสเกลให้เท่ากันแล้วบวกรวมเป็น &quot;คะแนนความเสื่อม&quot;
          จากนั้นเกลี่ยความสั่นของกราฟด้วยค่าเฉลี่ยเคลื่อนที่ แล้วกลับด้านเป็นคะแนนสุขภาพ
        </p>
        <div class="info-block purple" style="margin-top:14px">
          <strong>ทำไมต้องเกลี่ยด้วย rolling mean</strong><br>
          <span style="color:var(--muted);font-size:0.83rem">
            การวัดแต่ละครั้งมีสัญญาณรบกวนปนอยู่ ถ้าไม่เกลี่ย เฉลยจะกระโดดขึ้นลง
            ทำให้โมเดลสับสน การใช้ค่าเฉลี่ย 7 จุด (~70 นาที) ทำให้เส้นเฉลยเรียบขึ้นโดยยังคงแนวโน้มไว้
          </span>
        </div>
      </div>
      <div>
        <pre class="code-block"><span class="cmt"># สรุปการคำนวณ Health Index</span>
<span class="kw">def</span> <span class="fn">compute_health_index</span>(features, window=<span class="num">7</span>):
    <span class="cmt"># 1. ปรับ RMS + Kurtosis + Crest ของ</span>
    <span class="cmt">#    ลูกปืนทั้ง 4 ตัว ให้อยู่สเกล 0-1</span>
    degradation = sum(normalized_columns)

    <span class="cmt"># 2. ปรับคะแนนรวมให้อยู่ในช่วง 0-1</span>
    degradation /= degradation.max()

    <span class="cmt"># 3. เกลี่ยสัญญาณรบกวน</span>
    degradation = rolling_mean(window=<span class="num">7</span>)

    <span class="cmt"># 4. กลับด้าน: เสื่อมมาก = สุขภาพน้อย</span>
    <span class="kw">return</span> <span class="num">1.0</span> - degradation</pre>
      </div>
    </div>
  </div>

  <!-- 5.3 -->
  <div class="card" style="margin-top:20px">
    <h3><span class="step-num orange">3</span> ภาพนิ่งภาพเดียวไม่พอ → ใช้ Sliding Window</h3>
    <p style="color:var(--muted);font-size:0.88rem;line-height:1.95">
      ถ้าให้โมเดลดูข้อมูลแค่จุดเวลาเดียว มันจะเห็นแค่ &quot;ตอนนี้ค่าเท่านี้&quot;
      ซึ่งไม่พอที่จะบอกว่ากำลังเสื่อมหรือแค่สั่นผิดปกติชั่วคราว
      เราจึงป้อนข้อมูลเป็น<strong style="color:var(--text)">ช่วงเวลาต่อเนื่อง 20 จุด</strong>
      (20 × 10 นาที = ประมาณ 3 ชั่วโมง) เพื่อให้โมเดลเห็นแนวโน้ม
    </p>

    <div style="margin-top:22px;overflow-x:auto">
      <svg viewBox="0 0 760 230" width="100%" style="min-width:620px;display:block"
           role="img" aria-label="แผนภาพแสดงการเลื่อนหน้าต่างเวลา">
        <!-- row 1 -->
        <text x="10" y="34" fill="var(--muted)" font-size="12" font-family="Segoe UI, sans-serif">หน้าต่างที่ 1</text>
        <rect x="118" y="18" width="440" height="34" rx="7"
              fill="var(--accent1)" opacity="0.14" stroke="var(--accent1)" stroke-width="1.5"/>
        <g>
          <rect x="124" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="146" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="168" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <text x="200" y="40" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="240" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="262" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <text x="294" y="40" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="334" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="356" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <text x="388" y="40" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="428" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="450" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="472" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="494" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="516" y="24" width="16" height="22" rx="2" fill="var(--accent1)" opacity="0.75"/>
          <rect x="538" y="24" width="16" height="22" rx="2" fill="var(--good)" opacity="0.95"/>
        </g>
        <rect x="560" y="24" width="16" height="22" rx="2" fill="var(--border)"/>
        <rect x="582" y="24" width="16" height="22" rx="2" fill="var(--border)"/>
        <path d="M 546 56 L 546 74 L 640 74" stroke="var(--good)" stroke-width="1.5" fill="none"/>
        <text x="648" y="78" fill="var(--good)" font-size="12" font-family="Segoe UI, sans-serif">เฉลย</text>

        <!-- row 2 -->
        <text x="10" y="120" fill="var(--muted)" font-size="12" font-family="Segoe UI, sans-serif">หน้าต่างที่ 2</text>
        <rect x="140" y="104" width="440" height="34" rx="7"
              fill="var(--accent4)" opacity="0.14" stroke="var(--accent4)" stroke-width="1.5"/>
        <rect x="124" y="110" width="16" height="22" rx="2" fill="var(--border)"/>
        <g>
          <rect x="146" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="168" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <text x="200" y="126" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="240" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="262" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <text x="294" y="126" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="334" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="356" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <text x="388" y="126" fill="var(--muted)" font-size="13" font-family="Consolas, monospace">· · ·</text>
          <rect x="428" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="450" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="472" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="494" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="516" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="538" y="110" width="16" height="22" rx="2" fill="var(--accent4)" opacity="0.75"/>
          <rect x="560" y="110" width="16" height="22" rx="2" fill="var(--good)" opacity="0.95"/>
        </g>
        <rect x="582" y="110" width="16" height="22" rx="2" fill="var(--border)"/>
        <path d="M 568 142 L 568 160 L 640 160" stroke="var(--good)" stroke-width="1.5" fill="none"/>
        <text x="648" y="164" fill="var(--good)" font-size="12" font-family="Segoe UI, sans-serif">เฉลย</text>

        <!-- axis -->
        <line x1="118" y1="192" x2="600" y2="192" stroke="var(--border)" stroke-width="1.5"/>
        <polygon points="600,187 612,192 600,197" fill="var(--border)"/>
        <text x="118" y="214" fill="var(--muted)" font-size="11.5" font-family="Segoe UI, sans-serif">จุดเวลาที่ 1</text>
        <text x="500" y="214" fill="var(--muted)" font-size="11.5" font-family="Segoe UI, sans-serif">… จุดเวลาที่ 984</text>
        <text x="286" y="214" fill="var(--muted)" font-size="11.5" font-family="Segoe UI, sans-serif">เลื่อนทีละ 1 จุด →</text>
      </svg>
    </div>

    <div class="row-2" style="margin-top:18px">
      <div class="info-block orange">
        <strong>วิธีอ่านแผนภาพ</strong><br>
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
          แต่ละสี่เหลี่ยมคือหนึ่งจุดเวลา (ห่างกัน 10 นาที)<br>
          กล่องใหญ่คือหน้าต่าง 20 จุดที่ป้อนเข้าโมเดล<br>
          สี่เหลี่ยม<strong style="color:var(--good)">สีเขียว</strong>คือจุดสุดท้ายของหน้าต่าง —
          เราใช้ Health Index ของจุดนี้เป็นเฉลย<br>
          แล้วเลื่อนหน้าต่างไปทีละ 1 จุด ทำแบบนี้ไปเรื่อย ๆ
        </span>
      </div>
      <div class="info-block">
        <strong>ทำไมได้ 965 หน้าต่าง</strong><br>
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
          ข้อมูลมี 984 จุดเวลา หน้าต่างกว้าง 20 จุด<br>
          หน้าต่างแรกเริ่มที่จุด 1 หน้าต่างสุดท้ายเริ่มที่จุด 965<br>
          <strong style="color:var(--text)">984 − 20 + 1 = 965 หน้าต่าง</strong><br>
          แต่ละหน้าต่างคือหนึ่งตัวอย่างสำหรับเทรน
        </span>
      </div>
    </div>

    <details class="more">
      <summary>ดูวิธีแบ่งข้อมูลเป็น Train / Validation / Test</summary>
      <div class="more-body">
        <p style="color:var(--muted);font-size:0.85rem;line-height:1.9;margin-bottom:14px">
          เราต้องแบ่งข้อมูลเป็นสามส่วน เพราะถ้าวัดผลด้วยข้อมูลชุดเดียวกับที่ใช้สอน
          ก็เหมือนให้นักเรียนทำข้อสอบที่เคยเห็นเฉลยมาแล้ว — คะแนนสวยแต่ไม่ได้บอกว่าเก่งจริง
        </p>
        <table>
          <thead><tr><th>ชุด</th><th>สัดส่วน</th><th>จำนวน</th><th>ใช้ทำอะไร</th></tr></thead>
          <tbody>
            <tr><td style="color:var(--accent1);font-weight:700">Train</td><td>70%</td><td><strong>675</strong></td><td>ให้โมเดลเรียนรู้ ปรับน้ำหนักภายใน</td></tr>
            <tr><td style="color:var(--accent3);font-weight:700">Validation</td><td>15%</td><td><strong>144</strong></td><td>เช็คระหว่างเทรนว่าควรหยุดตอนไหน / เลือก checkpoint</td></tr>
            <tr><td style="color:var(--accent2);font-weight:700">Test</td><td>15%</td><td><strong>146</strong></td><td>ข้อสอบจริง ใช้ครั้งเดียวตอนจบ</td></tr>
          </tbody>
        </table>
        <table style="margin-top:16px">
          <thead><tr><th>พารามิเตอร์</th><th>ค่า</th><th>อธิบาย</th></tr></thead>
          <tbody>
            <tr><td>ขนาดหน้าต่าง</td><td><strong>20</strong></td><td>20 จุดเวลา = ~3 ชั่วโมง</td></tr>
            <tr><td>ระยะเลื่อน</td><td><strong>1</strong></td><td>เลื่อนทีละจุด เพื่อให้ได้ตัวอย่างมากที่สุด</td></tr>
            <tr><td>จำนวนหน้าต่าง</td><td><strong>965</strong></td><td>984 − 20 + 1</td></tr>
            <tr><td>ขนาดข้อมูลเข้า</td><td><strong>(B, 20, 56)</strong></td><td>batch × หน้าต่าง × features</td></tr>
          </tbody>
        </table>
        <div class="info-block pink" style="margin-top:16px">
          <strong>⚠️ ทำไมต้องสุ่มสลับก่อนแบ่ง (shuffle)</strong><br>
          <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
            ถ้าแบ่งตามลำดับเวลาตรง ๆ ชุด train จะได้แต่ช่วงที่ลูกปืนยังปกติ (70% แรกของการทดลอง)
            ส่วนชุด test จะเจอแต่ช่วงกำลังพัง โมเดลที่ไม่เคยเห็นสภาพเสื่อมเลยจะทำนายผิดทางทั้งหมด
            การสุ่มสลับทำให้ทุกชุดเห็นสภาพครบทุกระดับ<br>
            <span style="opacity:0.85">(วิธีนี้แลกมาด้วยข้อจำกัดข้อ 3 ที่ระบุไว้ในหัวข้อ 9)</span>
          </span>
        </div>
        <div class="info-block green" style="margin-top:12px">
          <strong>🔒 ป้องกันข้อมูลรั่ว (Data Leakage)</strong><br>
          <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
            ก่อนเข้าโมเดล ต้องปรับ features ทุกตัวให้อยู่สเกลใกล้เคียงกัน (Normalization)
            โดยใช้ค่าเฉลี่ยและส่วนเบี่ยงเบนของข้อมูล<br>
            สำคัญคือต้องคำนวณค่าเหล่านี้จาก<strong style="color:var(--text)">ชุด train เท่านั้น</strong>
            ถ้าเผลอใช้ข้อมูลทั้งหมด เท่ากับโมเดลได้แอบเห็นข้อมูลชุดทดสอบไปแล้ว ผลที่วัดได้จะดูดีเกินจริง
          </span>
        </div>
      </div>
    </details>
  </div>
</section>

<!-- ═══ 6. pipeline สรุป ═══ -->
<section>
  <div class="section-title">6 &nbsp; สรุปขั้นตอนทั้งหมดเป็นภาพเดียว</div>
  <div class="flow">
    <div class="flow-step">
      <span class="step-num">1</span>
      <div>
        <div class="title">📥 อ่านข้อมูลดิบ</div>
        <div class="desc">อ่าน 984 ไฟล์ → ก้อนข้อมูลขนาด (984, 20480, 4)</div>
      </div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">
      <span class="step-num purple">2</span>
      <div>
        <div class="title">🔬 สกัด Features</div>
        <div class="desc">บีบสัญญาณ 20,480 จุด เหลือ 14 ตัวเลขต่อลูกปืน → ตาราง (984, 56)</div>
      </div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">
      <span class="step-num green">3</span>
      <div>
        <div class="title">🏷️ สร้างเฉลย (Health Index)</div>
        <div class="desc">รวม RMS + Kurtosis + Crest Factor เป็นคะแนนสุขภาพ 0–1</div>
      </div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">
      <span class="step-num orange">4</span>
      <div>
        <div class="title">🪟 ตัดเป็นหน้าต่างเวลา</div>
        <div class="desc">Sliding window 20 จุด เลื่อนทีละ 1 → 965 ตัวอย่าง</div>
      </div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">
      <span class="step-num pink">5</span>
      <div>
        <div class="title">📊 แบ่งข้อมูล + ปรับสเกล</div>
        <div class="desc">Train 675 / Val 144 / Test 146 — ปรับสเกลด้วยค่าจาก train เท่านั้น</div>
      </div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step" style="border-color:var(--good)">
      <span class="step-num" style="background:var(--good);color:#000">✓</span>
      <div>
        <div class="title" style="color:var(--good)">เทรนและวัดผล 4 โมเดล</div>
        <div class="desc">เงื่อนไขเดียวกันทุกอย่าง ต่างกันแค่สถาปัตยกรรม</div>
      </div>
    </div>
  </div>
</section>

<!-- ═══ 7. โมเดล ═══ -->
<section>
  <div class="section-title">7 &nbsp; โมเดลทั้งสี่แบบ ต่างกันอย่างไร</div>
  <div class="card">
    <h3>🧠 ทุกตัวรับข้อมูลเหมือนกัน ต่างกันที่วิธี &quot;อ่าน&quot; ลำดับเวลา</h3>
    <table style="margin-top:6px">
      <thead><tr><th>โมเดล</th><th>อ่านข้อมูลอย่างไร</th><th>จุดเด่น</th></tr></thead>
      <tbody>
        <tr>
          <td><strong style="color:#f97316">🔁 LSTM</strong></td>
          <td>ไล่อ่านทีละจุดเวลาจากอดีตไปปัจจุบัน จำสิ่งที่ผ่านมาไว้ในหน่วยความจำภายใน</td>
          <td>เรียบง่าย เป็นมาตรฐานของงานลำดับเวลา</td>
        </tr>
        <tr>
          <td><strong style="color:#a78bfa">↔️ BiLSTM</strong></td>
          <td>อ่านสองรอบ — จากต้นไปท้าย และจากท้ายกลับมาต้น แล้วรวมสิ่งที่ได้</td>
          <td>ทุกจุดเวลาเห็นบริบททั้งก่อนและหลัง</td>
        </tr>
        <tr>
          <td><strong style="color:#4f8ef7">🧬 CNN-LSTM</strong></td>
          <td>ให้ CNN สรุปรูปแบบในช่วงสั้น ๆ ก่อน แล้วส่งผลสรุปให้ LSTM อ่านต่อ</td>
          <td>จับได้ทั้งรูปแบบเฉพาะที่และแนวโน้มระยะยาว</td>
        </tr>
        <tr>
          <td><strong style="color:#f472b6">🎯 Transformer</strong></td>
          <td>ให้ทุกจุดเวลามองเห็นกันทั้งหมดพร้อมกัน แล้วเลือกเองว่าจุดไหนสำคัญ</td>
          <td>ไม่ต้องไล่ตามลำดับ คำนวณขนานได้</td>
        </tr>
      </tbody>
    </table>
    <div class="info-block purple" style="margin-top:18px">
      <strong>⚖️ เทียบกันอย่างยุติธรรม</strong><br>
      <span style="color:var(--muted);font-size:0.85rem;line-height:1.9">
        ทั้งสี่โมเดลใช้ข้อมูลชุดเดียวกัน เฉลยเดียวกัน การแบ่งข้อมูลชุดเดียวกัน
        และวิธีเทรนเหมือนกันทุกประการ (ค่าเริ่มต้นการสุ่มก็ถูกรีเซ็ตให้เท่ากันก่อนสร้างทุกโมเดล)
        <strong style="color:var(--text)">สิ่งเดียวที่ต่างกันคือสถาปัตยกรรม</strong>
        ผลที่ออกมาจึงเทียบกันได้ตรง ๆ
      </span>
    </div>
  </div>

  <p style="color:var(--muted);font-size:0.88rem;margin:22px 0 16px">
    <strong style="color:var(--text)">คลิกที่การ์ดเพื่อดูผลของแต่ละโมเดลแบบละเอียด</strong> —
    แต่ละหน้ามีโครงสร้างทีละชั้น กราฟการเทรน กราฟทำนาย และการกระจายของความคลาดเคลื่อน
  </p>
  <div class="model-links">
__MODEL_CARDS__
  </div>
</section>

<!-- ═══ 8. อ่านผล ═══ -->
<section>
  <div class="section-title">8 &nbsp; วิธีอ่านผล — ตัวเลขแต่ละตัวแปลว่าอะไร</div>
  <div class="row-2">
    <div class="card">
      <h3>📏 ตัวชี้วัดที่ใช้</h3>
      <table>
        <thead><tr><th>ตัวชี้วัด</th><th>แปลว่า</th><th>ค่าที่ดี</th></tr></thead>
        <tbody>
          <tr>
            <td><strong>RMSE</strong></td>
            <td>ค่าคลาดเคลื่อนเฉลี่ย แต่ลงโทษความผิดพลาดก้อนใหญ่หนักเป็นพิเศษ</td>
            <td>ยิ่งน้อยยิ่งดี</td>
          </tr>
          <tr>
            <td><strong>MAE</strong></td>
            <td>ค่าคลาดเคลื่อนเฉลี่ยแบบตรงไปตรงมา ทุกความผิดพลาดนับเท่ากัน</td>
            <td>ยิ่งน้อยยิ่งดี</td>
          </tr>
          <tr>
            <td><strong>Pearson r</strong></td>
            <td>ค่าที่ทำนายขึ้นลงไปในทางเดียวกับค่าจริงแค่ไหน</td>
            <td>ใกล้ 1.0</td>
          </tr>
          <tr>
            <td><strong>R²</strong></td>
            <td>โมเดลอธิบายความผันแปรของสุขภาพได้กี่เปอร์เซ็นต์</td>
            <td>ใกล้ 1.0</td>
          </tr>
        </tbody>
      </table>
      <div class="info-block" style="margin-top:16px">
        <span style="color:var(--muted);font-size:0.83rem;line-height:1.9">
          <strong style="color:var(--text)">เคล็ดลับ:</strong> ถ้า RMSE สูงกว่า MAE มาก
          แปลว่ามีตัวอย่างส่วนน้อยที่โมเดลพลาดหนักมากจนดึงค่าเฉลี่ยขึ้น
          ซึ่งสำคัญกว่าค่าเฉลี่ยสวย ๆ ในงานบำรุงรักษา
        </span>
      </div>
    </div>

    <div class="card" style="border-color:rgba(249,115,22,0.3)">
      <h3>🧪 อย่าเพิ่งตื่นเต้นกับตัวเลขที่ดูน้อย</h3>
      <p style="color:var(--muted);font-size:0.87rem;line-height:1.95">
        RMSE ระดับ 0.00x ฟังดูแม่นมาก แต่ตัวเลขนี้จะมีความหมายก็ต่อเมื่อรู้ว่า
        <strong style="color:var(--text)">ค่าที่ต้องทายมันกระจายกว้างแค่ไหน</strong>
      </p>
      <div class="info-block orange" style="margin-top:14px">
        <strong>ความจริงที่ต้องรู้</strong><br>
        <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
          ใน test set ชุดนี้ <strong style="color:var(--accent3)">__CONC__%</strong>
          ของตัวอย่างมีค่า Health Index อยู่ในช่วงแคบ ๆ (±0.02 รอบค่ากลาง)
          เพราะลูกปืนปกติดีเกือบตลอดการทดลอง<br><br>
          แปลว่าถ้าโมเดล<strong style="color:var(--text)">โง่ ๆ ที่ทายค่าเฉลี่ยเท่ากันทุกครั้ง</strong>
          ก็จะได้ RMSE <strong style="color:var(--text)">__BASERMSE__</strong> แล้ว
          โดยไม่ต้องเรียนรู้อะไรเลย
        </span>
      </div>
      <div class="info-block green" style="margin-top:12px">
        <strong>✅ แล้วโมเดลของเราดีจริงไหม</strong><br>
        <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
          ดีจริง — ทุกโมเดลชนะ baseline นี้อย่างชัดเจน
          โดยดีขึ้น <strong style="color:var(--good)">__MINGAIN__–__MAXGAIN__%</strong>
          แปลว่ามันจับสัญญาณการเสื่อมได้จริง ไม่ได้แค่ทายค่ากลาง<br><br>
          <span style="opacity:0.9">
            แต่เวลาอ้างอิงผลไปเทียบกับงานวิจัยอื่น
            <strong style="color:var(--text)">ควรใช้ R² หรือ % ที่ดีกว่า baseline</strong>
            ไม่ใช่ RMSE ดิบ เพราะสเกลของเฉลยแต่ละงานไม่เท่ากัน
          </span>
        </span>
      </div>
      <div style="margin-top:14px">
        <a href="page__CMPPAGE__.html" style="color:var(--accent3);text-decoration:none;font-size:0.84rem;font-weight:600">
          ดูตาราง Sanity check เทียบ baseline แบบเต็ม →
        </a>
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:20px">
    <h3>📊 ผลลัพธ์ของทั้งสี่โมเดล</h3>
    <div class="chart-box"><canvas id="overviewChart"></canvas></div>
    <div class="info-block" style="margin-top:14px;padding:12px 16px">
      <span style="color:var(--muted);font-size:0.8rem">
        แท่งทึบคือ RMSE แท่งจางคือ MAE — ทั้งคู่ยิ่งเตี้ยยิ่งดี
      </span>
    </div>
  </div>
</section>

<!-- ═══ 9. สรุป ═══ -->
<section>
  <div class="section-title">9 &nbsp; สรุปผลและข้อจำกัด</div>
  <div class="row-2">
    <div class="card">
      <h3>✅ สิ่งที่ได้จากโปรเจกต์นี้</h3>
      <div class="info-block green">
        <span style="color:var(--muted);font-size:0.86rem;line-height:2">
          • Pipeline ครบวงจรตั้งแต่อ่านสัญญาณดิบจนได้ค่าทำนาย<br>
          • เทียบ 4 สถาปัตยกรรมบนเงื่อนไขเดียวกันอย่างยุติธรรม<br>
          • โมเดลที่ดีที่สุดคือ <strong style="color:__BEST_COLOR__">__BEST__</strong>
            (RMSE __BEST_RMSE__ · r __BEST_R__ · ดีกว่า baseline __BEST_GAIN__%)<br>
          • ใช้เวลาเทรนรวมทั้ง 4 โมเดลเพียง __TOTAL_TIME__ วินาทีบน CPU ธรรมดา
        </span>
      </div>
      <div class="info-block" style="margin-top:12px">
        <strong>📌 ข้อสังเกตที่น่าสนใจที่สุด</strong><br>
        <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
          โมเดลที่ซับซ้อนและมีพารามิเตอร์มากที่สุด<strong style="color:var(--text)">ไม่ได้ชนะ</strong>
          สถาปัตยกรรมที่เก็บรายละเอียดของลำดับเวลาไว้ครบทำได้ดีกว่าตัวที่บีบข้อมูลทิ้งไประหว่างทาง
          — เป็นตัวอย่างที่ดีว่าโมเดลใหญ่กว่าไม่ได้แปลว่าดีกว่าเสมอไป โดยเฉพาะเมื่อข้อมูลมีจำกัด
        </span>
      </div>
    </div>
    <div class="card">
      <h3>⚠️ ข้อจำกัดที่ต้องอ่านคู่กับตัวเลข</h3>
      <div class="info-block pink">
        <span style="color:var(--muted);font-size:0.84rem;line-height:1.95">
          <strong style="color:var(--text)">1. เฉลยถูกสร้างขึ้นเอง</strong><br>
          Health Index คำนวณจาก features ชุดเดียวกับที่ป้อนเข้าโมเดล
          จึงมีความสัมพันธ์กันอยู่ก่อนแล้วในระดับหนึ่ง ตัวเลขจึงดูดีกว่างานที่มีเฉลยอายุการใช้งานจริง<br><br>

          <strong style="color:var(--text)">2. เฉลยกระจุกตัว</strong><br>
          __CONC__% ของตัวอย่างมีค่าอยู่ในช่วงแคบ ทำให้ RMSE ดิบดูต่ำเกินจริง
          ต้องอ่านคู่กับ baseline เสมอ<br><br>

          <strong style="color:var(--text)">3. หน้าต่างซ้อนทับกัน</strong><br>
          หน้าต่างที่อยู่ติดกันใช้ข้อมูลร่วมกันถึง 19 จาก 20 จุด
          เมื่อสุ่มสลับแล้วแบ่ง ชุด test จึงไม่เป็นอิสระจากชุด train อย่างสมบูรณ์<br><br>

          <strong style="color:var(--text)">4. ทดสอบบนการทดลองเดียว</strong><br>
          ใช้เฉพาะ IMS 2nd_test ยังไม่ได้ยืนยันกับ 1st/3rd_test หรือเครื่องจักรอื่น<br><br>

          <strong style="color:var(--text)">5. รันครั้งเดียวต่อโมเดล</strong><br>
          ยังไม่ได้เทรนซ้ำหลายรอบ จึงยังบอกไม่ได้แน่ชัดว่าความต่างที่เห็นเกินความผันผวนจากการสุ่มหรือไม่
        </span>
      </div>
    </div>
  </div>
</section>

<!-- ═══ 10. ศัพท์ ═══ -->
<section>
  <div class="section-title">10 &nbsp; ศัพท์ที่เจอบ่อยในรายงานนี้</div>
  <div class="card">
    <table>
      <thead><tr><th>คำ</th><th>ความหมาย</th></tr></thead>
      <tbody>
        <tr><td><strong>RUL</strong> (Remaining Useful Life)</td><td>อายุการใช้งานที่เหลือก่อนชิ้นส่วนจะใช้ไม่ได้</td></tr>
        <tr><td><strong>PHM</strong></td><td>สาขาวิชาที่ศึกษาการทำนายสภาพและวางแผนบำรุงรักษาเครื่องจักร</td></tr>
        <tr><td><strong>Health Index (HI)</strong></td><td>คะแนนสุขภาพ 0–1 ที่เราสร้างขึ้นใช้เป็นเฉลย — สูง = ดี</td></tr>
        <tr><td><strong>Feature</strong></td><td>ตัวเลขที่สรุปลักษณะสำคัญของสัญญาณ เช่น RMS, Kurtosis</td></tr>
        <tr><td><strong>Sliding Window</strong></td><td>การตัดข้อมูลลำดับเวลาเป็นช่วง ๆ ที่เลื่อนไปเรื่อย ๆ</td></tr>
        <tr><td><strong>Epoch</strong></td><td>การเทรนหนึ่งรอบที่โมเดลได้เห็นข้อมูล train ครบทุกตัวอย่าง</td></tr>
        <tr><td><strong>Early Stopping</strong></td><td>หยุดเทรนอัตโนมัติเมื่อผลบนชุด validation ไม่ดีขึ้นแล้ว เพื่อกันการท่องจำ</td></tr>
        <tr><td><strong>Overfitting</strong></td><td>โมเดลท่องจำข้อมูลที่เคยเห็นได้ดี แต่ทำนายข้อมูลใหม่ไม่ได้</td></tr>
        <tr><td><strong>Baseline</strong></td><td>วิธีทำนายแบบง่ายที่สุดที่ใช้เป็นเกณฑ์เปรียบเทียบ</td></tr>
        <tr><td><strong>Data Leakage</strong></td><td>ข้อมูลชุดทดสอบรั่วเข้าไปในขั้นตอนเทรน ทำให้ผลดูดีเกินจริง</td></tr>
        <tr><td><strong>FFT</strong></td><td>วิธีแปลงสัญญาณจากโดเมนเวลาเป็นโดเมนความถี่</td></tr>
        <tr><td><strong>Outer Race</strong></td><td>วงแหวนรอบนอกของลูกปืน — จุดที่ Bearing 3 เสียหาย</td></tr>
      </tbody>
    </table>
  </div>
</section>

<!-- ═══ 11. รันเอง ═══ -->
<section>
  <div class="section-title">11 &nbsp; อยากลองรันเองต้องทำอย่างไร</div>
  <div class="card">
    <h3>💻 ทำซ้ำผลทั้งหมดได้ใน 4 คำสั่ง</h3>
    <pre class="code-block"><span class="cmt"># 1. ติดตั้ง dependencies</span>
pip install -r requirements.txt

<span class="cmt"># 2. แตกไฟล์ข้อมูล IMS</span>
python scripts/extract_data.py

<span class="cmt"># 3. เทรนและเปรียบเทียบทั้ง 4 โมเดล</span>
<span class="cmt">#    (รอบแรกจะอ่านไฟล์ดิบ 984 ไฟล์แล้ว cache features ไว้)</span>
python scripts/compare_models.py

<span class="cmt"># 4. สร้างรายงาน HTML ทุกหน้าจากผลที่ได้</span>
python scripts/make_report.py</pre>
    <div class="info-block green" style="margin-top:16px">
      <span style="color:var(--muted);font-size:0.84rem;line-height:1.9">
        ทุกหน้าในรายงานนี้ถูก<strong style="color:var(--text)">สร้างอัตโนมัติ</strong>จากไฟล์ผลการเทรน
        <code>outputs/comparison_results.json</code> — ไม่มีตัวเลขไหนถูกพิมพ์ด้วยมือ
        ถ้าเทรนใหม่แล้วรัน <code>make_report.py</code> ตัวเลขทุกหน้าจะอัปเดตตามทันที
      </span>
    </div>
  </div>
</section>
"""
