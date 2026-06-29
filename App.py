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
# قالب التنسيق السيادي وتحصين تمركز الشريط المتدرج وحواف النافذة (CSS الشامل الشامخ)
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

        html, body, .stMarkdown, p, span, label {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)
# ==========================================
# دالات النوافذ المنبثقة التفاعلية للمشروع وبوابة التغذية الرقمية الفولاذية
# ==========================================

# 1. الدالة المنبثقة التفاعلية للتعريف بالأطروحة ونبذة عن المشروع بعد التحيين المنقح وصفر أخطاء ترتيب
@st.dialog("نبذة عن المشروع")
def show_about_project_popup():
    st.markdown("<div class='popup-header-title'>🏛️ نبذة عن المشروع الأكاديمي</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='popup-content-text'>
        <p>يهدف هذا المشروع التراثي والمكنز الوطني السيادي الشامل إلى جمع وتوثيق ورقمنة كل ما يحتاجه طالب العلم والباحث الأنثروبولوجي من معطيات جغرافية، تاريخية، بيبليوغرافية، وأنثروبولوجية متعلقة بالمنشآت الروحية، الأضرحة، والمزارات الشريفة في ربوع المملكة المغربية الشريفة.</p>
        <p>إن هذه المنصة الرقمية المتقدمة لعام <b>2026</b> هي الثمرة التقنية الحية والتحويل التكنولوجي المتكامل للأطروحة العلمية والميدانية المتميزة التي نوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.</p>
        <hr style='border: 0; border-top: 1px solid #E5E7EB; margin: 15px 0;'>
        <p style='text-align: center; font-weight: bold; color: #1E3A8A;'>👨‍🎓 الباحث الدكتور: رشيد الجانبي</p>
        <p style='text-align: center; font-weight: bold; color: #D4AF37;'>👩‍🏫 الأستاذة المشرفة: الدكتورة فاطنة الغزي</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("إغلاق", use_container_width=True, key="close_popup_btn_v6_final"):
        st.rerun()
# 2. الدالة المنبثقة السيادية لبوابة الإدارة ودعم الاستيراد المتعدد للملفات والتقارير الإحصائية وسحق الـ tuple نهائياً مائة بالمائة
@st.dialog("بوابة إدارة وتغذية المكنز الوطني")
def show_admin_dashboard_popup():
    st.markdown("<div class='popup-header-title'>🔐 نظام التغذية الرقمية والاستيراد التراكمي الشامل</div>", unsafe_allow_html=True)
    developer_key = st.text_input("أدخل رمز العبور السيادي لتنشيط صلاحيات الإشراف:", type="password", key="popup_dev_key_fixed_v11")
    
    if developer_key == "MAROC_2026":
        st.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز بنجاح!")
        st.markdown("---")
        
        if "uploader_counter" not in st.session_state: 
            st.session_state.uploader_counter = 0
            
        uploaded_csv_list = st.file_uploader(
            "اختر ملفات الأضرحة والمصطلحات الشاملة بصيغة (.csv) [يمكنك اختيار ملفات متعددة معاً]:", 
            type=["csv"], 
            accept_multiple_files=True,
            key=f"popup_csv_uploader_multi_v11_{st.session_state.uploader_counter}"
        )
        
        if uploaded_csv_list:
            if st.button("🚀 البدء في معالجة وضخ كافة الملفات المحددة دفعة واحدة", use_container_width=True):
                files_count = len(uploaded_csv_list)
                added_shrines = 0
                added_terms = 0
                
                try:
                    for uploaded_csv in uploaded_csv_list:
                        df = pd.read_csv(uploaded_csv, encoding='utf-8')
                        rename_dict = {}
                        for col in df.columns:
                            clean_col = str(col).strip().replace('\n', '').replace(' ', '')
                            if 'shrine_name' in clean_col: rename_dict[col] = 'shrine_name'
                            elif 'shrine_type' in clean_col: rename_dict[col] = 'shrine_type'
                            elif 'province' in clean_col: rename_dict[col] = 'province'
                            elif 'exact_location' in clean_col: rename_dict[col] = 'exact_location'
                            elif 'history_details' in clean_col: rename_dict[col] = 'history_details'
                            elif 'daily_activ' in clean_col: rename_dict[col] = 'daily_activities'
                            elif 'annual_activities' in clean_col: rename_dict[col] = 'annual_activities'
                            elif 'researchers_books' in clean_col: rename_dict[col] = 'researchers_books'
                            elif 'creative_works' in clean_col: rename_dict[col] = 'creative_works'
                            elif 'web_links' in clean_col: rename_dict[col] = 'web_links'
                            elif 'belief_type' in clean_col: rename_dict[col] = 'belief_type'
                            elif 'belief_details' in clean_col: rename_dict[col] = 'belief_details'
                            elif 'scientific_source' in clean_col: rename_dict[col] = 'scientific_source'
                        df = df.rename(columns=rename_dict)
                        for index, row in df.iterrows():
                            s_name = str(row.get('shrine_name', '')).strip()
                            if not s_name or s_name == "nan" or "shrine_name" in s_name: continue
                            tags_val = str(row.get('tags', '')).strip()
                            s_type = str(row.get('shrine_type', 'أضرحة المسلمين')).strip()
                            hist_val = str(row.get('history_details', 'غير محدد')).strip()
                            sc_src = str(row.get('scientific_source', 'رواية شفوية ميدانية مأثورة')).strip()
                            b_type_val = str(row.get('belief_type', 'وظائف اجتماعية وقبلية')).strip()
                            b_details_val = str(row.get('belief_details', 'موثق بالتحقيق الميداني للأطروحة')).strip()
                            
                            if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                                existing_term_row = cursor.execute("SELECT id FROM thesaurus_terms WHERE term=?", (s_name,)).fetchone()
                                if existing_term_row: 
                                    cursor.execute("UPDATE thesaurus_terms SET category=?, definition=? WHERE term=?", (s_type, hist_val, s_name))
                                else: 
                                    cursor.execute("INSERT INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                                    added_terms += 1
                            else:
                                prov_name = str(row.get('province', 'إقليم شفشاون')).strip()
                                cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                                conn.commit()
                                
                                prov_id_row = cursor.execute("SELECT id FROM geography WHERE province=?", (prov_name,)).fetchone()
                                if prov_id_row:
                                    # 🟢 سحق خطأ الـ tuple الجغرافي الأول: تفريغ المعرف عبر استدعاء الفهرس الصافي الصافي 0 قسرياً
                                    prov_id = int(prov_id_row[0])
                                    era_val = str(row.get('historical_era', 'غير محدد')).strip()
                                    
                                    auto_lat = 31.7917
                                    auto_lon = -7.0926
                                    if 'شفشاون' in prov_name: auto_lat, auto_lon = 35.1687, -5.2636
                                    elif 'تطوان' in prov_name: auto_lat, auto_lon = 35.5785, -5.3684
                                    elif 'مراكش' in prov_name: auto_lat, auto_lon = 31.6295, -7.9811
                                    
                                    existing_row = cursor.execute("SELECT id FROM shrines WHERE name = ? AND province_id = ?", (s_name, prov_id)).fetchone()
                                    if existing_row:
                                        # 🟢 سحق خطأ الـ tuple المزاراتي الثاني: تفريغ المعرف المكرر عبر الفهرس الصفر 0 لتأمين التحديث الميداني
                                        shrine_id = int(existing_row[0])
                                        cursor.execute("""
                                            UPDATE shrines SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, creative_works=?, web_links=?, historical_era=?, tags=?, latitude=?, longitude=?, scientific_source=? WHERE id=?""", 
                                            (s_type, str(row.get('exact_location', 'ميداني')), hist_val, str(row.get('daily_activities', '')), str(row.get('annual_activities', '')), str(row.get('researchers_books', '')), str(row.get('creative_works', '')), str(row.get('web_links', '')), era_val, tags_val, auto_lat, auto_lon, sc_src, shrine_id))
                                    else:
                                        cursor.execute("""
                                            INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links, scientific_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                                        (s_name, s_type, prov_id, str(row.get('exact_location', 'ميداني')), hist_val, str(row.get('daily_activities', '')), str(row.get('annual_activities', '')), era_val, tags_val, auto_lat, auto_lon, str(row.get('researchers_books', '')), str(row.get('creative_works', '')), str(row.get('web_links', '')), sc_src))
                                        shrine_id = cursor.lastrowid
                                        added_shrines += 1
                                    
                                    cursor.execute("DELETE FROM beliefs_and_functions WHERE shrine_id = ?", (shrine_id,))
                                    cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, b_type_val, b_details_val))
                    conn.commit()
                    st.session_state.uploader_counter += 1
                    
                    # قذف الرسالة الإحصائية الناجحة والشاملة التي تبتغيها للأطروحة مائة بالمائة
                    success_msg = f"📊 تم استيراد عدد {files_count} من الملفات بنجاح؛ تمت إضافة عدد {added_shrines} من الأضرحة الجديدة، وعدد {added_terms} من المصطلحات المعجمية صلب المنظومة."
                    st.success(success_msg)
                    st.toast(success_msg, icon="🎉")
                except Exception as e: 
                    st.error(f"❌ خطأ أثناء الاستيراد الميداني التراكمي: {e}")
    elif developer_key != "":
        st.error("⚠️ الرمز السري غير صحيح، يرجى مراجعة حصانة المنظومة السيادية.")

# نحت صف روابط المكنز النصية صلب الشريط المتدرج بالقمة (ترتيب تتابعي محمي بنسبة 100%)
current_page_val = st.query_params.get("page", "home")
active_about_style = "color: #10B981 !important; font-weight:900;" if current_page_val == "about" else ""
active_admin_style = "color: #D4AF37 !important; font-weight:900;" if current_page_val == "admin" else ""

st.markdown(f"""
    <div class='shamel-top-gradient-fixed-ribbon'>
        <!-- صف روابط المكنز النصية الصافية والنحيفة بسقف المتصفح لعام 2026 مائة بالمائة -->
        <a class='shamel-nav-link' href='?page=home' target='_self'>الرئيسية</a>
        <a class='shamel-nav-link' href='?page=sections' target='_self'>أقسام المكنز</a>
        <a class='shamel-nav-link' href='?page=about' target='_self' style='{active_about_style}'>حول المشروع</a>
        <a class='shamel-nav-link' href='?page=contact' target='_self'>اتصل بنا</a>
        <a class='shamel-nav-link' href='?page=admin' target='_self' style='{active_admin_style}'>🔐 بوابة الإدارة</a>
        <a class='shamel-nav-link' href='?page=search' target='_self' style='margin-right: auto; font-weight: 900; color: #FFFFFF !important;'>🔍 البحث في المكنز</a>
    </div>
""", unsafe_allow_html=True)
# ==========================================
# معالج الاستدعاء الفوري والتحويل التفاعلي للنوافذ سحابياً (بصفر مشاكل Pylance وصفر أخطاء ترتيب)
# ==========================================

# بايثون يمرر الاستدعاء بنجاح تام لأن شرح وهندسة الدالات تم قراءته مسبقاً في البلوكات العليا
if current_page_val == "about":
    st.query_params.clear()
    show_about_project_popup()
elif current_page_val == "admin":
    st.query_params.clear()
    show_admin_dashboard_popup()

# حقن مسافة الأمان تحت الشريط لمنع تداخل المباحث القادمة بالأسفل صلب المنظومة المكتملة
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
