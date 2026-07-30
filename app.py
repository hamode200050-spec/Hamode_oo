import streamlit as st
import yt_dlp
from groq import Groq

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي (عبر Groq)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'فيديو')
            
            prompt = f"اقترح 3 مقاطع شورتس ممتازة للفيديو وعنوانه: {title} مع توقيت البداية والنهاية."
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            st.success("تم التحليل بنجاح!")
            st.write(completion.choices[0].message.content)
            
        except Exception as e:
            st.error(f"خطأ: {e}")
