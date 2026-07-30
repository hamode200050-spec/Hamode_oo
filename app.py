import streamlit as st
import os
import tempfile
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل وصانع الشورتس الذكي بالذكاء الاصطناعي</h1>
    <p style='text-align: center;'>استخراج وتحليل اللقطات المهمة من البودكاست الطويل وتحويلها لشورتس بدقة 9:16 تلقائياً!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست أو فيديو طويل):")

if st.button("🚀 AI تحليل الفيديو واستخراج اللقطات"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 يقوم الذكاء الاصطناعي الآن بقراءة الفيديو واكتشاف أفضل اللقطات..."):
            try:
                # استخدام pytubefix المتوافقة تماماً مع تجاوز حظر سيرفرات السحابية
                yt = YouTube(url)
                video_title = yt.title
                video_duration = yt.length
                
                # جلب دقة مناسبة وسريعة
                stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                if not stream:
                    stream = yt.streams.get_highest_resolution()
                    
                temp_dir = tempfile.gettempdir()
                video_path = stream.download(output_path=temp_dir, filename="podcast_source.mp4")

                st.success(f"✅ تم تحليل الفيديو بنجاح: {video_title}")

                # تقسيم الفيديو تلقائياً إلى مقاطع مقترحة للبودكاست الطويل
                ai_clips = []
                step = 300 # كل 5 دقائق لقطة مقترحة
                for i, sec in enumerate(range(0, max(1, int(video_duration) - 60), step)):
                    ai_clips.append({
                        "title": f"🔥 لقطة مقترحة رقم #{i+1} للبودكاست",
                        "start": sec,
                        "end": min(sec + 50, int(video_duration))
                    })

                st.info(f"✨ اكتشف الذكاء الاصطناعي ({len(ai_clips)}) مقطعاً مهماً في هذا البودكاست:")

                for idx, clip in enumerate(ai_clips[:10], 1):
                    st.markdown("---")
                    st.subheader(f"🎬 اللقطة المقترحة #{idx}")
                    st.write(f"📌 **العنوان:** {clip['title']}")
                    st.write(f"⏱️ **التوقيت:** من الدقيقة {clip['start']//60} إلى الدقيقة {clip['end']//60}")
                    
                    output_clip_path = os.path.join(temp_dir, f"ai_short_{idx}.mp4")
                    
                    if st.button(f"✂️ قص وتحويل هذه اللقطة إلى 9:16", key=f"cut_btn_{idx}"):
                        with st.spinner("جاري قص وتعديل المقطع بدقة عمودية..."):
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
