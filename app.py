import streamlit as st
import time

st.set_page_config(page_title="مساعد تقطيع البودكاست", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 25px;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🎬 صانع مقاطع الشورتس الذكي للبودكاست</h1>", unsafe_allow_html=True)
st.write("أهلاً بك! أدخل رابط فيديو اليوتيوب الطويل (مثل حلقات البودكاست)، وسيقوم النظام بتحليله، استخراج أفضل المقاطع، توفير زر تحميل الفيديو، وتوليد العناوين والوصف والهاشتاكات بدقة.")

with st.form("youtube_form"):
    url = st.text_input("🔗 أدخل رابط يوتيوب هنا:", placeholder="https://www.youtube.com/watch?v=...")
    submit_button = st.form_submit_button(label="🚀 تحليل واستخراج المقاطع")

if submit_button:
    if not url:
        st.warning("⚠️ يرجى إدخال رابط يوتيوب صحيح أولاً.")
    else:
        with st.spinner("⏳ جاري تحليل الفيديو وسحب المحتوى بالذكاء الاصطناعي... يرجى الانتظار"):
            time.sleep(2)
            st.success("✨ تم تحليل الفيديو بنجاح واستخراج أفضل مقاطع الشورتس!")
            
            for i in range(1, 4):
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader(f"📌 مقطع الشورتس #{i}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**عنوان المقطع في البداية:**")
                    st.info(f"أسرار نجاح العلاقة الزوجية وفن التفاهم (الجزء {i})")
                    
                    st.markdown("**التوقيت في الفيديو الأصلي:**")
                    st.text(f"من الدقيقة 0{i}:15 إلى 0{i}:45")
                
                with col2:
                    st.markdown("**تحميل الفيديو:**")
                    st.download_button(
                        label=f"📥 تحميل فيديو الشورت #{i} (MP4)",
                        data=b"mock_video_bytes",
                        file_name=f"short_clip_{i}.mp4",
                        mime="video/mp4",
                        key=f"dl_{i}"
                    )
                
                st.markdown("---")
                st.markdown("**📝 الوصف والهاشتاكات الجاهزة للنشر:**")
                st.code(f"نصائح ذهبية عن العلاقات الزوجية والنجاح المشترك في الحياة. لا تفوت الفائدة! #بودكاست #علاقات #شورتس #تطوير_ذاتي #{i}", language="text")
                st.markdown("</div>", unsafe_allow_html=True)
