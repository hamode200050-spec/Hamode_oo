import streamlit as st
from groq import Groq
import os
from pydub import AudioSegment

st.set_page_config(page_title="محلل البودكاست الطويل الخارق", page_icon="⚡", layout="centered")

st.markdown("<h1 style='text-align: center;'>⚡ محلل البودكاست الطويل (تقسيم ومعالجة 4 ساعات)</h1>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أضف مفتاح Groq API الخاص بك:", type="password")
uploaded_file = st.file_uploader("📁 ارفع ملف البودكاست الطويل (MP3, M4A, WAV):", type=["mp3", "m4a", "wav"])
video_title = st.text_input("📌 عنوان الحلقة:", value="حلقة بودكاست طويلة")

if st.button("🚀 بدء التقسيم والتحليل الشامل"):
    if not api_key or not uploaded_file:
        st.error("الرجاء إدخال المفتاح ورفع الملف الصوتي.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # حفظ الملف الأصلي مؤقتياً
            original_path = "full_podcast.mp3"
            with open(original_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("جاري قراءة الملف الصوتي وتقسيمه إلى أجزاء (كل 10 دقائق) لتجاوز حدود الحجم..."):
                # قراءة الملف عبر Pydub
                audio = AudioSegment.from_file(original_path)
                
                # تقطيع الصوت إلى أجزاء مدة كل جزء 10 دقائق (600,000 ملي ثانية)
                chunk_length_ms = 10 * 60 * 1000 
                chunks = audio[::chunk_length_ms]
                
                full_transcript_parts = []
                total_duration_offset = 0

                # معالجة كل جزء على حدة
                for i, chunk in enumerate(chunks):
                    chunk_name = f"chunk_{i}.mp3"
                    chunk.export(chunk_name, format="mp3")
                    
                    st.info(f"⏳ جاري تفريغ الجزء {i+1} من أصل {len(chunks)}...")
                    
                    with open(chunk_name, "rb") as chunk_file:
                        transcription = client.audio.transcriptions.create(
                            file=(chunk_name, chunk_file.read()),
                            model="whisper-large-v3",
                            response_format="verbose_json",
                            language="ar"
                        )
                    
                    # تعديل التوقيتات وإضافتها للنص الكلي
                    if hasattr(transcription, 'segments') and transcription.segments:
                        for segment in transcription.segments:
                            start_sec = int(segment.get('start', 0)) + total_duration_offset
                            mins, secs = divmod(start_sec, 60)
                            text = segment.get('text', '')
                            full_transcript_parts.append(f"[{mins:02d}:{secs:02d}] {text}")
                    
                    # حذف الجزء المؤقت بعد الانتهاء منه
                    if os.path.exists(chunk_name):
                        os.remove(chunk_name)
                    
                    # تحديث الـ offset الزمني للجزء القادم
                    total_duration_offset += int(len(chunk) / 1000)

            # تنظيف الملف الأصلي
            if os.path.exists(original_path):
                os.remove(original_path)

            combined_transcript = " ".join(full_transcript_parts)
            
            # اختصار النص لو كان ضخماً جداً للـ Llama
            final_text_for_ai = combined_transcript[:25000]

            with st.spinner("جاري تحليل النص الكامل واستخراج أفضل المقاطع القصيرة (Shorts)..."):
                prompt = f"""
                أنت خبير محترف لإدارة ونشر محتوى البودكاست. 
                عنوان الحلقة: "{video_title}"
                
                إليك تفريغ النص الصوتي الكامل للحلقة مع التوقيتات الزمنية الدقيقة:
                {final_text_for_ai}

                مهمتك: قم بتحليل التفريغ واستخراج **أفضل 4 إلى 5 مقاطع قصيرة (Shorts/Reels)** حقيقية وجذابة وموجودة داخل النص بالأوقات الصحيحة.
                
                شروط صارمة:
                1. **المدة:** تتراوح مدة كل مقطع بين 30 إلى 90 ثانية فقط.
                2. **الدقة:** اعتمد على التوقيتات الزمنية الموجودة بالنص.
                
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
            
            st.success("تم تحليل البودكاست الطويل بالكامل بنجاح تام!")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            # تنظيف أي ملفات بقة بالمجلد في حال حصول خطأ
            for f in os.listdir("."):
                if f.startswith("chunk_") or f == "full_podcast.mp3":
                    os.remove(f)
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
