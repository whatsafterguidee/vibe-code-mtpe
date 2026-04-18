import streamlit as st
import time
import re
import pandas as pd

# --- ฟังก์ชันนับตัวอักษรแบบคน ---
def count_display_chars(text):
    text_without_vowels = re.sub(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]', '', text)
    return len(text_without_vowels)

# --- ฟังก์ชันบังคับใช้ Glossary ทั่วไป (Fallback) ---
def apply_glossary(text, glossary_dict):
    if not glossary_dict:
        return text
    modified_text = text
    for source_word, target_word in glossary_dict.items():
        if source_word.lower() == 'i':
            modified_text = modified_text.replace("ผม", target_word).replace("ฉัน", target_word).replace("ข้า", target_word)
        elif source_word.lower() == 'you':
            modified_text = modified_text.replace("คุณ", target_word).replace("ท่าน", target_word)
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
    
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด", 20, 60, 45)
    
    st.divider()
    st.subheader("📌 คลังคำศัพท์ (Glossary)")
    
    uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ Termbase (.xlsx)", type=['xlsx'])
    
    st.markdown("**หรือพิมพ์คำบังคับด่วน:**")
    glossary_input = st.text_area("รูปแบบ: คำต้นฉบับ=คำแปล", 
                                 placeholder="epi=เอพิเนฟริน\ncharge paddles=ชาร์จเครื่องกระตุกหัวใจ",
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
                                  ["ซีรีส์วัยรุ่น / Slice of Life (Stranger Things)", 
                                   "ซีรีส์การแพทย์ (Grey's Anatomy)", 
                                   "ซีรีส์ย้อนยุค (Bridgerton)"])
    
    if context_choice == "ซีรีส์วัยรุ่น / Slice of Life (Stranger Things)":
        default_src = "There's more to life than stupid boys."
        default_mt = "มีอะไรในชีวิตมากกว่าเด็กผู้ชายโง่ๆ"
        timecode_val = "00:15:23,400 --> 00:15:25,500"
    elif context_choice == "ซีรีส์การแพทย์ (Grey's Anatomy)":
        default_src = "V-fib! Push 1 milligram of epi and charge paddles to 200."
        default_mt = "วีไฟบ์! ดันอีพาย 1 มิลลิกรัม
