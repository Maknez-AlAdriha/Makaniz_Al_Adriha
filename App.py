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
# 🎨 الجزء 3: قالب التنسيق السيادي وتحصين تمركز الشريط المتدرج (CSS الشامل)
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
        
        div[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. قسر الشريط العلوي على التدرج اللوني اللامع والثبات البصري في قمة الشاشة */
        .shamel-top-gradient-ribbon {{
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important; /* تدرج لوني انسيابي مأخوذ من عمق وعمارة الصورة */
            position: fixed !important; /* تثبيت مطلق صلب سقف المتصفح لضمان عدم التحرك */
            top: 0px !important;
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
        
        /* 3. الهندسة الجراحية: الروابط النصية الصافية والبيضاء الناصعة المنحوتة داخل التدرج */
        .shamel-nav-link {{
            color: #FFFFFF !important; /* خط أبيض ناصع ومضيء مائة بالمائة للوضوح المطلق */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم رصين واحترافي للحروف */
            font-size: 16px !important;
            text-decoration: none !important; /* نسف الخطوط التحتية الميتة */
            padding: 0 25px !important; /* مسافات أفقية مريحة ومتناسقة بين العناصر كالشاملة */
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        /* تأثير الوميض الزمردي الشريف عند تمرير مؤشر الفأرة فوق النص المتدرج */
        .shamel-nav-link:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة الحية للرابط */
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
# 📦 الجزء 4: نحت روابط الـ HTML النصية الصافية والبيضاء صلب شريط التدرج اللوني (الشاملة بالمليمتر)
# ==========================================
# قمنا هنا بحقن النصوص كروابط HTML صافية بداخل حاوية الشريط المتدرج مباشرة لضمان الانبثاق الفوري مائة بالمائة
st.markdown("""
    <div class='shamel-top-gradient-ribbon'>
        <!-- الكلمات تتراص بنحافة مطلقة من اليمين إلى اليسار صلب خلفية التدرج اللوني الشامخة لعام 2026 -->
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=search' target='_self' style='margin-right: auto; font-weight: 900; color: #D4AF37 !important;'>🔍 البحث في المكنز</a>
    </div>
""", unsafe_allow_html=True)

# مسافة أمان ترابية مريحة لدفع الصورة بالأسفل لتبدأ بنقاء تحت حافة الشريط المتدرج
st.markdown("<div style='margin-top: 65px;'></div>", unsafe_allow_html=True)
