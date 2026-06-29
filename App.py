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
        historical_era TEXT DEFAULT 'غير محدد', 
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
# 🎨 الجزء 4: قالب التنسيق السيادي وتحصين تمركز الشريط الملتصق بالقمة (CSS الشامل)
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
        
        div[data-testid="stHeader"], div[data-testid="stHorizontalBlock"] {{
            background: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* 2. بناء شريط الملاحة الأفقي الملتصق بالقمة بالتدرج اللوني اللامع لعمارة وصورة المكنز */
        .shamel-top-gradient-ribbon {{
            position: fixed !important;
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            height: 60px !important; /* ارتفاع نحيف وراقي جداً يوفر مساحة القراءة بالأسفل */
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important; /* تدرج الأزرق الملكي والأخضر الزمردي */
            border-bottom: 2px solid #D4AF37 !important; /* خط ذهبي مريني عريق يحدد حافة الشريط النحيف */
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        }}
        
        /* 3. الهندسة الجراحية: الروابط النصية الصافية والنحيفة مائة بالمائة وبدون أي مربعات خادعة */
        .shamel-nav-link {{
            color: #FFFFFF !important; /* لون الخط الأبيض الناصع والمضيء للوضوح المطلق */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important; /* خط نحيف ونقي تماماً ورصين */
            font-size: 16px !important;
            text-decoration: none !important; /* حذف أي خطوط تحت النص */
            padding: 0 25px !important; /* مسافات أفقية مريحة ومتناسقة بين العناصر كالشاملة */
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        /* تأثير الHover التفاعلي للشاملة: الوميض الفوري للأخضر الزمردي التراثي للمملكة عند تمرير الفأرة */
        .shamel-nav-link:hover {{
            color: #10B981 !important; /* لون الإضاءة الخضراء الشريفة للرابط */
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
# 📦 الجزء 5: حقن خماسية روابط الـ HTML النصية الصافية والبيضاء صلب شريط التدرج اللوني العالي
# ==========================================
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

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة بالأسفل
st.markdown("<div style='margin-top: 65px;'></div>", unsafe_allow_html=True)
