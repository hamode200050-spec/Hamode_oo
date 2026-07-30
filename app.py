import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from groq import Groq
import re

st.set_page_config(page_title="محلل البودكاست الذكي الاحترافي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي (مع سحب التفريغ الدقيق)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

def extract_video_id(youtube_url):
    # أنماط مختلفة لرابط يوتيوب لضمان التقاط المعرف (ID) بكل الحالات بدقة
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

if st.button("🚀 بدء التحليل الدقيق"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            video_id = extract_video_id(url)
            if not video_id:
                st.error("رابط اليوتيوب غير صالح أو غير مدعوم!")
            else:
                client = Groq(api_key=api_key)
                
                with st.spinner("جاري سحب معلومات الفيديو وتفريغ النص (Transcript)..."):
                    # 1. سحب عنوان ووصف الفيديو
                    with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = info.get('title', 'فيديو')
                    
                    # 2. سحب تفريغ النص الحقيقي من يوتيوب مع الأوقات
                    transcript_text = ""
                    try:
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
                        formatted_transcript = []
                        for entry in transcript_list:
                            start_sec = int(entry['start'])
                            mins, secs = divmod(start_sec, 60)
                            time_stamp = f"[{mins:02d}:{secs:02d}]"
                            formatted_transcript.append(f"{time_stamp} {entry['text']}")
                        
                        transcript_text = " ".join(formatted_transcript)
                        transcript_text = transcript_text[:15000] # اقتطاع النص لتفادي تجاوز حدود التوكنز
                    except (TranscriptsDisabled, NoTranscriptFound):
                        st.warning("⚠️ عذراً، تفريغ النص (Transcript) غير متوفر تلقائياً لهذا الفيديو. سيتم الاعتماد على سياق العنوان والوصف.")
                        transcript_text = "التفريغ غير متوفر، يرجى الاعتماد على العنوان والوصف."

                with st.spinner("جاري التحليل العميق واستخراج المقاطع القصيرة بالثواني الصحيحة..."):
                    
                    prompt = f"""
                    أنت خبير محترف لإدارة ونشر محتوى البودكاست وتحليل الفيديوهات. 
                    عنوان الفيديو: "{title}"
                    
                    إليك تفريغ النص (Transcript) الخاص بالفيديو مع التوقيتات الزمنية الدقيقة:
                    {transcript_text}

                    مهمتك: قم بتحليل التفريغ بعمق واستخراج **أفضل 4 إلى 5 مقاطع قصيرة (Shorts/Reels)** حقيقية وموجودة فعلياً داخل النص بالأوقات الصحيحة.
                    
                    شروط صارمة جداً:
                    1. **المدة:** يجب أن تتراوح مدة كل مقطع قصير بين 30 إلى 90 ثانية فقط (لا تقم أبداً باستخراج مقاطع طويلة لعدة دقائق).
                    2. **الدقة الزمنية:** اعتمد على الأوقات الموجودة في التفريغ النصي بالأعلى لتحديد وقت البداية ووقت النهاية بدقة متناهية (مثلاً: من 02:15 إلى 03:00).
                    
                    لكل مقطع قصير، اكتب التفاصيل التالية بوضوح وتحت كل مقطع على حدة:
                    - **اسم المقطع:** (عنوان جذاب ومستقل).
                    - **التوقيت الدقيق:** (من الدقيقة:الثانية إلى الدقيقة:الثانية، مع ذكر المدة بالثواني).
                    - **سبب القص:** (لماذا اخترنا هذا الجزء بالذات من الكلام).
                    - **وصف المقطع:** (وصف جاهز للنشر مع الريل).
                    - **الهاشتاقات:** (هاشتاقات خاصة بالمقطع).
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5,
                    )
                
                st.success("تم التحليل الدقيق بنجاح!")
                st.markdown(completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
