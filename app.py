import streamlit as st
import yt_dlp
import google.generativeai as genai

st.set_page_config(page_title="محلل البودكاست الذكي بالـ AI", page_icon="⚡", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>⚡ محلل البودكاست الذكي (مدعوم بالذكاء الاصطناعي)</h1>
    <p style='text-align: center;'>تحليل عنوان وسياق الفيديو واقتراح أفضل اللقطات للـ Shorts بذكاء تام!</p>
""", unsafe_allow_html=True)

# جلب المفتاح من الـ Secrets أو من الحقل اليدوي
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = st.text_input("🔑 أضف مفتاح Google Gemini API الخاص بك:", type="password")

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست طويل):")

def extract_video_info(youtube_url):
    ydl_opts = {'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return {
            'title': info.get('title', 'بدون عنوان'),
            'duration': info.get('duration', 600),
            'channel': info.get('uploader', 'قناة يوتيوب')
        }

if st.button("🚀 تحليل البودكاست واستخراج اللقطات الذكية"):
    if not api_key:
        st.warning("⚠️ الرجاء إدخال مفتاح Google Gemini API أولاً.")
    elif not url:
        st.warning("⚠️ الرجاء إدخال رابط يوتيوب.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # استخدام الطريقة الآمنة لاختيار النموذج المتاح حصراً لتوليد النصوص
            model_name = 'gemini-1.5-flash'
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name
                    break
            
            model = genai.GenerativeModel(model_name)

            with st.spinner("🔍 جاري جلب بيانات البودكاست وتحليله عبر الذكاء الاصطناعي..."):
                video_info = extract_video_info(url)
                title = video_info['title']
                duration = video_info['duration']
                channel = video_info['channel']

                prompt = f"""
                أنت خبير مونتاج وصناعة محتوى لـ YouTube Shorts.
                لدينا فيديو بودكاست بالمعلومات التالية:
                - عنوان الفيديو: "{title}"
                - اسم القناة: "{channel}"
                - المدة الإجمالية بالثواني: {duration}

                بناءً على عنوان البودكاست وموضوعه العام، قم بتقسيم الفيديو إلى 5 إلى 8 مقاطع (Shorts) ممتازة وجذابة.
                أعطني النتيجة حصراً بصيغة قائمة منسقة لكل مقطع تحتوي على:
                1. وقت البداية بالثواني (start_seconds)
                2. وقت النهاية بالثواني (end_seconds) - بحيث تكون مدة المقطع بين 40 إلى 60 ثانية.
                3. عنوان أو فكرة جذابة للمقطع (idea).
                
                اجعل الإجابة مرتبة وواضحة جداً.
                """

                response = model.generate_content(prompt)
                ai_text = response.text

            st.success("✨ تم تحليل البودكاست وتوليد المقاطع بنجاح!")
            st.markdown("---")
            st.subheader("📌 معلومات الفيديو:")
            st.info(f"العنوان: {title} | القناة: {channel}")

            st.subheader("🤖 اقتراحات الذكاء الاصطناعي للمقاطع:")
            st.write(ai_text)

            st.markdown("---")
            st.subheader("✍️ صندوق تجهيز الوصف والهاشتاقات:")
            
            for i in range(1, 6):
                with st.expander(f"🎬 مقطع مقترح رقم #{i}"):
                    st.text_input(f"عنوان الشورت #{i}", value=f"لقطة مميزة من: {title}", key=f"title_{i}")
                    st.text_area(f"الوصف #{i}", value=f"تابع التفاصيل الكاملة في بودكاست {channel}\n\n💡 لا تنس الإعجاب والاشتراك للمزيد من المحتوى الهادف!\n#shorts #بودكاست #اكسبلور", key=f"desc_{i}", height=70)

        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال أو التحليل: {e}")
