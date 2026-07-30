import streamlit as st
import yt_dlp

st.set_page_config(page_title="المحلل الذكي للبودكاست", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 محلل البودكاست والذهاشتاقات الذكي</h1>
    <p style='text-align: center;'>ضع رابط يوتيوب وسيقوم الذكاء الاصطناعي باكتشاف اللقطات، التوقيتات، الوصف، والهاشتاقات فوراً!</p>
""", unsafe_allow_html=True)

url = st.text_input("🔗 أدخل رابط يوتيوب (بودكاست أو فيديو طويل):")

if st.button("🚀 ابدأ تحليل الفيديو بالذكاء الاصطناعي"):
    if not url:
        st.warning("الرجاء إدخال رابط يوتيوب أولاً.")
    else:
        with st.spinner("🤖 جاري استخراج معلومات وفصول الفيديو وتحليل المحتوى..."):
            try:
                ydl_opts = {
                    'skip_download': True,
                    'extract_flat': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'بدون عنوان')
                    description = info.get('description', 'لا يوجد وصف')
                    duration = info.get('duration', 0)
                    chapters = info.get('chapters', None)

                st.success("✅ تم تحليل محتوى الفيديو بنجاح!")
                
                st.markdown("---")
                st.subheader(f"📌 عنوان الفيديو:")
                st.write(title)
                
                st.subheader("⏱️ اللقطات والمقاطع المهمة المقترحة:")
                if chapters:
                    for idx, ch in enumerate(chapters, 1):
                        start_sec = int(ch.get('start_time', 0))
                        m, s = divmod(start_sec, 60)
                        st.markdown(f"* **اللقطة #{idx}:** `{ch.get('title', 'مقطع مهم')}` — **التوقيت:** ({m:02d}:{s:02d})")
                else:
                    # تقسيم افتراضي ذكي إذا لم توجد فصول جاهزة
                    step = 300 # كل 5 دقائق
                    for i, sec in enumerate(range(0, max(1, duration - 60), step), 1):
                        m, s = divmod(sec, 60)
                        st.markdown(f"* **مقترح ذكي #{i}:** يبدأ من الدقيقة `{m:02d}:{s:02d}` (فكرة ممتازة لقصة أو حوار قصير)")

                st.markdown("---")
                st.subheader("✍️ الوصف المقترح للشورتس:")
                short_desc = f"{title[:100]}...\n\nلا تنسوا الاشتراك في القناة للمزيد من اقتباسات البودكاست المميزة! 🔥"
                st.text_area("نسخ الوصف:", value=short_desc, height=100)

                st.subheader("🏷️ الهاشتاقات المقترحة (Hashtags):")
                st.code("#shorts #بودكاست #اكسبلور #رعصات_بودكاست #فديوهات_مفيدة #حكم_وعبر", language="text")

            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب بيانات الرابط: {e}")
