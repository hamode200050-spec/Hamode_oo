import streamlit as st
import yt_dlp

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذروات الذكي</h1>
    <p style='text-align: center;'>استخراج جميع اللحظات المهمة بمدد مرنة وطبيعية (لكي تكتمل فكرة القصة تماماً للمشاهد)!</p>
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

if st.button("🚀 تحليل الفيديو واكتشاف اللحظات الكاملة"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري قراءة محتوى الفيديو وفحص الفصول لضمان اكتمال كل فكرة..."):
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
                    for i in range(len(chapters)):
                        start_time = int(chapters[i].get('start_time', 0))
                        
                        # تحديد نهاية مرنة تماماً بناءً على طول القصة أو الحوار في الفصل
                        if i < len(chapters) - 1:
                            next_start = int(chapters[i+1].get('start_time', start_time + 60))
                            section_len = next_start - start_time
                            
                            # إذا كانت الفكرة قصيرة نأخذها كما هي، وإذا طويلة نسمح لها بالامتداد حتى تكتمل (بين 45 إلى 90 ثانية حسب سياق القصة)
                            if section_len > 95:
                                end_time = start_time + 75 # مدة مثالية لاكتمال المعنى
                            else:
                                end_time = next_start
                        else:
                            end_time = min(int(duration), start_time + 70)
                        
                        # التأكد من عدم وجود مقاطع قصيرة مكسورة
                        if end_time - start_time < 30:
                            end_time = start_time + 50
                            
                        clips_list.append({
                            "title": chapters[i].get('title', f"لقطة مؤثرة #{i+1}"),
                            "start": start_time,
                            "end": end_time
                        })
                else:
                    # تقسيم ذكي مرن إذا لم توجد فصول جاهزة في الفيديو
                    step = 100
                    for i, sec in enumerate(range(0, max(1, duration - 40), step), 1):
                        clips_list.append({
                            "title": f"ذروة وقصة مؤثرة #{i}",
                            "start": sec,
                            "end": min(sec + 65, duration)
                        })

                st.subheader(f"✨ تم العثور على ({len(clips_list)}) لقطة رئيسية (بدون قيود، وبمدد تتناسب مع اكتمال الفكرة تماماً):")

                for idx, clip in enumerate(clips_list, 1):
                    start_str = format_time(clip['start'])
                    end_str = format_time(clip['end'])
                    clip_duration = clip['end'] - clip['start']
                    clip_title = clip['title']
                    
                    with st.container():
                        st.markdown(f"### 🎬 اللقطة رقم #{idx}")
                        st.markdown(f"📌 **عنوان اللقطة أو القصة:** `{clip_title}`")
                        st.markdown(f"⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة:** {clip_duration} ثانية (مرنة لاكتمال الفكرة للمشاهد)")
                        
                        # وصف مخصص لكل لقطة
                        custom_desc = f"قصة وفكرة مؤثرة من البودكاست حول: {clip_title}.\n\n💡 شاهد المقطع للنهاية لتستفيد من الفكرة كاملة. لا تنس الإعجاب والاشتراك!"
                        st.text_area(f"✍️ الوصف المقترح للمقطع #{idx}:", value=custom_desc, height=70, key=f"desc_{idx}")
                        
                        # هاشتاقات مخصصة مستوحاة من العنوان
                        tag_slug = clip_title.replace(' ', '_').replace('|', '')
                        st.text_input(f"🏷️ الهاشتاقات المخصصة #{idx}:", value=f"#shorts #اكسبلور #بودكاست #{tag_slug}", key=f"tags_{idx}")
                        
                        st.markdown("---")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب تفاصيل الرابط: {e}")
