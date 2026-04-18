import streamlit as st
import time
import re
import pandas as pd

# --- ฟังก์ชันนับตัวอักษรแบบคน ---
def count_display_chars(text):
    text_without_vowels = re.sub(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]', '', text)
    return len(text_without_vowels)

# --- ฟังก์ชันบังคับใช้ Glossary ทั่วไป ---
def apply_glossary(text, glossary_dict):
    if not glossary_dict:
        return text
    modified_text = text
    for source_word, target_word in glossary_dict.items():
        if source_word.lower() == 'i':
            modified_text = modified_text.replace("ผม", target_word).replace("ฉัน", target_word)
        elif source_word.lower() == 'คุณ':
            modified_text = modified_text.replace("คุณ", target_word)
        else:
            pattern = re.compile(re.escape(source_word), re.IGNORECASE)
            modified_text = pattern.sub(target_word, modified_text)
    return modified_text

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
        value="กึ่งทางการ" 
    )
    
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด", 20, 50, 40)
    
    st.divider()
    st.subheader("📌 คลังคำศัพท์ (Glossary)")
    
    uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ Termbase (.xlsx)", type=['xlsx'])
    
    st.markdown("**หรือพิมพ์คำบังคับด่วน:**")
    glossary_input = st.text_area("รูปแบบ: คำต้นฉบับ=คำแปล", 
                                 placeholder="I=เรา\nคุณ=แก",
                                 height=100)
    
    master_glossary = {}
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=None)
            for index, row in df.iterrows():
                if pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]):
                    source_val = str(row.iloc[0]).strip()
                    target_val = str(row.iloc[1]).strip()
                    master_glossary[source_val] = target_val
            st.success(f"✅ โหลดศัพท์สำเร็จ {len(master_glossary)} คำ!")
            
            with st.expander("ดูรายการคำศัพท์ที่โหลดมา"):
                st.write(master_glossary)
                
        except Exception as e:
            st.error("เกิดข้อผิดพลาดในการอ่านไฟล์")

    if glossary_input:
        for line in glossary_input.split('\n'):
            if '=' in line:
                s, t = line.split('=', 1)
                master_glossary[s.strip()] = t.strip()

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

    timecode = st.text_input("⏱️ Timecode", value="00:01:23,400 --> 00:01:25,500")
    source_text = st.text_area("ประโยคต้นฉบับ (Source)", value=default_src, height=100)
    mt_text = st.text_area("คำแปลจากระบบ (MT)", value=default_mt, height=100)

# 4. ปุ่มประมวลผลและแสดงผลลัพธ์
if st.button("🚀 เริ่มการเกลาซับไตเติล", use_container_width=True):
    with st.spinner("🧠 AI กำลังคำนวณบริบทและตรวจสอบกฎ..."):
        time.sleep(1.5)
        
        st.success("ประมวลผลเสร็จสิ้น!")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tone Match", "100%")
        
        st.divider()
        st.subheader("✨ ผลลัพธ์ซับไตเติลที่แนะนำ")
        
        # --- ลอจิกจำลองผลลัพธ์ (อัปเกรดให้ฉลาดขึ้น) ---
        if context_choice == "ซีรีส์วัยรุ่น / Slice of Life":
            if formality_level == "กันเอง/สแลง":
                final_res = "แกรู้ปะ ว่าแกคือเซฟโซนของฉันนะ แกโอเคไหม?"
            else:
                final_res = "ผมอยากให้คุณรู้ว่าคุณคือพื้นที่ปลอดภัยของผม คุณจะว่าอะไรไหมครับ?"
            # กรองคำสรรพนามทั่วไป
            final_res = apply_glossary(final_res, master_glossary)
        
        elif context_choice == "ซีรีส์การแพทย์ (Medical Drama)":
            # จำลองความฉลาดของ AI: ถ้าเจอคำว่า IV push ใน Excel ให้เปลี่ยนโครงสร้างประโยคเป็นภาษาหมอเลย
            has_iv_push = any("iv push" in k.lower() for k in master_glossary.keys())
            
            if has_iv_push:
                # ดึงคำแปลจาก Excel มาใช้
                target_iv = next(v for k, v in master_glossary.items() if "iv push" in k.lower())
                final_res = f"คนไข้อาการทรุดแล้ว! ให้เอพิเนฟริน 50 มก. {target_iv} ทันที"
            else:
                # ถ้าไม่มี Glossary ให้แปลทื่อๆ ไปก่อน
                final_res = "คนไข้อาการแย่แล้ว! ให้เอพิเนฟริน 50 มก. ทางสายน้ำเกลือเดี๋ยวนี้"
                
        else: # ซีรีส์ย้อนยุค
            if formality_level == "ทางการ/ย้อนยุค":
                final_res = "ข้าจะไม่มีวันอภัยให้กบฏครั้งนี้ ทหาร! ลากตัวมันออกไป"
            else:
                final_res = "ฉันไม่ยกโทษให้คนทรยศหรอกนะ รปภ. ลากเขาออกไปที"

        # --- คำนวณความยาว ---
        display_length = count_display_chars(final_res)
        is_passed = "ผ่าน" if display_length <= char_limit else "เกินขีดจำกัด"
        
        m2.metric("Length Check", f"{display_length}/{char_limit}", is_passed, delta_color="normal" if is_passed == "ผ่าน" else "inverse")
        m3.metric("Glossary Sync", f"Active ({len(master_glossary)} words)" if master_glossary else "None")
        m4.metric("Formality", formality_level)

        st.info(f"**ซับไตเติลไฟนอล:** {final_res}")
        
        srt_content = f"1\n{timecode}\n{final_res}\n"
        st.download_button("💾 ดาวน์โหลดไฟล์ .srt", srt_content, "sub.srt", use_container_width=True)
