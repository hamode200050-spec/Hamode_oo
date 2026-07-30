import streamlit as st
import yt_dlp

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذروات الذكي</h1>
    <p style='text-align: center;'>استخراج التوقيتات الدقيقة (بداية ونهاية)، العناوين، الوصف، والهاشتاقات بذكاء!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست طويل):")

def format_time(seconds):
    """دالة لتحويل الثواني إلى تنسيق زمني دقيق (ساعات:دقائق:ثواني أو دقائق:ثواني)"""
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
                    description = info.get('description', '')
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
                        # النهاية هي بداية الفصل التالي، أو نهاية الفيديو إذا كان الفصل الأخير
                        if i < len(chapters) - 1:
                            end_time = int(chapters[i+1].get('start_time', start_time + 60))
                        else:
                            end_time = int(duration)
                        
                        # إذا كان المقطع طويلاً جداً (أكثر من دقيقتين)، نقترحة كـ 60 ثانية مثالية للشورتس
                        if end_time - start_time > 90:
                            end_time = start_time + 60
                            
                        clips_list.append({
                            "title": chapters[i].get('title', f"مقطع مميز #{i+1}"),
                            "start": start_time,
                            "end": end_time
                        })
                else:
                    # تقسيم ذكي كل 5 دقائق إذا لم توجد فصول
                    step = 300
                    for i, sec in enumerate(range(0, max(1, duration - 60), step), 1):
                        clips_list.append({
                            "title": f"ذروة وحوار مهم للبودكاست #{i}",
                            "start": sec,
                            "end": min(sec + 55, duration)
                        })

                # عرض المققاطع بتنسيق مرتب وواضح
                for idx, clip in enumerate(clips_list, 1):
                    start_str = format_time(clip['start'])
                    end_str = format_time(clip['end'])
                    
                    with st.container():
                        st.markdown(f"### 🎬 اللقطة رقم #{idx}")
                        st.write(f"📌 **اسم المقطع:** `{clip['title']}`")
                        st.write(f"⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة:** {clip['end'] - clip['start']} ثانية")
                        st.markdown("---")

                st.subheader("✍️ الوصف الشامل المقترح للفيديو:")
                clean_desc = description[:300] if description else title
                suggested_description = f"{title}\n\n{clean_desc}...\n\n💡 اقتباسات وأجمل لقطات البودكاست.\n🔔 لا تنسوا الاشتراك والإعجاب ليصلكم كل جديد!"
                st.text_area("نسخ الوصف:", value=suggested_description, height=120)

                st.subheader("🏷️ الهاشتاقات المقترحة (Hashtags):")
                st.code("#shorts #اكسبلور #بودكاست #رعصات #تصميم_فيديوهات #فطنة #حكم_وعبر #فيديو_قصير", language="text")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب تفاصيل الرابط: {e}")
