import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse

# 🇲🇦 إعدادات الصفحة الترابية الشاملة: ضبط العرض العريض المتوافق مع شاشات المحمول والحواسب معاً
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# الاتصال بقاعدة البيانات التاريخية الكبرى لصلحاء المملكة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()
# حقن كود المحاذاة الصارمة وتثبيت الأزرار العليا، الإحصائيات، والبانر في قمة الشاشة دائماً
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* 📱💻 التنسيق العام لليمين للحاويات العربية مع السماح بالمرونة للأقسام الأجنبية */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown, p, span, label, button, select, input, textarea {
            font-family: 'Tajawal', sans-serif !important;
            font-size: 19px !important; 
            line-height: 1.8 !important;
            direction: rtl;
            text-align: right;
        }
        
        /* 🟢 حقن التثبيت المطلق والمجسم للوحة التحكم العلوية كاملة (البانر + الأزرار + الإحصائيات) في قمة الشاشة */
        div[data-testid="stVerticalBlock"] > div:has(img) {
            position: fixed !important;
            top: 45px !important;
            left: 0 !important;
            right: 0 !important;
            background-color: #FFFFFF !important;
            z-index: 99999 !important;
            padding: 10px 40px !important;
            border-bottom: 3px solid #D4AF37 !important;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1) !important;
        }
        
        /* 🟢 تثبيت صف الأزرار العليا التفاعلية لترسيخ توازنها البصري */
        div[data-testid="stHorizontalBlock"]:has(button[key*="toggle_sidebar_btn"]) {
            position: fixed !important;
            top: 240px !important;
            left: 0 !important;
            right: 0 !important;
            background-color: #FAFAFA !important;
            z-index: 99998 !important;
            padding: 10px 40px !important;
            border-bottom: 1px solid #E5E7EB !important;
        }
        
        /* 🟢 تثبيت المربعات الإحصائية الأربعة في القمة لتظل رهن إشارة المستخدم دائماً */
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetricValue"]) {
            position: fixed !important;
            top: 310px !important;
            left: 0 !important;
            right: 0 !important;
            background-color: #FFFFFF !important;
            z-index: 99997 !important;
            padding: 10px 40px !important;
            border-bottom: 2px solid #1E3A8A !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        }
        
        /* 🛡️ إضافة مسافة أمان هيكلية عريضة للمحتوى السفلي حتى لا يختفي خلف الحاويات الثابتة */
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stForm"]) {
            margin-top: 460px !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(div[data-baseweb="tab"]) {
            margin-top: 460px !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(h3) {
            margin-top: 460px !important;
        }
        
        /* حقن الحصانة اللاتينية الصارمة لقتل التشوهات في الفرنسية والانجليزية */
        .latin-text, .latin-text p, .latin-text span, .latin-text h3 {
            direction: ltr !important;
            text-align: left !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        
        .moroccan-title {
            font-family: 'Reem Kufi', serif !important;
            font-size: 40px !important;
            font-weight: 900 !important;
            color: #1E3A8A !important;
            text-align: center !important;
            line-height: 1.5 !important;
            margin-bottom: 5px !important;
            display: block !important;
        }
        
        .stTabs [data-baseweb="tab"] { background-color: #F3F4F6 !important; border: 1px solid #E5E7EB !important; padding: 8px 18px !important; border-radius: 8px 8px 0px 0px !important; font-weight: bold !important; }
        .stTabs [aria-selected="true"] { background-color: #1E3A8A !important; color: white !important; border-color: #1E3A8A !important; }
        div[style*="border:3px solid"] { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.05) !important; background-color: #FFFFFF !important; border-radius: 12px !important; }
        
        /* حجب أزرار المتصفح التلقائية لمنع الأيقونات اللغوية المقلوبة */
        [data-testid="collapsedControlButton"], 
        [data-testid="stSidebarCollapseButton"], 
        button[data-testid="sidebar-toggle"], 
        div[class*="StyledCollapsedControl"],
        .st-emotion-cache-1wbqy5l, 
        .st-emotion-cache-6q9w0x {
            display: none !important;
            font-size: 0px !important;
            color: transparent !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0px !important;
            height: 0px !important;
        }

        [data-testid="stCodeBlock"] button span, [data-testid="stCodeBlock"] button div, [data-testid="stCodeBlock"] span, [data-testid="stCodeBlock"] div, div[class*="copyButton"] span {
            display: none !important;
        }
        [data-testid="stCodeBlock"] button, div[class*="copyButton"] button {
            color: transparent !important;
        }
        [data-testid="stCodeBlock"] button::after, div[class*="copyButton"] button::after {
            content: "📋 اضغط هنا للنسخ الفوري" !important;
            font-size: 14px !important;
            font-family: 'Tajawal', sans-serif !important;
            color: #1E3A8A !important;
            font-weight: bold !important;
            display: block !important;
        }

        ::-webkit-scrollbar { width: 14px !important; height: 14px !important; display: block !important; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #1E3A8A, #3B82F6) !important; border-radius: 8px !important; border: 2px solid #FFFFFF !important; }
        ::-webkit-scrollbar-track { background: #F3F4F6 !important; border-radius: 8px !important; }
        
        .stButton>button {
            background: linear-gradient(135deg, #1E3A8A, #3B82F6) !important;
            color: white !important;
            font-weight: 900 !important;
            border: 2px solid #D4AF37 !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
            margin: 5px auto !important;
            display: block !important;
        }
    </style>
""", unsafe_allow_html=True)
# تم نقل هذا المربع بالكامل إلى القمة لكي يتعرف عليه مفسر بايثون فوراً قبل استدعائه في فصول الكود
PROVINCE_COORDINATES = {
    'إقليم خنيفرة': (32.9358, -5.6644), 'إقليم بني ملال': (32.3373, -6.3498),
    'إقليم تطوان': (35.5785, -5.3684), 'عمالة طنجة أصيلة': (35.7595, -5.8340),
    'إقليم آسفي': (32.2994, -9.2372), 'إقليم الحوز': (31.3483, -7.9542),
    'إقليم الصويرة': (31.5085, -9.7595), 'عمالة مراكش': (31.6295, -7.9811),
    'إقليم الرشيدية': (31.9315, -4.4244), 'إقليم تارودانت': (30.4703, -8.8770),
    'إقليم شفشاون': (35.1687, -5.2636), 'إقليم العرائش': (35.1841, -6.1554),
    'إقليم الجديدة': (33.2333, -8.5000), 'إقليم السطات': (33.0010, -7.6166),
    'عمالة سلا': (34.0333, -6.8000), 'عمالة مكناس': (33.8930, -5.5473),
    'عمالة فاس': (34.0333, -5.0000), 'إقليم تاونات': (34.5364, -4.6401),
    'إقليم الفحص أنجرة': (35.6687, -5.4854)
}

def get_auto_coords(province_name):
    return PROVINCE_COORDINATES.get(province_name, (31.7917, -7.0926))

def generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text):
    html_content = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #fff; padding: 20px; }}
            .page {{ width: 210mm; padding: 20px; margin: auto; border: 1px solid #ddd; }}
            .header {{ text-align: center; border-bottom: 3px double #D4AF37; }}
            .section {{ margin-bottom: 20px; padding: 10px; border-right: 4px solid #D4AF37; background: #F8FAFC; }}
            .section-title {{ font-weight: bold; color: #1E3A8A; font-size: 20px; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header">
                <h1>{name}</h1><div style="background:#1E3A8A; color:white; padding:5px; border-radius:5px;">{s_type}</div>
                <p>📍 {region} ⟵ {province} ({loc})</p>
            </div>
            <div class="section"><div class="section-title">📜 التاريخ والسيرة</div><p>{hist}</p></div>
            <div class="section"><div class="section-title">🔄 الأنشطة والطقوس</div><p>{daily}</p></div>
            <div class="section"><div class="section-title">🎉 الاحتفالات والمواسم</div><p>{annual}</p></div>
            <div class="section"><div class="section-title">💭 الأنثروبولوجيا والاعتقاد</div><p>{beliefs_text}</p></div>
            <div class="section"><div class="section-title">📚 الخزانة العلمية والمراجع</div><p>{books}<br>{creative}<br>{links}</p></div>
        </div>
    </body>
    </html>
    """
    return html_content
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
    
    cursor.execute("CREATE TABLE IF NOT EXISTS beliefs_and_functions (id INTEGER PRIMARY KEY AUTOINCREMENT, shrine_id INTEGER, function_type TEXT NOT NULL, details TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS thesaurus_terms (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT NOT NULL UNIQUE, category TEXT NOT NULL, definition TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS media_gallery (id INTEGER PRIMARY KEY AUTOINCREMENT, shrine_id INTEGER, image_path TEXT NOT NULL, caption TEXT)")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitor_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT,
        visitor_email TEXT,
        shrine_related TEXT,
        feedback_text TEXT NOT NULL,
        submission_date TEXT
    )""")
    
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

if "sidebar_visible" not in st.session_state: st.session_state.sidebar_visible = True
if "current_page" not in st.session_state: st.session_state.current_page = "search"

# تثبيت وحقن البانر البصري الجديد ثلاثي اللغات في أعلى الواجهة ليرسخ فخامته
banner_path = "banner.jpg"
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.markdown('<span class="moroccan-title">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</span>', unsafe_allow_html=True)

# رسم صف الأزرار العليا التفاعلية الثلاثة (ثابتة في مكانها ومتاحة دوماً للمستخدم)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    btn_label = "💥 إغلاق بوابات الإدارة لتوسيع التصفح ⬅️" if st.session_state.sidebar_visible else "🏛️ إظهار بوابات المنظومة والإدارة ➡️"
    if st.button(btn_label, key="toggle_sidebar_btn"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.session_state.current_page = "search"
        st.rerun()
with btn_col2:
    if st.button("🎓 حَول المَكْنِز الأكَادِيمِي", key="about_thesis_btn"):
        st.session_state.sidebar_visible = False
        st.session_state.current_page = "about"
        st.rerun()
with btn_col3:
    if st.button("📬 دَفْتَر التَّوَاصُل وِالمُلَاحَظَات", key="contact_page_btn"):
        st.session_state.sidebar_visible = False
        st.session_state.current_page = "contact"
        st.rerun()

# سحب العدادات الإحصائية الأربعة وتثبيتها تحت الأزرار مباشرة
t_res = cursor.execute("SELECT COUNT(*) FROM shrines").fetchone()
total_shrines = int(t_res[0]) if t_res else 0

m_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='أضرحة المسلمين'").fetchone()
muslim_count = int(m_res[0]) if m_res else 0

j_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='مزارات اليهود'").fetchone()
jewish_count = int(j_res[0]) if j_res else 0

term_res = cursor.execute("SELECT COUNT(*) FROM thesaurus_terms").fetchone()
total_terms = int(term_res[0]) if term_res else 0

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1: st.metric("📊 المعالم الروحية الموثقة", total_shrines)
with stat_col2: st.metric("🕌 صلحاء المسلمين", muslim_count)
with stat_col3: st.metric("🕍 مزارات اليهود", jewish_count)
with stat_col4: st.metric("📖 المصطلحات الموثقة", total_terms)

if st.session_state.sidebar_visible:
    st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight:900;'>🏛️ بوابات المنظومة</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio(
        "اختر فصل المعطيات لتصفحه أو تغذيته:",
        ["🔍 محرك البحث العلمي الشامل", "✍️ التوثيق الميداني (إدخال يدوي)", "🔄 لوحة المراجعة والتصحيح والتعديل", "📖 مكنز المصطلحات والمفاهيم الصوفية"]
    )
    st.session_state.current_page = "sidebar"
else:
    if st.session_state.current_page == "about": menu = "🎓 حول المكنز الأكاديمي"
    elif st.session_state.current_page == "contact": menu = "📬 دفتر التواصل"
    else: menu = "🔍 محرك البحث العلمي الشامل"


# ==========================================
# 🔍 الجزء 4: واجهة محرك البحث الشامل، المؤشرات الأربعة، وحقن البانر الأفقي الملكي الجديد
# ==========================================
if menu == "🔍 محرك البحث العلمي الشامل":
    banner_path = "banner.png" # 🟢 تم التحديث: الصورة المفتوحة لديك بصيغة png، تأكد من مطابقة الاسم بدقة بداخل المجلد
    if os.path.exists(banner_path):
        # تفعيل قراءة البانر الأفقي العريض بكامل امتداده الطبيعي الفخم ليغطي قمة المنصة الرقمية بنقاء
        st.image(banner_path, use_container_width=True)
    else:
        st.markdown('<span class="moroccan-title">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</span>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:18px; color:#4B5563; font-weight:500;'>منصة علمية شاملة لتوثيق جغرافيا، تاريخ، أنثروبولوجيا، وبيبليوغرافيا التراث الروحي للمملكة المغربية</p>", unsafe_allow_html=True)
        
    st.write("---")
    
    # تفكيك توبل العدادات لمنع لافتات التوقف في السيرفر السحابي
    t_res = cursor.execute("SELECT COUNT(*) FROM shrines").fetchone()
    total_shrines = int(t_res) if t_res else 0
    
    m_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='أضرحة المسلمين'").fetchone()
    muslim_count = int(m_res) if m_res else 0
    
    j_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='مزارات اليهود'").fetchone()
    jewish_count = int(j_res) if j_res else 0
    
    term_res = cursor.execute("SELECT COUNT(*) FROM thesaurus_terms").fetchone()
    total_terms = int(term_res) if term_res else 0
    
    # تقسيم الشاشة إلى 4 مؤشرات متناسقة لتأمين العداد الجديد الفخم للمصطلحات
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1: st.metric("📊 المعالم الروحية الموثقة", total_shrines)
    with stat_col2: st.metric("🕌 صلحاء المسلمين", muslim_count)
    with stat_col3: st.metric("🕍 مزارات اليهود", jewish_count)
    with stat_col4: st.metric("📖 المصطلحات والمفاهيم الموثقة", total_terms)
    st.write("---")
    
    # دمج الملاحظات في التبويب العلوي الرئيسي لسهولة تواصل زوار الأطروحة دون نزول
    main_tab_search, main_tab_contact = st.tabs(["🔍 استكشاف الأطلس ومحرك البحث العلمي", "📬 دفتر التواصل وإرسال الملاحظات والتحقيق"])
    
    with main_tab_search:
        with st.container():
            st.markdown("<b style='color:#1E3A8A;'>💡 المساعد المفاهيمي السريع للتحقيق العلمي (فحص فوري للمصطلحات والأعراف):</b>", unsafe_allow_html=True)
            quick_word = st.text_input("اكتب الكلمة المراد فك معناها الأنثروبولوجي (مثال: مريد، هيلولة...):", label_visibility="collapsed")
            if quick_word:
                term_fetch = cursor.execute("SELECT category, definition FROM thesaurus_terms WHERE term LIKE ?", (f"%{quick_word}%",)).fetchone()
                if term_fetch: st.info(f"📙 **التصنيف:** {term_fetch} \n\n 📝 **الشرح:** {term_fetch}")
                else:
                    shrine_fetch = cursor.execute("SELECT exact_location, history_details FROM shrines WHERE name LIKE ?", (f"%{quick_word}%",)).fetchone()
                    if shrine_fetch: st.info(f"📍 **الموقع:** {shrine_fetch} \n\n 📜 **المبحث التاريخي:** {shrine_fetch}")
                    else: st.caption("المصطلح غير مدرج حالياً.")
                
        st.write("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1: search_query = st.text_input("🔍 ابحث باسم الولي، الضريح، أو الوسم (#):")
        with col2: filter_type = st.selectbox("تصنيف المنشأة الروحية المعتمد:", ["الكل", "أضرحة المسلمين", "مزارات اليهود"])
        with col3:
            regions_list = ["الكل"] + [row for row in cursor.execute("SELECT DISTINCT region FROM geography").fetchall()]
            selected_region = st.selectbox("الفلترة بجهات المملكة المغربية الـ 12:", regions_list)
        with col4:
            era_list = ["الكل", "العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"]
            selected_era = st.selectbox("الفلترة بالعصر السياسي والتاريخي:", era_list)
            
    with main_tab_contact:
        st.markdown("<p style='font-size:16px; color:#4B5563; text-align:right;'>هل تملك تصحيحاً، رواية شفوية، أو مراجع إضافية لإغناء هذا المعلم التراثي؟ أرسل ملاحظتك سراً إلى المشرف على المنصة.</p>", unsafe_allow_html=True)
        with st.form("visitor_feedback_public_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1: v_name = st.text_input("اسم الباحث / الزائر الكريم:")
            with f_col2: v_email = st.text_input("البريد الإلكتروني للتواصل:")
            with f_col3: v_shrine = st.text_input("اسم الضريح أو المصطلح المعني بالملاحظة:")
            v_text = st.text_area("نص الملاحظة، التصويب العلمي، أو الإغناء البيبليوغرافي المقترح:")
            if st.form_submit_button("🚀 إرسال الملاحظة سراً إلى إدارة المكنز"):
                if v_text:
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    cursor.execute("INSERT INTO visitor_feedback (visitor_name, visitor_email, shrine_related, feedback_text, submission_date) VALUES (?, ?, ?, ?, ?)", (v_name, v_email, v_shrine, v_text, now_str))
                    conn.commit()
                    st.success("🙏 تم إرسال ملاحظتكم بنجاح وسرية تامة إلى الدكتور رشيد الجانبي للعمل بها.")
                else: st.error("⚠️ من فضلك اكتب نص الملاحظة أولاً قبل الإرسال.")





if st.session_state.sidebar_visible:
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h4 style='color: #1E3A8A;'>🔐 بوابـة المشـرف والباحث المعتمد</h4>", unsafe_allow_html=True)
    developer_key = st.sidebar.text_input("أدخل رمز العبور لتغذية وإدارة المكنز:", type="password", key="dev_key_final")
    
    if developer_key == "MAROC_2026":
        st.sidebar.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز!")
        st.sidebar.markdown("<h5 style='color: #D4AF37; margin-bottom: 5px;'>📬 صندوق ملاحظات الباحثين والزوار الحية:</h5>", unsafe_allow_html=True)
        
        feedbacks = cursor.execute("SELECT visitor_name, visitor_email, shrine_related, feedback_text, submission_date FROM visitor_feedback ORDER BY id DESC").fetchall()
        if not feedbacks: st.sidebar.caption("الصندوق فارغ حالياً.")
        else:
            for index, (f_name, f_email, f_shrine, f_text, f_date) in enumerate(feedbacks):
                st.sidebar.markdown(f"""
                <div style='background-color:#FFFFFF; border-right:4px solid #1E3A8A; padding:15px; margin-bottom:10px; border-radius:8px; text-align:right;'>
                    <small style='color:#9CA3AF;'>📅 {f_date}</small><br>
                    <b>👤 المرسل:</b> {f_name}<br>
                    <b>📧 البريد:</b> {f_email}<br>
                    <b>🕌 خاص بـ:</b> {f_shrine}<br>
                    <b>📝 الملاحظة:</b> {f_text}
                </div>
                """, unsafe_allow_html=True)
                
                subject_reply = urllib.parse.quote(f"رد من المكنز الوطني للأضرحة: بخصوص ملاحظتكم حول ({f_shrine})")
                body_reply = urllib.parse.quote(f"السلام عليكم ورحمة الله وبركاته الأخ الفاضل {f_name}،\n\nنشكركم جزيلاً على ملاحظتكم القيمة التي أرسلتموها عبر المنصة...\n\nتحياتنا،\nالدكتور رشيد الجانبي")
                mailto_link = f"mailto:{f_email}?subject={subject_reply}&body={body_reply}"
                
                st.sidebar.markdown(f"""
                <a href="{mailto_link}" target="_blank" style="text-decoration: none; width: 100%;">
                    <div style="background: linear-gradient(135deg, #15803D, #16A34A); color: white; text-align: center; padding: 6px; border-radius: 6px; font-size: 14px; font-weight: bold; margin-bottom: 20px; border: 1px solid #14532D;">
                        ✉️ اضغط هنا للرد الفوري على {f_name}
                    </div>
                </a>
                """, unsafe_allow_html=True)
                st.sidebar.markdown("<hr style='margin: 5px 0 15px 0; border-top: 1px dashed #D1D5DB;'>", unsafe_allow_html=True)

        st.sidebar.markdown("---")
        uploaded_csv = st.sidebar.file_uploader("اختر ملف الأضرحة أو المصطلحات الشامل (.csv):", type=["csv"], key="final_uploader")
        if uploaded_csv is not None:
            try:
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
                    elif 'daily_activities' in clean_col: rename_dict[col] = 'daily_activities'
                    elif 'annual_activities' in clean_col: rename_dict[col] = 'annual_activities'
                    elif 'researchers_books' in clean_col: rename_dict[col] = 'researchers_books'
                    elif 'creative_works' in clean_col: rename_dict[col] = 'creative_works'
                    elif 'web_links' in clean_col: rename_dict[col] = 'web_links'
                    elif 'belief_type' in clean_col: rename_dict[col] = 'belief_type'
                    elif 'belief_details' in clean_col: rename_dict[col] = 'belief_details'
                
                df = df.rename(columns=rename_dict)
                required_cols = ['shrine_name', 'shrine_type', 'province', 'exact_location', 'history_details', 'daily_activities', 'annual_activities', 'researchers_books', 'creative_works', 'web_links', 'belief_type', 'belief_details']
                for col in required_cols:
                    if col not in df.columns: df[col] = "غير محدد"
                        
                added_shrine, updated_shrine = 0, 0
                added_term, updated_term = 0, 0
                p_dict = {str(row[1]).strip(): row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
                
                for index, row in df.iterrows():
                    s_name = str(row['shrine_name']).strip()
                    if not s_name or s_name == "nan" or "shrine_name" in s_name: continue
                    tags_val = str(row['tags']).strip() if 'tags' in df.columns and pd.notna(row['tags']) else ''
                    s_type = str(row['shrine_type']).strip() if pd.notna(row['shrine_type']) else 'أضرحة المسلمين'
                    hist_val = str(row['history_details']).strip() if pd.notna(row['history_details']) else 'غير محدد'
                    
                    if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                        existing_term = cursor.execute("SELECT id FROM thesaurus_terms WHERE term=?", (s_name,)).fetchone()
                        if existing_term:
                            cursor.execute("UPDATE thesaurus_terms SET category=?, definition=? WHERE term=?", (s_type, hist_val, s_name))
                            updated_term += 1
                        else:
                            cursor.execute("INSERT INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                            added_term += 1
                    else:
                        prov_name = str(row['province']).strip()
                        if prov_name not in p_dict and prov_name != "nan" and prov_name != "":
                            cursor.execute("INSERT INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                            conn.commit()
                            p_dict = {str(row[1]).strip(): row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
                        
                        if prov_name in p_dict:
                            prov_id = p_dict[prov_name]
                            era_val = str(row['historical_era']).strip() if 'historical_era' in df.columns and pd.notna(row['historical_era']) else 'غير محدد'
                            existing = cursor.execute("SELECT id FROM shrines WHERE name = ? AND province_id = ?", (s_name, prov_id)).fetchone()
                            if existing:
                                cursor.execute("UPDATE shrines SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, creative_works=?, web_links=?, historical_era=?, tags=?, latitude=?, longitude=? WHERE id=?", (s_type, str(row['exact_location']), hist_val, str(row['daily_activities']), str(row['annual_activities']), str(row['researchers_books']), str(row['creative_works']), str(row['web_links']), era_val, tags_val, 31.7917, -7.0926, existing[0]))
                                updated_shrine += 1
                                shrine_id = existing[0]
                            else:
                                cursor.execute("INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (s_name, s_type, prov_id, str(row['exact_location']), hist_val, str(row['daily_activities']), str(row['annual_activities']), era_val, tags_val, 31.7917, -7.0926, str(row['researchers_books']), str(row['creative_works']), str(row['web_links'])))
                                added_shrine += 1
                                shrine_id = cursor.lastrowid
                            
                            cursor.execute("DELETE FROM beliefs_and_functions WHERE shrine_id = ?", (shrine_id,))
                            cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, str(row['belief_type']), str(row['belief_details'])))
                
                conn.commit()
                if added_term > 0 or updated_term > 0: st.sidebar.success("📙 تم دمج المصطلحات بنجاح!")
                if added_shrine > 0 or updated_shrine > 0: st.sidebar.success("🕌 تم دمج الأضرحة بنجاح!")
                st.rerun()
            except Exception as e: st.sidebar.error(f"❌ خطأ أثناء الاستيراد الميداني: {e}")
