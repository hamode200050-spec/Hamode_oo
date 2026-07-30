import streamlit as st
import yt_dlp
from google import genai

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Google Gemini API:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            # تهيئة العميل بالطريقة الرسمية الجديدة التي أرسلتها
            client = genai.Client(api_key=api_key)
            
            with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'فيديو')
            
            prompt = f"اقترح 3 مقاطع شورتس ممتازة للفيديو وعنوانه: {title}"
            
            # الاستدعاء بالطريقة الحديثة المطابقة للموقع
            interaction = client.interactions.create(
                model="gemini-2.5-flash",
                input=prompt
            )
            
            st.success("تم التحليل بنجاح!")
            st.write(interaction.output_text)
            
        except Exception as e:
            st.error(f"خطأ: {e}")
