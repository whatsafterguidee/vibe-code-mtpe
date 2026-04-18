import streamlit as st
import time

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="SubSync Pro", page_icon="🎬", layout="wide")
st.title("🎬 SubSync Pro: Professional Subtitle Localizer")
st.markdown("ระบบเกลาซับไตเติลอัจฉริยะ: ควบคุมศัพท์เฉพาะทาง ความยาว และระดับความสุภาพ")
st.divider()

# 2. ส่วนตั้งค่า (Settings & Constraints) - ใช้ Sidebar เพื่อความโปร
with st.sidebar:
    st.header("⚙️ การตั้งค่าการเกลาซับ")
    
    # ฟีเจอร์ 1: Formality Level
    formality_level = st.select_slider(
        "🎭 ระดับความสุภาพ (Formality)",
        options=["กันเอง/สแลง", "กึ่งทางการ", "ทางการ"],
        value="กันเอง/สแลง"
    )
    
    # ฟีเจอร์ 2: Character Limit
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด", 20, 50, 35)
    
    # ฟีเจอร์ 3: Glossary Management
    st.subheader("📌 คลังคำศัพท์ (Glossary)")
    glossary_input = st.text_area("ใส่คำบังคับ (เช่น Beijing=ทางการจีน)", 
                                 placeholder="คำต้นฉบับ=คำแปลที่ต้องการ",
                                 height=100)
    
    st.divider()
    st.info("💡 ทริค: การตั้งค่าเหล่านี้จะช่วยให้ AI ควบคุมผลลัพธ์ให้แม่นยำขึ้น 100%")

# 3. ส่วนทำงานหลัก (Main Interface)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🇬🇧 Input")
    context_choice = st.selectbox("เลือกประเภทซีรีส์", ["ซีรีส์วัยรุ่น", "ข่าวการเมือง/เศรษฐกิจ"])
    
    if context_choice == "ซีรีส์วัยรุ่น":
        default_src = "I just want you to know that you are my safe zone. Are you okay with that?"
        default_mt = "ฉันแค่อยากให้คุณรู้ว่าคุณคือโซนปลอดภัยของฉัน คุณโอเคกับสิ่งนั้นไหม?"
    else:
        default_src = "Beijing officials reported that the city's GDP has exceeded expectations."
        default_mt = "เจ้าหน้าที่ปักกิ่งรายงานว่า GDP ของเมืองเกินความคาดหมาย"

    source_text = st.text_area("ประโยคต้นฉบับ (Source)", value=default_src, height=100)
    mt_text = st.text_area("คำแปลจากระบบ (MT)", value=default_mt, height=100)

# 4. ปุ่มประมวลผลและแสดงผลลัพธ์
if st.button("🚀 เริ่มการเกลาซับไตเติล", use_container_width=True):
    with st.spinner("🧠 AI กำลังคำนวณบริบทและตรวจสอบกฎ..."):
        time.sleep(1.5)
        
        # ส่วน Metrics (แสดงคะแนนความเป๊ะ)
        st.success("ประมวลผลเสร็จสิ้น!")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tone Match", "100%")
        
        # จำลองการตรวจสอบความยาว
        current_len = 32 if context_choice == "ซีรีส์วัยรุ่น" else 34
        is_passed = "ผ่าน" if current_len <= char_limit else "เกินขีดจำกัด"
        m2.metric("Length Check", f"{current_len}/{char_limit}", is_passed)
        
        m3.metric("Glossary Sync", "Active" if glossary_input else "None")
        m4.metric("Formality", formality_level)

        st.divider()
        
        # ผลลัพธ์จำลองตามการตั้งค่า
        st.subheader("✨ ผลลัพธ์ซับไตเติลที่แนะนำ")
        
        if context_choice == "ซีรีส์วัยรุ่น":
            if formality_level == "กันเอง/สแลง":
                final_res = "แกรู้ปะ ว่าแกคือเซฟโซนของฉันนะ แกโอเคไหม?"
            else:
                final_res = "ผมอยากให้คุณรู้ว่าคุณคือพื้นที่ปลอดภัยของผม คุณจะว่าอะไรไหมครับ?"
        else:
            # จำลองการใช้ Glossary: เปลี่ยน Beijing เป็น ทางการจีน
            final_res = "ทางการจีนรายงานว่า ตัวเลข GDP สูงกว่าที่คาดการณ์ไว้"

        st.info(f"**ซับไตเติลไฟนอล:** {final_res}")
        
        # ปุ่ม Export
        srt_content = f"1\n00:00:01,000 --> 00:00:03,000\n{final_res}"
        st.download_button("💾 ดาวน์โหลดไฟล์ .srt", srt_content, "sub.srt", use_container_width=True)
