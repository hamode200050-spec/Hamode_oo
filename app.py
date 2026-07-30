import streamlit as st
import os
import tempfile
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 صانع الشورتس السريع للبودكاست</h1>
    <p style='text-align: center;'>أدخل الرابط، حدد وقت المقطع، وحوله إلى 9:16 فوراً بدون أخطاء!</p>
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
        with st.spinner("⏳ جاري سحب المقطع بدقة وتعديله..."):
            try:
                yt = YouTube(url)
                # استخدام دقة متوسطة لتسريع العملية وتجنب الحظر
                stream = yt.streams.filter(file_extension='mp4', res="720p").first()
                if not stream:
                    stream = yt.streams.filter(file_extension='mp4').first()
                
                temp_dir = tempfile.gettempdir()
                video_path = stream.download(output_path=temp_dir, filename="target_video.mp4")

                start_total = (start_min * 60) + start_sec
                end_total = (end_min * 60) + end_sec

                output_clip_path = os.path.join(temp_dir, "final_short.mp4")

                with VideoFileClip(video_path) as video:
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
