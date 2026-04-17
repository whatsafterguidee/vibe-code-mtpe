import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Context-Aware MTPE Assistant", page_icon="🌐", layout="centered")
st.title("🌐 MTPE Assistant: แปลเป๊ะ โทนปัง")
st.markdown("เครื่องมือช่วยปรับแก้คำแปล (Post-Editing) โดยวิเคราะห์ตามบริบทของเนื้อหา")

# 2. เชื่อมต่อ API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. ตั้งค่าโมเดล (ใช้ gemini-pro ธรรมดาที่เสถียรที่สุด)
model = genai.GenerativeModel('gemini-pro')

# 4. สร้างหน้าตา UI
st.divider()

col1, col2 = st.columns(2)
with col1:
    context_choice = st.selectbox("🎭 เลือกบริบท/แนวเนื้อหา", 
                                  ["นิยายสืบสวน/ระทึกขวัญ", "นิยายโรแมนติก", "บทความวิชาการ/การแพทย์", "UI ซอฟต์แวร์/เกม", "ข่าวทั่วไป"])
with col2:
    glossary = st.text_input("📌 คำศัพท์บังคับ (ถ้ามี)", placeholder="เช่น ชื่อคน, ชื่อแบรนด์")

source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", height=100)
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", height=100)

# 5. ปุ่มกดเพื่อสั่งให้ AI ทำงาน
if st.button("🚀 วิเคราะห์และปรับแก้คำแปล", use_container_width=True):
    if source_text and mt_text:
        with st.spinner("กำลังประมวลผลบริบท..."):
            
            # จับ System Prompt และ User Data มัดรวมกันเป็นก้อนเดียว (สูตรนี้รันผ่านแน่นอน)
            master_prompt = f"""
            You are an Expert Translator and Machine Translation Post-Editing (MTPE) Specialist focusing on English to Thai translation. 
            Your task is to review the provided `Source Text` and its initial `Machine Translation` based on the user's specified `Context`.

            ### 🛑 STRICT CONSTRAINTS:
            1. Preserve all special characters, HTML tags, and placeholders (e.g., {{0}}, \\n).
            2. Do not hallucinate external information.
            3. Adjust the tone to perfectly match the requested `Context`.

            ### 📤 OUTPUT FORMAT (Respond in THAI using Markdown):
            **🔍 วิเคราะห์ปัญหา:** (1-2 sentences explaining why the MT is awkward)
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
            
            try:
                # เรียกใช้ AI
                response = model.generate_content(master_prompt)
                st.success("ประมวลผลเสร็จสิ้น!")
                
                # แสดงผลลัพธ์
                st.markdown("### ผลลัพธ์จากผู้ช่วย MTPE")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("⚠️ กรุณาใส่ทั้งประโยคต้นฉบับและคำแปลจากระบบก่อนครับ")
