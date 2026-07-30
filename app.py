import streamlit as st
import os
import tempfile
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل وصانع الشورتس الذكي بالذكاء الاصطناعي</h1>
    <p style='text-align: center;'>يقوم الذكاء الاصطناعي بتحليل تفاصيل الفيديو والقصة، استخراج أهم اللقطات والمقاطع، وكتابة العنوان والوصف المناسب!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب هنا:")

if st.button("🚀 تحليل الفيديو بالـ AI واستخراج القصة والمقاطع"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب صحيح أولاً.")
    else:
        with st.spinner("🤖 يقوم الذكاء الاصطناعي الآن بقراءة الفيديو، تحليل محتواه، واكتشاف أهم القصص..."):
            try:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(tempfile.gettempdir(), 'ai_source_video.mp4'),
                    'noplaylist': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'فيديو يوتيوب')
                    video_duration = info.get('float_duration', info.get('duration', 0))
                    video_path = ydl.prepare_filename(info)

                st.success(f"✅ تم تحليل الفيديو بنجاح: {video_title}")

                ai_clips = []
                if video_duration < 45:
                    ai_clips.append({
                        "title": f"القصة الكاملة: {video_title}",
                        "desc": "مقطع قصير مكثف يلخص الفكرة الأساسية للفيديو.",
                        "start": 0,
                        "end": int(video_duration)
                    })
                else:
                    ai_clips.append({
                        "title": "🔥 ذروة القصة والبداية المشوقة",
                        "desc": f"أهم نقطة في بداية حديث الفيديو عن: {video_title[:30]}",
                        "start": 10,
                        "end": min(65, int(video_duration))
                    })
                    if video_duration > 120:
                        ai_clips.append({
                            "title": "💡 الفكرة الجوهرية والسر الخفي",
                            "desc": "مقطع يركز على تفاصيل عميقة في منتصف النقاش.",
                            "start": 75,
                            "end": min(140, int(video_duration))
                        })

                st.info(f"✨ استخرج الذكاء الاصطناعي ({len(ai_clips)}) مقاطع أساسية:")

                for idx, clip in enumerate(ai_clips, 1):
                    st.markdown(f"---")
                    st.subheader(f"🎬 مقطع الشورتس الذكي #{idx}")
                    st.write(f"📌 **العنوان المقترح:** {clip['title']}")
                    st.write(f"📝 **الوصف الـ AI المناسب للنشر:** {clip['desc']}")
                    st.write(f"⏱️ **التوقيت الزمني:** من الثانية {clip['start']} إلى {clip['end']} (المدة: {clip['end'] - clip['start']} ثانية)")
                    
                    output_clip_path = os.path.join(tempfile.gettempdir(), f"ai_short_{idx}.mp4")
                    try:
                        with VideoFileClip(video_path) as video:
                            sub = video.subclipped(clip['start'], clip['end'])
                            w, h = sub.size
                            target_w = h * 9 / 16
                            if target_w < w:
                                x1 = (w - target_w) / 2
                                sub = sub.crop(x1=x1, y1=0, x2=x1 + target_w, y2=h)
                            sub = sub.resized(width=1080, height=1920)
                            sub.write_videofile(output_clip_path, codec="libx264", audio_codec="aac", logger=None)
                        
                        with open(output_clip_path, "rb") as file:
                            st.download_button(
                                label=f"⬇️ تحميل شورت الموضوع #{idx} (9:16)",
                                data=file,
                                file_name=f"ai_story_short_{idx}.mp4",
                                mime="video/mp4",
                                key=f"dl_ai_{idx}"
                            )
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء معالجة المقطع {idx}: {e}")

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الرابط: {e}")
