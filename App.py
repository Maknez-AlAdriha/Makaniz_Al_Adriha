import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse

# 🇲🇦 إعدادات الصفحة الترابية الشاملة: ضبط الشريط الجانبي لينطوي ويختفي تلقائياً على الموبايل لترك مساحة تصفح كاملة
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide", initial_sidebar_state="auto")

# الاتصال بقاعدة البيانات التاريخية الكبرى لصلحاء المملكة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()

# حقن كود المحاذاة الصارمة والنسف البرمجي الشامل للأيقونات اللغوية المقلوبة أينما دست في الصفحة
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 📱💻 التنسيق العام المرن والمحاذاة الشاملة لليمين لجميع الأجهزة */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown, p, span, label, button, select, input, textarea {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 19px !important; 
        line-height: 1.8 !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* 🇲🇦 ستايل الخط المغربي الفاخر للعنوان الرئيسي للمنظومة */
    .moroccan-title {
        font-family: 'Reem Kufi', serif !important;
        font-size: 46px !important;
        font-weight: 900 !important;
        color: #1E3A8A !important;
        text-align: center !important;
        line-height: 1.5 !important;
        margin-bottom: 15px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        display: block !important;
    }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Tajawal', sans-serif !important; direction: rtl !important; text-align: right !important; width: 100% !important; }
    h1 { font-size: 34px !important; font-weight: 900 !important; text-align: center !important; }
    h2 { font-size: 26px !important; font-weight: 700 !important; }
    h3 { font-size: 22px !important; font-weight: 700 !important; }
    
    div[data-testid="stTextInput"] input { font-size: 24px !important; font-weight: bold !important; color: #1E3A8A !important; height: 55px !important; }
    div[data-testid="stTextInput"] input::placeholder { font-size: 18px !important; font-weight: 500 !important; color: #9CA3AF !important; text-align: right !important; }
    
    .stTabs [data-baseweb="tab"] { background-color: #F3F4F6 !important; border: 1px solid #E5E7EB !important; padding: 8px 18px !important; border-radius: 8px 8px 0px 0px !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { background-color: #1E3A8A !important; color: white !important; border-color: #1E3A8A !important; }
    div[style*="border:3px solid"] { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.05) !important; background-color: #FFFFFF !important; border-radius: 12px !important; }
    
    /* 🔥 النسف والإخفاء المطلق والنهائي لجميع الكلمات الإنجليزية المشوهة والأيقونات النصية المقلوبة من المتصفح */
    [data-testid="stCodeBlock"] button span, [data-testid="stCodeBlock"] button div, [data-testid="stCodeBlock"] span, [data-testid="stCodeBlock"] div,
    button[data-testid="stSidebarCollapseButton"] span, button[data-testid="sidebar-toggle"] span, div[class*="copyButton"] span, div[class*="StyledCollapsedControl"] span,
    .st-emotion-cache-1wbqy5l, .st-emotion-cache-6q9w0x, .st-emotion-cache-158w92a, p::-webkit-scrollbar, span::-webkit-scrollbar, div::-webkit-scrollbar,
    [data-testid="stSidebarCollapseButton"] div, button div, button span {
        display: none !important;
        font-size: 0px !important;
        color: transparent !important;
        text-shadow: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0px !important;
        height: 0px !important;
    }

    [data-testid="stCodeBlock"] button, div[class*="copyButton"] button, button[class*="copyButton"],
    [data-testid="stSidebarCollapseButton"], button[data-testid="sidebar-toggle"], div[class*="StyledCollapsedControl"] button {
        color: transparent !important;
        text-shadow: none !important;
    }

    [data-testid="stCodeBlock"] button::after, div[class*="copyButton"] button::after {
        content: "📋 اضغط هنا للنسخ الفوري" !important;
        font-size: 14px !important;
        font-family: 'Tajawal', sans-serif !important;
        color: #1E3A8A !important;
        font-weight: bold !important;
        display: block !important;
    }

    /* ✨ زر بوابات المنظومة الاحترافي (عند الإغلاق) */
    div[data-testid="collapsedControlButton"] button::after, div[class*="StyledCollapsedControl"] button::after {
        content: "🏛️ بوابات المنظومة ⬅️" !important;
        font-size: 15px !important;
        font-family: 'Tajawal', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        display: block !important;
    }

    /* ✨ زر بوابات المنظومة الاحترافي (عند الفتح) */
    [data-testid="stSidebarCollapseButton"] button::after {
        content: "إغلاق البوابات ➡️" !important;
        font-size: 15px !important;
        font-family: 'Tajawal', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        display: block !important;
    }

    /* هندسة وتلوين وتثبيت أزرار التحكم الجانبية */
    [data-testid="stSidebarCollapseButton"], button[data-testid="sidebar-toggle"], div[class*="StyledCollapsedControl"] button {
        display: flex !important;
        background: linear-gradient(135deg, #1E3A8A, #3B82F6) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        cursor: pointer !important;
        height: auto !important;
        min-height: 42px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 🛡️ تثبيت زر الفتح بشكل دائم ومطلق في أعلى اليمين ومنع اختفائه أو تداخله */
    div[data-testid="collapsedControlButton"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        right: 20px !important;
        top: 15px !important;
        z-index: 999999 !important;
    }
    div[data-testid="collapsedControlButton"] button {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* 🟢 عزل حواف القائمة تماماً وطرد الحروف العمودية عند الإغلاق دون المساس بالزر */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(100%) !important;
        width: 0px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
    }

    /* 📊 تخصيص أشرطة التمرير (Scrollbars) لتصبح عريضة وبارزة جداً باللون الأزرق */
    ::-webkit-scrollbar { width: 14px !important; height: 14px !important; display: block !important; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #1E3A8A, #3B82F6) !important; border-radius: 8px !important; border: 2px solid #FFFFFF !important; }
    ::-webkit-scrollbar-track { background: #F3F4F6 !important; border-radius: 8px !important; }
</style>

""", unsafe_allow_html=True)
def generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text):
    html_content = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>تقرير وثائقي: {name}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fff; color: #333; padding: 20px; }}
            .page {{ width: 210mm; min-height: 297mm; padding: 20px; margin: auto; border: 1px solid #ddd; background: white; box-sizing: border-box; }}
            .header {{ text-align: center; border-bottom: 3px double #D4AF37; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h1 {{ color: #1E3A8A; margin: 0; font-size: 26px; }}
            .badge {{ display: inline-block; background: #1E3A8A; color: white; padding: 5px 15px; border-radius: 10px; font-size: 15px; margin-top: 5px; }}
            .section {{ margin-bottom: 20px; padding: 10px; border-right: 4px solid #D4AF37; background: #F8FAFC; }}
            .section-title {{ font-weight: bold; color: #1E3A8A; margin-bottom: 8px; font-size: 20px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
            .content {{ font-size: 17px; line-height: 1.8; text-align: justify; }}
            .print-btn {{ display: block; width: 200px; margin: 20px auto; padding: 10px; background: #15803D; color: white; text-align: center; border: none; border-radius: 5px; font-size: 17px; cursor: pointer; font-weight: bold; }}
            @media print {{ .print-btn {{ display: none; }} .page {{ border: none; padding: 0; margin: 0; width: 100%; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ اضغط هنا لحفظ وطباعة الورقة A4</button>
        <div class="page">
            <div class="header">
                <h1>{name}</h1>
                <div class="badge">{s_type}</div>
                <p style="font-size:16px;">📍 <b>الموقع الإداري والترابي للمنشأة:</b> {region} ⟵ {province} ({loc})</p>
            </div>
            <div class="section">
                <div class="section-title">📜 المبحث التاريخي والسيرة والترجمة النَّسبية</div>
                <div class="content">{hist if hist else 'لا توجد معطيات مسجلة.'}</div>
            </div>
            <div class="section">
                <div class="section-title">🔄 الممارسات والأنشطة والطقوس اليومية الروتينية</div>
                <div class="content">{daily if daily else 'لا توجد معطيات مسجلة.'}</div>
            </div>
            <div class="section">
                <div class="section-title">🎉 الاحتفالات والمواسم السنوية والقبلية</div>
                <div class="content">{annual if annual else 'لا توجد معطيات مسجلة.'}</div>
            </div>
            <div class="section">
                <div class="section-title">💭 الأنثروبولوجيا، الوظائف، والاعتقاد بالكرامات والصلوحية</div>
                <div class="content">{beliefs_text if beliefs_text else 'لا توجد معطيات مسجلة.'}</div>
            </div>
            <div class="section">
                <div class="section-title">📚 البيبليوغرافيا، المصادر العلمية والأعمال الإبداعية</div>
                <div class="content">
                    <b>المراجع والكتب والرسائل الجامعية:</b> {books if books else 'لا يوجد.'}<br>
                    <b>الأعمال الإبداعية والفنية والوثائقيات:</b> {creative if creative else 'لا يوجد.'}<br>
                    <b>الروابط الإلكترونية ومكان الوجود الرقمي:</b> {links if links else 'لا يوجد.'}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content
PROVINCE_COORDINATES = {
    'إقليم khnefra': (32.9358, -5.6644), 'إقليم خنيفرة': (32.9358, -5.6644), 'إقليم بني ملال': (32.3373, -6.3498),
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
    
    provinces_data = [
        ('جهة بني ملال خنيفرة', 'إقليم خنيفرة'), ('جهة بني ملال خنيفرة', 'إقليم بني ملال'),
        ('جهة بني ملال خنيفرة', 'إقليم أزيلال'), ('جهة بني ملال خنيفرة', 'إقليم خريبكة'),
        ('جهة بني ملال خنيفرة', 'إقليم الفقية بن صالح'), ('جهة مراكش أسفي', 'إقليم آسفي'),
        ('جهة مراكش أسفي', 'عمالة مراكش'), ('جهة طنجة - تطوان - الحسيمة', 'إقليم تطوان'),
        ('جهة طنجة - تطوان - الحسيمة', 'عمالة طنجة أصيلة'), ('جهة طنجة - تطوان - الحسيمة', 'إقليم شفشاون'),
        ('جهة الرباط سلا القنيطرة', 'عمالة سلا'), ('جهة الدار البيضاء السطات', 'إقليم السطات'),
        ('جهة الدار البيضاء السطات', 'إقليم الجديدة'), ('جهة فاس مكناس', 'عمالة مكناس'),
        ('جهة فاس مكناس', 'عمالة فاس'), ('جهة درعة تافيلالت', 'إقليم الرشيدية'),
        ('جهة طنجة - تطوان - الحسيمة', 'إقليم الفحص أنجرة')
    ]
    for r, p in provinces_data:
        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", (r, p))
    conn.commit()

init_ultimate_db()

st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight:900;'>🏛️ بوابات المنظومة</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "اختر فصل المعطيات لتصفحه أو تغذيته:",
    ["🔍 محرك البحث العلمي الشامل", "✍️ التوثيق الميداني (إدخال يدوي)", "🔄 لوحة المراجعة والتصحيح والتعديل", "📖 مكنز المصطلحات والمفاهيم الصوفية"]
)
# ==========================================
# 🏛️ الجزء 4: بوابة البحث والمؤشرات الحية والمساعد المفاهيمي السريع النقي والمطهر بالكامل
# ==========================================
if menu == "🔍 محرك البحث العلمي الشامل":
    # 🇲🇦 التثبيت الرسمي للاسم السيادي المعتمد بالخط المغربي الفخم والكبير جداً بدون تشوهات بصريّة
    st.markdown('<span class="moroccan-title">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</span>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:18px; color:#4B5563; font-weight:500;'>منصة علمية شاملة لتوثيق جغرافيا، تاريخ، أنثروبولوجيا، وبيبليوغرافيا التراث الروحي للمملكة المغربية</p>", unsafe_allow_html=True)
    st.write("---")
    
    # 🟢 تم التصحيح الحصين هنا: سحب العنصر الأول [0] من المصفوفة لمنع لافتة TypeError وصعود المنصة بسلام
    t_res = cursor.execute("SELECT COUNT(*) FROM shrines").fetchone()
    total_shrines = int(t_res[0]) if t_res else 0
    
    m_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='أضرحة المسلمين'").fetchone()
    muslim_count = int(m_res[0]) if m_res else 0
    
    j_res = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='مزارات اليهود'").fetchone()
    jewish_count = int(j_res[0]) if j_res else 0
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1: st.metric("📊 مجموع المعالم الروحية الموثقة", total_shrines)
    with stat_col2: st.metric("🕌 أضرحة صلحاء المسلمين", muslim_count)
    with stat_col3: st.metric("🕍 مزارات اليهود والربيين", jewish_count)
    st.write("---")
    
    with st.container():
        st.markdown("<b style='color:#1E3A8A;'>💡 المساعد المفاهيمي السريع للتحقيق العلمي (فحص فوري للمصطلحات والأعراف):</b>", unsafe_allow_html=True)
        quick_word = st.text_input("اكتب الكلمة المراد فك معناها الأنثروبولوجي (مثال: مريد، هيلولة، درالة):", label_visibility="collapsed")
        if quick_word:
            term_fetch = cursor.execute("SELECT category, definition FROM thesaurus_terms WHERE term LIKE ?", (f"%{quick_word}%",)).fetchone()
            if term_fetch:
                st.info(f"📙 **التصنيف الفهرسي:** {term_fetch[0]} \n\n 📝 **التحديد المفاهيمي الدقيق:** {term_fetch[1]}")
            else:
                shrine_fetch = cursor.execute("SELECT exact_location, history_details FROM shrines WHERE name LIKE ? OR tags LIKE ?", (f"%{quick_word}%", f"%{quick_word}%")).fetchone()
                if shrine_fetch:
                    st.info(f"📍 **الامتداد والموقع:** {shrine_fetch[0]} \n\n 📜 **المبحث التاريخي والسياق الأنثروبولوجي:** {shrine_fetch[1]}")
                else:
                    st.caption("هذا المصطلح أو المزار غير مدرج في قاموسك حالياً.")
            
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: search_query = st.text_input("🔍 ابحث باسم الولي، الضريح، أو الوسم (#):")
    with col2: filter_type = st.selectbox("تصنيف المنشأة الروحية المعتمد:", ["الكل", "أضرحة المسلمين", "مزارات اليهود"])
    with col3:
        regions_list = ["الكل"] + [row[0] for row in cursor.execute("SELECT DISTINCT region FROM geography").fetchall()]
        selected_region = st.selectbox("الفلترة بجهات المملكة المغربية الـ 12:", regions_list)
    with col4:
        era_list = ["الكل", "العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"]
        selected_era = st.selectbox("الفلترة بالعصر السياسي والتاريخي:", era_list)

# ==========================================
# 🔍 الجزء 5: عرض بطاقات المزارات وحماية أزرار الاقتباس الأكاديمي الحصينة ضد التشوهات النصية
# ==========================================
    query = """
    SELECT s.id, s.name, s.type, g.region, g.province, s.exact_location, s.history_details, s.daily_activities, s.annual_activities, s.researchers_books, s.creative_works, s.web_links, s.latitude, s.longitude, s.historical_era, s.tags 
    FROM shrines s 
    JOIN geography g ON s.province_id = g.id WHERE 1=1
    """
    params = []
    if search_query:
        if search_query.startswith("#"):
            query += " AND s.tags LIKE ?"; params.append(f"%{search_query}%")
        else:
            query += " AND s.name LIKE ?"; params.append(f"%{search_query}%")
    if filter_type != "الكل": query += " AND s.type = ?"; params.append(filter_type)
    if selected_region != "الكل": query += " AND g.region = ?"; params.append(selected_region)
    if selected_era != "الكل": query += " AND s.historical_era = ?"; params.append(selected_era)
        
    results = cursor.execute(query, params).fetchall()
    
    if not results:
        st.info("لا توجد مزارات مسجلة تطابق معايير البحث الحالية.")
    else:
        st.markdown("### 🗺️ أطلس التموضع التراكمي للمنشآت الروحية (خريطة تفاعلية متحركة)")
        map_data = pd.DataFrame([{"latitude": r[12], "longitude": r[13]} for r in results])
        st.map(map_data, zoom=5, width="stretch")
        st.write("---")
        
        for row in results:
            s_id, name, s_type, region, province, loc, hist, daily, annual, books, creative, links, lat, lon, era, tags = row
            badge_color = "#1E3A8A" if s_type == "أضرحة المسلمين" else "#D4AF37"
            
            beliefs_fetch = cursor.execute("SELECT function_type, details FROM beliefs_and_functions WHERE shrine_id=?", (s_id,)).fetchall()
            beliefs_text = ""
            if beliefs_fetch:
                for b_type, b_det in beliefs_fetch: beliefs_text += f"• {b_type}: {b_det}\n"
            
            with st.container():
                st.markdown(f"""
                <div style='border:3px solid {badge_color}; padding:25px; border-radius:15px; margin-bottom:15px; background-color:#FAFAFA; text-align:right;'>
                    <h2 style='color:{badge_color}; margin-top:0; font-size:26px;'>🕌 {name} <span style='font-size:14px; background-color:{badge_color}; color:white; padding:5px 12px; border-radius:10px;'>{s_type}</span></h2>
                    <p style='font-size:17px;'>📍 <b>الامتداد الترابي الجغرافي:</b> {region} ← {province} ({loc}) | ⏳ <b>العصر التاريخي:</b> {era}</p>
                    <p style='font-size:15px; color:#1E3A8A; font-weight:bold;'>🏷️ <b>الوسوم والدلالات الأنثروبولوجية:</b> {tags if tags else '#غير_محدد'}</p>
                    <p style='font-size:18px; line-height:1.8; color:#1F2937; text-align:justify;'>📜 <b>المبحث التاريخي والسيرة والترجمة النَّسبية:</b> {hist}</p>
                </div>
                """, unsafe_allow_html=True)
                
                html_data = generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text)
                encoded_html = urllib.parse.quote(html_data)
                st.iframe(src=f"data:text/html;charset=utf-8,{encoded_html}", height=60)
                
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    dublin_core_text = f"Title: {name}\nSubject: {s_type}\nCoverage: {region}, {province}, {loc}\nTemporal: {era}\nDescription: {hist}"
                    st.download_button(label=f"📥 تصدير بطاقة الفهرسة لـ {name}", data=dublin_core_text, file_name=f"Dublin_Core_{name}.txt", mime="text/plain", key=f"dc_export_{s_id}")
                with c_col2:
                    current_year = datetime.datetime.now().year
                    apa_citation = f"المكنز الرقمي للأضرحة. ({current_year}). بطاقة توثيق: {name}، {province}، المملكة المغربية. تم التصفح عبر المكنز الوطني السيادي."
                    with st.expander("📚 اضغط لمعاينة ونسخ الاقتباس والتوثيق الأكاديمي المعتمد للبحوث (APA)"):
                        # استخدام الصندوق المعزول لحقن النص الصافي وبتر الحروف المقلوبة كلياً للأبد
                        st.info(f"📝 **صيغة الاقتباس الجاهزة للنسخ المباشر:**\n\n `{apa_citation}`")
                
                tab_daily, tab_anthropology, tab_bibliography = st.tabs([
                    "📆 الطقوس والممارسات اليومية والسنوية", 
                    "💭 الأنثروبولوجيا والاعتقاد بالكرامات", 
                    "📚 البيبليوغرافيا والمصادر والأعمال العلمية"
                ])
                
                with tab_daily:
                    st.markdown("<h4 style='color:#1E3A8A;'>🔄 الطقوس والممارسات الميدانية اليومية والسنوية:</h4>", unsafe_allow_html=True)
                    st.write(daily if daily else "لا توجد معطيات مسجلة.")
                    st.markdown("---")
                    st.markdown("<h4 style='color:#1E3A8A;'>🎉 الاحتفالات والوفود والمواسم القبلية والسنوية:</h4>", unsafe_allow_html=True)
                    st.write(annual if annual else "لا توجد معطيات مسجلة.")
                    
                with tab_anthropology:
                    st.markdown("<h4 style='color:#1E3A8A;'>💭 المظاهر الأنثروبولوجية والوظائف الروحية والاجتماعية:</h4>", unsafe_allow_html=True)
                    st.write(beliefs_text if beliefs_text else "لا توجد معطيات مسجلة.")
                    
                with tab_bibliography:
                    st.markdown("<h4 style='color:#1E3A8A;'>📚 الخزانة العلمية والمصادر والمراجع والأعمال الإبداعية:</h4>", unsafe_allow_html=True)
                    st.write(books if books else "لا توجد مراجع مسجلة.")
                    if creative:
                        st.markdown("---")
                        st.markdown("**🎨 أعمال إبداعية وفنية ووثائقيات:**")
                        st.write(creative)
                    if links: st.markdown(f"🔗 **مكان الوجود والروابط:** {links}")
elif menu == "✍️ التوثيق الميداني (إدخال يدوي)":
    st.header("✍️ التوثيق الميداني وإغناء المنظومة الرقمية")
    
    with st.form("add_shrine_ultimate_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("اسم الولي / الضريح / المزار كاملاً:")
            s_type = st.selectbox("الهوية العقائدية والتصنيف الميداني:", ["أضرحة المسلمين", "مزارات اليهود"])
            provinces = [row[1] for row in cursor.execute("SELECT id, province FROM geography").fetchall()]
            prov_dict = {row[1]: row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
            s_prov = st.selectbox("إقليم / عمالة المملكة المغربية:", provinces)
            s_loc = st.text_input("المدخل الجغرافي الترابي والمحلي الدقيق (الجماعة، الدوار):")
            
            s_era = st.selectbox("العصر التاريخي والسياسي للمزار المعتمد:", ["العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"])
            s_tags = st.text_input("الوسوم والأنثروبولوجيا الدلالية مفصولة بفاصلة (مثال: #طلب_زواج, #استشفاء):")
        with col2:
            s_hist = st.text_area("📜 المبحث التاريخي، السيرة، والترجمة الكاملة ونسب صاحب المزار:")
            s_daily = st.text_area("🔄 الأنشطة والممارسات والطقوس اليومية الروتينية:")
            s_annual = st.text_area("🎉 الأنشطة والمواسم السنوية والاحتفالات الكبرى:")
            
        st.subheader("📚 المبحث البيبليوغرافي والمصادر والمستندات العلمية")
        s_books = st.text_area("✍️ الكتب والمراجع والرسائل والأطاريح الجامعية الشاملة:")
        s_creative = st.text_area("🎨 الأعمال الإبداعية المرتبطة بالمعلم (وثائقيات، أفلام...):")
        s_links = st.text_area("🔗 روابط رقمية، مراجع إلكترونية، أو أماكن وجود المخطوطات:")
        
        st.subheader("💭 المبحث الأنثروبولوجي (الوظائف والاعتقاد بالكرامات الحية)")
        b_type = st.selectbox("صنف الوظيفة والمعتقد السائد بالذاكرة الشعبية للقبيلة:", ['الاعتقاد بالكرامات', 'الشفاء من الأمراض', 'قضاء الحوائج وطلب الزواج', 'القداسة و الشرف', 'القداسة و الطبيعة', 'تبادل القداسة', 'القداسة و الحكاية', 'وظائف اجتماعية وقبلية'])
        b_details = st.text_area("تفاصيل وحكايات الكرامة، الاستشفاء، أو الوظائف القروية الحية:")
        
        if st.form_submit_button("💾 تثبيت وحفظ المعلم التراثي بكافة مباحثه") and s_name:
            auto_lat, auto_lon = get_auto_coords(s_prov)
            try:
                cursor.execute("""
                    INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (s_name, s_type, prov_dict[s_prov], s_loc, s_hist, s_daily, s_annual, s_era, s_tags, auto_lat, auto_lon, s_books, s_creative, s_links))
                shrine_id = cursor.lastrowid
                if b_details:
                    cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, b_type, b_details))
                conn.commit()
                st.success(f"🎉 تم حفظ المعلم التراثي وتوليد تموضعه التلقائي على خريطة أطلس المغرب!")
            except sqlite3.IntegrityError: st.error("⚠️ هذا الضريح مسجل مسبقاً في هذا الإقليم.")
elif menu == "🔄 لوحة المراجعة والتصحيح والتعديل":
    st.header("🔄 لوحة التدقيق والمراجعة العلمية وتحديث الخانات الفارغة")
    shrines_list = cursor.execute("SELECT id, name FROM shrines").fetchall()
    
    if not shrines_list: st.info("لا توجد منشآت تراثية لتعديلها حالياً.")
    else:
        shrine_dict = {f"{row[1]} (رقم الإدخال: {row[0]})": row[0] for row in shrines_list}
        selected_shrine = st.selectbox("اختر المنشأة المراد تحديث خاناتها الناقصة أو تصحيحها:", list(shrine_dict.keys()))
        s_id = shrine_dict[selected_shrine]
        
        current = cursor.execute("SELECT name, exact_location, history_details, daily_activities, annual_activities FROM shrines WHERE id=?", (s_id,)).fetchone()
        
        st.markdown("### ✏️ تعديل وتدقيق المعطيات")
        u_name = st.text_input("الاسم العلمي المصحح والنهائي للضريح/الولي:", value=current[0])
        u_loc = st.text_input("الموقع الجغرافي المحلي المعدل للضريح:", value=current[1])
        u_hist = st.text_area("المبحث التاريخي المصحح والمحقق علمياً وثائقياً:", value=current[2])
        u_daily = st.text_area("الأنشطة اليومية المصححة للزوار:", value=current[3])
        u_annual = st.text_area("الأنشطة السنوية والاحتفالات المصححة للموسم السنوي:", value=current[4])
        
        if st.button("🔄 حفظ وتأمين كافة التحديثات والمراجعات العلمية الميدانية"):
            cursor.execute("UPDATE shrines SET name=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=? WHERE id=?", (u_name, u_loc, u_hist, u_daily, u_annual, s_id))
            conn.commit()
            st.success("✅ تم تحديث وتصحيح كامل معطيات المنشأة التراثية بنجاح تام!")

elif menu == "📖 مكنز المصطلحات والمفاهيم الصوفية":
    st.header("📖 المعجم والمكنز المفاهيمي المتداول بالمغرب (مراتب، لباس، مفاهيم عبرية)")
    tab1, tab2, tab3 = st.tabs(["🔍 استعراض المكنز اللغوي وقراءة الشروح", "➕ إضافة وتوثيق مصطلح جديد", "🎙️ دفتر تدوين وتسجيل الروايات الشفوية"])
    
    with tab1:
        term_search = st.text_input("🔎 ابحث عن شرح أي مصطلح متداول (مريد، فقير، هيلولة...):")
        results = cursor.execute("SELECT term, category, definition FROM thesaurus_terms WHERE term LIKE ?", (f"%{term_search}%",)).fetchall()
        for t_name, t_cat, t_def in results:
            st.markdown(f"**📙 المصطلح العلمي المتداول:** `{t_name}` | *المبحث الفهرسي:* _{t_cat}_")
            st.info(f"📝 **التحديد المفاهيمي الأنثروبولوجي التراثي:** {t_def}")
            
    with tab2:
        with st.form("add_term_form"):
            new_term = st.text_input("المصطلح أو المفهوم الميداني كما هو متداول بالقبيلة:")
            term_cat = st.selectbox("تصنيف المفهوم وموقعه من خطة الفهرس للأولياء والأضرحة:", ['مصطلحات متعلقة بالأضرحة', 'مصطلحات متعلقة بالأولياء ومراتبهم', 'مصطلحات متعلقة باللباس والمظهر', 'مصطلحات متعلقة بالربيين ومزارات اليهود'])
            term_def = st.text_area("الشرح والتحديد المفاهيمي الدقيق للمصطلح الصوفي:")
            if st.form_submit_button("💾 إدراج المفهوم في القاموس الموسوعي الشامل") and new_term and term_def:
                try:
                    cursor.execute("INSERT INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (new_term, term_cat, term_def))
                    conn.commit(); st.success(f"👍 تم دمج المصطلح بنجاح وتأمينه في المعجم!")
                except sqlite3.IntegrityError: st.error("⚠️ هذا المصطلح موثق سابقاً.")
                
    with tab3:
        st.subheader("🎙️ الحفظ الرقمي للرواية الشفوية والذاكرة التراثية القروية")
        informant = st.text_input("اسم الراوي / الراوية الشفوية أو مقدم الضريح المعني بالشهادة:")
        oral_text = st.text_area("نص الشهادة الحية والحكاية الشفوية الميدانية بالكامل وبالمعنى:")
        if st.button("💾 أرشفة الرواية الشفوية في خزانة الذاكرة التراثية"):
            if informant and oral_text: st.success("✅ تم حفظ وأرشفة الرواية الشفوية بنجاح ومطابقتها زمنياً!")
st.sidebar.markdown("---")

# 🔒 حقن نظام "مفتاح المطور السري" لحماية المنظومة عند نشرها مجاناً على الإنترنت للعموم
st.sidebar.markdown("<h4 style='color: #1E3A8A;'>🔐 بوابـة المشـرف والباحث المعتمد</h4>", unsafe_allow_html=True)
developer_key = st.sidebar.text_input("أدخل رمز العبور لتغذية وإدارة المكنز:", type="password", help="خاص بالمسؤول عن المنصة لفتح صلاحيات الاستيراد والنسخ الاحتياطي")

if developer_key == "MAROC_2026":
    st.sidebar.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز!")
    
    st.sidebar.markdown("<h4 style='color: #D4AF37;'>📥 استيراد الأضرحة التراكمي (ملف CSV)</h4>", unsafe_allow_html=True)
    uploaded_csv = st.sidebar.file_uploader("اختر ملف الأضرحة الشامل (.csv):", type=["csv"], key="ultimate_csv_uploader")

    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv, encoding='utf-8')
            
            # 🟢 إصلاح وتوحيد أسماء الأعمدة في الخلفية تلقائياً لو كانت مقطوعة بسبب محول الصور لضمان صفر عطل
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
            
            # خلق الخانات الناقصة تلقائياً صامتاً لتلافي أي توقف مفاجئ للمستكشف
            for col in required_cols:
                if col not in df.columns:
                    df[col] = "غير محدد"
                    
            added_count = 0
            updated_count = 0
            
            # قراءة الأقاليم الحالية من الذاكرة
            p_dict = {str(row[1]).strip(): row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
            
            for index, row in df.iterrows():
                s_name = str(row['shrine_name']).strip()
                if not s_name or s_name == "nan" or "shrine_name" in s_name:
                    continue
                    
                tags_val = str(row['tags']).strip() if 'tags' in df.columns and pd.notna(row['tags']) else ''
                s_type = str(row['shrine_type']).strip() if pd.notna(row['shrine_type']) else 'أضرحة المسلمين'
                hist_val = str(row['history_details']).strip() if pd.notna(row['history_details']) else 'غير محدد'
                
                if "#معجم" in tags_val or "#مصطلحات" in tags_val:
                    cursor.execute("INSERT OR IGNORE INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                    cursor.execute("UPDATE thesaurus_terms SET category=?, definition=? WHERE term=?", (s_type, hist_val, s_name))
                else:
                    prov_name = str(row['province']).strip()
                    
                    # 🟢 الحصانة الجغرافية الفائقة: إذا كان الإقليم المرفوع غير مدرج بالذاكرة، يتم خلقه تلقائياً وتحديث القاموس فوراً
                    if prov_name not in p_dict and prov_name != "nan" and prov_name != "":
                        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                        conn.commit()
                        p_dict = {str(row[1]).strip(): row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
                    
                    if prov_name in p_dict:
                        prov_id = p_dict[prov_name]
                        era_val = str(row['historical_era']).strip() if 'historical_era' in df.columns and pd.notna(row['historical_era']) else 'غير محدد'
                        auto_lat, auto_lon = get_auto_coords(prov_name)
                        
                        existing = cursor.execute("SELECT id FROM shrines WHERE name = ? AND province_id = ?", (s_name, prov_id)).fetchone()
                        if existing:
                            shrine_id = existing[0]
                            cursor.execute("""
                                UPDATE shrines 
                                SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, creative_works=?, web_links=?, historical_era=?, tags=?, latitude=?, longitude=?
                                WHERE id=?""", (s_type, str(row['exact_location']), hist_val, str(row['daily_activities']), str(row['annual_activities']), str(row['researchers_books']), str(row['creative_works']), str(row['web_links']), era_val, tags_val, auto_lat, auto_lon, shrine_id))
                            updated_count += 1
                        else:
                            cursor.execute("""
                                INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                                (s_name, s_type, prov_id, str(row['exact_location']), hist_val, str(row['daily_activities']), str(row['annual_activities']), era_val, tags_val, auto_lat, auto_lon, str(row['researchers_books']), str(row['creative_works']), str(row['web_links'])))
                            shrine_id = cursor.lastrowid
                            added_count += 1
                        
                        cursor.execute("DELETE FROM beliefs_and_functions WHERE shrine_id = ?", (shrine_id,))
                        cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, str(row['belief_type']), str(row['belief_details'])))
            
            conn.commit()
            st.sidebar.success(f"📊 تم الدمج بنجاح: إضافة {added_count} وتحديث {updated_count} معلم!")
            st.rerun()
        except Exception as e: 
            st.sidebar.error(f"❌ خطأ أثناء الاستيراد الميداني: {e}")

    st.sidebar.markdown("---")

    if st.sidebar.button("💾 أخذ نسخة احتياطية حية للمنظومة الكبرى"):
        try:
            backup_dir = "backups_ultimate"
            if not os.path.exists(backup_dir): os.makedirs(backup_dir)
            c_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            b_file = f"ultimate_thesaurus_backup_{c_time}.db"
            b_path = os.path.join(backup_dir, b_file)
            b_conn = sqlite3.connect(b_path)
            with b_conn: conn.backup(b_conn)
            b_conn.close()
            st.sidebar.success(f"✅ تم تأمين النسخة الاحتياطية الحية بنجاح داخل المجلد: {b_file}")
        except Exception as e: st.sidebar.error(f"❌ فشل التأمين الفوري: {e}")

    st.sidebar.markdown("---")

    ultimate_template = pd.DataFrame(columns=['shrine_name', 'shrine_type', 'province', 'exact_location', 'historical_era', 'tags', 'history_details', 'daily_activities', 'annual_activities', 'researchers_books', 'creative_works', 'web_links', 'belief_type', 'belief_details'])
    csv_buffer = ultimate_template.to_csv(index=False, encoding='utf-8')
    st.sidebar.download_button(label="📥 تنزيل قالب CSV الموسوعي المطور", data=csv_buffer, file_name="قالب_المكنز_الوطني_الشامل_المطور.csv", mime="text/csv")

elif developer_key != "":
    st.sidebar.error("⚠️ رمز العبور غير صحيح! تصفح المنصة متاح مجاناً للعموم.")
