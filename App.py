import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse
import base64

# إعدادات الشاشة بعرض المتصفح الكامل 100% الشامل للمملكة لعام 2026
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
# قالب التنسيق وتحصين تمركز الشريط والتبويبات أفقياً بألوان المكتبة الشاملة (CSS الفخم)
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
        
        div[data-testid="stHeader"] {{ background: transparent !important; z-index: 9999 !important; }}
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        
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
            padding: 0 60px !important;
            direction: rtl !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}
        
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
        /* سحق التداخل كلياً في العناوين والرموز عبر عزل وعرض التبويبات ككتل أفقية صافية ومتباعدة */
        div[data-testid="stTabs"] {{
            background: #FFFFFF !important;
            padding: 15px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        }}
        div[data-testid="stTabScrollList"] {{
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-around !important;
            gap: 20px !important;
            border-bottom: 3px solid #D4AF37 !important;
            padding-bottom: 10px !important;
            margin-bottom: 15px !important;
        }}
        button[data-testid="stTab"] {{
            font-family: 'Tajawal', sans-serif !important;
            font-weight: bold !important;
            font-size: 16px !important;
            color: #4B5563 !important;
            background: #F3F4F6 !important;
            padding: 12px 30px !important;
            border-radius: 8px 8px 0 0 !important;
            border: 1px solid #E5E7EB !important;
            border-bottom: none !important;
            width: 100% !important;
            text-align: center !important;
        }}
        button[data-testid="stTab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            background: #064E3B !important;
            font-weight: 900 !important;
        }}
        
        /* تنسيق البطاقة الأنيقة والمرتبة للمعلومات الكاملة داخل الـ Popup */
        .card-shrine-popup {{
            background: #FFFFFF !important;
            border-right: 6px solid #D4AF37 !important;
            padding: 20px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            margin-top: 10px !important;
            direction: rtl !important;
        }}
        .card-shrine-field {{
            font-size: 16px !important;
            line-height: 1.8 !important;
            margin-bottom: 10px !important;
            color: #1F2937 !important;
        }}
        
        div[data-testid="stDialog"], div[data-testid="stDialog"] > div, div[data-testid="stDialog"] .stForm, div[data-testid="stDialog"] div[data-testid="stVerticalBlock"] {{
            max-height: 560px !important;
            overflow-y: auto !important;
        }}
        div[data-testid="stDialog"]::-webkit-scrollbar {{ width: 8px !important; }}
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
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
        }}
    </style>
""", unsafe_allow_html=True)
# 1. دالة نبذة عن المشروع
def show_about_project_popup():
    st.markdown("<div class='popup-header-title'>🏛️ نبذة عن المشروع الأكاديمي</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='popup-content-text'>
        <p>يهدف هذا المشروع التراثي والمكنز الوطني السيادي الشامل إلى جمع وتوثيق ورقمنة كل ما يحتاجه طالب العلم والباحث الأنثروبولوجي من معطيات جغرافية متعلقة بالمنشآت الروحية بالمملكة المغربية الشريفة.</p>
        <p>إن هذه المنصة الرقمية المتقدمة لعام <b>2026</b> هي الثمرة التقنية الحية والتحويل التكنولوجي المتكامل للأطروحة العلمية المتميزة التي نوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.</p>
        <hr style='border: 0; border-top: 1px solid #E5E7EB; margin: 15px 0;'>
        <p style='text-align: center; font-weight: bold; color: #1E3A8A;'>👨‍🎓 الباحث الدكتور: رشيد الجانبي</p>
        <p style='text-align: center; font-weight: bold; color: #D4AF37;'>👩‍🏫 الأستاذة المشرفة: الدكتورة فاطنة الغزي</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("إغلاق", use_container_width=True, key="close_about_btn"):
        st.rerun()

# 2. دالة دفتر التواصل
@st.dialog("دفتر التواصل الرقمي مع إدارة المكنز", width="large")
def show_contact_us_popup():
    st.markdown("<div class='popup-header-title'>📬 تواصل علمي وتحقيق ميداني</div>", unsafe_allow_html=True)
    with st.form("shamel_contact_secure_form", clear_on_submit=True):
        c_sender_name = st.text_input("اسم الباحث / المرسل الكريم:")
        c_sender_email = st.text_input("البريد الإلكتروني للمرسل:")
        c_sender_subject = st.text_input("موضوع المراسلة صلب الموضوع:")
        c_sender_message = st.text_area("نص الرسالة أو الملاحظة الترابية بالكامل:")
        if st.form_submit_button("🚀 إرسال الرسالة بنجاح وإرسال التذكير", use_container_width=True):
            if c_sender_email and c_sender_message:
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute("INSERT INTO visitor_feedback (visitor_name, visitor_email, shrine_related, feedback_text, submission_date) VALUES (?, ?, ?, ?, ?)", (c_sender_name, c_sender_email, c_sender_subject, c_sender_message, now_str))
                conn.commit()
                st.success("🔔 تم إرسال رسالة تذكير بنجاح إلى الموقع!")
                st.rerun()
# دالات فرعية مخصصة تنبثق كنافذة Popup ثانية مستقلة عند الضغط على أي ولي أو مصطلح لعرض بطاقته الكاملة
@st.dialog("البطاقة العلمية الكاملة للمَعلم التراثي", width="large")
def popup_individual_shrine_card(shrine_name):
    # سحب تفاصيل المزار بالكامل من قاعدة البيانات
    row = cursor.execute("""
        SELECT shrines.name, geography.province, shrines.historical_era, shrines.exact_location, shrines.history_details, shrines.scientific_source, shrines.daily_activities, shrines.annual_activities, shrines.researchers_books
        FROM shrines JOIN geography ON shrines.province_id = geography.id WHERE shrines.name = ?""", (shrine_name,)).fetchone()
    if row:
        st.markdown(f"<h3 style='color:#1E3A8A; text-align:center; font-family:\"Reem Kufi\"; border-bottom:2px solid #D4AF37; padding-bottom:10px;'>🕌 {row[0]}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup'>
            <div class='card-shrine-field'><b>📍 الإقليم الجغرافي:</b> {row[1]}</div>
            <div class='card-shrine-field'><b>⏳ العصر التاريخي:</b> {row[2]}</div>
            <div class='card-shrine-field'><b>🗺️ الموقع الميداني الدقيق:</b> {row[3]}</div>
            <div class='card-shrine-field'><b>📜 النبذة والتحقيق الأنثروبولوجي:</b> {row[4]}</div>
            <div class='card-shrine-field'><b>📝 العادات والأنشطة السنوية:</b> {row[7]}</div>
            <div class='card-shrine-field'><b>📚 المصادر والكتب البيبليوغرافية:</b> {row[8]}</div>
            <div class='card-shrine-field' style='color:#064E3B; font-weight:bold;'><b>🔬 المصدر العلمي للأطروحة:</b> {row[5]}</div>
        </div>
        """, unsafe_allow_html=True)

@st.dialog("البطاقة العلمية للمصطلح المحقق", width="large")
def popup_individual_term_card(term_name):
    row = cursor.execute("SELECT term, category, definition FROM thesaurus_terms WHERE term = ?", (term_name,)).fetchone()
    if row:
        st.markdown(f"<h3 style='color:#064E3B; text-align:center; font-family:\"Reem Kufi\"; border-bottom:2px solid #D4AF37; padding-bottom:10px;'>📖 مصطلح: {row[0]}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup' style='border-right-color:#064E3B;'>
            <div class='card-shrine-field'><b>🗂️ الفئة الأنثروبولوجية صلب الأطروحة:</b> {row[1]}</div>
            <div class='card-shrine-field' style='font-size:18px !important; line-height:2;'><b>📚 التعريف العلمي المعتمد الأكاديمي:</b><br>{row[2]}</div>
        </div>
        """, unsafe_allow_html=True)
# لوحة تصفح الأقسام الثلاثة المحدثة والمطهرة من مشكلة التداخل والمزودة بميزة البطاقات المنبثقة لكل ولي
def show_maknez_sections_dashboard():
    st.markdown("<h3 style='text-align:center; color:#1E3A8A; font-family:\"Reem Kufi\";'>🏛️ لوحة تصفح الأقسام والتحقيقات الميدانية للأطروحة</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6B7280;'>اضغط على اسم أي ضريح أو مصطلح بالأسفل لتنبثق لك بطاقته العلمية الأنيقة والمرتبة فوراً</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🕌 رواق صلحاء المسلمين", "📜 رواق مزارات اليهود", "📖 المكنز اللغوي والمصطلحات"])
    
    with tab1:
        st.markdown("<h5 style='color:#1E3A8A; font-weight:bold; margin-bottom:15px;'>🕌 الأولياء والصلحاء المسلمون بالمملكة:</h5>", unsafe_allow_html=True)
        shrines_m = cursor.execute("SELECT name, id FROM shrines WHERE type = 'أضرحة المسلمين' ORDER BY id DESC").fetchall()
        if not shrines_m:
            st.info("لا توجد معطيات للأضرحة الإسلامية حالياً.")
        else:
            # عرض الأولياء في شبكة بطاقات تفاعلية جذابة بدلاً من جداول صامتة ومداخلة
            cols = st.columns(3)
            for idx, (name, s_id) in enumerate(shrines_m):
                with cols[idx % 3]:
                    if st.button(f"🕌 {name}", key=f"m_sh_btn_{s_id}", use_container_width=True):
                        popup_individual_shrine_card(name)

    with tab2:
        st.markdown("<h5 style='color:#064E3B; font-weight:bold; margin-bottom:15px;'>📜 مزارات اليهود المغاربة التراثية:</h5>", unsafe_allow_html=True)
        shrines_j = cursor.execute("SELECT name, id FROM shrines WHERE type = 'مزارات اليهود' ORDER BY id DESC").fetchall()
        if not shrines_j:
            st.info("لا توجد معطيات لمزارات اليهود حالياً.")
        else:
            cols = st.columns(3)
            for idx, (name, s_id) in enumerate(shrines_j):
                with cols[idx % 3]:
                    if st.button(f"📜 {name}", key=f"j_sh_btn_{s_id}", use_container_width=True):
                        popup_individual_shrine_card(name)

    with tab3:
        st.markdown("<h5 style='color:#0F5132; font-weight:bold; margin-bottom:15px;'>📖 قاموس المكنز اللغوي والمفاهيم الصوفية:</h5>", unsafe_allow_html=True)
        terms = cursor.execute("SELECT term, id FROM thesaurus_terms ORDER BY term ASC").fetchall()
        if not terms:
            st.info("المعجم اللغوي فارغ حالياً.")
        else:
            cols = st.columns(4)
            for idx, (term, t_id) in enumerate(terms):
                with cols[idx % 4]:
                    if st.button(f"📖 {term}", key=f"term_btn_{t_id}", use_container_width=True):
                        popup_individual_term_card(term)
# بوابة إدارة وتغذية المكنز الوطني ودعم الاستيراد التراكمي
@st.dialog("بوابة إدارة وتغذية المكنز الوطني")
def show_admin_dashboard_popup():
    st.markdown("<div class='popup-header-title'>🔐 نظام التغذية الرقمية والاستيراد التراكمي الشامل</div>", unsafe_allow_html=True)
    developer_key = st.text_input("أدخل رمز العبور لتنشيط صلاحيات الإشراف:", type="password", key="pop_dev_k")
    if developer_key == "MAROC_2026":
        st.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز بنجاح!")
        st.markdown("---")
        st.markdown("<h5>📬 صندوق الملاحظات ورسائل الباحثين الحية:</h5>", unsafe_allow_html=True)
        feedbacks = cursor.execute("SELECT visitor_name, visitor_email, shrine_related, feedback_text, submission_date FROM visitor_feedback ORDER BY id DESC").fetchall()
        if not feedbacks:
            st.info("الصندوق فارغ حالياً.")
        else:
            for index, (f_name, f_email, f_shrine, f_text, f_date) in enumerate(feedbacks):
                st.markdown(f"<div style='background:#F3F4F6; padding:10px; margin-bottom:5px; border-right:4px solid #1E3A8A;'>📅 {f_date} | <b>👤 {f_name}</b><br>📌 {f_shrine}<br>📝 {f_text}</div>", unsafe_allow_html=True)
                subject_reply = urllib.parse.quote(f"رد من المكنز الوطني: ملاحظتكم حول ({f_shrine})")
                mailto_link = f"mailto:{f_email}?subject={subject_reply}"
                st.markdown(f'<a href="{mailto_link}" target="_self" style="text-decoration:none;"><div style="background:#15803D; color:white; text-align:center; padding:5px; border-radius:4px; margin-bottom:15px; font-size:13px;">✉️ رد مباشر لبريد الباحث</div></a>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<h5>📥 بوابة ضخ ملفات الـ CSV التراكمية:</h5>", unsafe_allow_html=True)
        if "uploader_counter" not in st.session_state: st.session_state.uploader_counter = 0
        uploaded_csv_list = st.file_uploader("اختر ملفات الـ CSV:", type=["csv"], accept_multiple_files=True, key=f"pop_csv_u_{st.session_state.uploader_counter}")
        if uploaded_csv_list and st.button("🚀 البدء في معالجة وضخ الملفات دفعة واحدة", use_container_width=True):
            added_shrines, added_terms = 0, 0
            for uploaded_csv in uploaded_csv_list:
                df = pd.read_csv(uploaded_csv, encoding='utf-8')
                # (حلقة التفكيك والقراءة للمصفوفات مع سحق معضلات الـ Tuple)
                for index, row in df.iterrows():
                    s_name = str(row.get('shrine_name', '')).strip()
                    if not s_name or s_name == "nan": continue
                    tags_val = str(row.get('tags', '')).strip()
                    s_type = str(row.get('shrine_type', 'أضرحة المسلمين')).strip()
                    hist_val = str(row.get('history_details', 'غير محدد')).strip()
                    prov_name = str(row.get('province', 'إقليم شفشاون')).strip()
                    
                    if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                        cursor.execute("INSERT OR IGNORE INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                        added_terms += 1
                    else:
                        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة", prov_name))
                        prov_id = cursor.execute("SELECT id FROM geography WHERE province=?", (prov_name,)).fetchone()[0]
                        cursor.execute("INSERT OR IGNORE INTO shrines (name, type, province_id, history_details) VALUES (?, ?, ?, ?)", (s_name, s_type, prov_id, hist_val))
                        added_shrines += 1
            conn.commit()
            st.session_state.uploader_counter += 1
            st.success(f"📊 تم الضخ التراكمي بنجاح: +{added_shrines} ضريح، +{added_terms} مصطلح.")
# نحت صف روابط المكنز النصية صلب الشريط المتدرج بالقمة (ترتيب تتابعي محمي بنسبة 100% عازل للحظر سحابياً)
current_page_val = st.query_params.get("page", "home")
active_sections_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "sections" else ""
active_about_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "about" else ""
active_admin_style = "color: #D4AF37 !important; font-weight:900;" if current_page_val == "admin" else ""

st.markdown(f"""
    <div class='shamel-top-gradient-fixed-ribbon'>
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self' style='{active_sections_style}'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self' style='{active_about_style}'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=admin' target='_self' style='{active_admin_style}'>🔐 بوابة الإدارة</a>
    </div>
""", unsafe_allow_html=True)

if current_page_val == "about":
    st.query_params.clear()
    show_about_project_popup()
elif current_page_val == "admin":
    st.query_params.clear()
    show_admin_dashboard_popup()
elif current_page_val == "contact":
    st.query_params.clear()
    show_contact_us_popup()
elif current_page_val == "sections":
    st.query_params.clear()
    show_maknez_sections_dashboard()

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة بالأسفل صلب المنظومة المكتملة
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
