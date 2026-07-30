import streamlit as st
import yt_dlp

st.set_page_config(page_title="محلل البودكاست الذكي", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذروات الذكي</h1>
    <p style='text-align: center;'>استخراج أهم اللحظات والقصص الأساسية فقط مع عناوينها الحقيقية، الوصف، والهاشتاقات!</p>
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

if st.button("🚀 تحليل واكتشاف أهم اللحظات والقصص"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري استخراج الفصول والقصص الأساسية وتحليل محتواها..."):
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

                st.success("✅ تم استخراج أهم لقطات البودكاست بنجاح!")
                
                st.markdown("---")
                st.subheader(f"📌 عنوان الفيديو الأصلي:")
                st.info(title)
                
                clips_list = []
                
                if chapters:
                    # الاعتماد على فصول البودكاست الحقيقية (أهم اللحظات والقصص)
                    for i in range(len(chapters)):
                        start_time = int(chapters[i].get('start_time', 0))
                        chapter_title = chapters[i].get('title', f'قصة مؤثرة #{i+1}')
                        
                        # تحديد نهاية مرنة للفصل (حتى بداية الفصل التالي أو بحد أقصى 85 ثانية لاكتمال الفكرة)
                        if i < len(chapters) - 1:
                            next_start = int(chapters[i+1].get('start_time', start_time + 60))
                            section_len = next_start - start_time
                            if section_len > 90:
                                end_time = start_time + 75  # مدة ممتازة ومثالية للشورتس
                            else:
                                end_time = next_start
                        else:
                            end_time = min(int(duration), start_time + 75)
                            
                        # التأكد من عدم قصر المدة بشكل يضر بالفكرة
                        if end_time - start_time < 30:
                            end_time = start_time + 50

                        clips_list.append({
                            "title": chapter_title,
                            "start": start_time,
                            "end": end_time
                        })
                else:
                    # إذا لم توجد فصول رسمية، سنكتفي بأفضل اللقطات الموزعة بذكاء (حوالي 8-10 لقطات رئيسية فقط)
                    step = max(60, duration // 10) if duration > 600 else 60
                    for i, sec in enumerate(range(0, int(duration) - 30, step), 1):
                        clips_list.append({
                            "title": f"ذروة وحوار رئيسي رقم #{i}",
                            "start": sec,
                            "end": min(sec + 70, duration)
                        })

                st.subheader(f"✨ تم العثور على ({len(clips_list)}) من أهم اللحظات والقصص المؤثرة في الحلقة:")

                for idx, clip in enumerate(clips_list, 1):
                    start_str = format_time(clip['start'])
                    end_str = format_time(clip['end'])
                    clip_duration = clip['end'] - clip['start']
                    clip_title = clip['title']
                    
                    with st.container():
                        st.markdown(f"### 🎬 اللقطة رقم #{idx}")
                        st.markdown(f"📌 **اسم المقطع / القصة:** `{clip_title}`")
                        st.markdown(f"⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة:** {clip_duration} ثانية")
                        
                        # وصف مخصص دقيق مستوحى من عنوان القصة
                        custom_desc = f"قصة مؤثرة جداً من البودكاست تتحدث عن: {clip_title}.\n\n💡 شاهد المقطع للنهاية لتستفيد من الفكرة الكاملة. لا تنس الإعجاب والاشتراك للمزيد!"
                        st.text_area(f"✍️ الوصف المقترح للمقطع #{idx}:", value=custom_desc, height=75, key=f"desc_{idx}")
                        
                        # هاشتاقات مخصصة مستوحاة من اسم الفصل أو القصة
                        tag_slug = clip_title.replace(' ', '_').replace('|', '').replace('?', '').replace('!', '')
                        custom_tags = f"#shorts #اكسبلور #بودكاست #{tag_slug} #تطوير_الذات #قصص"
                        st.text_input(f"🏷️ الهاشتاقات المخصصة #{idx}:", value=custom_tags, key=f"tags_{idx}")
                        
                        st.markdown("---")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب تفاصيل الرابط: {e}")
