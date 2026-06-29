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
# 🎨 الجزء 3: قالب التنسيق السيادي وسحق أشرطة وصناديق الأزرار كلياً (CSS الشامل)
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
        
        /* 2. بناء شريط الملاحة الأفقي الملتصق بالقمة الشفاف مائة بالمائة وبأبعاد الشاملة */
        .shamel-top-ribbon {{
            position: fixed !important;
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            height: 60px !important; /* ارتفاع نحيف جداً وراقي يوفر كامل المساحة بالتصفح بالأسفل */
            background: rgba(0, 0, 0, 0.55) !important; /* غسق داكن يحمي الحروف ويمنع التداخل البصري */
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; /* خط الشاملة الأفقي الرقيق جداً */
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
        }}
        
        /* 3. الهندسة الجراحية: الروابط النصية الصافية والنحيفة مائة بالمائة وبدون أي مربعات خادعة */
        .shamel-nav-link {{
            color: #CDD5E0 !important; /* لون الخط الأبيض العاجي والناعم للمكتبة الشاملة */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 500 !important; /* خط نحيف ونقي تماماً */
            font-size: 16px !important;
            text-decoration: none !important; /* حذف أي خطوط تحت النص */
            padding: 0 15px !important;
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        /* تأثير الHover التفاعلي للشاملة: الوميض الفوري للأخضر الزمردي الشريف للمملكة عند تمرير الفأرة */
        .shamel-nav-link:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة للرابط */
            transform: translateY(-1px) !important;
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
# 📦 الجزء 4: حقن خماسية روابط الـ HTML النصية الصافية والمنحوتة صلب شريط القمة (تقليد دقيق للشاملة)
# ==========================================
# قمنا هنا باستخدام كود الـ HTML الصافي مائة بالمائة لكسر حلقة الصناديق البيضاء التلقائية لبايثون
st.markdown("""
    <div class='shamel-top-ribbon'>
        <!-- روابط الشاملة تتراص أفقياً بمرونة متناهية ونحافة مطلقة من اليمين إلى اليسار -->
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=search' target='_self' style='margin-right: auto; font-weight: 700;'>🔍 البحث في المكنز</a>
    </div>
""", unsafe_allow_html=True)

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة بالأسفل
st.markdown("<div style='margin-top: 70px;'></div>", unsafe_allow_html=True)
