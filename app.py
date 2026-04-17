import streamlit as st
import requests
import json

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Context-Aware MTPE Assistant", page_icon="🌐", layout="centered")
st.title("🌐 MTPE Assistant: แปลเป๊ะ โทนปัง (AI Powered)")
st.markdown("เครื่องมือช่วยปรับแก้คำแปล (Post-Editing) ขับเคลื่อนด้วย AI วิเคราะห์ตามบริบท")
st.divider()

# 2. สร้าง UI หน้าบ้าน
col1, col2 = st.columns(2)
with col1:
    context_choice = st.selectbox("🎭 เลือกบริบท/แนวเนื้อหา", 
                                  ["ข่าวทั่วไป", "UI ซอฟต์แวร์/เกม", "นิยายสืบสวน/ระทึกขวัญ", "แปลอิสระ (Free Translation)"])
with col2:
    glossary = st.text_input("📌 คำศัพท์บังคับ (ถ้ามี)", placeholder="เช่น ชื่อคน, ชื่อแบรนด์")

# โหลดข้อความตัวอย่างตามบริบท
if context_choice == "ข่าวทั่วไป":
    default_src = "It also marks the first release of official GDP figures since Beijing cut its annual economic growth target last month to a range of 4.5%-5%, its lowest expansion goal since 1991."
    default_mt = "นอกจากนี้ยังถือเป็นการเปิดเผยตัวเลข GDP อย่างเป็นทางการครั้งแรกนับตั้งแต่ปักกิ่งปรับลดเป้าหมายการเติบโตทางเศรษฐกิจประจำปีลงเหลือ 4.5%-5% เมื่อเดือนที่แล้ว ซึ่งเป็นเป้าหมายการขยายตัวที่ต่ำที่สุดนับตั้งแต่ปี 1991"
elif context_choice == "UI ซอฟต์แวร์/เกม":
    default_src = "Warning: The target object {0} cannot be spawned in the [Safe_Zone]. Do you wish to proceed?"
    default_mt = "คำเตือน: วัตถุเป้าหมาย {0} ไม่สามารถวางไข่ได้ใน [โซนปลอดภัย] คุณต้องการดำเนินการต่อหรือไม่?"
else:
    default_src = ""
    default_mt = ""

source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", value=default_src, height=130)
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", value=default_mt, height=130)

# 3. ส่งคำสั่งไปหา AI ของจริงผ่าน REST API
if st.button("🚀 วิเคราะห์และปรับแก้คำแปล (ด้วย AI)", use_container_width=True):
    if source_text.strip() == "" or mt_text.strip() == "":
        st.warning("⚠️ กรุณาใส่ประโยคต้นฉบับและคำแปลให้ครบก่อนครับ")
    else:
        with st.spinner("🧠 AI กำลังวิเคราะห์บริบทและประมวลผล..."):
            
            # ดึงกุญแจจากระบบ
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            
            # ประกอบร่างสมอง AI (Prompt)
            master_prompt = f"""
            You are an Expert Translator and Machine Translation Post-Editing (MTPE) Specialist focusing on English to Thai translation. 
            Your task is to review the provided `Source Text` and its initial `Machine Translation` based on the user's specified `Context`.

            ### 🛑 STRICT CONSTRAINTS:
            1. Preserve all special characters, HTML tags, and placeholders (e.g., {{0}}, [ ], \\n) exactly as they are.
            2. Do not hallucinate external information.
            3. Adjust the tone to perfectly match the requested `Context`.
            4. If a Glossary is provided, you MUST use it.

            ### 📤 OUTPUT FORMAT (Respond entirely in THAI using Markdown):
            **🔍 วิเคราะห์ปัญหา:** (1-2 sentences explaining why the MT is awkward or incorrect for the context)
            **✨ คำแปลที่แนะนำ:** * **Option 1 (Best Fit):** ...
            * **Option 2 (Alternative):** ...
            **💡 ทริคการแปล:** (Brief note on word choice)

            ---
            **ข้อมูลสำหรับวิเคราะห์:**
            Context: {context_choice}
            Glossary: {glossary if glossary else 'None'}
            Source Text: {source_text}
            Machine Translation: {mt_text}
            """
            
            # จัดแพ็กเกจข้อมูลส่งให้ Google
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": master_prompt}]}],
                "generationConfig": {"temperature": 0.4} # คุมไม่ให้ AI มั่ว
            }
            
            try:
                # ยิง API ตรงๆ (ท่านี้ไม่พึ่งไลบรารี SDK)
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                
                # แกะกล่องเอาคำตอบออกมาโชว์
                if "candidates" in response_data:
                    ai_result = response_data['candidates'][0]['content']['parts'][0]['text']
                    st.success("✨ ประมวลผลเสร็จสิ้นด้วย AI ตัวจริง!")
                    st.markdown("### ผลลัพธ์จากผู้ช่วย MTPE")
                    st.info(ai_result)
                else:
                    st.error("เกิดข้อผิดพลาดจากเซิร์ฟเวอร์ AI กรุณาลองใหม่อีกครั้ง")
                    st.write(response_data) # เอาไว้ดูว่า Error อะไร
                    
            except Exception as e:
                st.error(f"🚨 ไม่สามารถเชื่อมต่อกับ AI ได้: {e}")
