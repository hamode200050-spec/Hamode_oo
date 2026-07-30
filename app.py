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
                description = info.get('description', '')[:2000] # توسيع النبذة قليلاً لتعطاء سياق أعمق للنموذج
            
            # برومفت محسن بدقة لضمان استخراج المقاطع القصيرة بالثواني المرنة وحسب اكتمال الفكرة مع تفاصيلها الكاملة
            prompt = f"""
            أنت خبير محترف لإدارة ونشر محتوى البودكاست وتحليل الفيديوهات. هذا الفيديو عنوانه الأصلي: "{title}"، ومدة الفيديو الكلية هي {duration} ثانية.
            نبذة عن محتوى الفيديو من الوصف: {description}

            بناءً على فهمك العميق للموضوع، قم بتوليد ما يلي باللغة العربية وبشكل منظم جداً:

            1. **اسم مقترح جذاب وقوي للفيديو الأساسي** (أو تحسين العنوان الحالي).
            2. **وصف تفصيلي احترافي للفيديو الأساسي** يناسب منصات النشر.
            3. **أفضل الهاشتاقات (Hashtags)** المتعلقة بموضوع البودكاست بالكامل.
            4. **أفضل المقاطع القصيرة (Shorts/Reels) المستخرجة بناءً على اكتمال الأفكار:**
               - لا تستخدم زمناً عشوائياً أو ثابتاً طويلاً. اجعل طول كل مقطع يتراوح طبيعياً بين 30 إلى 90 ثانية (مثل: 30، 50، 60، 70، 80، 90 ثانية) بناءً على بداية الفكرة ونهايتها واكتمال معناها.
               - لكل مقطع قصير، اذكر بوضوح وتحت كل مقطع على حدة:
                 * **اسم المقطع:** (عنوان جذاب ومستقل للمقطع).
                 * **التوقيت الدقيق:** (من الدقيقة/الثانية إلى الدقيقة/الثانية، مع ذكر المدة الفعلية بالثواني).
                 * **سبب القص:** (ليش اخترنا هذا الجزء بالذات وشنو أهمية الكلام فيه).
                 * **وصف المقطع:** (وصف احترافي جاهز للنشر مع الـ Reel).
                 * **الهاشتاقات:** (هاشتاقات خاصة بهذا المقطع فقط).
            """
            
            with st.spinner("جاري التحليل العميق واستخراج المقاطع بالثواني المرنة والمنظمة..."):
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
