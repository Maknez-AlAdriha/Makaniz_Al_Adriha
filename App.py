import streamlit as st
import os
import base64

# ==========================================
# 🇲🇦 الجزء 1: إعدادات الشاشة بعرض المتصفح الكامل 100% لعام 2026
# ==========================================
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# ==========================================
# 🏢 الجزء 2: محرك استدعاء وتجهيز الصورة الملكية بنظام القراءة الفورية
# ==========================================
target_banner = None
for valid_name in ["banner.png", "banner..png", "Banner.png", "banner.PNG", "banner.jpg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

encoded_string = ""
if target_banner:
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

# ==========================================
# 🎨 الجزء 3: قالب التنسيق السيادي وتضخيم الروابط النصية لتصبح بيضاء مضيئة (CSS الشامل)
# ==========================================
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* 1. تثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود الشاشة ومقاومة التمرير قسرياً */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover !important;
            background-position: center top !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            width: 100vw !important;
            min-height: 100vh !important;
            height: 100vh !important;
        }}
        
        /* تصفير الهوامش والبطانات الخارجية للمنصة لسحق المساحات الميتة والجوانب البيضاء */
        div[data-testid="stAppViewBlockContainer"] {{
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
            margin: 0rem !important;
            background: transparent !important;
        }}
        .main .block-container {{
            max-width: 100% !important;
            padding: 0rem !important;
            margin: 0rem !important;
            background: transparent !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. بناء شريط الملاحة الأفقي الملتصق بالقمة الشفاف مائة بالمائة وبأبعاد الشاملة المحدثة */
        .shamel-top-ribbon {{
            position: fixed !important;
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            height: 60px !important; /* ارتفاع نحيف جداً وراقي يوفر كامل المساحة بالتصفح بالأسفل */
            background: rgba(0, 0, 0, 0.6) !important; /* غسق داكن واقي يحمي الحروف ويمنع التداخل البصري */
            border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important; /* خط الشاملة الأفقي الرقيق جداً */
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
        }}
        
        /* 3. الهندسة الجراحية: الروابط النصية الصافية المضيئة باللون الأبيض الناصع مائة بالمائة */
        .shamel-nav-link {{
            color: #FFFFFF !important; /* 🟢 التطوير الحاسم: جعل الخطوط بيضاء ناصعة ومضيئة مائة بالمائة لتدمر الاختفاء */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم فخم ورشيق للروابط ليبرز وضوحها */
            font-size: 17px !important; /* حجم رصين واحترافي */
            text-decoration: none !important; /* حذف أي خطوط ميتة تحت النص */
            padding: 0 25px !important; /* توسيع المسافة الأفقية المريحة بين الكلمات */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important; /* حقن ظلال سوداء خلف الحروف لتبرز فوق السحاب */
            transition: color 0.25s ease-in-out, transform 0.25s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        /* تأثير الHover التفاعلي للشاملة: الوميض الفوري للأخضر الزمردي التراثي للمملكة عند تمرير الفأرة */
        .shamel-nav-link:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة الحية للرابط */
            transform: translateY(-1px) !important;
            text-shadow: 0px 0px 8px rgba(16, 185, 129, 0.6) !important;
        }}

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 📦 الجزء 4: حقن خماسية روابط الـ HTML النصية الصافية والبيضاء الناصعة صلب شريط القمة (الشاملة مائة بالمائة)
# ==========================================
st.markdown("""
    <div class='shamel-top-ribbon'>
        <!-- روابط الشاملة المضيئة تتراص أفقياً بمرونة مطلقة من اليمين إلى اليسار لعام 2026 -->
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=search' target='_self' style='margin-right: auto; font-weight: 900; color: #D4AF37 !important;'>🔍 البحث في المكنز</a>
    </div>
""", unsafe_allow_html=True)

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة بالأسفل
st.markdown("<div style='margin-top: 70px;'></div>", unsafe_allow_html=True)
