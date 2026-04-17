import streamlit as st
import time

# 1. ตั้งค่าหน้าเพจ (ปรับให้กว้างขึ้นนิดนึงเพื่อโชว์ UI แบบโปร)
st.set_page_config(page_title="MY MTPE Assistant", page_icon="👩🏻‍💻", layout="centered")

# --- อัปเกรด 1: เพิ่ม Sidebar ให้ดูเป็นเครื่องมือระดับ Advanced ---
with st.sidebar:
    st.header("⚙️ ตั้งค่าขั้นสูง (Advanced)")
    tone_setting = st.radio("🎚️ ระดับการปรับแก้ (Post-Edit Level)", 
                            ["Light PE (เน้นความถูกต้อง)", "Full PE (ปรับให้อ่านเป็นธรรมชาติ)", "Transcreation (เน้นอารมณ์/บริบท)"],
                            index=1)
    st.divider()
    st.caption("✨ Powered by MTPE Context-Aware Logic")

# 2. ส่วนหัวของแอป
st.title("👩🏻‍💻 Guide to MTPE: MY MTPE Assistant")
st.markdown("เครื่องมือช่วยปรับแก้คำแปล (Post-Editing) โดยวิเคราะห์ตามบริบทของเนื้อหาและคำศัพท์บังคับ")
st.divider()

# 3. สร้าง UI หน้าบ้าน
col1, col2 = st.columns(2)
with col1:
    context_choice = st.selectbox("🎭 เลือกบริบท/แนวเนื้อหา", 
                                  ["ข่าวทั่วไป", "UI ซอฟต์แวร์/เกม", "นิยายสืบสวน/ระทึกขวัญ"])
with col2:
    glossary = st.text_input("📌 คำศัพท์บังคับ (Glossary)", placeholder="พิมพ์คำที่ต้องการบังคับใช้")

# กลไกเปลี่ยนข้อความอัตโนมัติตามบริบทที่เลือก
if context_choice == "ข่าวทั่วไป":
    default_src = "It also marks the first release of official GDP figures since Beijing cut its annual economic growth target last month to a range of 4.5%-5%, its lowest expansion goal since 1991."
    default_mt = "นอกจากนี้ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรกนับตั้งแต่ปักกิ่งปรับลดเป้าหมายการเติบโตทางเศรษฐกิจประจำปีลงเหลือ 4.5%-5% เมื่อเดือนที่แล้ว ซึ่งเป็นเป้าหมายการขยายตัวที่ต่ำที่สุดนับตั้งแต่ปี 1991"
elif context_choice == "UI ซอฟต์แวร์/เกม":
    default_src = "Warning: The target object {0} cannot be spawned in the [Safe_Zone]. Do you wish to proceed?"
    default_mt = "คำเตือน: วัตถุเป้าหมาย {0} ไม่สามารถวางไข่ได้ใน [โซนปลอดภัย] คุณต้องการดำเนินการต่อหรือไม่?"
else:
    default_src = "He heard a dull thump behind the door, followed by a long silence."
    default_mt = "เขาได้ยินเสียงโครมครามดังมาจากหลังประตู ตามด้วยความเงียบงันอันยาวนาน"

source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", value=default_src, height=130)
mt_text = st.text_area("🤖 คำแปลจากระบบ MT", value=default_mt, height=130)

# 4. กลไกจำลองผลลัพธ์ (Smart Mock-up)
if st.button("🚀 วิเคราะห์และปรับแก้คำแปล", use_container_width=True, type="primary"):
    with st.spinner(f"กำลังประมวลผลโหมด {tone_setting}..."):
        time.sleep(1.8) # หน่วงเวลา
        
        st.success("ประมวลผลเสร็จสิ้น!")
        
        # --- อัปเกรด 2: ระบบตอบสนองต่อ Glossary ---
        if glossary:
            st.info(f"✅ ตรวจพบ Glossary: ระบบได้บังคับใช้คำว่า **'{glossary}'** ในผลลัพธ์แล้ว")
        
        # Dashboard สถิติ
        st.markdown("### 📊 สถิติการปรับแก้ (Metrics)")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tone Match", value="98%", delta="High Accuracy")
        if context_choice == "UI ซอฟต์แวร์/เกม":
            m2.metric(label="Tag Preservation", value="100%", delta="{0}, [ ] intact")
            m3.metric(label="Length Limit", value="-15 Chars", delta="Fit for UI", delta_color="inverse")
        else:
            m2.metric(label="Readability", value="Native", delta="Flow Improved")
            m3.metric(label="Fluency", value="Excellent", delta="Reduced literal translation")
        
        st.divider()
        
        # --- อัปเกรด 3: จัด Layout ผลลัพธ์แบบ Tab ให้ดูโปร ---
        st.markdown("### ✨ ผลลัพธ์การปรับแก้")
        tab1, tab2 = st.tabs(["📝 คำแปลที่แนะนำ (พร้อมก๊อปปี้)", "🔍 เทียบจุดที่แก้ไข (Diff)"])
        
        with tab1:
            if context_choice == "ข่าวทั่วไป":
                st.write("**Option 1 (Best Fit):**")
                st.code("นอกจากนี้ ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรก นับตั้งแต่ทางการจีนปรับลดเป้าหมายการเติบโตทางเศรษฐกิจประจำปีลงเหลือ 4.5%-5% เมื่อเดือนที่แล้ว ซึ่งเป็นเป้าหมายการขยายตัวที่ต่ำที่สุดนับตั้งแต่ปี 1991", language="text")
                st.write("**Option 2 (Alternative):**")
                st.code("ข้อมูลดังกล่าวยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรก นับตั้งแต่รัฐบาลจีนหั่นเป้าหมายการเติบโตทางเศรษฐกิจ...", language="text")
                
            elif context_choice == "UI ซอฟต์แวร์/เกม":
                st.write("**Option 1 (Best Fit - โหมดเกมเมอร์):**")
                st.code("คำเตือน: ไม่สามารถสร้างไอเทม {0} ใน [Safe_Zone] ได้ ต้องการทำรายการต่อหรือไม่?", language="text")
                st.write("**Option 2 (Shorter UI - สำหรับจอมือถือ):**")
                st.code("ไม่สามารถเสก {0} ใน [Safe_Zone] ยืนยันที่จะทำต่อ?", language="text")
                
            else:
                st.write("**Option 1 (Best Fit - คงความระทึกขวัญ):**")
                st.code("เขาได้ยินเสียงกระแทกทึบๆ ดังมาจากหลังบานประตู ตามด้วยความเงียบงันอันยาวนาน", language="text")
        
        with tab2:
            st.markdown("ระบบได้ทำการปรับแก้คำแปล (Post-Editing) เพื่อให้เข้ากับบริบทดังนี้:")
            if context_choice == "ข่าวทั่วไป":
                st.markdown("> ...นับตั้งแต่ ~~ปักกิ่ง~~ 👉 **ทางการจีน** ปรับลดเป้าหมาย...")
                st.caption("💡 **เหตุผล:** ข่าวภาษาอังกฤษมักใช้ชื่อเมืองหลวงแทนรัฐบาล การแปลตรงตัวจะทำให้เสียอรรถรสในภาษาไทย")
            elif context_choice == "UI ซอฟต์แวร์/เกม":
                st.markdown("> ...ไม่สามารถ ~~วางไข่ได้ใน [โซนปลอดภัย]~~ 👉 **สร้างไอเทม ใน [Safe_Zone]**...")
                st.caption("💡 **เหตุผล:** ป้องกัน String Tags เสียหาย และปรับศัพท์ให้เข้ากับ UI ของเกม")
            else:
                st.markdown("> เขาได้ยินเสียง ~~โครมคราม~~ 👉 **กระแทกทึบๆ** ดังมาจากหลังประตู...")
                st.caption("💡 **เหตุผล:** น้ำหนักเสียง 'โครมคราม' ไม่ตรงกับ 'dull thump' และทำลายบรรยากาศเงียบสงัดของนิยาย")
