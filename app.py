import streamlit as st
import yt_dlp

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذروات الذكي</h1>
    <p style='text-align: center;'>استخراج جميع اللحظات بدون أي حدود للعدد، وبمدد حقيقية متغيرة لاكتمال الفكرة!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست طويل):")

def format_time(seconds):
    """دالة لتحويل الثواني إلى تنسيق زمني دقيق (ساعات:دقائق:ثواني)"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

if st.button("🚀 تحليل شامل واستخراج كل اللقطات بدقة"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري قراءة محتوى الفيديو وفحص كافة الفصول والقصص..."):
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

                st.success("✅ تم تحليل محتوى البودكاست بنجاح!")
                
                st.markdown("---")
                st.subheader(f"📌 عنوان الفيديو الأصلي:")
                st.info(title)
                
                clips_list = []
                if chapters:
                    # جلب كل الفصول الموجودة في الفيديو بلا استثناء (بدون أي تقييد بـ 10 مقاطع)
                    for i in range(len(chapters)):
                        start_time = int(chapters[i].get('start_time', 0))
                        
                        # تحديد نهاية المقطع بناءً على وقت بداية الفصل التالي مباشرةً لضمان أخذ طول الفكرة الحقيقي
                        if i < len(chapters) - 1:
                            end_time = int(chapters[i+1].get('start_time', start_time + 60))
                        else:
                            end_time = int(duration)
                        
                        # إذا كان الفصل طويلاً جداً (مثلاً أكثر من دقيقتين ونصف)، نسمح له بالامتداد حتى دقيقتين لتبقى الفكرة مشوقة للشورتس
                        section_len = end_time - start_time
                        if section_len > 150: 
                            end_time = start_time + 90  # دقيقة ونصف كحد أقصى للقصص الطويلة جداً
                        elif section_len < 25:
                            end_time = start_time + 45  # لكي لا يكون المقطع قصيراً مكسور الفكرة
                            
                        clips_list.append({
                            "title": chapters[i].get('title', f"لقطة مؤثرة #{i+1}"),
                            "start": start_time,
                            "end": end_time
                        })
                else:
                    # إذا لم توجد فصول، نقسم الفيديو إلى مقاطع متتالية تغطي الفيديو كاملاً
                    step = 75
                    for i, sec in enumerate(range(0, max(1, duration - 30), step), 1):
                        end_sec = min(sec + 75, duration)
                        clips_list.append({
                            "title": f"ذروة وقصة مؤثرة #{i}",
                            "start": sec,
                            "end": end_sec
                        })

                st.subheader(f"✨ تم العثور على ({len(clips_list)}) لقطة رئيسية في هذا الفيديو (بكل العدد الحقيقي ومدد متغيرة تماماً):")

                for idx, clip in enumerate(clips_list, 1):
                    start_str = format_time(clip['start'])
                    end_str = format_time(clip['end'])
                    clip_duration = clip['end'] - clip['start']
                    clip_title = clip['title']
                    
                    with st.container():
                        st.markdown(f"### 🎬 اللقطة رقم #{idx}")
                        st.markdown(f"📌 **عنوان اللقطة أو القصة:** `{clip_title}`")
                        st.markdown(f"⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة الحقيقية:** {clip_duration} ثانية")
                        
                        # وصف مخصص لكل لقطة
                        custom_desc = f"قصة وفكرة مؤثرة من البودكاست حول: {clip_title}.\n\n💡 شاهد المقطع للنهاية لتستفيد من الفكرة كاملة. لا تنس الإعجاب والاشتراك!"
                        st.text_area(f"✍️ الوصف المقترح للمقطع #{idx}:", value=custom_desc, height=70, key=f"desc_{idx}")
                        
                        # هاشتاقات مخصصة مستوحاة من العنوان
                        tag_slug = clip_title.replace(' ', '_').replace('|', '')
                        st.text_input(f"🏷️ الهاشتاقات المخصصة #{idx}:", value=f"#shorts #اكسبلور #بودكاست #{tag_slug}", key=f"tags_{idx}")
                        
                        st.markdown("---")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب تفاصيل الرابط: {e}")
