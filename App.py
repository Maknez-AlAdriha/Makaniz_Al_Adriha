import streamlit as st
import os
import base64

# 🇲🇦 1. إعدادات الشاشة بعرض المتصفح الكامل 100% وبدون هوامش ميتة لعام 2026
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# 🎨 2. حقن كود الـ CSS الجراحي لإجبار الأزرار على الصعود إلى أعلى قمة الصورة زجاجياً
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* تصفير الهوامش الخارجية البيضاء لالتصاق البانر بأطراف الشاشة تماماً */
        div[data-testid="stAppViewBlockContainer"] {
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
        }
        
        /* إلغاء الفراغات العمودية التلقائية بين مكونات هيدر التطبيق */
        div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
        
        /* الحاوية المطلقة لإجبار صف الأزرار على الصعود إلى أعلى السقف قسرياً */
        .shamel-menu-container {
            position: absolute !important;
            top: 15px !important;
            right: 40px !important;
            left: 40px !important;
            z-index: 99999 !important;
        }
        
        /* التنسيق الجمالي للأزرار الخمسة العائمة بتأثير زجاجي فخم منسجم مع العمارة المغربية */
        .shamel-nav-btn button {
            background: rgba(0, 0, 0, 0.45) !important; /* خلفية داكنة خفيفة تبرز الحروف بوضوح فوق السحاب */
            color: #FFFFFF !important; /* خط أبيض ناصع وبارز */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 4px !important; /* حواف كلاسيكية مستقيمة ومطابقة للمكتبة الشاملة */
            padding: 6px 22px !important;
            backdrop-filter: blur(8px) !important; /* تأثير التغبيش الزجاجي الفخم */
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 0px auto !important;
            display: block !important;
        }
        
        /* تأثير الوميض الزمردي الشريف للمملكة عند تمرير مؤشر الفأرة فوق أزرار الملاحة */
        .shamel-nav-btn button:hover {
            background: #10B981 !important; 
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.45) !important;
            transform: translateY(-1px);
        }

        /* ضبط الخطوط والمحاذاة الصارمة لليمين لجميع عناصر وتكليفات الشاشات */
        html, body, .stMarkdown, p, span, label {
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# 🏢 3. محرك استدعاء وعرض البانر الملكي المندمج بنظام التشجير وقراءة الصورة
target_banner = None
for valid_name in ["banner.png", "banner..png", "Banner.png", "banner.PNG", "banner.jpg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

if target_banner:
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # 🟢 غلق اللحام: وضع الصورة والأزرار بداخل حاوية نسبية واحدة تمنع انفصالهما أو هبوط الأزرار للأسفل
    st.markdown(f"""
    <div style='position: relative; width: 100%; text-align: center; margin: 0; padding: 0;'>
        <img src='data:image/png;base64,{encoded_string}' style='width: 100%; height: auto; display: block; margin: 0; padding: 0;'>
    </div>
    """, unsafe_allow_html=True)
    
    # استدعاء الحاوية الفولاذية العلوية لرص الأزرار الخمسة أفقياً في القمة الشامخة
    st.markdown("<div class='shamel-menu-container'>", unsafe_allow_html=True)
    menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.7, 3.5])
    
    with menu_col_1:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("الرئيسية", key="btn_home_v5"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_2:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("أقسام المكنز", key="btn_sections_v5"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_3:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("حول المكنز", key="btn_about_v5"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_4:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("اتصل بنا", key="btn_contact_v5"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_5:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("🔍 شعار البحث في المكنز", key="btn_search_v5"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown('<div style="background-color:#1E3A8A; color:white; padding:40px; text-align:center; font-family:\'Reem Kufi\'; font-size:24px;">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</div>', unsafe_allow_html=True)
