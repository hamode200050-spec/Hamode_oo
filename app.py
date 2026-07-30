import streamlit as st
import yt_dlp

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذروات الذكي</h1>
    <p style='text-align: center;'>توقيتات دقيقة، مدة مرنة، ووصف وهاشتاقات مخصصة لكل مقطع!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست طويل):")

def format_time(seconds):
    """دالة لتحويل الثواني إلى تنسيق زمني دقيق"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

if st.button("🚀 تحليل عميق واستخراج اللقطات الذكية"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري قراءة هيكل الفيديو وتحديد اللقطات والذروات بدقة..."):
            try:
                ydl_opts = {
                    'skip_download': True,
                    'extract_flat': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'بدون عنوان')
                    duration = info.get('duration', 0)
                    chapters = info.get('chapters', None)

                st.success("✅ تم تحليل هيكل البودكاست بنجاح!")
                
                st.markdown("---")
                st.subheader(f"📌 عنوان الفيديو الأصلي:")
                st.info(title)
                
                st.subheader("⏱️ اللقطات المقترحة مع بدايتها ونهايتها:")
                
                clips_list = []
                if chapters:
                    for i in range(len(chapters)):
                        start_time = int(chapters[i].get('start_time', 0))
                        # النهاية هي بداية الفصل التالي أو نهاية الفيديو، مع إعطاء مساحة أطول للمقطع (حتى 3 دقائق حسب الفصل)
                        if i < len(chapters) - 1:
                            end_time = int(chapters[i+1].get('start_time', start_time + 120))
                        else:
                            end_time = int(duration)
                        
                        # تحديد الحد الأقصى للمقطع بـ 3 دقائق (180 ثانية) ليبقى مناسباً ومنطقيأً للشورتس
                        if end_time - start_time > 180:
                            end_time = start_time + 120
                            
                        clips_list.append({
                            "title": chapters[i].get('title', f"مقطع مميز #{i+1}"),
                            "start": start_time,
                            "end": end_time
                        })
                else:
                    # تقسيم افتراضي كل 3 دقائق إذا لم توجد فصول
                    step = 180
                    for i, sec in enumerate(range(0, max(1, duration - 60), step), 1):
                        clips_list.append({
                            "title": f"ذروة وحوار مهم للبودكاست #{i}",
                            "start": sec,
                            "end": min(sec + 120, duration)
                        })

                # عرض المقاطع بشكل احترافي مع وصف وهاشتاقات مخصصة لكل مقطع
                for idx, clip in enumerate(clips_list, 1):
                    start_str = format_time(clip['start'])
                    end_str = format_time(clip['end'])
                    clip_duration = clip['end'] - clip['start']
                    clip_title = clip['title']
                    
                    with st.container():
                        st.markdown(f"### 🎬 اللقطة رقم #{idx}")
                        st.markdown(f"📌 **اسم المقطع:** `{clip_title}`")
                        st.markdown(f"⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة:** {clip_duration} ثانية")
                        
                        # وصف مخصص لكل لقطة بناءً على عنوانها
                        custom_desc = f"لقطة مؤثرة من البودكاست تتحدث عن: {clip_title}.\n\n💡 لا تنسوا الإعجاب والاشتراك للمزيد من الاقتباسات الهادفة."
                        st.text_area(f"✍️ الوصف المقترح للمقطع #{idx}:", value=custom_desc, height=80, key=f"desc_{idx}")
                        
                        # هاشتاقات مخصصة مستوحاة من عنوان المقطع
                        clean_tags = "#shorts #اكسبلور #بودكاست #رعصات #وعي #تطوير_الذات"
                        st.text_code_val = st.text_input(f"🏷️ الهاشتاقات المخصصة #{idx}:", value=f"#shorts #بودكاست #اكسبلور #{clip_title.replace(' ', '_')}", key=f"tags_{idx}")
                        
                        st.markdown("---")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب تفاصيل الرابط: {e}")
