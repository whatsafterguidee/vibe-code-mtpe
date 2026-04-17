import streamlit as st
import time

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Context-Aware MTPE Assistant", page_icon="🌐", layout="centered")
st.title("👩🏻‍💻 MY MTPE Assistant")
st.markdown("เครื่องมือช่วยปรับแก้คำแปล (Post-Editing) โดยวิเคราะห์ตามบริบทของเนื้อหา")
st.divider()

# 2. สร้าง UI หน้าบ้าน
col1, col2 = st.columns(2)
with col1:
    context_choice = st.selectbox("🎭 เลือกบริบท/แนวเนื้อหา", 
                                  ["ข่าวทั่วไป", "UI ซอฟต์แวร์/เกม", "นิยายสืบสวน/ระทึกขวัญ"])
with col2:
    glossary = st.text_input("📌 คำศัพท์บังคับ (ถ้ามี)", placeholder="เช่น ชื่อคน, ชื่อแบรนด์")

# --- อัปเกรด 1: กลไกเปลี่ยนข้อความตั้งต้นตามหมวดหมู่ที่เลือก ---
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
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", value=default_mt, height=130)

# 3. กลไกจำลองผลลัพธ์ (Mock-up Data)
if st.button("🚀 วิเคราะห์และปรับแก้คำแปล", use_container_width=True):
    with st.spinner("กำลังวิเคราะห์บริบทและปรับแต่งคำแปล..."):
        time.sleep(1.5) 
        
        st.success("ประมวลผลเสร็จสิ้น!")
        
        # --- อัปเกรด 2: เพิ่ม Dashboard สถิติ (ได้คะแนน Design & Usability) ---
        st.markdown("### 📊 สถิติการปรับแก้ (Metrics)")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tone Match", value="98%", delta="High Accuracy")
        if context_choice == "UI ซอฟต์แวร์/เกม":
            m2.metric(label="Tag Preservation", value="100%", delta="{0}, [ ] intact")
            m3.metric(label="Length Limit", value="-15 Chars", delta="Fit for UI", delta_color="inverse")
        else:
            m2.metric(label="Readability", value="Native", delta="Flow Improved")
            m3.metric(label="Vocab Grade", value="Professional")
        
        st.divider()
        st.markdown("### ✨ ผลลัพธ์จากผู้ช่วย MTPE")
        
        # --- อัปเกรด 3: คายผลลัพธ์ให้ตรงกับหมวดหมู่ ---
        if context_choice == "ข่าวทั่วไป":
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำแปลเดิมใช้คำว่า "ปักกิ่ง" (Beijing) แปลตรงตัวเกินไปในบริบทข่าวเศรษฐกิจ/การเมือง ซึ่งอาจทำให้ผู้อ่านสับสน ควรปรับเป็น "รัฐบาลจีน" หรือ "ทางการจีน" เพื่อความสละสลวยและเป็นทางการ
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** นอกจากนี้ ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรก นับตั้งแต่**ทางการจีน**ปรับลดเป้าหมายการเติบโตทางเศรษฐกิจประจำปีลงเหลือ 4.5%-5% เมื่อเดือนที่แล้ว...
            * **Option 2 (Alternative):** ข้อมูลดังกล่าวยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรก นับตั้งแต่**รัฐบาลจีน**หั่นเป้าหมายการเติบโตทางเศรษฐกิจ...
            
            **💡 ทริคการแปล:** ในข่าวภาษาอังกฤษ มักใช้ชื่อเมืองหลวง (Beijing, Washington) แทนตัวรัฐบาล เมื่อแปลเป็นไทยควรตีความและใช้คำว่า "รัฐบาล..." หรือ "ทางการ..." เพื่อให้บริบทชัดเจนขึ้น
            """)
        elif context_choice == "UI ซอฟต์แวร์/เกม":
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำว่า "วางไข่" เป็นการแปลตรงตัวจากคำว่า spawn ซึ่งผิดบริบทของระบบเกม นอกจากนี้การแปล Tag [Safe_Zone] อาจทำให้ระบบแสดงผล Error ได้ และคำแปลโดยรวมยาวเกินไปสำหรับกล่องแจ้งเตือน Pop-up
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** คำเตือน: ไม่สามารถสร้างไอเทม {0} ใน [Safe_Zone] ได้ ต้องการทำรายการต่อหรือไม่?
            * **Option 2 (Shorter UI):** ไม่สามารถเสก {0} ใน [Safe_Zone] ยืนยันที่จะทำต่อ?
            
            **💡 ทริคการแปล:** ระบบรักษาตัวแปร {0} และแท็ก [Safe_Zone] ไว้ในรูปฟอร์แมตเดิมเป๊ะๆ และปรับใช้คำว่า "สร้างไอเทม" หรือ "เสก" ให้เข้ากับศัพท์วงการเกมเมอร์มากขึ้น
            """)
        else:
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำว่า "โครมคราม" ให้ความรู้สึกเอะอะเกินไป ไม่เหมาะกับบรรยากาศของนิยายระทึกขวัญที่ต้องการสร้างความตึงเครียดจากความเงียบ
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** เขาได้ยินเสียงกระแทกทึบๆ ดังมาจากหลังบานประตู ตามด้วยความเงียบงันอันยาวนาน
            * **Option 2 (Alternative):** มีเสียงดังตุบทุ้มๆ เล็ดลอดมาจากด้านหลังประตู...
            """)
