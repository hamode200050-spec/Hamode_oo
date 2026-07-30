import streamlit as st
import yt_dlp
from groq import Groq
import os
import re

st.set_page_config(page_title="محلل البودكاست الذكي (النسخة الصوتية الخارقة)", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الذكي (مع تحليل الصوت الحقيقي Whisper)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
url = st.text_input("🔗 أدخل رابط يوتيوب:")

if st.button("🚀 تحليل الصوت الحقيقي واستخراج المقاطع"):
    if not api_key or not url:
        st.error("الرجاء إدخال المفتاح والرابط.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # 1. تحميل الصوت بصيغة خفيفة جداً ومؤقتة باستخدام yt_dlp
            ydl_opts = {
                'format': 'worstaudio/worst',
                'outtmpl': 'temp_audio.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '64',
                }],
                'quiet': True,
                'noplaylist': True
            }
            
            with st.spinner("جاري تنزيل عينة الصوت من يوتيوب لتحليلها..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'فيديو')
                    
            # البحث عن الملف الصوتي الناتج
            audio_file_path = "temp_audio.mp3"
            if not os.path.exists(audio_file_path):
                # البحث عن أي امتداد آخر لو حدث اختلاف
                for file in os.listdir("."):
                    if file.startswith("temp_audio"):
                        audio_file_path = file
                        break

            # 2. إرسال الملف الصوتي إلى نموذج Whisper الذكي في Groq لتفريغه حرفياً مع التوقيتات
            with st.spinner("جاري تفريغ الصوت وتحويله إلى نص دقيق عبر نموذج Whisper..."):
                with open(audio_file_path, "rb") as file_to_transcribe:
                    transcription = client.audio.transcriptions.create(
                        file=(audio_file_path, file_to_transcribe.read()),
                        model="whisper-large-v3",
                        response_format="verbose_json",  # للحصول على التوقيتات الزمنية بدقة
                        language="ar"
                    )
                
                # استخراج النصوص مع أوقاتها الحقيقية من نتيجة Whisper
                transcript_segments = []
                # التحقق من وجود المقاطع الزمنية بالاستجابة
                if hasattr(transcription, 'segments') and transcription.segments:
                    for segment in transcription.segments:
                        start_sec = int(segment.get('start', 0))
                        mins, secs = divmod(start_sec, 60)
                        text = segment.get('text', '')
                        transcript_segments.append(f"[{mins:02d}:{secs:02d}] {text}")
                else:
                    # استخلاص النص الكلي لو الـ segments غير متوفرة
                    transcript_segments.append(getattr(transcription, 'text', str(transcription)))
                
                full_transcript = " ".join(transcript_segments)[:15000]

            # تنظيف وحذف الملف المؤقت من النظام
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            # 3. تحليل النص الدقيق عبر Llama واستخراج المقاطع
            with st.spinner("جاري استخراج المقاطع القصيرة بناءً على التفريغ الصوتي الحقيقي..."):
                prompt = f"""
                أنت خبير محترف لإدارة ونشر محتوى البودكاست وتحليل الفيديوهات. 
                عنوان الفيديو: "{title}"
                
                إليك تفريغ النص الصوتي الحقيقي (Transcript) المستخرج من الفيديو مع التوقيتات:
                {full_transcript}

                مهمتك: قم بتحليل التفريغ بعمق واستخراج **أفضل 4 إلى 5 مقاطع قصيرة (Shorts/Reels)** موجودة فعلياً داخل النص بالأوقات الصحيحة.
                
                شروط صارمة جداً:
                1. **المدة:** تتراوح مدة كل مقطع بين 30 إلى 90 ثانية فقط.
                2. **الدقة الزمنية:** اعتمد حصراً على التوقيتات الزمنية الموجودة في النص الصوتي بالأعلى لتبدأ وتنتهي الأفكار بشكل صحيح ودقيق.
                
                لكل مقطع قصير، اكتب التفاصيل التالية بوضوح وتحت كل مقطع على حدة:
                - **اسم المقطع:** (عنوان جذاب ومستقل).
                - **التوقيت الدقيق:** (من الدقيقة:الثانية إلى الدقيقة:الثانية، مع ذكر المدة بالثواني).
                - **سبب القص:** (لماذا اخترنا هذا الجزء).
                - **وصف المقطع:** (وصف جاهز للنشر).
                - **الهاشتاقات:** (هاشتاقات خاصة بالمقطع).
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                )
            
            st.success("تم تحليل الصوت الحقيقي واستخراج المقاطع بنجاح تام!")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            # تنظيف الملف لو حدث خطأ
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")
            st.error(f"حدث خطأ أثناء معالجة الصوت: {e}")
