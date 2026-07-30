import streamlit as st
import os
import tempfile
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="صانع الشورتس السريع", page_icon="🎬", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🎬 صانع الشورتس السريع للبودكاست</h1>
    <p style='text-align: center;'>تحويل اللقطات إلى 9:16 بدون حظر يوتيوب!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب:")

col1, col2 = st.columns(2)
with col1:
    start_min = st.number_input("⏱️ دقيقة البداية:", min_value=0, value=0, step=1)
    start_sec = st.number_input(" ثانية البداية:", min_value=0, max_value=59, value=0, step=1)
with col2:
    end_min = st.number_input("⏱️ دقيقة النهاية:", min_value=0, value=1, step=1)
    end_sec = st.number_input(" ثانية النهاية:", min_value=0, max_value=59, value=0, step=1)

if st.button("✂️ قص وتحويل المقطع إلى 9:16"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب.")
    else:
        with st.spinner("⏳ جاري سحب المقطع وتعديله بدقة..."):
            try:
                temp_dir = tempfile.gettempdir()
                output_video = os.path.join(temp_dir, "target_video.mp4")
                
                # إعدادات yt-dlp المتطورة لتجاوز حظر البوتات والـ 403
                ydl_opts = {
                    'format': 'best[height<=720]',
                    'outtmpl': output_video,
                    'noplaylist': True,
                    'socket_timeout': 30,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Sec-Fetch-Mode': 'navigate',
                    },
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                start_total = (start_min * 60) + start_sec
                end_total = (end_min * 60) + end_sec
                output_clip_path = os.path.join(temp_dir, "final_short.mp4")

                with VideoFileClip(output_video) as video:
                    if end_total > video.duration:
                        end_total = int(video.duration)
                    
                    sub = video.subclipped(start_total, end_total)
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
                        label="⬇️ تحميل الشورت جاهز للنشر (9:16)",
                        data=file,
                        file_name="podcast_short.mp4",
                        mime="video/mp4"
                    )

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
