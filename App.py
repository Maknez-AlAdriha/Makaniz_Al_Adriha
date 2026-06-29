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
# 🎨 الجزء 3: قالب التنسيق السيادي وإزاحة شريط القمة ليكون مرئياً بالكامل (CSS الشامل)
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
        
        /* تصفير الهوامش والبطانات الخارجية للمنصة لسحق المساحات الميتة والجوانب البيضاء كلياً */
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
        
        /* 🟢 تصحيح حاسم: إعطاء رأس الصفحة مساحة آمنة لمنع اختفاء شريط الأزرار بالقمة */
        div[data-testid="stHeader"] {{
            background: transparent !important;
            height: 55px !important; /* حجز مساحة مرئية ثابتة للشريط في قمة المتصفح */
            z-index: 99998 !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. الخلفية المتدرجة الساحرة: إزاحة موضع التمركز (top) ليكون مكشوفاً مائة بالمائة تحت حافة الشاشة */
        .shamel-top-gradient-ribbon {{
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important;
            position: absolute !important; /* تحويل التموضع إلى نسبي للحاوية لمنع الهروب خلف أشرطة جوجل كروم */
            top: 0px !important; /* الالتصاق التام والمرئي بالمليمتر في الجزء المخصص له */
            right: 0px !important;
            left: 0px !important;
            width: 100vw !important;
            height: 55px !important; /* ارتفاع رصين ومطابق للشاملة */
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
            border-bottom: 2px solid #D4AF37 !important; /* خط ذهبي مريني عريق يحدد الحافة */
        }}
        
        /* 3. النصوص الصافية المضيئة كالشاملة صلب شريط التدرج */
        .shamel-nav-text p {{
            color: #FFFFFF !important; /* خط أبيض ناصع مائة بالمائة للوضوح المطلق */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم رصين واحترافي للحروف */
            font-size: 16px !important;
            text-align: center !important;
            margin: 0 !important;
            padding: 2px 0 !important;
            cursor: pointer !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
            transition: color 0.2s ease-in-out !important;
        }}
        
        /* تأثير الوميض الزمردي عند تحريك الفأرة */
        .shamel-nav-text p:hover {{
            color: #10B981 !important; 
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
# 📦 الجزء 4: حقن روابط الشاملة صلب شريط التدرج اللوني الموجه برمجياً للظهور الصريح
# ==========================================
# تغليف الروابط الخمسة داخل الحاوية المصححة والمكشوفة للمتصفح تلقائياً
st.markdown("<div class='shamel-top-gradient-ribbon'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# مسافة أمان ترابية مريحة لدفع الصورة بالأسفل لتبدأ بنقاء تحت حافة الشريط المتدرج المرئي
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
