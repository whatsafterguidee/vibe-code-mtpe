import streamlit as st
import time

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="SubSync: AI Subtitle Localizer", page_icon="🎬", layout="centered")
st.title("🎬 SubSync: AI Subtitle Localizer")
st.markdown("เครื่องมือช่วยเกลาคำแปลซับไตเติลให้เข้ากับคาแรคเตอร์ บริบท และยุคสมัย")
st.divider()

# 2. สร้าง UI หน้าบ้าน (ปรับเป็น Top-Bottom Stack เพื่อให้รองรับ Mobile Size ได้ดีขึ้น)
context_choice = st.selectbox("🎭 เลือกบริบท/ความสัมพันธ์ตัวละคร", 
                              ["ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)", "ซีรีส์ย้อนยุค (สแลงยุค 90s)", "แฟนด้อม/วงการบันเทิง"])
glossary = st.text_input("📌 กฎเหล็ก/เงื่อนไขเพิ่มเติม (ถ้ามี)", placeholder="เช่น ห้ามเกิน 35 ตัวอักษร, ใช้คำลงท้ายว่า 'แก-ฉัน'")

# --- กลไกเปลี่ยนข้อความตั้งต้นตามบริบท ---
if context_choice == "ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)":
    default_src = "I just want you to know that you are my safe zone. Are you okay with that?"
    default_mt = "ฉันแค่อยากให้คุณรู้ว่าคุณคือโซนปลอดภัยของฉัน คุณโอเคกับสิ่งนั้นไหม?"
elif context_choice == "ซีรีส์ย้อนยุค (สแลงยุค 90s)":
    default_src = "That concert was totally awesome! I can't believe we got front row tickets."
    default_mt = "คอนเสิร์ตนั้นยอดเยี่ยมมาก! ฉันไม่อยากจะเชื่อเลยว่าเราได้ตั๋วแถวหน้า"
else:
    default_src = "Did you see their comeback stage? The center completely ate and left no crumbs!"
    default_mt = "คุณเห็นเวทีคัมแบ็คของพวกเขาไหม? เซ็นเตอร์กินหมดจดและไม่เหลือเศษเลย!"

st.write("") # เว้นบรรทัดนิดนึงให้ดูคลีน
source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", value=default_src, height=100)
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", value=default_mt, height=100)

# 3. กลไกจำลองผลลัพธ์
if st.button("🚀 เกลาซับไตเติลให้เป๊ะ!", use_container_width=True):
    with st.spinner("กำลังวิเคราะห์บริบทตัวละครและริมฝีปาก..."):
        time.sleep(1.5) 
        
        st.success("ประมวลผลเสร็จสิ้น!")
        
        # Dashboard สถิติซับไตเติล
        st.markdown("### 📊 Subtitle Metrics")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tone & Vibe", value="Natural", delta="100% Match")
        if context_choice == "ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)":
            m2.metric(label="Character Limit", value="32/35", delta="Pass", delta_color="normal")
            m3.metric(label="Relationship", value="Intimate")
        elif context_choice == "ซีรีส์ย้อนยุค (สแลงยุค 90s)":
             m2.metric(label="Slang Era", value="1990s", delta="Adjusted")
             m3.metric(label="Reading Speed", value="15 CPS", delta="Optimal")
        else:
             m2.metric(label="Pop Culture", value="Detected", delta="Idol Slang")
             m3.metric(label="Localization", value="High")
        
        st.divider()
        st.markdown("### ✨ ซับไตเติลที่แนะนำ")
        
        # ผลลัพธ์ตามหมวดหมู่
        if context_choice == "ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)":
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำแปลเดิมแข็งเกินไป ใช้คำว่า "คุณ-ฉัน" ซึ่งไม่เข้ากับบริบทเด็กนักเรียนวัยรุ่นที่สนิทกัน และคำว่า "สิ่งนั้น" ดูเป็นภาษาเขียนมากไป
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** ฉันแค่อยากให้แกรู้ว่าแกคือเซฟโซนของฉันนะ แกโอเคป่าว?
            * **Option 2 (Shorter):** แกคือเซฟโซนของฉันนะ แกโอเคไหม?
            
            **💡 ทริคการปรับ:** เปลี่ยนสรรพนามเป็น แก-ฉัน ให้ดูสนิทสนมขึ้น และปรับคำถามท้ายประโยคให้กระชับ เพื่อให้อ่านซับได้ทันภายใน 2 วินาที
            """)
        elif context_choice == "ซีรีส์ย้อนยุค (สแลงยุค 90s)":
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** คำว่า "ยอดเยี่ยมมาก" ดูเป็นทางการเกินไป ไม่เข้ากับอารมณ์วัยรุ่นที่กำลังตื่นเต้นกับคอนเสิร์ตในยุค 90 
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** คอนเสิร์ตโคตรจ๊าบเลย! ไม่อยากจะเชื่อว่าได้ตั๋วหน้าสุด
            * **Option 2 (Alternative):** งานนี้อย่างเจ๋งเป้ง! ไม่คิดเลยว่าจะกดบัตรแถวหน้าทัน
            
            **💡 ทริคการปรับ:** เติมสแลงยุค 90 อย่างคำว่า "จ๊าบ" หรือ "เจ๋งเป้ง" ลงไปแทนคำว่า awesome เพื่อดึง Vibe ของยุคสมัยออกมาให้ชัดเจนที่สุด
            """)
        else:
            st.info("""
            **🔍 วิเคราะห์ปัญหา:** "กินหมดจดและไม่เหลือเศษเลย" เป็นการแปลตรงตัวจากสแลง ate and left no crumbs ซึ่งทำให้คนดูงงแน่นอน
            
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** เห็นสเตจคัมแบ็กปะ? เซ็นเตอร์คือทำถึงมาก ปังไม่ไหว!
            * **Option 2 (Alternative):** สเตจคัมแบ็กคือเริ่ด! เซ็นเตอร์กินเรียบ ฆ่าได้ฆ่า
            
            **💡 ทริคการปรับ:** ต้องทำ Localization สแลงขั้นสุด โดยใช้คำศัพท์ด้อมในยุคปัจจุบันอย่าง "ทำถึง" หรือ "ปังไม่ไหว" เพื่อสื่อถึงความเพอร์เฟกต์ของการแสดง
            """)
