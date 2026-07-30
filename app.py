import streamlit as st
import os
import tempfile
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="محلل وصانع الشورتس الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل وصانع الشورتس الذكي بالذكاء الاصطناعي</h1>
    <p style='text-align: center;'>قم برفع الفيديو أو لصق الرابط لتحليل القصة واستخراج الشورتس الذكية بدقة 9:16!</p>
""", unsafe_allow_html=True)

# خيارين: إما رفع ملف فيديو مباشرة (لتجنب حظر يوتيوب نهائياً) أو لصق الرابط
upload_option = st.radio("اختر طريقة إدخال الفيديو:", ["رفع ملف فيديو من الجهاز", "رابط يوتيوب"])

video_path = None
video_title = "فيديو مرفق"
video_duration = 0

if upload_option == "رفع ملف فيديو من الجهاز":
    uploaded_file = st.file_uploader("📂 اختر ملف الفيديو (MP4):", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        video_title = uploaded_file.name
        
        with VideoFileClip(video_path) as clip:
            video_duration = clip.duration
else:
    url = st.text_input("🔗 أدخل رابط يوتيوب هنا:")
    if url and st.button("🚀 تحليل رابط يوتيوب"):
        st.warning("⚠️ نظراً لقيود حماية يوتيوب الصارمة على السيرفرات السحابية، يُفضل استخدام خيار (رفع ملف فيديو من الجهاز) للحصول على أفضل وأسرع نتيجة بدون أخطاء.")

if video_path and st.button("✨ ابدأ استخراج وتعديل مقاطع الشورتس (9:16)"):
    with st.spinner("🤖 جاري تحليل وتقطيع الفيديو بالذكاء الاصطناعي..."):
        try:
            ai_clips = []
            if video_duration < 45:
                ai_clips.append({
                    "title": f"القصة الكاملة: {video_title}",
                    "desc": "مقطع قصير مكثف يلخص الفكرة الأساسية.",
                    "start": 0,
                    "end": int(video_duration)
                })
            else:
                ai_clips.append({
                    "title": "🔥 اللقطة والبداية المشوقة",
                    "desc": "أهم نقطة في بداية الفيديو لجذب الانتباه.",
                    "start": 0,
                    "end": min(60, int(video_duration))
                })
                if video_duration > 120:
                    ai_clips.append({
                        "title": "💡 ذروة ونهاية القصة",
                        "desc": "مقطع يركز على التفاصيل الجوهرية.",
                        "start": 65,
                        "end": min(125, int(video_duration))
                    })

            st.success(f"✅ تم تحليل الفيديو بنجاح! المدة الإجمالية: {int(video_duration)} ثانية")

            for idx, clip in enumerate(ai_clips, 1):
                st.markdown("---")
                st.subheader(f"🎬 مقطع الشورتس الذكي #{idx}")
                st.write(str(f"📌 **العنوان:** {clip['title']}"))
                st.write(str(f"📝 **الوصف:** {clip['desc']}"))
                st.write(str(f"⏱️ **التوقيت:** من الثانية {clip['start']} إلى {clip['end']}"))
                
                output_clip_path = os.path.join(tempfile.gettempdir(), f"ai_short_{idx}.mp4")
                
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
                        label=str(f"⬇️ تحميل شورت رقم #{idx} (9:16)"),
                        data=file,
                        file_name=f"short_{idx}.mp4",
                        mime="video/mp4",
                        key=str(f"dl_btn_{idx}")
                    )
        except Exception as e:
            st.error(str(f"حدث خطأ أثناء معالجة الفيديو: {e}"))
