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
# 🎨 الجزء 3: قالب التنسيق السيادي وسحق أزرار الصناديق لتطابق الشاملة (CSS الشامل)
# ==========================================
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* 1. بسط وتثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود الشاشة ومقاومة التمرير قسرياً */
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
        
        /* تصفير الهوامش والبطانات الخارجية للمنصة لسحق المساحات الميتة */
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
            height: 60px !important; /* ارتفاع نحيف جداً وأنيق */
            background: rgba(0, 0, 0, 0.55) !important; /* Voile غسقي يحمي القراءة ويمنع التداخل */
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; /* خط الشاملة الأفقي الرقيق جداً */
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 50px !important;
        }}
        
        /* 3. الهندسة الجراحية: نسف وسحق الصناديق والحدود والخلفيات الزجاجية لتصبح نصوصاً صافية مائة بالمائة كالشاملة */
        .shamel-nav-btn button {{
            background: transparent !important; /* حذف الخلفية تماماً */
            color: #CDD5E0 !important; /* لون الخط الأبيض العاجي والناعم للشاملة */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 500 !important; /* خط نحيف ونقي وغير غليظ */
            font-size: 16px !important;
            border: none !important; /* نسف الحدود والخطوط المحيطة بالزر */
            border-radius: 0px !important;
            padding: 0px !important; /* إلغاء البطانة الداخلية ليتحول لنص حر */
            box-shadow: none !important;
            transition: color 0.2s ease-in-out !important;
            cursor: pointer;
            margin: 0px !important;
            text-align: right !important;
        }}
        
        /* تأثير الHover التفاعلي: الوميض الفوري للأخضر الزمردي التراثي للمملكة عند تمرير الفأرة */
        .shamel-nav-btn button:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة للرابط النشط */
            background: transparent !important;
            box-shadow: none !important;
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
# 📦 الجزء 4: توزيع وهندسة خماسية روابط الشاملة بالتوازي صلب الشريط النحيف بالقمة
# ==========================================
st.markdown("<div class='shamel-top-ribbon'>", unsafe_allow_html=True)

# تقسيم الأعمدة بالمليمتر البرمجي: العنوان يميناً، تتلوه الروابط متراصة أفقياً بنحافة، والبحث والاتصال يساراً
menu_col_title, menu_col_home, menu_col_sec, menu_col_about, menu_col_contact, menu_col_search, _ = st.columns([2.5, 0.9, 1.1, 1.0, 1.0, 1.8, 4.0])

with menu_col_title:
    # اسم المكنز الفخم ناصعاً في قمة اليمين ككلمة "المكتبة الشاملة"
    st.markdown("<p style='color:#FFFFFF; font-family:\"Tajawal\",sans-serif; font-size:18px; font-weight:900; margin-top:16px; padding-right:10px; cursor:default;'>المكنز الوطني للأضرحة</p>", unsafe_allow_html=True)

with menu_col_home:
    st.markdown("<div class='shamel-nav-btn' style='margin-top:16px;'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="shamel_btn_home"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_sec:
    st.markdown("<div class='shamel-nav-btn' style='margin-top:16px;'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="shamel_btn_sections"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_about:
    st.markdown("<div class='shamel-nav-btn' style='margin-top:16px;'>", unsafe_allow_html=True)
    if st.button("حول المشروع", key="shamel_btn_about"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_contact:
    st.markdown("<div class='shamel-nav-btn' style='margin-top:16px;'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="shamel_btn_contact"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_search:
    # أيقونة وشعار البحث مستقلة ومصاحبة في الجناح الأيسر للشريط المتناسق
    st.markdown("<div class='shamel-nav-btn' style='margin-top:16px;'>", unsafe_allow_html=True)
    if st.button("🔍 البحث في المكنز", key="shamel_btn_search"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة
st.markdown("<div style='margin-top: 70px;'></div>", unsafe_allow_html=True)
