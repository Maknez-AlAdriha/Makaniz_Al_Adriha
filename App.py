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
# 🎨 الجزء 3: سحق الهوامش وبناء الشريط الأسود المطور لأزرار بايثون الأصلية (CSS الشامل)
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
        
        /* تصفير الهوامش والبطانات الخارجية للمنصة لالتصاق الشريط الأسود بسقف المتصفح تماماً وبدون حواف بيضاء */
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
        
        /* إلغاء الفراغات العمودية التلقائية وحجب رأس الصفحة الافتراضي لمنع الحجب البصري */
        div[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px !important;
        }}
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. صبغ الحاوية الأفقية العلوية لبايثون بالأسود الملكي الفاخر قسرياً وثباتها في السقف */
        div[data-testid="stHorizontalBlock"] {{
            background-color: #000000 !important; /* صبغ الشريط بالأسود المصمت والكامل قسرياً */
            border-bottom: 2px solid #1E3A8A !important; /* خط أزرق ملكي رقيق يعزل عمارة الصورة الشامخة */
            width: 100vw !important;
            padding: 10px 60px !important;
            margin: 0px !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}
        
        /* 3. تدمير الصناديق والمربعات البيضاء لأزرار بايثون تماماً وتحويلها لنصوص حرة ونحيفة كالشاملة */
        .shamel-nav-native-btn button {{
            background: transparent !important; /* سحق الخلفية البيضاء كلياً */
            color: #FFFFFF !important; /* خط أبيض ناصع ومضيء مائة بالمائة فوق السواد */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم رصين واحترافي للحروف */
            font-size: 16px !important;
            border: none !important; /* نسف الحدود والخطوط المحيطة بالزر */
            border-radius: 0px !important;
            padding: 4px 10px !important;
            box-shadow: none !important;
            transition: color 0.2s ease-in-out !important;
            cursor: pointer !important;
            margin: 0px auto !important;
            display: block !important;
        }}
        
        /* تأثير الوميض الزمردي التراثي للمملكة عند تمرير مؤشر الفأرة فوق نصوص بايثون المحدثة */
        .shamel-nav-native-btn button:hover {{
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
# 📦 الجزء 4: إطلاق ورص خماسية أزرار بايثون الأصلية والمنقحة (سحق خطأ st.st.rerun)
# ==========================================
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.0, 1.2, 1.2, 1.1, 1.8, 4.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="btn_shamel_native_home"):
        st.rerun()  # 🟢 تم إصلاح اللحام هنا وحذف التكرار لتنطلق الحروف فوراً
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="btn_shamel_native_sections"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("حول المشروع", key="btn_shamel_native_about"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="btn_shamel_native_contact"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("🔍 البحث في المكنز", key="btn_shamel_native_search"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# حقن مسافة الأمان تحت الشريط الأسود لتبدأ الصورة بالأسفل بنقاء ونظام
st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
