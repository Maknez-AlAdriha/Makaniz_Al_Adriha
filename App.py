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
    
    # حقن قنوات الصور والمخطوطات والأوديو للأضرحة منعاً للانهيار صلب السيرفر
    try:
        cursor.execute("ALTER TABLE shrines ADD COLUMN image_url TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE shrines ADD COLUMN manuscript_url TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE shrines ADD COLUMN audio_url TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE shrines ADD COLUMN scientific_source TEXT DEFAULT 'رواية شفوية ميدانية مأثورة'")
    except sqlite3.OperationalError:
        pass
        
    cursor.execute("CREATE TABLE IF NOT EXISTS beliefs_and_functions (id INTEGER PRIMARY KEY AUTOINCREMENT, shrine_id INTEGER, function_type TEXT NOT NULL, details TEXT NOT NULL)")
    
    # تشييد جدول المصطلحات وتزويده بقناة الشواهد البصرية والمخطوطات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS thesaurus_terms (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        term TEXT NOT NULL UNIQUE, 
        category TEXT NOT NULL, 
        definition TEXT NOT NULL
    )""")
    
    try:
        cursor.execute("ALTER TABLE thesaurus_terms ADD COLUMN term_image TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
        
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
        
        div[data-testid="stHeader"] {{
            background: transparent !important;
            z-index: 9999 !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        /* شريط الملاحة الأفقي الملتصق بالقمة قسرياً بالتوجيه السيادي المطلق العازل للحظر سحابياً */
        .shamel-top-gradient-fixed-ribbon {{
            position: fixed !important;
            top: 0px !important;
            right: 0px !important;
            left: 0px !important;
            height: 55px !important;
            background: linear-gradient(90deg, #1E3A8A 0%, #064E3B 50%, #0F5132 100%) !important;
            border-bottom: 2px solid #D4AF37 !important;
            z-index: 9999999 !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 15px !important;
            direction: rtl !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}
        
        .shamel-nav-link {{
            color: #FFFFFF !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            text-decoration: none !important;
            padding: 0 12px !important;
            transition: color 0.2s ease-in-out, transform 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        .shamel-nav-link:hover {{
            color: #10B981 !important;
            transform: translateY(-1px) !important;
        }}

        div[data-testid="stTabs"] {{
            background: rgba(255, 255, 255, 0.98) !important;
            padding: 20px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12) !important;
        }}
        div[data-testid="stTabScrollList"] {{
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-around !important;
            gap: 20px !important;
            border-bottom: 3px solid #D4AF37 !important;
            padding-bottom: 12px !important;
            margin-bottom: 20px !important;
        }}
        button[data-testid="stTab"] {{
            font-family: 'Tajawal', sans-serif !important;
            font-weight: bold !important;
            font-size: 16px !important;
            color: #374151 !important;
            background: #F3F4F6 !important;
            padding: 12px 35px !important;
            border-radius: 8px 8px 0 0 !important;
            border: 1px solid #E5E7EB !important;
            width: 100% !important;
        }}
        button[data-testid="stTab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            background: #064E3B !important;
            font-weight: 900 !important;
        }}
        
        div[data-testid="stSelectbox"] div[role="button"], div[data-testid="stSelectbox"] select, .stSelectbox {{
            text-align: right !important;
            direction: rtl !important;
            font-family: 'Tajawal', sans-serif !important;
            font-weight: bold !important;
            font-size: 15px !important;
        }}
        div[data-baseweb="select"] {{
            direction: rtl !important;
            text-align: right !important;
        }}
        
        .shamel-dashboard-container {{
            background: rgba(255, 255, 255, 0.96) !important; 
            padding: 25px !important; 
            border-radius: 12px !important; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important; 
            margin: 20px auto !important; 
            max-width: 96% !important; 
            direction: rtl !important;
        }}

        div[data-testid="stTextInput"] input {{
            text-align: center !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            color: #1E3A8A !important;
        }}
        div[data-testid="stTextInput"] input::placeholder {{
            text-align: center !important;
            color: #1E3A8A !important;
            font-weight: bold !important;
            opacity: 0.7 !important;
        }}

        div[data-testid="stMetric"] {{
            background: #FFFFFF !important;
            border-top: 4px solid #D4AF37 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            text-align: center !important;
        }}

        form, .stForm, div[data-testid="stBlock"], div[data-testid="stDialog"] {{
            direction: rtl !important;
            text-align: right !important;
        }}
        label, div[data-testid="stWidgetLabel"] p {{
            text-align: right !important;
            direction: rtl !important;
            width: 100% !important;
            display: block !important;
            font-family: 'Tajawal', sans-serif !important;
        }}
        input, textarea {{
            text-align: right !important;
            direction: rtl !important;
        }}

        .card-shrine-popup {{
            background: #FFFFFF !important;
            border-right: 6px solid #D4AF37 !important;
            padding: 22px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
            margin-top: 12px !important;
            direction: rtl !important;
            text-align: right;
        }}
        .card-shrine-field {{
            font-size: 16px !important;
            line-height: 1.8 !important;
            margin-bottom: 12px !important;
            color: #1F2937 !important;
            border-bottom: 1px dashed #E5E7EB;
            padding-bottom: 6px;
            direction: rtl !important;
            text-align: right !important;
        }}
        
        div[data-testid="stDialog"] {{ max-height: 85vh !important; background: #FFFFFF !important; border-radius: 12px !important; }}
        div[data-testid="stDialog"] .stForm {{ max-height: 380px !important; overflow-y: auto !important; padding-left: 10px !important; }}
        div[data-testid="stDialog"]::-webkit-scrollbar {{ width: 8px !important; display: block !important; }}
        div[data-testid="stDialog"]::-webkit-scrollbar-thumb {{ background-color: #1E3A8A !important; border-radius: 4px !important; }}

        footer {{ visibility: hidden !important; }}
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
    </style>
""", unsafe_allow_html=True)
# الدالة المنبثقة التفاعلية للتعريف بالأطروحة ونبذة عن المشروع (محصنة ومطهرة بالكامل ومغلقة)
@st.dialog("نبذة عن المشروع الأكاديمي", width="large")
def show_about_project_popup():
    st.markdown("""
        <div style='direction: rtl; text-align: right; padding: 10px; background: #FFFFFF; border-radius: 8px;'>
            <h3 style='color: #1E3A8A; font-family: "Reem Kufi", serif; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; text-align: center; margin-bottom: 15px;'>🏛️ نبذة عن المشروع الأكاديمي والمكنز التراثي</h3>
            <p style='font-family: "Tajawal", sans-serif; font-size: 16px; line-height: 1.8; color: #1F2937;'>
                يهدف هذا المشروع التراثي والمكنز الوطني السيادي الشامل إلى جمع وتوثيق ورقمنة كل ما يحتاجه طالب العلم والباحث الأنثروبولوجي من معطيات جغرافية، تاريخية، بيبليوغرافية، وأنثروبولوجية متعلقة بالمنشآت الروحية، الأضرحة، والمزارات الشريفة في ربوع المملكة المغربية الشريفة.
            </p>
            <p style='font-family: "Tajawal", sans-serif; font-size: 16px; line-height: 1.8; color: #1F2937;'>
                إن هذه المنصة الرقمية المتقدمة لعام <b>2026</b> هي الثمرة التقنية الحية والتحويل التكنولوجي المتكامل للأطروحة العلمية والميدانية المتميزة التي نوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.
            </p>
            <hr style='border: 0; border-top: 1px solid #E5E7EB; margin: 20px 0;'>
            <p style='text-align: center; font-family: "Tajawal", sans-serif; font-weight: bold; font-size: 16px; color: #1E3A8A; margin-bottom: 5px;'>👨‍🎓 الباحث الدكتور: رشيد الجانبي</p>
            <p style='text-align: center; font-family: "Tajawal", sans-serif; font-weight: bold; font-size: 15px; color: #D4AF37; margin-bottom: 10px;'>👩‍🏫 الأستاذة المشرفة: الدكتورة فاطنة الغزي</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("❌ إغلاق النافذة والعودة للمكنز", use_container_width=True, key="shamel_about_popup_close_secure_v26"):
        st.query_params.clear()
        st.rerun()

@st.dialog("دفتر التواصل الرقمي مع إدارة المكنز", width="large")
def show_contact_us_popup():
    st.markdown("<div class='popup-header-title'>📬 تواصل علمي وتحقيق ميداني</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #F8FAFC; border-right: 5px solid #1E3A8A; padding: 15px; border-radius: 4px; margin-bottom: 20px; direction: rtl; text-align: right;'>
        <p style='margin:0; font-weight:700; color:#1E3A8A; font-size:16px;'>📞 للاتصال المباشر مع الدكتور رشيد الجانبي:</p>
        <p style='margin:5px 0 0 0; font-weight:900; color:#10B981; font-size:18px; direction:ltr; text-align:right;'>+212 666-271681</p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("shamel_contact_secure_form", clear_on_submit=True):
        c_sender_name = st.text_input("اسم الباحث / المرسل الكريم:", placeholder="اكتب اسمك الكامل هنا...")
        c_sender_email = st.text_input("البريد الإلكتروني للمرسل (لاستقبال الرد الآلي السريع):", placeholder="example@domain.com")
        c_sender_subject = st.text_input("موضوع المراسلة صلب الموضوع:", placeholder="مثال: تصويب علمي، إغناء بيبليوغرافي...")
        c_sender_message = st.text_area("نص الرسالة أو الملاحظة الترابية بالكامل:")
        st.text_input("المرسل إليه (إدارة المكنز الوطني الشريف):", value="rachid.janebi@gmail.fr", disabled=True)
        submit_clicked = st.form_submit_button("🚀 إرسال الرسالة بنجاح وإرسال التذكير", use_container_width=True)
        if submit_clicked:
            if c_sender_email and c_sender_message:
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute("INSERT INTO visitor_feedback (visitor_name, visitor_email, shrine_related, feedback_text, submission_date) VALUES (?, ?, ?, ?, ?)", (c_sender_name, c_sender_email, c_sender_subject, c_sender_message, now_str))
                conn.commit()
                st.success("🔔 تم إرسال رسالة تذكير بنجاح إلى الموقع!")
                st.rerun()
            else: st.error("⚠️ منظومة الأمان تمنع الإرسال، يرجى كتابة بريدك الإلكتروني ونص الرسالة أولاً.")

# ==========================================
# 🏛️ البلوك 8 من 14 المطور والمطهر: تثبيت النوافذ المنبثقة قسرياً وسحق الاختفاء التلقائي أثناء التمرير
# ==========================================

# ==========================================
# 📦 البلوك 9 و 10 الملحم والمطهر: تفكيك كتل الـ Tuple للوسائط وسحق الانهيار بالسطر 401
# ==========================================

@st.dialog("البطاقة العلمية للمصطلح القاموسي المحقق", width="large", dismissible=False)
def popup_individual_term_card(term_name):
    # سحب تفاصيل المفهوم اللغوي من قاعدة البيانات
    row = cursor.execute("SELECT term, category, definition, term_image FROM thesaurus_terms WHERE term = ?", (term_name,)).fetchone()
    if row:
        # 🟢 تفكيك جراحي للمصفوفة لضمان استخراج نصوص حرة ونظيفة مائة بالمائة
        t_term = str(row[0])
        t_category = str(row[1])
        t_definition = str(row[2])
        t_img = str(row[3]).strip() if row[3] else ""
        
        if t_img and t_img != "nan" and t_img != "":
            st.image(t_img, use_container_width=True, caption=f"📸 الرسم التوضيحي/المخطوط للمصطلح: {t_term}")
            
        st.markdown(f"<h3 style='color:#064E3B; text-align:center; font-family:\"Reem Kufi\"; border-bottom:3px solid #D4AF37; padding-bottom:12px;'><b>📖 مصطلح: {t_term}</b></h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup' style='border-right-color:#064E3B; direction: rtl; text-align: right;'>
            <div class='card-shrine-field'><b>🗂️ الفئة الأنثروبولوجية صلب الأطروحة:</b> {t_category}</div>
            <div class='card-shrine-field' style='font-size:18px !important; line-height:2; border-bottom:none;'><b>📚 التعريف العلمي المعتمد الأكاديمي:</b><br>{t_definition}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 1px dashed #D4AF37;'>", unsafe_allow_html=True)
        term_citation = f"الجانبي، رشيد ({datetime.datetime.now().year}). m مادة قاموسية: {t_term} ({t_category})، معجم المكنز اللغوي والمفاهيم الأنثروبولوجية، المملكة المغربية الشريفة."
        st.text_area("📥 التخريج والتوثيق الأكاديمي المعتمد للاقتباس (معايير APA الدولي):", value=term_citation, height=70, key="cit_term_fixed_v18_final")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("❌ إغلاق البطاقة والعودة للمكنز", use_container_width=True, key="secure_close_term_popup_btn"):
            st.rerun()

@st.dialog("البطاقة العلمية الكاملة للمَعلم التراثي المحقق", width="large", dismissible=False)
def popup_individual_shrine_card(shrine_name):
    # سحب تفاصيل المزار بالكامل من قاعدة بيانات الأطروحة التاريخية
    row = cursor.execute("""
        SELECT name, history_details, exact_location, historical_era, scientific_source, daily_activities, annual_activities, researchers_books, image_url, manuscript_url, audio_url
        FROM shrines WHERE name = ?""", (shrine_name,)).fetchone()
    if row:
        # 🟢 تفكيك جراحي شامل وصارم للمصفوفة لمنع تمرير الـ Tuple إلى دالة st.image وسحق الخطأ بالسطر 401
        s_name = str(row[0])
        s_history = str(row[1])
        s_location = str(row[2])
        s_era = str(row[3])
        s_source = str(row[4])
        s_daily = str(row[5])
        s_annual = str(row[6])
        s_books = str(row[7])
        s_img = str(row[8]).strip() if row[8] else ""
        s_manuscript = str(row[9]).strip() if row[9] else ""
        s_audio = str(row[10]).strip() if row[10] else ""
        
        if s_img and s_img != "nan" and s_img != "":
            st.image(s_img, use_container_width=True, caption=f"📸 الشاهد البصري الميداني للمزار: {s_name}")
            
        if s_manuscript and s_manuscript != "nan" and s_manuscript != "":
            st.image(s_manuscript, use_container_width=True, caption=f"📜 الوثيقة التاريخية / الظهير الملحق الشريف لـ {s_name}")
            
        if s_audio and s_audio != "nan" and s_audio != "":
            st.audio(s_audio, format="audio/mp3")
            
        st.markdown(f"<h3 style='color:#1E3A8A; text-align:center; font-family:\"Reem Kufi\"; border-bottom:3px solid #D4AF37; padding-bottom:12px;'><b>  🕌 {s_name}</b></h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup' style='direction: rtl; text-align: right;'>
            <div class='card-shrine-field'><b>⏳ العصر التاريخي المعاصر له:</b> {s_era}</div>
            <div class='card-shrine-field'><b>🗺️ الموقع الجغرافي الميداني الدقيق:</b> {s_location}</div>
            <div class='card-shrine-field'><b>📜 النبذة والتحقيق الأنثروبولوجي الموثق:</b> {s_history}</div>
            <div class='card-shrine-field'><b>📅 الأنشطة اليومية والموسمية وطبيعة الإشراف:</b> {s_daily} | {s_annual}</div>
            <div class='card-shrine-field'><b>📚 المصادر والكتب البيبليوغرافية للباحثين والمؤرخين:</b> {s_books}</div>
            <div class='card-shrine-field' style='color:#064E3B; font-weight:bold; border-bottom:none;'><b>🔬 المصدر العلمي المعتمد للأطروحة:</b> {s_source}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 1px dashed #D4AF37;'>", unsafe_allow_html=True)
        citation_text = f"الجانبي، رشيد ({datetime.datetime.now().year}). تحقيق مَعلم: {s_name} ({s_location})، المكنز الوطني للأضرحة والمزارات بالمغرب، الثمرة التكنولوجية للأطروحة العلمية الشاملة."
        st.text_area("📥 التخريج والتوثيق الأكاديمي المعتمد للاقتباس المباشر (معايير APA الدولي):", value=citation_text, height=70, key="cit_sh_fixed_v18_final")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("❌ إغلاق البطاقة والعودة للمكنز", use_container_width=True, key="secure_close_shrine_popup_btn"):
            st.rerun()



# لوحة تصفح الأقسام الثلاثة كصفحة كاملة ومطهرة من مشكلة التداخل ومزودة بميزة الـ Popup الفردي لكل زر وتوسط العناوين
def show_maknez_sections_dashboard():
    st.markdown("""
        <div class='shamel-dashboard-container'>
            <h2 style='text-align:center; color:#1E3A8A; font-family:"Reem Kufi", serif; margin-bottom: 5px;'>🏛️ لوحة تصفح الأقسام والتحقيقات الميدانية للأطروحة العلمية</h2>
            <p style='text-align:center; color:#4B5563; font-family:"Tajawal", sans-serif; font-size:16px; margin-bottom: 10px;'>اضغط على اسم أي ضريح أو معلم تراثي أو مصطلح محقق لتنبثق لك بطاقته العلمية الأنيقة فوراً</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🕌 رواق صلحاء المسلمين", "📜 رواق مزارات اليهود", "📖 المكنز اللغوي والمصطلحات"])
    
    with tab1:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 6px; border-right: 5px solid #1E3A8A; margin-top:15px; margin-bottom:15px; direction: rtl; text-align: center;'>
                <h4 style='color:#1E3A8A; font-family:"Reem Kufi", serif; font-weight:bold; margin:0;'>🕌 الأولياء والصلحاء المسلمون بالمملكة الشريفة:</h4>
            </div>
        """, unsafe_allow_html=True)
        
        shrines_m = cursor.execute("SELECT name, id FROM shrines WHERE type = 'أضرحة المسلمين' ORDER BY id DESC").fetchall()
        if not shrines_m: st.info("لا توجد معطيات للأضرحة الإسلامية حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(3)
            # تم قفل وسحق خطأ الأقواس بالمليمتر صلب محرك التصفح الدائري بايثون لعام 2026
            for idx, (name, s_id) in enumerate(shrines_m):
                with cols[idx % 3]:
                    if st.button(f"🕌 {name}", key=f"m_sh_btn_{s_id}", use_container_width=True): popup_individual_shrine_card(name)

    with tab2:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 6px; border-right: 5px solid #064E3B; margin-top:15px; margin-bottom:15px; direction: rtl; text-align: center;'>
                <h4 style='color:#064E3B; font-family:"Reem Kufi", serif; font-weight:bold; margin:0;'>📜 مزارات ومعالم اليهود المغاربة التراثية التاريخية:</h4>
            </div>
        """, unsafe_allow_html=True)
        
        shrines_j = cursor.execute("SELECT name, id FROM shrines WHERE type = 'مزارات اليهود' ORDER BY id DESC").fetchall()
        if not shrines_j: st.info("لا توجد معطيات لمزارات اليهود حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(3)
            for idx, (name, s_id) in enumerate(shrines_j):
                with cols[idx % 3]:
                    if st.button(f"📜 {name}", key=f"j_sh_btn_{s_id}", use_container_width=True): popup_individual_shrine_card(name)

    with tab3:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 6px; border-right: 5px solid #0F5132; margin-top:15px; margin-bottom:15px; direction: rtl; text-align: center;'>
                <h4 style='color:#0F5132; font-family:"Reem Kufi", serif; font-weight:bold; margin:0;'>📖 قاموس المكنز اللغوي والمفاهيم الأنثروبولوجية المحققة:</h4>
            </div>
        """, unsafe_allow_html=True)
        
        terms = cursor.execute("SELECT term, id FROM thesaurus_terms ORDER BY term ASC").fetchall()
        if not terms: st.info("المعجم اللغوي القاموسي فارغ حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(4)
            for idx, (term, t_id) in enumerate(terms):
                with cols[idx % 4]:
                    if st.button(f"📖 {term}", key=f"term_btn_{t_id}", use_container_width=True): popup_individual_term_card(term)
# صفحة البحث المتقدم والمتقاطع المستوحاة بالكامل من خصائص المكتبة الشاملة العريقة
def show_shamel_search_engine_page():
    st.markdown("""
        <div class='shamel-dashboard-container' style='border-right: 6px solid #064E3B;'>
            <h2 style='text-align:center; color:#064E3B; font-family:"Reem Kufi", serif; margin-bottom: 5px;'>🔍 محرك البحث الشامل والمتقاطع في المكنز الوطني</h2>
            <p style='text-align:center; color:#4B5563; font-family:"Tajawal", sans-serif; font-size:16px;'>بوابة الغربال الفوري والفرز الدقيق للمزارات والأضرحة والمصطلحات صلب الموضوع</p>
        </div>
    """, unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1: search_query = st.text_input("🔍 اكتب كلمة البحث (اسم الولي، مَعلم، جزء من نص التاريخ...):", placeholder="اكتب أول الحروف هنا للبحث الحي...")
    with f_col2: type_filter = st.selectbox("🗂️ فرز حسب الرواق المعلمي:", ["الكل كحزمة واحدة", "أضرحة المسلمين", "مزارات اليهود"])
    with f_col3:
        db_provinces = cursor.execute("SELECT province FROM geography ORDER BY province ASC").fetchall()
        provinces_list = [p[0] for p in db_provinces]
        all_provinces = ["كل الأقاليم الترابية"] + provinces_list
        province_filter = st.selectbox("📍 فرز حسب الإقليم التاريخي للمملكة:", all_provinces)
        
    st.markdown("<hr style='border-top: 2px solid #D4AF37; margin: 15px 0;'>", unsafe_allow_html=True)
    
    sql_base = "SELECT shrines.name, geography.province, shrines.historical_era, shrines.type, shrines.id FROM shrines JOIN geography ON shrines.province_id = geography.id WHERE 1=1"
    params = []
    if search_query:
        sql_base += " AND (shrines.name LIKE ? OR shrines.history_details LIKE ? OR shrines.tags LIKE ?)"
        q_like = f"%{search_query}%"
        params.extend([q_like, q_like, q_like])
    if type_filter != "الكل كحزمة واحدة":
        sql_base += " AND shrines.type = ?"
        params.append(type_filter)
    if province_filter != "كل الأقاليم الترابية":
        sql_base += " AND geography.province = ?"
        params.append(province_filter)
        
    sql_base += " ORDER BY shrines.id DESC"
    results = cursor.execute(sql_base, params).fetchall()
    st.markdown(f"<h5>📊 نتائج الغربال الشامل: تم العثور على عدد ({len(results)}) معلم تراثي مطابق للفلاتر</h5>", unsafe_allow_html=True)
    
    if not results: st.info("لا توجد نتائج تطابق خيارات البحث الحالية.")
    else:
        r_cols = st.columns(3)
        for idx, (s_name, p_name, era_name, s_type, s_id) in enumerate(results):
            with r_cols[idx % 3]:
                border_color = "#1E3A8A" if s_type == "أضرحة المسلمين" else "#064E3B"
                card_html = f"""
                    <div style='background:#FFFFFF; padding:15px; border-radius:8px; border-right: 5px solid {border_color}; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom:10px; direction: rtl; text-align: right;'>
                        <span style='font-size:12px; color:#6B7280; font-weight:bold;'>📌 {s_type}</span><br>
                        <b style='color:#1F2937; font-size:16px;'>  🔑 {s_name}</b><br>
                        <span style='font-size:13px; color:#4B5563;'>📍 {p_name} | ⏳ {era_name}</span>
                    </div>"""
                st.markdown(card_html, unsafe_allow_html=True)
              
              
              
              
              
                if st.button("🔎 افتح البطاقة العلمية الكاملة", key=f"src_sh_btn_{s_id}_{idx}", use_container_width=True): popup_individual_shrine_card(s_name)
# ==========================================
# 📦 البلوك 13 من 18 الأصلي والمطهر: محرك أطلس المكنز والقفز الجغرافي وحاوية التموضع الترابي
# ==========================================
# ==========================================
# 📦 Le Bloc 13 de 18 Corrigé : Atlas du thésaurus et carte interactive avec variable rectifiée
# ==========================================
def show_maknez_atlas_interactive_map_page():
    st.markdown("""
        <div class='shamel-dashboard-container' style='border-right: 6px solid #1E3A8A;'>
            <h2 style='text-align:center; color:#1E3A8A; font-family:"Reem Kufi", serif; margin-bottom: 5px;'>🗺️ أطلس المكنز الوطني للأضرحة والمزارات الشريفة</h2>
            <p style='text-align:center; color:#4B5563; font-family:"Tajawal", sans-serif; font-size:16px; font-weight:bold;'>الملاحة الجغرافية الفورية والتركيز التلقائي فوق إحداثيات المعالم والصلحاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    sh_map_data = cursor.execute("""
        SELECT shrines.name, shrines.latitude, shrines.longitude, shrines.type, geography.province, geography.region, shrines.exact_location 
        FROM shrines 
        JOIN geography ON shrines.province_id = geography.id""").fetchall()
    
    if not sh_map_data:
        st.info("💡 الأطلس الجغرافي بانتظار ضخ البيانات؛ يرجى رفع ملفات الأولية من بوابة الإدارة.")
    else:
        st.markdown("<div style='direction: rtl; text-align: right;'><b style='font-family:\"Tajawal\"; font-size:16px; color:#1E3A8A;'>🔍 ابحث عن أي ضريح للقفز والتركيز عليه في الخريطة واستخراج بطاقته الترابية حياً:</b></div>", unsafe_allow_html=True)
        search_map_input = st.text_input("", placeholder="اكتب اسم الضريح أو الولي هنا للقفز الجغرافي الفوري صلب الموضوع...", key="shamel_live_map_search_input_v2026")
        
        search_query_fixed = search_map_input.strip().lower()
        
        filtered_data = []
        if search_query_fixed:
            for row in sh_map_data:
                if search_query_fixed in str(row).lower():
                    filtered_data.append(row)
        else:
            filtered_data = sh_map_data
        
        map_list = []
        for name, lat, lon, s_type, prov, reg, loc_det in filtered_data:
            p_color = "#1E3A8A" if s_type == "أضرحة المسلمين" else "#064E3B"
            map_list.append({
                "name": name, 
                "latitude": float(lat) if lat else 31.7917, 
                "longitude": float(lon) if lon else -7.0926, 
                "color": p_color
            })
            
        df_map = pd.DataFrame(map_list)
        
        if search_query_fixed and not df_map.empty:
            center_lat = float(df_map.iloc[0]["latitude"])
            center_lon = float(df_map.iloc[0]["longitude"])
            map_zoom = 13  
        else:
            center_lat, center_lon, map_zoom = 31.7917, -7.0926, 6  
            
        st.map(df_map, latitude=center_lat, longitude=center_lon, zoom=map_zoom, size=60, color="color", use_container_width=True)
        
        # 🟢 Correction de la variable : Utilisation stricte de filtered_data à la place de results
        if search_query_fixed and len(filtered_data) > 0:
            target_sh = filtered_data[0][0]  
            target_lat = filtered_data[0][1]
            target_lon = filtered_data[0][2]
            target_prov = filtered_data[0][4]
            target_reg = filtered_data[0][5]
            target_loc = filtered_data[0][6] if filtered_data[0][6] else "غير محدد"
            
            st.markdown(f"""
                <div style='background: #FFFFFF; border-right: 6px solid #1E3A8A; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-top: 15px; direction: rtl; text-align: right;'>
                    <h4 style='color:#1E3A8A; font-family:"Reem Kufi", serif; margin-bottom:15px; font-weight:900;'>📍 بطاقة الإحداثيات والمعطيات الترابية الحية للمزار المستهدف:</h4>
                    <div class='card-shrine-field'><b>🏛️ اسم الضريح / المزار المحقق:</b> {target_sh}</div>
                    <div class='card-shrine-field'><b>🌐 الإحداثيات الجغرافية بالسيرفر:</b> خط العرض: {target_lat} | خط الطول: {target_lon}</div>
                    <div class='card-shrine-field'><b>🇲🇦 الجهة الإدارية الشريفة:</b> {target_reg}</div>
                    <div class='card-shrine-field'><b>📌 العمالة / الإقليم التاريخي:</b> {target_prov}</div>
                    <div class='card-shrine-field'><b>🏙️ جماعة ترابية / الدوار / تفاصيل التموضع الميداني:</b> {target_loc}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"📚 افتح النبذة التاريخية والتحقيق العلمي الكامل لـ {target_sh}", use_container_width=True, key="atlas_sh_popup_btn_fixed_v2026"):
                popup_individual_shrine_card(target_sh)
        else:
            st.markdown("<p style='color:#6B7280; font-size:15px; font-weight:bold; margin-top:15px; direction: rtl; text-align: right;'>💡 اكتب اسم المعلم صلب خانة البحث بالأعلى لتفعيل القفز الجغرافي الفوري واستخراج بطاقة (الجهة، الجماعة، والدوار) حياً صلب الأطلس.</p>", unsafe_allow_html=True)













def show_maknez_statistics_page():


    st.markdown("""
        <div class='shamel-dashboard-container' style='border-right: 6px solid #D4AF37; margin-top: 10px !important;'>
            <h2 style='text-align:center; color:#1E3A8A; font-family:"Reem Kufi", serif; margin-bottom: 5px;'>📊 لوحة المؤشرات الرقمية والعدادات الإحصائية التراكمية</h2>
            <p style='text-align:center; color:#4B5563; font-family:"Tajawal", sans-serif; font-size:16px;'>التقرير البياني الحي الموثق الثمرة العلمية للتحقيق الميداني للأطروحة لعام 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    total_shrines = cursor.execute("SELECT COUNT(*) FROM shrines").fetchone()
    muslim_shrines = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='أضرحة المسلمين'").fetchone()
    jew_shrines = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='مزارات اليهود'").fetchone()
    total_terms = cursor.execute("SELECT COUNT(*) FROM thesaurus_terms").fetchone()
    
    m_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with m_col1: st.metric(label="🏛️ إجمالي المنشآت الروحية المحققة", value=total_shrines)
    with f_col2: st.metric(label="🕌 رواق أولياء وصلحاء الإسلام", value=muslim_shrines)
    with f_col3: st.metric(label="📜 رواق المزارات اليهودية التاريخية", value=jew_shrines)
    with f_col4: st.metric(label="📖 المصطلحات والمفاهيم المعجمية", value=total_terms)
    
    st.markdown("<hr style='border-top: 2px solid #D4AF37; margin: 25px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.95); padding: 15px 25px; border-radius: 8px; border-right: 5px solid #1E3A8A; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; direction: rtl; text-align: center;'>
            <h4 style='color: #1E3A8A; font-family: "Reem Kufi", serif; font-weight: bold; margin: 0;'>📈 التوزيع البياني التراكمي للمعالم حسب الأقاليم التاريخية للملكة المغربية الشريفة:</h4>
        </div>
    """, unsafe_allow_html=True)
    
    geo_df = pd.read_sql_query("""
        SELECT geography.province as 'الإقليم الترابي', COUNT(shrines.id) as 'عدد المعالم الموثقة' 
        FROM shrines JOIN geography ON shrines.province_id = geography.id 
        GROUP BY geography.province""", conn)
        
    if geo_df.empty: st.info("الرسوم البيانية بانتظار ضخ ملفات الـ CSV لتفعيل المؤشرات.")
    else: st.bar_chart(geo_df.set_index('الإقليم الترابي'), use_container_width=True)
@st.dialog("بوابة إدارة وتغذية وتعديل المكنز الوطني الكوني", width="large")
def show_admin_dashboard_popup():
    st.markdown("<div class='popup-header-title'>🔐 نظام التغذية الرقمية والاستيراد وتعديل كافة الأقسام حياً لعام 2026</div>", unsafe_allow_html=True)
    developer_key = st.text_input("أدخل رمز العبور لتنشيط صلاحيات الإشراف:", type="password", key="pop_dev_k")
    if developer_key == "MAROC_2026":
        st.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز بنجاح!")
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📥 ضخ ملفات CSV جديدة", "🕌 تعديل الأضرحة (مسلمون ويهود)", "📖 تعديل ومصورة القاموس"])
        
        with admin_tab1:
            st.markdown("##### 📥 استيراد ملفات CSV تراكمية:")
            if "uploader_counter" not in st.session_state: st.session_state.uploader_counter = 0
            uploaded_csv_list = st.file_uploader("اختر ملفات الـ CSV المحددة:", type=["csv"], accept_multiple_files=True, key=f"pop_csv_u_{st.session_state.uploader_counter}")
            
            if uploaded_csv_list and st.button("🚀 البدء في معالجة وضخ الملفات دفعة واحدة", use_container_width=True):
                for uploaded_csv in uploaded_csv_list:
                    df = pd.read_csv(uploaded_csv, encoding='utf-8')
                    for index, row_data in df.iterrows():
                        s_name = str(row_data.get('shrine_name', '')).strip()
                        if not s_name or s_name == "nan" or "shrine_name" in s_name: continue
                        tags_val = str(row_data.get('tags', '')).strip()
                        s_type = str(row_data.get('shrine_type', 'أضرحة المسلمين')).strip()
                        hist_val = str(row_data.get('history_details', 'غير محدد')).strip()
                        prov_name = str(row_data.get('province', 'إقليم شفشاون')).strip()
                        lat_val = float(row_data.get('latitude', 31.7917))
                        lon_val = float(row_data.get('longitude', -7.0926))
                        img_val = str(row_data.get('image_url', '')).strip() if row_data.get('image_url') else ""
                        
                        if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                            cursor.execute("INSERT OR IGNORE INTO thesaurus_terms (term, category, definition, term_image) VALUES (?, ?, ?, ?)", (s_name, s_type, hist_val, img_val))
                        else:
                            cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                            prov_id_row = cursor.execute("SELECT id FROM geography WHERE province=?", (prov_name,)).fetchone()
                            if prov_id_row:
                                prov_id = int(prov_id_row) 
                                cursor.execute("INSERT OR IGNORE INTO shrines (name, type, province_id, history_details, latitude, longitude, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)", (s_name, s_type, prov_id, hist_val, lat_val, lon_val, img_val))
                conn.commit()
                st.session_state.uploader_counter += 1
                st.success("📊 تم الضخ التراكمي وتتويج جداول المكنز بنجاح.")
                st.rerun()
                
        with admin_tab2:
            st.markdown("##### 🕌 محرك تعديل وإغناء كتل الأضرحة والمزارات بـ (الصور، المخطوطات، والملفات الصوتية) حياً:")
            all_live_shrines = [item for item in cursor.execute("SELECT name FROM shrines ORDER BY name ASC").fetchall()]
            shrine_to_edit = st.selectbox("🎯 اختر اسم الضريح أو المزار المراد تعديله أو تزويده بشواهد ميدانية:", ["--- اختر معلماً لتعديله ---"] + all_live_shrines, key="sel_sh_edit_con_v14_13")
            
            if shrine_to_edit != "--- اختر معلماً لتعديله ---":
                current_data = cursor.execute("""
                    SELECT exact_location, history_details, daily_activities, annual_activities, researchers_books, latitude, longitude, type, image_url, manuscript_url, audio_url 
                    FROM shrines WHERE name = ?""", (shrine_to_edit,)).fetchone()
                
                if current_data:
                    with st.form("shamel_shrine_edit_form_v14_13"):
                        st.info(f"⚙️ نموذج تعديل بطاقة المعلم الشاملة: {shrine_to_edit}")
                        new_type = st.selectbox("🗂️ تصنيف المعلم التراثي:", ["أضرحة المسلمين", "مزارات اليهود"], index=0 if current_data == "أضرحة المسلمين" else 1)
                        
                        new_img = st.text_input("📸 مسار أو رابط الصورة الميدانية للمزار (مثال: `larache1.jpg`):", value=str(current_data) if current_data else "")
                        new_manuscript = st.text_input("📜 مسار أو رابط المخطوط/الظهير الشريف المصاحب (مثال: `dahir1.png`):", value=str(current_data) if current_data else "")
                        new_audio = st.text_input("🎙️ مسار أو رابط التسجيل الصوتي للرواية الشفوية (مثال: `audio1.mp3`):", value=str(current_data) if current_data else "")
                        
                        new_loc = st.text_input("🏙️ التموضع الترابي الدقيق (الجماعة / الدوار):", value=current_data if current_data else "")
                        new_hist = st.text_area("📜 النبذة والتحقيق الأنثروبولوجي الموثق:", value=current_data if current_data else "")
                        new_daily = st.text_input("📅 الأنشطة اليومية وطبيعة المشرف:", value=current_data if current_data else "")
                        new_annual = st.text_input("🌾 الأنشطة الموسمية والطقوس:", value=current_data if current_data else "")
                        new_books = st.text_area("📚 المصادر والكتب البيبليوغرافية للباحثين:", value=current_data if current_data else "")
                        
                        col_lat, col_lon = st.columns(2)
                        with col_lat: new_lat = st.number_input(" خط العرض الجغرافي:", value=float(current_data) if current_data else 31.7917, format="%.4f", key="num_lat_sh_v14")
                        with col_lon: new_lon = st.number_input(" خط الطول الجغرافي:", value=float(current_data) if current_data else -7.0926, format="%.4f", key="num_lon_sh_v14")
                        
                        if st.form_submit_button("💾 حفظ كافة التعديلات وتحديث بطاقة المعلم فوراً", use_container_width=True):
                            cursor.execute("""
                                UPDATE shrines 
                                SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, latitude=?, longitude=?, image_url=?, manuscript_url=?, audio_url=?
                                WHERE name=?""", (new_type, new_loc, new_hist, new_daily, new_annual, new_books, new_lat, new_lon, new_img, new_manuscript, new_audio, shrine_to_edit))
                            conn.commit()
                            st.success(f"🔔 تم تحديث مَعلم {shrine_to_edit} وحقن شواهده الميدانية بنجاح فورياً صلب المنصة!")
                            st.rerun()
                            
        with admin_tab3:
            st.markdown("##### 📖 محرك تعديل المصطلحات والمفاهيم القاموسية الملحقة بصور (المكنز اللغوي) :")
            all_live_terms = [item for item in cursor.execute("SELECT term FROM thesaurus_terms ORDER BY term ASC").fetchall()]
            term_to_edit = st.selectbox("🎯 اختر المصطلح أو المفهوم المراد تصحيحه أو دعم التحقيق بصورة:", ["--- اختر مصطلحاً لتعديله ---"] + all_live_terms, key="sel_term_edit_con_v14_13")
            
            if term_to_edit != "--- اختر مصطلحاً لتعديله ---":
                current_term_data = cursor.execute("SELECT category, definition, term_image FROM thesaurus_terms WHERE term = ?", (term_to_edit,)).fetchone()
                
                if current_term_data:
                    with st.form("shamel_term_edit_form_v14_13"):
                        st.info(f"⚙️ نموذج تعديل بطاقة القاموس البصرية: {term_to_edit}")
                        new_term_cat = st.text_input("🗂️ الفئة الأنثروبولوجية صلب الأطروحة:", value=current_term_data if current_term_data else "")
                        new_term_img = st.text_input("📸 مسار أو رابط صورة المخطوط/الوثيقة للمصطلح (مثال: `doc1.jpg`):", value=str(current_term_data) if current_term_data else "")
                        new_term_def = st.text_area("📚 التعريف العلمي المعتمد الأكاديمي:", value=current_term_data if current_term_data else "")
                        
                        if st.form_submit_button("💾 حفظ تعديلات المصطلح وتحديث القاموس فوراً", use_container_width=True):
                            cursor.execute("UPDATE thesaurus_terms SET category=?, definition=?, term_image=? WHERE term=?", (new_term_cat, new_term_def, new_term_img, term_to_edit))
                            conn.commit()
                            st.success(f"🔔 تم تحديث المفهوم القاموسي {term_to_edit} وحقن الشاهد المصور بنجاح فورياً صلب المكنز!")
                            st.rerun()
# نحت صف روابط المكنز النصية صلب الشريط المتدرج بالسقف لعام 2026 مائة بالمائة 
current_page_val = st.query_params.get("page", "home")
active_sections_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "sections" else ""
active_about_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "about" else ""
active_admin_style = "color: #D4AF37 !important; font-weight:900;" if current_page_val == "admin" else ""
active_search_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "search" else ""
active_atlas_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "atlas" else ""
active_stats_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "stats" else ""

st.markdown(f"""
    <div class='shamel-top-gradient-fixed-ribbon'>
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self' style='{active_sections_style}'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self' style='{active_about_style}'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=admin' target='_self' style='{active_admin_style}'>🔐 بوابة الإدارة</a>
        <a class='shamel-nav-link' href='?page=search' target='_self' style='{active_search_style}'>🔍 البحث في المكنز</a>
        <a class='shamel-nav-link' href='?page=atlas' target='_self' style='{active_atlas_style}'>🗺️ أطلس المكنز</a>
        <a class='shamel-nav-link' href='?page=stats' target='_self' style='margin-right: auto; {active_stats_style}'>📊 إحصائيات المكنز</a>
    </div>
""", unsafe_allow_html=True)

if current_page_val == "about": show_about_project_popup()
elif current_page_val == "admin": show_admin_dashboard_popup()
elif current_page_val == "contact": show_contact_us_popup()

if current_page_val == "sections": show_maknez_sections_dashboard()
elif current_page_val == "search": show_shamel_search_engine_page()
elif current_page_val == "atlas": show_maknez_atlas_interactive_map_page()
elif current_page_val == "stats": show_maknez_statistics_page()
else: st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
