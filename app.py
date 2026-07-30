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
            # التوثيق بالطريقة الكلاسيكية المستقرة التي تتوافق مع المفاتيح المتاحة لديك
            genai.configure(api_key=api_key)
            
            # استخدام مكتبة استعلام النماذج المتاحة تلقائياً لتجنب خطأ 404 نهائياً
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("لا توجد نماذج متاحة لهذا المفتاح.")
            else:
                # اختيار أول نموذج متوافق مدعوم تلقائياً
                model_name = available_models[0]
                model = genai.GenerativeModel(model_name)
                
                with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'فيديو')
                
                prompt = f"اقترح 3 مقاطع شورتس ممتازة للفيديو وعنوانه: {title}"
                response = model.generate_content(prompt)
                
                st.success(f"تم التحليل بنجاح باستخدام النموذج: {model_name}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"خطأ: {e}")
