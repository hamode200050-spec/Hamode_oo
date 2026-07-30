import streamlit as st
import yt_dlp
from groq import Groq

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل شامل"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'فيديو')
                duration = info.get('duration', 0)
                description = info.get('description', '')[:1000] # أخذ نبذة من وصف يوتيوب الأصلي
            
            # برومفت شامل واحترافي لجلب العنوان، الوصف، الهاشتاقات، والشورتس بالتفصيل
            prompt = f"""
            أنت مساعد محترف لإدارة ونشر محتوى البودكاست. هذا الفيديو مدته طويلة (بودكاست)، وعنوانه الأصلي هو: "{title}".
            نبذة عن محتوى الفيديو: {description}

            بناءً على ذلك، قم بتوليد ما يلي باللغة العربية وبشكل منظم تماماً:
            1. **اسم مقترح جذاب للفيديو الأساسي** (أو تحسين العنوان الحالي).
            2. **وصف تفصيلي احترافي للفيديو** يناسب منصات النشر.
            3. **أفضل الهاشتاقات (Hashtags)** المتعلقة بموضوع البودكاست.
            4. **أفضل 3 إلى 5 مقاطع قصيرة (Shorts)** مستخرجة من هذا البودكاست مع ذكر:
               - عنوان المقطع.
               - التوقيت (البداية والنهاية).
               - نبذة قصيرة لماذا هذا المقطع ممتاز للنشر.
            """
            
            with st.spinner("جاري تحليل البودكاست بالكامل واستخراج التفاصيل..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
            
            st.success("تم التحليل الشامل بنجاح!")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            st.error(f"خطأ: {e}")
