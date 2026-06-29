import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse
import base64

# ==========================================
# 🇲🇦 الجزء 1: إعدادات الشاشة بعرض المتصفح الكامل 100% لعام 2026
# ==========================================
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# الاتصال بقاعدة البيانات التاريخية الكبرى لصلحاء المملكة المغربية الشريفة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()

# ==========================================
# 🏢 الجزء 2: البناء المعماري الموثق لجداول قاعدة البيانات لضمان استقرار السيرفر
# ==========================================
def init_ultimate_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geography (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT NOT NULL,
        province TEXT NOT NULL UNIQUE
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shrines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('أضرحة المسلمين', 'مزارات اليهود')) NOT NULL,
        province_id INTEGER,
        exact_location TEXT,
        history_details TEXT,
        daily_activities TEXT,
        annual_activities TEXT,
        researchers_books TEXT,
        creative_works TEXT,
        web_links TEXT,
        historical_era TEXT DEFAULT 'غير مححدد', 
        tags TEXT DEFAULT '',                    
        latitude REAL DEFAULT 31.7917,   
        longitude REAL DEFAULT -7.0926,
        FOREIGN KEY (province_id) REFERENCES geography(id),
        UNIQUE (name, province_id)
    )""")
    
    try:
        cursor.execute("ALTER TABLE shrines ADD COLUMN scientific_source TEXT DEFAULT 'رواية شفوية ميدانية مأثورة'")
    except sqlite3.OperationalError:
        pass
        
    cursor.execute("CREATE TABLE IF NOT EXISTS beliefs_and_functions (id INTEGER PRIMARY KEY AUTOINCREMENT, shrine_id INTEGER, function_type TEXT NOT NULL, details TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS thesaurus_terms (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT NOT NULL UNIQUE, category TEXT NOT NULL, definition TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS visitor_feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT, visitor_email TEXT, shrine_related TEXT, feedback_text TEXT NOT NULL, submission_date TEXT)")
    
    provinces_data = [
        ('جهة طنجة - تطوان - الحسيمة', 'إقليم شفشاون'), ('جهة طنجة - تطوان - الحسيمة', 'إقليم تطوان'),
        ('جهة طنجة - تطوان - الحسيمة', 'عمالة طنجة أصيلة'), ('جهة طنجة - تطوان - الحسيمة', 'إقليم العرائش'),
        ('جهة طنجة - تطوان - الحسيمة', 'إقليم الفحص أنجرة'), ('جهة مراكش أسفي', 'إقليم آسفي'),
        ('جهة مراكش أسفي', 'عمالة مراكش'), ('جهة الرباط سلا القنيطرة', 'عمالة سلا'),
        ('جهة بني ملال خنيفرة', 'إقليم خنيفرة'), ('جهة بني ملال خنيفرة', 'إقليم بني ملال'),
        ('جهة الدار البيضاء السطات', 'إقليم السطات'), ('جهة الدار البيضاء السطات', 'إقليم الجديدة'),
        ('جهة فاس مكناس', 'عمالة مكناس'), ('جهة فاس مكناس', 'عمالة فاس'), 
        ('جهة درعة تافيلالت', 'إقليم الرشيدية'), ('جهة سوس ماسة', 'إقليم تارودانت')
    ]
    for r, p in provinces_data:
        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", (r, p))
    conn.commit()

init_ultimate_db()

# ==========================================
# 🏢 الجزء 3: محرك استدعاء وتجهيز الصورة الملكية بنظام القراءة الفورية
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
# 🎨 الجزء 4: تلوين الحاوية الأفقية الأصلية بالتدرج اللوني وسحق الصناديق كلياً (CSS الشامل الشامخ)
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
        
        /* حجب رأس الصفحة الافتراضي لمنع الحجب البصري */
        div[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px !important;
        }}
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. 🟢 الحل الجراحي المعترف به سحابياً: تلوين حاوية الكتل الأصلية لبايثون بالتدرج اللوني وتثبيتها بالقمة قسرياً */
        div[data-testid="stHorizontalBlock"] {{
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important; /* تدرج الأزرق الملكي والأخضر الزمردي التراثي الأصيل */
            position: fixed !important; /* تثبيت مطلق صلب سقف المتصفح لضمان عدم الاختفاء */
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            width: 100vw !important;
            height: 55px !important; /* ارتفاع رصين ومطابق للشاملة */
            display: flex !important;
            align-items: center !important;
            padding: 0px 60px !important;
            direction: rtl !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
            border-bottom: 2px solid #D4AF37 !important; /* خط ذهبي مريني عريق يحدد الحافة */
        }}
        
        /* 3. 🟢 تدمير وسحق الصناديق والمربعات البيضاء لأزرار بايثون تماماً وتحويلها لنصوص حرة ونحيفة كالشاملة */
        .shamel-nav-native-btn button {{
            background: transparent !important; /* سحق الخلفية البيضاء والحواف كلياً */
            color: #FFFFFF !important; /* خط أبيض ناصع ومضيء مائة بالمائة للوضوح المطلق */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* تضخيم رصين واحترافي للحروف */
            font-size: 16px !important;
            border: none !important; /* نسف الحدود والخطوط المحيطة بالزر */
            border-radius: 0px !important;
            padding: 4px 15px !important;
            box-shadow: none !important;
            transition: color 0.2s ease-in-out !important;
            cursor: pointer !important;
            margin: 0px auto !important;
            display: block !important;
        }}
        
        /* تأثير الHover التفاعلي للشاملة: الوميض الفوري للأخضر الزمردي التراثي للمملكة عند تمرير الفأرة */
        .shamel-nav-native-btn button:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة للرابط */
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
# 📦 الجزء 5: إطلاق ورص خماسية أزرار بايثون الملقاة صلب شريط التدرج اللوني العالي (الظهور الفوري الحتمي)
# ==========================================
# استخدمنا هنا قنوات بايثون الأصلية المعترف بها من السيرفر مع عزل الأزرار بالـ CSS لمنع الصناديق البيضاء
menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.0, 1.2, 1.2, 1.1, 1.8, 4.5])

with menu_col_1:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("الرئيسية", key="btn_shamel_native_home_fixed"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_2:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("أقسام المكنز", key="btn_shamel_native_sections_fixed"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_3:
    st.markdown("<div class='shamel-nav-btn' style='display:none;'>", unsafe_allow_html=True) # إخفاء وهمي للكتلة الميتة
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("حول المشروع", key="btn_shamel_native_about_fixed"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_4:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("اتصل بنا", key="btn_shamel_native_contact_fixed"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with menu_col_5:
    st.markdown("<div class='shamel-nav-native-btn'>", unsafe_allow_html=True)
    if st.button("🔍 البحث في المكنز", key="btn_shamel_native_search_fixed"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

