import streamlit as st
import os
import base64

# 🇲🇦 1. إعدادات الشاشة بعرض التراب الرقمي الشامل 100% وبدون هوامش ميتة
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# 🏢 2. محرك استدعاء وتجهيز الصورة الملكية بنظام القراءة الفورية
target_banner = None
for valid_name in ["banner.png", "banner..png", "Banner.png", "banner.PNG", "banner.jpg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

# تحويل الصورة إلى نص مشفر لإجبار المتصفح على بسطها بالكامل
encoded_string = ""
if target_banner:
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

# 🎨 3. حقن كود الـ CSS الجراحي المصحح بالكامل بمضاعفة الأقواس لمنع الـ SyntaxError
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* 🟢 الحل الحاسم: نسف وتصغير كافة الهوامش والفراغات الجانبية في الحاويات الأم للمنصة */
        div[data-testid="stAppViewBlockContainer"] {{
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
            margin: 0rem !important;
        }}
        .main .block-container {{
            max-width: 100% !important;
            padding: 0rem !important;
            margin: 0rem !important;
        }}
        
        /* إلغاء الفراغات العمودية التلقائية بين المكونات العليا */
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* تنسيق الأزرار الخمسة كأشرطة علوية رشيقة ومستقلة */
        .shamel-nav-btn button {{
            background: rgba(0, 0, 0, 0.65) !important; /* خلفية داكنة ناعمة لبروز الحروف */
            color: #FFFFFF !important; /* خط أبيض ناصع وبارز */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 4px !important; /* حواف كلاسيكية مطابقة للشاملة */
            padding: 6px 20px !important;
            backdrop-filter: blur(5px) !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 15px auto 10px auto !important;
            display: block !important;
        }
        
        .shamel-nav-btn button:hover {{
            background: #10B981 !important; 
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
        }}

        /* قسر تمدد حاوية الصورة لتشغل العرض الكامل للشاشة 100% بدون أي فواصل جراحية */
        .full-width-banner {{
            width: 100vw !important;
            max-width: 100vw !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            padding: 0 !important;
            left: 0 !important;
            right: 0 !important;
        }}
        .full-width-banner img {{
            width: 100% !important;
            height: auto !important;
            display: block !important;
        }}

        /* ضبط الخطوط والمحاذاة الصارمة لليمين */
        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }}
    </style>
""", unsafe_allow_html=True)

# 🏢 4. رسم صف الأزرار الخمسة أولاً في قمة الواجهة
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.8, 3.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="btn_home_final_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="btn_sections_final_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("حول المكنز", key="btn_about_final_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="btn_contact_final_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("🔍 شعار البحث في المكنز", key="btn_search_final_v2"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 🏢 5. بسط وقذف الصورة الملكية الممتدة بعرض الشاشة الكامل 100% مباشرة أسفل الأزرار
if encoded_string:
    st.markdown(f"""
    <div class='full-width-banner'>
        <img src='data:image/png;base64,{encoded_string}'>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div style="background-color:#1E3A8A; color:white; padding:40px; text-align:center; font-family:\'Reem Kufi\'; font-size:24px;">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</div>', unsafe_allow_html=True)
