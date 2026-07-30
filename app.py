import streamlit as st
import os
import tempfile
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل وصانع الشورتس الذكي بالذكاء الاصطناعي</h1>
    <p style='text-align: center;'>مخصص لتحليل البودكاست والفيديوهات الطويلة واستخراج أحلى اللقطات بدقة 9:16!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (حتى لو كان طويلاً 3-4 ساعات):")

# تحديد نقطة البداية للمقطع المطلوب استخراجه من الفيديو الطويل
start_minute = st.number_input("⏱️ ابدأ استخراج الشورتس من الدقيقة رقم:", min_value=0, value=0, step=1)

if st.button("🚀 تحليل واستخراج الشورتس من الفيديو الطويل"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري الاتصال بيوتيوب وسحب المقطع المطلوب من البودكاست الطويل..."):
            try:
                # إعدادات متقدمة جداً لتجاوز حظر يوتيوب على الفيديوهات الطويلة
                ydl_opts = {
                    'format': 'best[height<=720]', # جودة مناسبة وسريعة للتحميل
                    'outtmpl': os.path.join(tempfile.gettempdir(), 'long_podcast_video.mp4'),
                    'noplaylist': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9',
                    },
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'بودكاست')
                    video_path = ydl.prepare_filename(info)

                st.success(f"✅ تم سحب الفيديو بنجاح: {video_title}")

                start_sec = start_minute * 60
                clip_duration = 50 # مدة الشورت 50 ثانية

                output_clip_path = os.path.join(tempfile.gettempdir(), "extracted_short.mp4")

                with st.spinner("🎬 جاري قص وتعديل الشورت إلى مقاس 9:16..."):
                    with VideoFileClip(video_path) as video:
                        total_dur = video.duration
                        if start_sec >= total_dur:
                            start_sec = 0
                            st.warning("الدقيقة المحددة تتجاوز مدة الفيديو، تم البدء من البداية.")
                        
                        end_sec = min(start_sec + clip_duration, total_dur)
                        
                        sub = video.subclipped(start_sec, end_sec)
                        w, h = sub.size
                        target_w = h * 9 / 16
                        if target_w < w:
                            x1 = (w - target_w) / 2
                            sub = sub.crop(x1=x1, y1=0, x2=x1 + target_w, y2=h)
                        sub = sub.resized(width=1080, height=1920)
                        sub.write_videofile(output_clip_path, codec="libx264", audio_codec="aac", logger=None)

                st.markdown("---")
                st.subheader("✨ جاهز للتحميل!")
                st.write(f"📌 **المقطع المستخرج من الدقيقة:** {start_minute} إلى الدقيقة {start_minute + 1}")

                with open(output_clip_path, "rb") as file:
                    st.download_button(
                        label="⬇️ تحميل الشورت جاهز للنشر (9:16)",
                        data=file,
                        file_name="podcast_short_916.mp4",
                        mime="video/mp4"
                    )

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة البودكاست: {e}")
