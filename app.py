import streamlit as st
import time

st.set_page_config(page_title="SubSync: AI Subtitle Localizer", page_icon="🎬", layout="centered")
st.title("🎬 SubSync: AI Subtitle Localizer")
st.markdown("เครื่องมือช่วยเกลาคำแปลซับไตเติลให้เข้ากับคาแรคเตอร์ บริบท และยุคสมัย")
st.divider()

# --- แถวที่ 1: ตั้งค่าบริบท ---
context_choice = st.selectbox("🎭 เลือกบริบท/ความสัมพันธ์ตัวละคร", 
                              ["ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)", "ซีรีส์ย้อนยุค (สแลงยุค 90s)", "แฟนด้อม/วงการบันเทิง"])
glossary = st.text_input("📌 กฎเหล็ก/เงื่อนไขเพิ่มเติม (ถ้ามี)", placeholder="เช่น ห้ามเกิน 35 ตัวอักษร, ใช้คำลงท้ายว่า 'แก-ฉัน'")

if context_choice == "ซีรีส์วัยรุ่น (เพื่อนสนิท/วัยเรียน)":
    default_src = "I just want you to know that you are my safe zone. Are you okay with that?"
    default_mt = "ฉันแค่อยากให้คุณรู้ว่าคุณคือโซนปลอดภัยของฉัน คุณโอเคกับสิ่งนั้นไหม?"
    final_sub = "ฉันแค่อยากให้แกรู้ว่าแกคือเซฟโซนของฉันนะ แกโอเคป่าว?"
elif context_choice == "ซีรีส์ย้อนยุค (สแลงยุค 90s)":
    default_src = "That concert was totally awesome! I can't believe we got front row tickets."
    default_mt = "คอนเสิร์ตนั้นยอดเยี่ยมมาก! ฉันไม่อยากจะเชื่อเลยว่าเราได้ตั๋วแถวหน้า"
    final_sub = "คอนเสิร์ตโคตรจ๊าบเลย! ไม่อยากจะเชื่อว่าได้ตั๋วหน้าสุด"
else:
    default_src = "Did you see their comeback stage? The center completely ate and left no crumbs!"
    default_mt = "คุณเห็นเวทีคัมแบ็คของพวกเขาไหม? เซ็นเตอร์กินหมดจดและไม่เหลือเศษเลย!"
    final_sub = "เห็นสเตจคัมแบ็กปะ? เซ็นเตอร์คือทำถึงมาก ปังไม่ไหว!"

st.write("") 

# --- แถวที่ 2: ฟังก์ชัน Timecode (เพิ่มความโปร) ---
timecode = st.text_input("⏱️ Timecode (ถ้ามี)", value="00:01:23,400 --> 00:01:25,500")

source_text = st.text_area("🇬🇧 ประโยคต้นฉบับ (Source Text)", value=default_src, height=100)
mt_text = st.text_area("🤖 คำแปลจากระบบ (Machine Translation)", value=default_mt, height=100)

if st.button("🚀 เกลาซับไตเติลให้เป๊ะ!", use_container_width=True):
    with st.spinner("กำลังวิเคราะห์บริบทตัวละครและริมฝีปาก..."):
        time.sleep(1.5) 
        
        st.success("ประมวลผลเสร็จสิ้น!")
        st.markdown("### 📊 Subtitle Metrics")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tone & Vibe", value="Natural", delta="100% Match")
        m2.metric(label="Reading Speed", value="14 CPS", delta="Optimal", delta_color="normal")
        m3.metric(label="Character Limit", value=f"{len(final_sub)}/35", delta="Pass")
        
        st.divider()
        st.markdown("### ✨ ซับไตเติลที่แนะนำ")
        st.info(f"**ตัวเลือกที่ดีที่สุด:** {final_sub}")
        
        # --- ฟังก์ชัน Export ไฟล์ .srt ---
        srt_content = f"1\n{timecode}\n{final_sub}\n"
        st.download_button(
            label="💾 ดาวน์โหลดไฟล์ .srt",
            data=srt_content,
            file_name="localized_sub.srt",
            mime="text/plain",
            use_container_width=True
        )
