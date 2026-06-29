import streamlit as st
import os
import base64

# إعدادات الشاشة بعرض التراب الرقمي الشامل 100% وبدون هوامش ميتة
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")
# فحص وتأمين مسار قراءة الصورة المحلية بكافة الامتدادات الممكنة في مجلد السيرفر
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
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* تثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود شاشة الحاسوب 100% ومقاومة التمرير */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            width: 100vw !important;
            min-height: 100vh !important;
            height: 100vh !important;
        }}
        
        /* تصفير الهوامش والبطانات الداخلية للحاويات تماماً لجعل الرؤية فسيحة */
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
        
        /* إلغاء الفراغات العمودية الافتراضية بين المكونات العليا */
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* تنسيق الأزرار الخمسة كأشرطة علوية رشيقة ومستقلة تطفو بنقاء صوفي كالشاملة */
        .shamel-nav-btn button {{
            background: rgba(0, 0, 0, 0.65) !important;
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 4px !important;
            padding: 6px 22px !important;
            backdrop-filter: blur(5px) !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 15px auto 10px auto !important;
            display: block !important;
        }}
        
        .shamel-nav-btn button:hover {{
            background: #10B981 !important; 
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
        }}

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.8, 3.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="btn_home_modular_v1"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="btn_sections_modular_v1"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("حول المكنز", key="btn_about_modular_v1"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="btn_contact_modular_v1"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
    if st.button("🔍 شعار البحث في المكنز", key="btn_search_modular_v1"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
