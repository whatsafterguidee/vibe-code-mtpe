import streamlit as st
import time
import re # นำเข้าไลบรารีจัดการข้อความ

def count_display_chars(text):
    # สั่งให้ลบสระบน-ล่าง และวรรณยุกต์ทิ้งไปก่อนชั่วคราว
    # \u0e31 คือ ไม้หันอากาศ
    # \u0e34-\u0e3a คือ สระ อิ อี อึ อื อุ อู พินทุ
    # \u0e47-\u0e4e คือ ไม้ไต่คู้ วรรณยุกต์ และการันต์
    text_without_vowels = re.sub(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]', '', text)
    
    # พอลบทิ้งแล้ว ค่อยนับความยาวที่เหลือ
    return len(text_without_vowels)
import re

# --- ฟังก์ชันนับตัวอักษรแบบคน (ไม่นับสระลอย/วรรณยุกต์) ---
def count_display_chars(text):
    text_without_vowels = re.sub(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]', '', text)
    return len(text_without_vowels)

# --- ฟังก์ชันบังคับใช้ Glossary ให้ทำงานจริง ---
def apply_glossary(text, glossary_input):
    if not glossary_input:
        return text
    
    modified_text = text
    # แยกคำศัพท์ทีละบรรทัด
    for line in glossary_input.split('\n'):
        if '=' in line:
            source_word, target_word = line.split('=', 1)
            source_word = source_word.strip()
            target_word = target_word.strip()
            
            # ดักเคสพิเศษ ถ้าพิมพ์ I=เรา ให้แก้สรรพนาม ฉัน/ผม เป็น เรา ให้เนียนๆ
            if source_word.lower() == 'i':
                modified_text = modified_text.replace("ผม", target_word).replace("ฉัน", target_word)
            else:
                # ถ้าเป็นคำอื่นๆ ให้สับเปลี่ยนคำตรงๆ เลย (เช่น IV push=ฉีดเข้าหลอดเลือดดำ)
                modified_text = modified_text.replace(source_word, target_word)
                
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
        value="กึ่งทางการ" # ตั้งค่าเริ่มต้นตามรูปของคุณ
    )
    
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด", 20, 50, 35)
    
    st.subheader("📌 คลังคำศัพท์ (Glossary)")
    glossary_input = st.text_area("ใส่คำบังคับ (เช่น I=เรา, safe zone=พื้นที่ปลอดภัย)", 
                                 placeholder="คำต้นฉบับ=คำแปลที่ต้องการ\nขึ้นบรรทัดใหม่สำหรับคำต่อไป",
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
        
        # --- ลอจิกจำลองผลลัพธ์พื้นฐาน ---
        if context_choice == "ซีรีส์วัยรุ่น / Slice of Life":
            if formality_level == "กันเอง/สแลง":
                final_res = "แกรู้ปะ ว่าแกคือเซฟโซนของฉันนะ แกโอเคไหม?"
            else:
                final_res = "ผมอยากให้คุณรู้ว่าคุณคือพื้นที่ปลอดภัยของผม คุณจะว่าอะไรไหมครับ?"
        
        elif context_choice == "ซีรีส์การแพทย์ (Medical Drama)":
            final_res = "คนไข้อาการแย่แล้ว! ให้เอพิเนฟริน 50 มก. ทางสายน้ำเกลือเดี๋ยวนี้"
                
        else: # ซีรีส์ย้อนยุค
            if formality_level == "ทางการ/ย้อนยุค":
                final_res = "ข้าจะไม่มีวันอภัยให้กบฏครั้งนี้ ทหาร! ลากตัวมันออกไป"
            else:
                final_res = "ฉันไม่ยกโทษให้คนทรยศหรอกนะ รปภ. ลากเขาออกไปที"

        # --- สำคัญสุด! เอาผลลัพธ์มาผ่านเครื่องกรอง Glossary ก่อนแสดงผล ---
        final_res = apply_glossary(final_res, glossary_input)

        # --- คำนวณความยาว (ใช้ฟังก์ชันนับแบบคน) ---
        display_length = count_display_chars(final_res)
        is_passed = "ผ่าน" if display_length <= char_limit else "เกินขีดจำกัด"
        m2.metric("Length Check", f"{display_length}/{char_limit}", is_passed, delta_color="normal" if is_passed == "ผ่าน" else "inverse")
        
        m3.metric("Glossary Sync", "Active" if glossary_input else "None")
        m4.metric("Formality", formality_level)

        st.info(f"**ซับไตเติลไฟนอล:** {final_res}")
        
        srt_content = f"1\n{timecode}\n{final_res}\n"
        st.download_button("💾 ดาวน์โหลดไฟล์ .srt", srt_content, "sub.srt", use_container_width=True)
