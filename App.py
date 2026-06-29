import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse
import base64

# 🇲🇦 إعدادات الشاشة بعرض المتصفح الكامل 100% الشامل للمملكة لعام 2026
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide", initial_sidebar_state="collapsed")
# تأسيس الاتصال بقاعدة البيانات التاريخية الكبرى لصلحاء المملكة المغربية الشريفة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()

# البناء المعماري الموثق للجداول الإدارية والجغرافية ومقاومة التصفير السحابي
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
# محرك استدعاء وفحص مسار الصورة وتجهيز دفق الـ Base64 الصافي لمنع المربع الأزرق نهائياً
target_banner = None
for valid_name in ["banner.png", "banner..png", "Banner.png", "banner.PNG", "banner.jpg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

encoded_string = ""
if target_banner:
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
# قالب التنسيق السيادي وتحصين تمركز الشريط وتفعيل التمرير العمودي لجميع النوافذ (CSS الشامل الشامخ)
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* تثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود الشاشة ومقاومة التمرير قسرياً مائة بالمائة */
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
        
        /* الحسم التكنولوجي المعتمد سحابياً: نسف وحظر الأشرطة التلقائية لبايثون لمنع كسر الهيكل الصافي */
        div[data-testid="stHeader"] {{ display: none !important; height: 0px !important; }}
        div[data-testid="stHorizontalBlock"] {{ display: none !important; }}
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* بناء شريط الملاحة الأفقي الملتصق بالقمة قسرياً بالتدرج اللوني اللامع لعمارة وصورة المكنز */
        .shamel-top-gradient-fixed-ribbon {{
            position: fixed !important;
            top: 0px !important; /* الالتصاق التام والصريح بسقف الشاشة فوق حافة الصورة العلوية */
            right: 0px !important;
            left: 0px !important;
            height: 55px !important;
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important;
            border-bottom: 2px solid #D4AF37 !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}
        
        /* روابط نصوص الشاملة الصافية والنحيفة مائة بالمائة وبدون أي مربعات خادعة */
        .shamel-nav-link {{
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            text-decoration: none !important;
            padding: 0 25px !important;
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        .shamel-nav-link:hover {{
            color: #10B981 !important;
            transform: translateY(-1px) !important;
        }}

        /* تنسيق وتفخيم محتوى النافذة المنبثقة التراثية لتطابق نموذج المكتبة الشاملة */
        .popup-header-title {{
            font-family: "Reem Kufi", serif !important;
            color: #1E3A8A;
            font-size: 24px;
            font-weight: bold;
            border-bottom: 2px solid #D4AF37;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .popup-content-text {{
            font-family: 'Tajawal', sans-serif !important;
            font-size: 17px;
            line-height: 1.8;
            color: #1F2937;
            text-align: justify;
            direction: rtl;
        }}

        /* 🟢 تفعيل شريط التمرير الـ Scroll اليدوي المرن لكلا النافذتين قسرياً وبأحرف دقيقة متناسقة مع أمان السيرفر السحابي */
        div[data-testid="stDialog"] {{
            max-height: 82vh !important; /* تحديد الارتفاع الأقصى بـ 82% من مساحة الشاشة لتوفير فسحة تصفح */
            overflow-y: auto !important; /* توليد وحقن شريط تمرير عمودي مرن فوراً عند تمدد وتراكم الخانات */
            padding-bottom: 25px !important;
        }}
        
        /* ضبط وتجميل مظهر مقبض شريط التمرير الـ Scroll الداخلي للنافذة ليتناسق مع المكنز */
        div[data-testid="stDialog"]::-webkit-scrollbar {{
            width: 8px !important;
        }}
        div[data-testid="stDialog"]::-webkit-scrollbar-thumb {{
            background-color: #1E3A8A !important;
            border-radius: 4px !important;
        }}

        /* تلوين وتغيير وسم التذييل التلقائي ليحمل توقيع الدكتور رشيد الجانبي بوقار علمي ملوكي */
        footer {{
            visibility: hidden !important;
        }}
        footer:after {{
            content: 'Created by JANEBI RACHID' !important;
            visibility: visible !important;
            display: block !important;
            position: relative !important;
            padding: 5px !important;
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: bold !important;
            font-size: 14px !important;
            text-align: right !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
        }}

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)
# قالب التنسيق السيادي وتحصين تمركز الشريط وتفعيل التمرير العمودي لجميع النوافذ (CSS الشامل الشامخ)
st.markdown(f"""
    <style>
        @import url('https://googleapis.com');
        
        /* 1. تثبيت الصورة كخلفية كاملة ممتدة تلتصق بحدود الشاشة ومقاومة التمرير قسرياً مائة بالمائة */
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
        
        /* الحسم التكنولوجي المعتمد سحابياً: نسف وحظر الأشرطة التلقائية لبايثون لمنع كسر الهيكل الصافي */
        div[data-testid="stHeader"] {{ display: none !important; height: 0px !important; }}
        div[data-testid="stHorizontalBlock"] {{ display: none !important; }}
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
        /* بناء شريط الملاحة الأفقي الملتصق بالقمة قسرياً بالتدرج اللوني اللامع لعمارة وصورة المكنز */
        .shamel-top-gradient-fixed-ribbon {{
            position: fixed !important;
            top: 0px !important; /* الالتصاق التام والصريح بسقف الشاشة فوق حافة الصورة العلوية */
            right: 0px !important;
            left: 0px !important;
            height: 55px !important;
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important;
            border-bottom: 2px solid #D4AF37 !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 60px !important;
            direction: rtl !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}
        
        /* روابط نصوص الشاملة الصافية والنحيفة مائة بالمائة وبدون أي مربعات خادعة */
        .shamel-nav-link {{
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            text-decoration: none !important;
            padding: 0 25px !important;
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        .shamel-nav-link:hover {{
            color: #10B981 !important;
            transform: translateY(-1px) !important;
        }}

        /* تنسيق وتفخيم محتوى النافذة المنبثقة التراثية لتطابق نموذج المكتبة الشاملة */
        .popup-header-title {{
            font-family: "Reem Kufi", serif !important;
            color: #1E3A8A;
            font-size: 24px;
            font-weight: bold;
            border-bottom: 2px solid #D4AF37;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .popup-content-text {{
            font-family: 'Tajawal', sans-serif !important;
            font-size: 17px;
            line-height: 1.8;
            color: #1F2937;
            text-align: justify;
            direction: rtl;
        }}

        /* 🟢 التصحيح الفولاذي الشامل: تفعيل شريط التمرير الـ Scroll اليدوي المرن بحرف D كبير قسرياً وبأمر نفاذ علوي */
        div[data-testid="stDialog"] {{
            max-height: 80vh !important; /* تحديد الارتفاع الأقصى بـ 80% من مساحة الشاشة لتوفير فسحة تصفح */
            overflow-y: auto !important; /* توليد وحقن شريط تمرير عمودي مرن فوراً عند تمدد وتراكم الخانات */
            padding-bottom: 25px !important;
        }}
        
        /* ضبط وتجميل مظهر مقبض شريط التمرير الـ Scroll الداخلي للنافذة ليتناسق مع المكنز */
        div[data-testid="stDialog"]::-webkit-scrollbar {{
            width: 8px !important;
            display: block !important;
        }}
        div[data-testid="stDialog"]::-webkit-scrollbar-thumb {{
            background-color: #1E3A8A !important;
            border-radius: 4px !important;
        }}
        div[data-testid="stDialog"]::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.05) !important;
        }}

        /* تلوين وتغيير وسم التذييل التلقائي ليحمل توقيع الدكتور رشيد الجانبي بوقار علمي ملوكي */
        footer {{
            visibility: hidden !important;
        }}
        footer:after {{
            content: 'Created by JANEBI RACHID' !important;
            visibility: visible !important;
            display: block !important;
            position: relative !important;
            padding: 5px !important;
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: bold !important;
            font-size: 14px !important;
            text-align: right !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
        }}

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)
