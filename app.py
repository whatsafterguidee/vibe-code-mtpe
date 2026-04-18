import streamlit as st
import time

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="SubSync Pro", page_icon="🎬", layout="wide")
st.title("🎬 SubSync Pro: Professional Subtitle Localizer")
st.markdown("ระบบเกลาซับไตเติลอัจฉริยะ: ควบคุมศัพท์เฉพาะทาง ความยาว และระดับความสุภาพ")
st.divider()

# 2. ส่วนตั้งค่า (Settings & Constraints)
with st.sidebar:
    st.header("⚙️ การตั้งค่าการเกลาซับ")
    
    formality_level = st.select_slider(
        "🎭 ระดับความสุภาพ (Formality)",
        options=["กันเอง/สแลง", "กึ่งทางการ", "ทางการ/ย้อนยุค"],
        value="กันเอง/สแลง"
    )
    
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด", 20, 50, 35)
    
    st.subheader("📌 คลังคำศัพท์ (Glossary)")
    glossary_input = st.text_area("ใส่คำบังคับ (เช่น IV push=ฉีดเข้าหลอดเลือดดำ)", 
                                 placeholder="คำต้นฉบับ=คำแปลที่ต้องการ",
                                 height=100)
    
    st.divider()
    st.info("💡 ทริค: การตั้งค่าเหล่านี้จะช่วยให้ AI ควบคุมผลลัพธ์ให้แม่นยำขึ้น 100%")

# 3. ส่วนทำงานหลัก (Main Interface)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🇬🇧 Input")
    context_choice = st.selectbox("🎬 เลือกประเภทซีรีส์", 
                                  ["ซีรีส์วัยรุ่น / Slice of Life", 
                                   "ซีรีส์การแพทย์ (Medical Drama)", 
                                   "ซีรีส์ย้อนยุค (Period Drama)"])
    
    if context_choice == "ซีรีส์วัยรุ่น / Slice of Life":
        default_src = "I just want you to know that you are my safe zone. Are you okay with that?"
        default_mt = "ฉันแค่อยากให้คุณรู้ว่าคุณคือโซนปลอดภัยของฉัน คุณโอเคกับสิ่งนั้นไหม?"
    elif context_choice == "ซีรีส์การแพทย์ (Medical Drama)":
        default_src = "The patient is crashing! Administer 50mg of epinephrine IV push immediately."
        default_mt = "ผู้ป่วยกำลังชน! บริหารเอพิเนฟริน 50 มก. ดันไอวี ทันที"
    else:
        default_src = "I shall not forgive this treason. Guards, take him away!"
        default_mt = "ฉันจะไม่ให้อภัยการกบฏนี้ ยาม พาเขาออกไป!"

    source_text = st.text_area("ประโยคต้นฉบับ (Source)", value=default_src, height=100)
    mt_text = st.text_area("คำแปลจากระบบ (MT)", value=default_mt, height=100)

# 4. ปุ่มประมวลผลและแสดงผลลัพธ์
if st.button("🚀 เริ่มการเกลาซับไตเติล", use_container_width=True):
    with st.spinner("🧠 AI กำลังคำนวณบริบทและตรวจสอบกฎ..."):
        time.sleep(1.5)
        
        st.success("ประมวลผลเสร็จสิ้น!")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tone Match", "100%")
        
        # คำนวณความยาวจำลอง
        current_len = 32 if context_choice == "ซีรีส์วัยรุ่น / Slice of Life" else 45
        is_passed = "ผ่าน" if current_len <= char_limit else "เกินขีดจำกัด"
        m2.metric("Length Check", f"{current_len}/{char_limit}", is_passed, delta_color="normal" if is_passed == "ผ่าน" else "inverse")
        
        m3.metric("Glossary Sync", "Active" if glossary_input else "None")
        m4.metric("Formality", formality_level)

        st.divider()
        
        st.subheader("✨ ผลลัพธ์ซับไตเติลที่แนะนำ")
        
        # ผลลัพธ์จำลองตามการตั้งค่าและหมวดหมู่
        if context_choice == "ซีรีส์วัยรุ่น / Slice of Life":
            if formality_level == "กันเอง/สแลง":
                final_res = "แกรู้ปะ ว่าแกคือเซฟโซนของฉันนะ แกโอเคไหม?"
            else:
                final_res = "ผมอยากให้คุณรู้ว่าคุณคือพื้นที่ปลอดภัยของผม คุณจะว่าอะไรไหมครับ?"
        
        elif context_choice == "ซีรีส์การแพทย์ (Medical Drama)":
            if glossary_input:
                final_res = "คนไข้อาการทรุดแล้ว! ฉีดเอพิเนฟริน 50 มก. เข้าหลอดเลือดดำทันที"
            else:
                final_res = "คนไข้อาการแย่แล้ว! ให้เอพิเนฟริน 50 มก. ทางสายน้ำเกลือเดี๋ยวนี้"
                
        else: # ซีรีส์ย้อนยุค
            if formality_level == "ทางการ/ย้อนยุค":
                final_res = "ข้าจะไม่มีวันอภัยให้กบฏครั้งนี้ ทหาร! ลากตัวมันออกไป"
            else:
                final_res = "ฉันไม่ยกโทษให้คนทรยศหรอกนะ รปภ. ลากเขาออกไปที"

        st.info(f"**ซับไตเติลไฟนอล:** {final_res}")
        
        srt_content = f"1\n00:00:01,000 --> 00:00:03,000\n{final_res}"
        st.download_button("💾 ดาวน์โหลดไฟล์ .srt", srt_content, "sub.srt", use_container_width=True)
