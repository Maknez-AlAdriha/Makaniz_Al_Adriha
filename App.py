import streamlit as st
import os
import base64

# ==========================================
# 🇲🇦 الجزء 1: إعدادات الشاشة السيادية بعرض المتصفح الكامل 100% لعام 2026
# ==========================================
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# ==========================================
# 🏢 الجزء 2: محرك استدعاء وتجهيز الصورة الملكية بنظام القراءة الفورية الشاملة
# ==========================================
target_banner = None
for valid_name in ["banner.png", "banner..png", "Banner.png", "banner.PNG", "banner.jpg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

# تحويل الصورة إلى نص مشفر لإجبار المتصفح على دمجها كخلفية ممتدة بالكامل
encoded_string = ""
if target_banner:
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

# ==========================================
# 🎨 الجزء 3: قالب التنسيق السيادي وعزل شريط الملاحة العلوي النحيف (CSS الشامل)
# ==========================================
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* 1. تثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود شاشة الحاسوب 100% ومقاومة التمرير قسرياً */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover !important;
            background-position: center top !important; /* دفع الصورة لتبدأ من القمة بنقاء */
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            width: 100vw !important;
            min-height: 100vh !important;
            height: 100vh !important;
        }}
        
        /* 2. تصفير الهوامش والبطانات الداخلية للحاويات تماماً لجعل الرؤية فسيحة وبدون حواف بيضاء ميتة */
        div[data-testid="stAppViewBlockContainer"] {{
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
            margin: 0rem !important;
            background: transparent !important; /* جعل الحاوية شفافة لتظهر الخلفية الملكية من ورائها */
        }}
        .main .block-container {{
            max-width: 100% !important;
            padding: 0rem !important;
            margin: 0rem !important;
            background: transparent !important;
        }}
        
        /* إلغاء الفراغات العمودية الافتراضية بين المكونات العليا لـ Streamlit */
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 3. حاوية الشريط الأفقي النحيف والعلوي لمنع التراكب وحماية عنوان المكنز وعلم المملكة الشريفة */
        .shamel-top-ribbon {{
            position: fixed !important;
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            height: 65px !important; /* ارتفاع نحيف جداً وراقي يوفر المساحة الشاملة للتصفح بالأسفل */
            background: rgba(0, 0, 0, 0.45) !important; /* غسق داكن يحمي الحروف ويمنع التداخل البصري */
            border-bottom: 2px solid rgba(212, 175, 55, 0.4) !important; /* خط ذهبي ملكي رقيق يعكس عراقة التراث */
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 40px !important;
        }}
        
        /* 4. تنسيق الأزرار الخمسة داخل الشريط العلوي النحيف كروابط رشيقة ومستقلة تطفو بنقاء صوفي كالشاملة */
        .shamel-nav-btn button {{
            background: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 4px !important;
            padding: 5px 18px !important;
            backdrop-filter: blur(5px) !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 0px !important; /* إلغاء الهوامش لتستقر بانتظام وهدوء داخل الشريط النحيف */
        }}
        
        .shamel-nav-btn button:hover {{
            background: #10B981 !important; /* التحول الفوري للأخضر الزمردي التراثي الأصيل للمملكة المغربية الشريفة */
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
            transform: translateY(-1px);
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
# 📦 الجزء 4: رص وإطلاق خماسية الملاحة صلب الشريط العلوي النحيف والآمن بالقمة الشامخة
# ==========================================
st.markdown("<div class='shamel-top-ribbon'>", unsafe_allow_html=True)

# تقسيم الأعمدة بالتوالي لإجبار الأزرار على التراص أفقياً في جهة اليمين بنقاء تام دون تداخل
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.0, 1.2, 1.2, 1.1, 1.6, 4.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-btn' style='margin-top: 8px;'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="btn_home_modular_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-btn' style='margin-top: 8px;'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="btn_sections_modular_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-btn' style='margin-top: 8px;'>", unsafe_allow_html=True)
    if st.button("حول المكنز", key="btn_about_modular_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-btn' style='margin-top: 8px;'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="btn_contact_modular_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-btn' style='margin-top: 8px;'>", unsafe_allow_html=True)
    if st.button("🔍 شعار البحث في المكنز", key="btn_search_modular_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# حقن فراغ وهمي مريح بالأسفل لتهيئة استقبال وتدفق أي محتوى قادم بسلام تحت نطاق البانر المضيء
st.markdown("<div style='margin-top: 75px;'></div>", unsafe_allow_html=True)
