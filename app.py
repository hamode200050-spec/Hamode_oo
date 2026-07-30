import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

st.set_page_config(page_title="محلل النصوص والذروات للبودكاست", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست الذكي (عبر تحليلات النص)</h1>
    <p style='text-align: center;'>قراءة سكريبت الفيديو واستخراج اللحظات التي تحتوي على قصص وأفكار كاملة بذكاء!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست طويل):")

def extract_video_id(youtube_url):
    """استخراج معرف الفيديو من الرابط بدقة"""
    if "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in youtube_url:
        return youtube_url.split("watch?v=")[1].split("&")[0]
    return None

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

if st.button("🚀 بدء تحليل النص واستخراج أفضل اللحظات"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("رابط يوتيوب غير صالح، يرجى التحقق منه.")
        else:
            with st.spinner("🤖 جاري سحب نصوص الفيديو (Transcript) وتحليل الكلام للبحث عن الذروات..."):
                try:
                    # جلب معلومات الفيديو الأساسية
                    ydl_opts = {'skip_download': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = info.get('title', 'بدون عنوان')

                    # محاولة جلب الترجمة أو النص باللغة العربية أو الإنجليزية
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
                    
                    st.success("✅ تم بنجاح قراءة وتحليل نص البودكاست!")
                    
                    st.markdown("---")
                    st.subheader(f"📌 عنوان الفيديو الأصلي:")
                    st.info(title)

                    # خوارزمية ذكية لتجميع النص إلى مقاطع قصيرة (بين 45 إلى 85 ثانية لكل مقطع) بناءً على تدفق الكلام
                    clips = []
                    current_clip_start = 0
                    current_text_chunk = []
                    
                    for entry in transcript_list:
                        start = entry['start']
                        text = entry['text']
                        
                        if start - current_clip_start < 75:  # تجميع الجمل حتى نقترب من المدة المثالية للشورتس
                            current_text_chunk.append(text)
                        else:
                            if len(current_text_chunk) > 3:  # نتأكد أن هناك محتوى كافي
                                end_time = start
                                snippet_text = " ".join(current_text_chunk[:5]) # أخذ أول جمل تعبر عن فكرة المقطع كعنوان
                                clips.append({
                                    "start": int(current_clip_start),
                                    "end": int(end_time),
                                    "summary": snippet_text[:60] + "..."
                                })
                            current_clip_start = start
                            current_text_chunk = [text]

                    if not clips:
                        st.warning("لم يتم العثور على مقاطع كافية داخل النص.")
                    else:
                        st.subheader(f"✨ تم العثور على ({len(clips)}) لقطة حقيقية مستخرجة من سياق الكلام:")

                        for idx, clip in enumerate(clips, 1):
                            start_str = format_time(clip['start'])
                            end_str = format_time(clip['end'])
                            clip_duration = clip['end'] - clip['start']
                            clip_snippet = clip['summary']

                            with st.container():
                                st.markdown(### 🎬 اللقطة رقم #{idx})
                                st.markdown(📌 **فكرة المقطع من النص:** `{clip_snippet}` )
                                st.markdown(⏳ **التوقيت الدقيق:** من (`{start_str}`) إلى (`{end_str}`) | **المدة:** {clip_duration} ثانية)
                                
                                custom_desc = f"لقطة مؤثرة من البودكاست حول: {clip_snippet}\n\n💡 شاهد المقطع للنهاية لتستفيد من الفكرة كاملة. لا تنس الإعجاب والاشتراك!"
                                st.text_area(f"✍️ الوصف المقترح للمقطع #{idx}:", value=custom_desc, height=75, key=f"desc_{idx}")
                                
                                st.text_input(f"🏷️ الهاشتاقات المخصصة #{idx}:", value=f"#shorts #اكسبلور #بودكاست #وعي #قصص", key=f"tags_{idx}")
                                
                                st.markdown("---")

                except TranscriptsDisabled:
                    st.error("❌ عذراً، الترجمة أو النصوص غير مفعلة لهذا الفيديو، ولا يمكن استخراج النص داخله.")
                except NoTranscriptFound:
                    st.error("❌ لم يتم العثور على نصوص متوفرة بهذا الفيديو باللغة العربية أو الإنجليزية.")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تحليل النص: {e}")
