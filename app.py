import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
import re

st.set_page_config(page_title="محلل البودكاست الذكي الاحترافي", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي (النسخة الذكية المطورة)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

def extract_video_id(youtube_url):
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

if st.button("🚀 بدء التحليل الذكي"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            video_id = extract_video_id(url)
            if not video_id:
                st.error("رابط اليوتيوب غير صالح أو غير مدعوم!")
            else:
                client = Groq(api_key=api_key)
                
                with st.spinner("جاري فحص وفحص محتوى الفيديو وسحب البيانات..."):
                    # سحب العنوان، الوصف الكامل، والمدة الحقيقية من yt_dlp
                    with yt_dlp.YoutubeDL({'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = info.get('title', 'فيديو')
                        duration = info.get('duration', 0)
                        full_description = info.get('description', 'لا يوجد وصف')
                    
                    # محاولة سحب التفريغ النصي الحقيقي
                    transcript_text = ""
                    is_transcript_available = False
                    
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                        transcript = None
                        try:
                            transcript = transcript_list.find_transcript(['ar'])
                        except:
                            try:
                                transcript = transcript_list.find_transcript(['en'])
                            except:
                                transcript = next(iter(transcript_list))
                        
                        fetched_data = transcript.fetch()
                        formatted_transcript = []
                        for entry in fetched_data:
                            start_sec = int(entry.get('start', 0))
                            mins, secs = divmod(start_sec, 60)
                            time_stamp = f"[{mins:02d}:{secs:02d}]"
                            text_part = entry.get('text', '')
                            formatted_transcript.append(f"{time_stamp} {text_part}")
                        
                        transcript_text = " ".join(formatted_transcript)[:15000]
                        is_transcript_available = True
                    except:
                        is_transcript_available = False

                with st.spinner("جاري التحليل العميق بالذكاء الاصطناعي..."):
                    
                    if is_transcript_available:
                        context_data = f"إليك تفريغ النص (Transcript) الخاص بالفيديو مع التوقيتات الدقيقة:\n{transcript_text}"
                        instruction_note = "اعتمد على الأوقات الحقيقية الموجودة في التفريغ النصي بالأعلى."
                    else:
                        st.warning("⚠️ ملاحظة: التفريغ التلقائي مغلق من يوتيوب لهذا الفيديو، تم الاعتماد على تحليل الوصف الشامل والعنوان والمدة الكلية بدقة.")
                        context_data = f"وصف الفيديو الشامل:\n{full_description}\n\nمدة الفيديو الكلية بالثواني: {duration}"
                        instruction_note = "بما أن التفريغ غير متوفر، قم بتقدير الأوقات والترتيبات بشكل منطقي واحترافي بناءً على هيكل ونقاط الوصف المذكورة."

                    prompt = f"""
                    أنت خبير محترف لإدارة ونشر محتوى البودكاست وتحليل الفيديوهات. 
                    عنوان الفيديو: "{title}"
                    
                    {context_data}

                    مهمتك: قم بتحليل المحتوى واستخراج **أفضل 4 إلى 5 مقاطع قصيرة (Shorts/Reels)** احترافية.
                    
                    شروط صارمة جداً:
                    1. **المدة:** يجب أن تتراوح مدة كل مقطع قصير بين 30 إلى 90 ثانية فقط.
                    2. **الدقة الزمنية:** {instruction_note}
                    
                    لكل مقطع قصير، اكتب التفاصيل التالية بوضوح وتحت كل مقطع على حدة:
                    - **اسم المقطع:** (عنوان جذاب ومستقل).
                    - **التوقيت الدقيق:** (من الدقيقة:الثانية إلى الدقيقة:الثانية، مع ذكر المدة بالثواني).
                    - **سبب القص:** (لماذا اخترنا هذا الجزء بالذات).
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
                
                st.success("تم التحليل بنجاح تام!")
                st.markdown(completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
