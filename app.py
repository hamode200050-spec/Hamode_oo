import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="محلل البودكاست الذكي المباشر", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست المباشر (بدون تعقيدات)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
uploaded_file = st.file_uploader("📁 ارفع ملف البودكاست (MP3, M4A, WAV):", type=["mp3", "m4a", "wav"])
video_title = st.text_input("📌 عنوان الحلقة:", value="حلقة بودكاست")

if st.button("🚀 بدء التحليل الفوري"):
    if not api_key or not uploaded_file:
        st.error("الرجاء إدخال المفتاح ورفع الملف الصوتي.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # حفظ الملف المرفوع مؤقتياً
            temp_path = "podcast_temp.mp3"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("جاري تفريغ الصوت وتحليله عبر نموذج Whisper..."):
                with open(temp_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=(temp_path, audio_file.read()),
                        model="whisper-large-v3",
                        response_format="verbose_json",
                        language="ar"
                    )
                
                transcript_segments = []
                if hasattr(transcription, 'segments') and transcription.segments:
                    for segment in transcription.segments:
                        start_sec = int(segment.get('start', 0))
                        mins, secs = divmod(start_sec, 60)
                        text = segment.get('text', '')
                        transcript_segments.append(f"[{mins:02d}:{secs:02d}] {text}")
                else:
                    transcript_segments.append(getattr(transcription, 'text', str(transcription)))
                
                full_transcript = " ".join(transcript_segments)[:25000]

            # تنظيف الملف المؤقت
            if os.path.exists(temp_path):
                os.remove(temp_path)

            with st.spinner("جاري استخراج أفضل المقاطع القصيرة (Shorts)..."):
                prompt = f"""
                أنت خبير محترف لإدارة ونشر محتوى البودكاست. 
                عنوان الحلقة: "{video_title}"
                
                إليك تفريغ النص الصوتي مع التوقيتات:
                {full_transcript}

                مهمتك: استخرج **أفضل 4 إلى25 مقاطع قصيرة (Shorts/Reels)** حقيقية وجذابة بالأوقات الصحيحة.
                
                شروط صارمة:
                1. **المدة:** تتراوح بين 30 إلى 90 ثانية لكل مقطع.
                2. **الدقة:** اعتمد على التوقيتات الموجودة في النص.
                
                لكل مقطع، اكتب:
                - **اسم المقطع:** 
                - **التوقيت الدقيق:** (من الدقيقة:الثانية إلى الدقيقة:الثانية)
                - **سبب القص:** 
                - **وصف المقطع:** 
                - **الهاشتاقات:** 
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
            
            st.success("تم التحليل واستخراج المقاطع بنجاح تام!")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            if os.path.exists("podcast_temp.mp3"):
                os.remove("podcast_temp.mp3")
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
