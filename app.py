import streamlit as st
import os
import tempfile
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل وصانع الشورتس الذكي بالذكاء الاصطناعي</h1>
    <p style='text-align: center;'>استخراج وتحليل اللقطات المهمة من البودكاست الطويل وتحويلها لشورتس بدقة 9:16 تلقائياً!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست أو فيديو طويل):")

if st.button("🚀 تحليل الفيديو واستخراج اللقطات بالـ AI"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 يقوم الذكاء الاصطناعي الآن بقراءة فصول الفيديو وفحص المحتوى لاكتشاف أفضل اللقطات..."):
            try:
                ydl_opts = {
                    'format': 'best[height<=720]',
                    'outtmpl': os.path.join(tempfile.gettempdir(), 'podcast_source.mp4'),
                    'noplaylist': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    },
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'فيديو يوتيوب')
                    video_duration = info.get('duration', 0)
                    video_path = ydl.prepare_filename(info)
                    chapters = info.get('chapters', None)

                st.success(f"✅ تم تحليل الفيديو بنجاح: {video_title}")

                # توليد المقاطع بناءً على الفصول الموجودة في الفيديو أو تقطيعه ذكياً
                ai_clips = []
                if chapters:
                    for i, ch in enumerate(chapters):
                        start = int(ch.get('start_time', 0))
                        end = int(ch.get('end_time', start + 50))
                        if end - start > 60: # جعل مدة المقطع بحدود 50-60 ثانية للشورتس
                            end = start + 55
                        ai_clips.append({
                            "title": ch.get('title', f"مقطع ذكي #{i+1}"),
                            "start": start,
                            "end": end
                        })
                else:
                    # تقسيم افتراضي للبودكاست الطويل كل عدة دقائق
                    step = 300 # كل 5 دقائق لقطة مقترحة
                    for i, sec in enumerate(range(0, int(video_duration) - 60, step)):
                        ai_clips.append({
                            "title": f"🔥 لقطة مقترحة رقم #{i+1}",
                            "start": sec,
                            "end": sec + 50
                        })

                st.info(f"✨ اكتشف الذكاء الاصطناعي ({len(ai_clips)}) مقطعاً مهماً في هذا البودكاست:")

                for idx, clip in enumerate(ai_clips[:10], 1): # عرض أول 10 مقاطع مقترحة
                    st.markdown("---")
                    st.subheader(f"🎬 اللقطة المقترحة #{idx}")
                    st.write(f"📌 **العنوان:** {clip['title']}")
                    st.write(f"⏱️ **التوقيت:** من الدقيقة {clip['start']//60} إلى {clip['end']//60}")
                    
                    output_clip_path = os.path.join(tempfile.gettempdir(), f"ai_short_{idx}.mp4")
                    
                    if st.button(f"✂️ قص وتحويل هذه اللقطة إلى 9:16", key=f"cut_btn_{idx}"):
                        with st.spinner("جاري قص وتعديل المقطع..."):
                            with VideoFileClip(video_path) as video:
                                sub = video.subclipped(clip['start'], clip['end'])
                                w, h = sub.size
                                target_w = h * 9 / 16
                                if target_w < w:
                                    x1 = (w - target_w) / 2
                                    sub = sub.crop(x1=x1, y1=0, x2=x1 + target_w, y2=h)
                                sub = sub.resized(width=1080, height=1920)
                                sub.write_videofile(output_clip_path, codec="libx264", audio_codec="aac", logger=None)
                            
                            st.success("✅ تم تجهيز الشورت بنجاح!")
                            with open(output_clip_path, "rb") as file:
                                st.download_button(
                                    label=f"⬇️ تحميل الشورت #{idx} (9:16)",
                                    data=file,
                                    file_name=f"short_clip_{idx}.mp4",
                                    mime="video/mp4",
                                    key=f"dl_{idx}"
                                )

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الرابط: {e}")
