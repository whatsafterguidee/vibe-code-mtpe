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
st.set_page_config(page_title="SubSync", page_icon="🎬", layout="wide")
st.title("🎬 SubSync: Your Subtitle Localization Assistant")
st.markdown("ระบบช่วยเกลาซับไตเติล: ควบคุมศัพท์เฉพาะทาง ความยาว และระดับความสุภาพ")
st.divider()

# 2. ส่วนตั้งค่า (Settings & Constraints)
with st.sidebar:
    theme_toggle = st.radio("🎨 Theme (ธีมหน้าจอ)", ["☀️ Light Mode", "🌙 Dark Mode"], horizontal=True)
    
    # --- CSS Injection สำหรับ Dark Mode (เวอร์ชันแก้ตาบอดสี!) ---
    if theme_toggle == "🌙 Dark Mode":
        st.markdown("""
        <style>
            /* เปลี่ยนพื้นหลังหลักและ Header */
            .stApp, .stApp > header { background-color: #0E1117 !important; }
            /* เปลี่ยนพื้นหลัง Sidebar */
            [data-testid="stSidebar"] { background-color: #262730 !important; }
            
            /* บังคับตัวอักษรทั้งหมดให้เป็นสีสว่าง (ขาว/เทาอ่อน) */
            p, h1, h2, h3, h4, h5, h6, label, span, .st-markdown { 
                color: #E0E0E0 !important; 
            }
            
            /* ปรับสีกล่องข้อความและ Dropdown */
            .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] > div { 
                background-color: #1E1E24 !important; 
                color: #FFFFFF !important; 
                border: 1px solid #555 !important; 
            }
            
            /* ปรับแต่งกล่อง Upload ไฟล์ให้ตัวอักษรสว่างขึ้น */
            [data-testid="stFileUploadDropzone"] div { color: #E0E0E0 !important; }
            
            /* ปรับสีของ Metrics (ตัวเลขสถิติ) */
            [data-testid="stMetricValue"] { color: #FFFFFF !important; }
            
            /* ปรับกรอบปุ่มกด */
            button { border-color: #555 !important; color: #E0E0E0 !important; }
        </style>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.header("⚙️ การตั้งค่า (Setting)")
    
    formality_level = st.select_slider(
        "🎭 ระดับความสุภาพ (Formality)",
        options=["กันเอง/สแลง", "กึ่งทางการ", "ทางการ/ย้อนยุค"],
        value="กึ่งทางการ" 
    )
    
    char_limit = st.slider("📏 จำกัดจำนวนตัวอักษรต่อบรรทัด (Chars. limit)", 20, 60, 45)
    
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
    st.subheader("🌐 Input")
    context_choice = st.selectbox("🎬 เลือกประเภทซีรีส์", 
                                  ["ซีรีส์วัยรุ่น / Slice of Life", 
                                   "ซีรีส์การแพทย์", 
                                   "ซีรีส์ย้อนยุค"])
    
    if context_choice == "ซีรีส์วัยรุ่น / Slice of Life (Stranger Things)":
        default_src = "There's more to life than stupid boys."
        default_mt = "มีอะไรในชีวิตมากกว่าเด็กผู้ชายโง่ๆ"
        timecode_val = "00:15:23,400 --> 00:15:25,500"
    elif context_choice == "ซีรีส์การแพทย์ (Grey's Anatomy)":
        default_src = "V-fib! Push 1 milligram of epi and charge paddles to 200."
        default_mt = "วีไฟบ์! ดันอีพาย 1 มิลลิกรัม และชาร์จไม้พายไปที่ 200"
        timecode_val = "00:22:10,100 --> 00:22:12,800"
    else:
        default_src = "You are the bane of my existence and the object of all my desires."
        default_mt = "คุณคือความหายนะของการดำรงอยู่ของฉันและเป็นวัตถุแห่งความปรารถนาทั้งหมดของฉัน"
        timecode_val = "00:45:30,000 --> 00:45:34,200"

    timecode = st.text_input("⏱️ Timecode", value=timecode_val)
    source_text = st.text_area("ประโยคต้นฉบับ(Source)", value=default_src, height=100)
    mt_text = st.text_area("คำแปลจากระบบ (MT)", value=default_mt, height=100)

# 4. ปุ่มประมวลผลและแสดงผลลัพธ์
if st.button("🚀 เริ่มการเกลาซับไตเติล", use_container_width=True):
    with st.spinner("🧠 AI กำลังประมวลผล Glossary Injection และปรับไวยากรณ์..."):
        time.sleep(1.8)
        
        st.success("ประมวลผลเสร็จสิ้น!")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tone Match", "100%")
        
        st.divider()
        st.subheader("✨ ผลลัพธ์ซับไตเติลที่แนะนำ")
        
        # --- ลอจิกจำลองผลลัพธ์ที่เนียนระดับ AI 100% ---
        if context_choice == "ซีรีส์วัยรุ่น / Slice of Life (Stranger Things)":
            if formality_level == "กันเอง/สแลง":
                final_res = "ชีวิตเรามีอะไรให้ทำอีกเยอะ ดีกว่ามานั่งงมงายกับผู้ชายงี่เง่านะแก"
            else:
                final_res = "ชีวิตยังมีอะไรอีกมากมาย มากกว่าแค่เรื่องผู้ชายแย่ๆ นะ"
            final_res = apply_glossary(final_res, master_glossary)
        
        elif context_choice == "ซีรีส์การแพทย์ (Grey's Anatomy)":
            has_medical_terms = any("epi" in k.lower() or "charge paddles" in k.lower() for k in master_glossary.keys())
            
            if has_medical_terms:
                final_res = "คนไข้หัวใจเต้นผิดจังหวะ! ฉีดเอพิเนฟริน 1 มิลลิกรัม แล้วชาร์จเครื่องกระตุกหัวใจที่ 200 จูล"
            else:
                final_res = "วีไฟบ์! ดันอีพาย 1 มิลลิกรัม และชาร์จไม้พายไปที่ 200"
                
        else: # ซีรีส์ย้อนยุค Bridgerton
            if formality_level == "ทางการ/ย้อนยุค":
                final_res = "ท่านคือความปั่นป่วนในชีวิตข้า และเป็นยอดปรารถนาเพียงหนึ่งเดียวของข้า"
            elif formality_level == "กันเอง/สแลง":
                final_res = "แกทำให้ชีวิตฉันวุ่นวาย แต่ฉันก็หยุดคิดถึงแกไม่ได้เลยจริงๆ"
            else:
                final_res = "คุณคือความวุ่นวายในชีวิตฉัน และเป็นเพียงสิ่งเดียวที่ฉันปรารถนา"
            final_res = apply_glossary(final_res, master_glossary)

        # --- คำนวณความยาว ---
        display_length = count_display_chars(final_res)
        is_passed = "ผ่าน" if display_length <= char_limit else "เกินขีดจำกัด"
        
        m2.metric("Length Check", f"{display_length}/{char_limit}", is_passed, delta_color="normal" if is_passed == "ผ่าน" else "inverse")
        m3.metric("Glossary Sync", f"Active ({len(master_glossary)} words)" if master_glossary else "None")
        m4.metric("Formality", formality_level)

        st.info(f"**ซับไตเติลไฟนอล:** {final_res}")
        
        srt_content = f"1\n{timecode}\n{final_res}\n"
        st.download_button("💾 ดาวน์โหลดไฟล์ .srt", srt_content, "sub.srt", use_container_width=True)
