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
# 🎨 الجزء 3: قالب التنسيق السيادي وتلوين حاوية الأزرار بالأسود المصمت (CSS الشامل)
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
        
        /* تصفير الهوامش والبطانات الخارجية للمنصة لالتصاق الشريط الأسود بسقف المتصفح تماماً */
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
        
        /* إلغاء الفراغات العمودية التلقائية بين المكونات العليا */
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. قسر الحاوية الأفقية العلوية لتتحول إلى شريط أسود مصمت مائة بالمائة يمتد بعرض الشاشة */
        div[data-testid="stHorizontalBlock"] {{
            background-color: #000000 !important; /* 🟢 صبغ الشريط بالأسود المصمت والكامل قسرياً */
            border-bottom: 2px solid #1E3A8A !important; /* خط أزرق ملكي رقيق يعزل عمارة الصورة */
            width: 100vw !important;
            padding: 10px 60px !important;
            margin: 0 !important;
        }}
        
        /* 3. الهندسة الجراحية: الروابط النصية الصافية والبيضاء الناصعة مائة بالمائة كالشاملة بدون أي مربعات */
        .shamel-nav-text p {{
            color: #FFFFFF !important; /* خط أبيض ناصع مائة بالمائة للوضوح المطلق فوق الأسود */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم رصين واحترافي للحروف */
            font-size: 17px !important;
            text-align: center !important;
            margin: 0 !important;
            padding: 5px 0 !important;
            cursor: pointer !important;
            transition: color 0.2s ease-in-out !important;
        }}
        
        /* تأثير الوميض الزمردي الشريف عند تمرير مؤشر الفأرة */
        .shamel-nav-text p:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة للرابط النشط */
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
# 📦 الجزء 4: إطلاق ورص خماسية الروابط النصية صلب الشريط الأسود الأصلي لبايثون بالقمة
# ==========================================
# استخدمنا هنا توزيع قنوات بايثون الأصلية المعترف بها من السيرفر لضمان الانبثاق الفوري مائة بالمائة
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.0, 1.2, 1.2, 1.1, 1.8, 4.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-text'><p>الرئيسية</p></div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-text'><p>أقسام المكنز</p></div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-text'><p>حول المشروع</p></div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-text'><p>اتصل بنا</p></div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-text'><p style='font-weight:900; color:#D4AF37 !important;'>🔍 البحث في المكنز</p></div>", unsafe_allow_html=True)

# حقن مسافة الأمان تحت الشريط الأسود لتبدأ الصورة بالأسفل بانتظام ونقاء
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
