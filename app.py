import streamlit as st
import yt_dlp
from groq import Groq

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل عميق وشامل"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'فيديو')
                duration = info.get('duration', 0)
                description = info.get('description', '')[:1500]
            
            # برومفت ذكي يعتمد على اكتمال الفكرة وبأطوال مختلفة (من 30 ثانية إلى دقيقتين حسب سياق الموضوع)
            prompt = f"""
            أنت خبير محتوى ومونتير محترف لبودكاست مدته طويلة (مدة الفيديو الكلية تقريباً {duration // 60} دقيقة).
            عنوان الفيديو: "{title}"
            نبذة عن المحتوى: {description}

            بناءً على فهمك العميق للفيديو، قم باستخراج حزمة احترافية متكاملة تشمل:
            1. **اسم مقترح جذاب وقوي للفيديو الأساسي**.
            2. **وصف تفصيلي احترافي للفيديو** جاهز للنشر على يوتيوب.
            3. **أفضل الهاشتاقات (Hashtags)** المتعلقة بالموضوع بدقة.
            4. **أفضل المقاطع القصيرة (Shorts/Reels) المستخرجة من كامل الفيديو**:
               - اعتمد على **"اكتمال الفكرة"** وليس على وقت ثابت أبداً.
               - قد يكون المقطع قصير جداً وقوي (مثل 30 أو 45 ثانية) إذا كانت الفكرة مركزة، أو قد يمتد إلى (60، 75، 90 ثانية أو حتى دقيقتين) إذا كانت الفكرة تحتاج وقتاً لكي تكتمل بنجاح وتشد المشاهد.
               - لكل مقطع اذكر: (عنوان المقطع، التوقيت من-إلى بدقة، ومدته الزمنية، وسبب اختيار هذا المقطع ولماذا فكرته ممتازة للنشر).
            """
            
            with st.spinner("جاري تحليل كامل الفيديو والبحث عن الأفكار المترابطة..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
            
            st.success("تم التحليل واستخراج الأفكار بنجاح!")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            st.error(f"خطأ: {e}")
