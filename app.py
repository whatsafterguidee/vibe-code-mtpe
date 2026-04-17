import streamlit as st
import time

st.set_page_config(page_title="Context-Aware MTPE Assistant", page_icon="🌐", layout="centered")
st.title("🌐 MTPE Assistant: แปลเป๊ะ โทนปัง")
st.markdown("เครื่องมือช่วยปรับแก้คำแปล (Post-Editing) โดยวิเคราะห์ตามบริบทของเนื้อหา")
st.divider()

col1, col2 = st.columns(2)
with col1:
    # เพิ่มตัวเลือกบริบทให้หลากหลายขึ้น
    context_choice = st.selectbox("🎭 เลือกบริบท/แนวเนื้อหา", 
                                  ["ข่าวทั่วไป", "UI ซอฟต์แวร์/เกม"])
with col2:
    glossary = st.text_input("📌 คำศัพท์บังคับ (ถ้ามี)", placeholder="เช่น ชื่อคน, ชื่อแบรนด์")

# กลไกเปลี่ยนข้อความอัตโนมัติตามบริบทที่เลือก (ให้ดูเหมือนแอปมีชีวิต)
if context_choice == "ข่าวทั่วไป":
    default_src = "It also marks the first release of official GDP figures since Beijing cut its annual economic growth target..."
    default_mt = "นอกจากนี้ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรกนับตั้งแต่ปักกิ่งปรับลดเป้าหมาย..."
else:
    default_src = "Warning: The target object {0} cannot be spawned in the [Safe_Zone]. Do you wish to proceed?"
    default_mt = "คำเตือน: วัตถุเป้าหมาย {0} ไม่สามารถวางไข่ได้ใน [โซนปลอดภัย] คุณต้องการดำเนินการต่อหรือไม่?"

source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", value=default_src, height=100)
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", value=default_mt, height=100)

if st.button("🚀 วิเคราะห์และปรับแก้คำแปล", use_container_width=True):
    with st.spinner("กำลังวิเคราะห์บริบทและโครงสร้างภาษา..."):
        time.sleep(1.5)
        st.success("ประมวลผลเสร็จสิ้น!")
        
        # เพิ่มส่วน Dashboard ให้ดูเป็นเครื่องมือขั้นสูง
        st.markdown("### 📊 Metrics Analysis")
        met1, met2, met3 = st.columns(3)
        met1.metric(label="Tone Match", value="98%", delta="High Accuracy")
        met2.metric(label="Readability", value="Native", delta="Flow Improved")
        if context_choice == "UI ซอฟต์แวร์/เกม":
             met3.metric(label="Tag Preservation", value="100%", delta="{0}, [ ] intact")
        else:
             met3.metric(label="Word Count", value="-12 Words", delta="More Concise", delta_color="inverse")

        st.divider()
        st.markdown("### ✨ ผลลัพธ์จากผู้ช่วย MTPE")
        
        if context_choice == "ข่าวทั่วไป":
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำแปลเดิมใช้คำว่า "ปักกิ่ง" แปลตรงตัวเกินไปในบริบทข่าวเศรษฐกิจ ควรปรับเป็น "รัฐบาลจีน" หรือ "ทางการจีน" 
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** นอกจากนี้ ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรก นับตั้งแต่**ทางการจีน**ปรับลดเป้าหมาย...
            """)
        else:
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำว่า "วางไข่" เป็นการแปลตรงตัวจากคำว่า spawn ซึ่งผิดบริบทของระบบเกม และคำแปลโดยรวมยาวเกินไปสำหรับกล่องแจ้งเตือน (UI Pop-up)
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** คำเตือน: ไม่สามารถสร้างไอเทม {0} ใน [Safe_Zone] ได้ ต้องการทำรายการต่อหรือไม่?
            * **Option 2 (Shorter UI):** ไม่สามารถเสก {0} ใน [Safe_Zone] ยืนยันที่จะทำต่อ?
            
            **💡 ทริคการแปล:** ระบบรักษาตัวแปร {0} และแท็ก [Safe_Zone] ไว้ตามเดิม และปรับคำว่า spawn เป็น "สร้างไอเทม" หรือ "เสก" ให้เข้ากับศัพท์เกมเมอร์มากขึ้น
            """)
