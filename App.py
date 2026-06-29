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
    cursor.execute("CREATE TABLE IF NOT EXISTS thesaurus_terms (id INTEGER PRIMARY KEY AUTOINCREMENT, term NOT NULL UNIQUE, category TEXT NOT NULL, definition TEXT NOT NULL)")
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
        
        /* تخصيص هيدر المنصة ليكون شفافاً مائة بالمائة لضمان بقاء شريط الملاحة مرئياً وصافياً وحراً */
        div[data-testid="stHeader"] {{
            background: transparent !important;
            z-index: 9999 !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
        /* بناء شريط الملاحة الأفقي الملتصق بالقمة قسرياً بالتوجيه السيادي المطلق العازل للحظر سحابياً */
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
        
        .shamel-nav-link:hover {{
            color: #10B981 !important;
            transform: translateY(-1px) !important;
        }}

        /* 🟢 الحل الحاسم لمنع المستطيلات البيضاء الميتة: حظر فرض التمرير الإجباري على جميع النوافذ بشكل أعمى */
        div[data-testid="stDialog"] {{
            max-height: 85vh !important;
            background: #FFFFFF !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
        }}
        
        /* 🟢 تفعيل شريط التمرير الـ Scroll الداخلي قسرياً وحصرياً لنوافذ الاستمارات الممتدة دون تشويه النبذة */
        div[data-testid="stDialog"] .stForm {{
            max-height: 380px !important;
            overflow-y: auto !important;
            padding-left: 10px !important;
        }}

        /* سحق التداخل كلياً في العناوين والرموز عبر عزل وعرض التبويبات ككتل أفقية صافية ومتباعدة بجاذبية تامة */
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
            border-bottom: none !important;
            width: 100% !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
        }}
        button[data-testid="stTab"]:hover {{
            background: #E5E7EB !important;
            color: #1E3A8A !important;
        }}
        button[data-testid="stTab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            background: #064E3B !important;
            font-weight: 900 !important;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.15) !important;
        }}
        
        /* تنسيق البطاقة الأنيقة للمعلومات الكاملة داخل الـ Popup الملوكي */
        .card-shrine-popup {{
            background: #FFFFFF !important;
            border-right: 6px solid #D4AF37 !important;
            padding: 22px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
            margin-top: 12px !important;
            direction: rtl !important;
        }}
        .card-shrine-field {{
            font-size: 16px !important;
            line-height: 1.8 !important;
            margin-bottom: 12px !important;
            color: #1F2937 !important;
            border-bottom: 1px dashed #E5E7EB;
            padding-bottom: 6px;
        }}
        
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

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)
# 1. الدالة المنبثقة التفاعلية للتعريف بالأطروحة ونبذة عن المشروع (محمية ومطهرة بالكامل)
@st.dialog("نبذة عن المشروع الأكاديمي")
def show_about_project_popup():
    st.markdown("<div class='popup-header-title'>🏛️ نبذة عن المشروع الأكاديمي</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='popup-content-text' style='padding: 10px 5px;'>
        <p>يهدف هذا المشروع التراثي والمكنز الوطني السيادي الشامل إلى جمع وتوثيق ورقمنة كل ما يحتاجه طالب العلم والباحث الأنثروبولوجي من معطيات جغرافية، تاريخية، بيبليوغرافية، وأنثروبولوجية متعلقة بالمنشآت الروحية، الأضرحة، والمزارات الشريفة في ربوع المملكة المغربية الشريفة.</p>
        <p>إن هذه المنصة الرقمية المتقدمة لعام <b>2026</b> هي الثمرة التقنية الحية والتحويل التكنولوجي المتكامل للأطروحة العلمية والميدانية المتميزة التي نوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.</p>
        <hr style='border: 0; border-top: 1px solid #E5E7EB; margin: 15px 0;'>
        <p style='text-align: center; font-weight: bold; color: #1E3A8A; margin-bottom:5px;'>👨‍🎓 الباحث الدكتور: رشيد الجانبي</p>
        <p style='text-align: center; font-weight: bold; color: #D4AF37;'>👩‍🏫 الأستاذة المشرفة: الدكتورة فاطنة الغزي</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏛️ إغلاق النافذة والعودة للمكنز", use_container_width=True, key="close_about_clean_btn"):
        st.query_params.clear()
        st.rerun()
# 2. الواجهة العريضة الأفقية (width="large") المطهرة بالكامل والخالية من أزرار الرد للزوار العاديين
@st.dialog("دفتر التواصل الرقمي مع إدارة المكنز", width="large")
def show_contact_us_popup():
    st.markdown("<div class='popup-header-title'>📬 تواصل علمي وتحقيق ميداني</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #F8FAFC; border-right: 5px solid #1E3A8A; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>
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
                
                cursor.execute("""
                    INSERT INTO visitor_feedback (visitor_name, visitor_email, shrine_related, feedback_text, submission_date) 
                    VALUES (?, ?, ?, ?, ?)""", 
                    (c_sender_name, c_sender_email, c_sender_subject, c_sender_message, now_str))
                conn.commit()
                
                st.success("🔔 تم إرسال رسالة تذكير بنجاح إلى الموقع! يرجى من الدكتور رشيد الجانبي تفقد بريده الإلكتروني للاطلاع على التفاصيل الكاملة للمراسلة.")
                st.toast("📨 تم قذف رسالة التذكير بنجاح!", icon="🔔")
                st.rerun()
            else:
                st.error("⚠️ منظومة الأمان تمنع الإرسال، يرجى كتابة بريدك الإلكتروني ونص الرسالة أولاً.")
# اللحام التكنولوجي السيادي الحاسم: استفراد وسم @st.dialog للبطاقات الفردية لتعمل بنجاح عند نقر أزرار لوحة الأقسام
@st.dialog("البطاقة العلمية الكاملة للمَعلم التراثي المحقق", width="large")
def popup_individual_shrine_card(shrine_name):
    row = cursor.execute("""
        SELECT name, history_details, exact_location, historical_era, scientific_source, daily_activities, annual_activities, researchers_books
        FROM shrines WHERE name = ?""", (shrine_name,)).fetchone()
    if row:
        st.markdown(f"<h3 style='color:#1E3A8A; text-align:center; font-family:\"Reem Kufi\"; border-bottom:3px solid #D4AF37; padding-bottom:12px;'>🕌 {row[0]}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup'>
            <div class='card-shrine-field'><b>⏳ العصر التاريخي المعاصر له:</b> {row[3]}</div>
            <div class='card-shrine-field'><b>🗺️ الموقع الجغرافي الميداني الدقيق:</b> {row[2]}</div>
            <div class='card-shrine-field'><b>📜 النبذة والتحقيق الأنثروبولوجي الموثق:</b> {row[1]}</div>
            <div class='card-shrine-field'><b>📅 الأنشطة اليومية والموسمية:</b> {row[5]} | {row[6]}</div>
            <div class='card-shrine-field'><b>📚 المصادر والكتب البيبليوغرافية للباحثين:</b> {row[7]}</div>
            <div class='card-shrine-field' style='color:#064E3B; font-weight:bold; border-bottom:none;'><b>🔬 المصدر العلمي المعتمد للأطروحة:</b> {row[4]}</div>
        </div>
        """, unsafe_allow_html=True)

@st.dialog("البطاقة العلمية للمصطلح القاموسي المحقق", width="large")
def popup_individual_term_card(term_name):
    row = cursor.execute("SELECT term, category, definition FROM thesaurus_terms WHERE term = ?", (term_name,)).fetchone()
    if row:
        st.markdown(f"<h3 style='color:#064E3B; text-align:center; font-family:\"Reem Kufi\"; border-bottom:3px solid #D4AF37; padding-bottom:12px;'>📖 مصطلح: {row[0]}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-shrine-popup' style='border-right-color:#064E3B;'>
            <div class='card-shrine-field'><b>🗂️ الفئة الأنثروبولوجية صلب الأطروحة:</b> {row[1]}</div>
            <div class='card-shrine-field' style='font-size:18px !important; line-height:2; border-bottom:none;'><b>📚 التعريف العلمي المعتمد الأكاديمي:</b><br>{row[2]}</div>
        </div>
        """, unsafe_allow_html=True)
# لوحة تصفح الأقسام الثلاثة المحدثة كصفحة كاملة ومطهرة من مشكلة التداخل والمزودة بميزة الـ Popup الفردي لكل زر
def show_maknez_sections_dashboard():
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.96); padding: 25px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); margin: 20px auto; max-width: 96%; direction: rtl;'>
            <h2 style='text-align:center; color:#1E3A8A; font-family:"Reem Kufi", serif; margin-bottom: 5px;'>🏛️ لوحة تصفح الأقسام والتحقيقات الميدانية للأطروحة العلمية</h2>
            <p style='text-align:center; color:#4B5563; font-family:"Tajawal", sans-serif; font-size:16px; margin-bottom: 10px;'>اضغط على اسم أي ضريح أو معلم تراثي أو مصطلح محقق لتنبثق لك بطاقته العلمية الأنيقة والمرتبة فوراً</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🕌 رواق صلحاء المسلمين", "📜 رواق مزارات اليهود", "📖 المكنز اللغوي والمصطلحات"])
    
    with tab1:
        st.markdown("<h4 style='color:#1E3A8A; font-weight:bold; margin-top:20px; margin-bottom:20px; border-right: 5px solid #1E3A8A; padding-right:10px;'>🕌 الأولياء والصلحاء المسلمون بالمملكة الشريفة:</h4>", unsafe_allow_html=True)
        shrines_m = cursor.execute("SELECT name, id FROM shrines WHERE type = 'أضرحة المسلمين' ORDER BY id DESC").fetchall()
        if not shrines_m:
            st.info("لا توجد معطيات للأضرحة الإسلامية حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(3)
            for idx, (name, s_id) in enumerate(shrines_m):
                with cols[idx % 3]:
                    if st.button(f"🕌 {name}", key=f"m_sh_btn_{s_id}", use_container_width=True):
                        popup_individual_shrine_card(name)

    with tab2:
        st.markdown("<h4 style='color:#064E3B; font-weight:bold; margin-top:20px; margin-bottom:20px; border-right: 5px solid #064E3B; padding-right:10px;'>📜 مزارات ومعالم اليهود المغاربة التراثية التاريخية:</h4>", unsafe_allow_html=True)
        shrines_j = cursor.execute("SELECT name, id FROM shrines WHERE type = 'مزارات اليهود' ORDER BY id DESC").fetchall()
        if not shrines_j:
            st.info("لا توجد معطيات لمزارات اليهود حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(3)
            for idx, (name, s_id) in enumerate(shrines_j):
                with cols[idx % 3]:
                    if st.button(f"📜 {name}", key=f"j_sh_btn_{s_id}", use_container_width=True):
                        popup_individual_shrine_card(name)

    with tab3:
        st.markdown("<h4 style='color:#0F5132; font-weight:bold; margin-top:20px; margin-bottom:20px; border-right: 5px solid #0F5132; padding-right:10px;'>📖 قاموس المكنز اللغوي والمفاهيم الأنثروبولوجية المحققة:</h4>", unsafe_allow_html=True)
        terms = cursor.execute("SELECT term, id FROM thesaurus_terms ORDER BY term ASC").fetchall()
        if not terms:
            st.info("المعجم اللغوي القاموسي فارغ حالياً صلب قاعدة البيانات.")
        else:
            cols = st.columns(4)
            for idx, (term, t_id) in enumerate(terms):
                with cols[idx % 4]:
                    if st.button(f"📖 {term}", key=f"term_btn_{t_id}", use_container_width=True):
                        popup_individual_term_card(term)
# بوابة إدارة وتغذية المكنز الوطني ودعم الاستيراد التراكمي الشامل
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
                body_reply = urllib.parse.quote(f"المرسل الكريم {f_name}،\n\nنشكركم على تواصلكم العلمي الميداني مع المكنز الوطني لعام 2026.\n\nمع تحيات،\nالدكتور رشيد الجانبي")
                mailto_link = f"mailto:{f_email}?subject={subject_reply}&body={body_reply}"
                st.markdown(f'<a href="{mailto_link}" target="_self" style="text-decoration:none;"><div style="background:#15803D; color:white; text-align:center; padding:8px; border-radius:4px; margin-bottom:15px; font-size:14px; font-weight:bold;">✉️ رد سريع ومباشر لبريد الباحث {f_name}</div></a>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<h5>📥 بوابة ضخ ملفات الـ CSV التراكمية:</h5>", unsafe_allow_html=True)
        if "uploader_counter" not in st.session_state: st.session_state.uploader_counter = 0
        uploaded_csv_list = st.file_uploader("اختر ملفات الـ CSV المحددة:", type=["csv"], accept_multiple_files=True, key=f"pop_csv_u_{st.session_state.uploader_counter}")
        
        if uploaded_csv_list and st.button("🚀 البدء في معالجة وضخ الملفات دفعة واحدة", use_container_width=True):
            added_shrines, added_terms = 0, 0
            for uploaded_csv in uploaded_csv_list:
                df = pd.read_csv(uploaded_csv, encoding='utf-8')
                for index, row in df.iterrows():
                    s_name = str(row.get('shrine_name', '')).strip()
                    if not s_name or s_name == "nan" or "shrine_name" in s_name: continue
                    tags_val = str(row.get('tags', '')).strip()
                    s_type = str(row.get('shrine_type', 'أضرحة المسلمين')).strip()
                    hist_val = str(row.get('history_details', 'غير محدد')).strip()
                    prov_name = str(row.get('province', 'إقليم شفشاون')).strip()
                    
                    if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                        cursor.execute("INSERT OR IGNORE INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                        added_terms += 1
                    else:
                        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                        prov_id_row = cursor.execute("SELECT id FROM geography WHERE province=?", (prov_name,)).fetchone()
                        if prov_id_row:
                            prov_id = int(prov_id_row[0])
                            cursor.execute("INSERT OR IGNORE INTO shrines (name, type, province_id, history_details) VALUES (?, ?, ?, ?)", (s_name, s_type, prov_id, hist_val))
                            added_shrines += 1
            conn.commit()
            st.session_state.uploader_counter += 1
            st.success(f"📊 تم الضخ التراكمي بنجاح: +{added_shrines} ضريح، +{added_terms} مصطلح معجمي.")
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
    show_about_project_popup()
elif current_page_val == "admin":
    show_admin_dashboard_popup()
elif current_page_val == "contact":
    show_contact_us_popup()

# حقن استدعاء الصفحة الكاملة والديناميكية للأقسام بنجاح ودون تداخل نوافذ
if current_page_val == "sections":
    show_maknez_sections_dashboard()
else:
    # حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث في الصفحة الرئيسية الافتراضية
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
