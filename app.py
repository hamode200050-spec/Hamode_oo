import streamlit as st
import yt_dlp
import google.generativeai as genai

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Google Gemini API:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # البحث التلقائي عن أي نموذج يدعم توليد المحتوى لتجنب خطأ 404 نهائياً
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if not available_models:
                st.error("لا توجد نماذج متاحة لهذا المفتاح.")
            else:
                model_to_use = available_models[0]
                model = genai.GenerativeModel(model_to_use)
                
                with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'فيديو')
                
                response = model.generate_content(f"اقترح 3 مقاطع شورتس ممتازة للفيديو وعنوانه: {title}")
                st.success(f"تم التحليل بنجاح باستخدام النموذج: {model_to_use}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"خطأ: {e}")
