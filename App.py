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
# حقن كود المحاذاة الصارمة وتنسيق الواجهات لتعمل بمرونة وحركة فائقة السرعة بدون تشنج
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* التنسيق العام لليمين للحاويات العربية مع السماح بالمرونة للأقسام الأجنبية */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown, p, span, label, button, select, input, textarea {
            font-family: 'Tajawal', sans-serif !important;
            font-size: 19px !important; 
            line-height: 1.8 !important;
            direction: rtl;
            text-align: right;
        }
        
        /* تحسين انسيابية الحاويات العلوية لمنع تجمد الشاشة وحجب المحتوى السفلي */
        div[data-testid="stVerticalBlock"] {
            gap: 1.5rem !important;
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
            <div class="section"><div class="section-title">📚 المراجع والمصادر</div><p>{books}<br>{creative}<br>{links}</p></div>
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

# 1. حقن وعرض البانر الأفقي الفخم في أعلى المنصة
banner_path = "banner.png"
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.markdown('<span class="moroccan-title">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</span>', unsafe_allow_html=True)

# 2. رسم صف الأزرار العليا التفاعلية الثلاثة بانسيابية تامة لفك التشنج
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

# 3. سحب المؤشرات الإحصائية الأربعة الصافية من الجداول وعرضها بنسق هندسي مرن
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

# توجيه التنقل البرمجي السليم بناءً على تصفح المستخدم
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
if menu == "🔍 محرك البحث العلمي الشامل":
    with st.container():
        st.markdown("<b style='color:#1E3A8A;'>💡 المساعد المفاهيمي السريع للتحقيق العلمي (فحص فوري للمصطلحات والأعراف):</b>", unsafe_allow_html=True)
        quick_word = st.text_input("اكتب الكلمة المراد فك معناها الأنثروبولوجي (مثال: مريد، هيلولة...):", label_visibility="collapsed")
        if quick_word:
            term_fetch = cursor.execute("SELECT category, definition FROM thesaurus_terms WHERE term LIKE ?", (f"%{quick_word}%",)).fetchone()
            if term_fetch: st.info(f"📙 **التصنيف:** {term_fetch[0]} \n\n 📝 **الشرح:** {term_fetch[1]}")
            else:
                shrine_fetch = cursor.execute("SELECT exact_location, history_details FROM shrines WHERE name LIKE ?", (f"%{quick_word}%",)).fetchone()
                if shrine_fetch: st.info(f"📍 **الموقع:** {shrine_fetch[0]} \n\n 📜 **المبحث التاريخي:** {shrine_fetch[1]}")
                else: st.caption("المصطلح غير مدرج حالياً.")
                
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
    if menu == "🔍 محرك البحث العلمي الشامل":
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
            map_list = []
            for r in results:
                try:
                    lat_val = float(r[12]) if r[12] is not None else 31.7917
                    lon_val = float(r[13]) if r[13] is not None else -7.0926
                    map_list.append({"latitude": lat_val, "longitude": lon_val})
                except Exception:
                    map_list.append({"latitude": 31.7917, "longitude": -7.0926})
            
            if map_list: st.map(pd.DataFrame(map_list), zoom=5, use_container_width=True)
            st.write("---")
            
            for row in results:
                s_id, name, s_type, region, province, loc, hist, daily, annual, books, creative, links, lat, lon, era, tags = row
                badge_color = "#1E3A8A" if s_type == "أضرحة المسلمين" else "#D4AF37"
                
                beliefs_fetch = cursor.execute("SELECT function_type, details FROM beliefs_and_functions WHERE shrine_id=?", (s_id,)).fetchall()
                beliefs_text = ""
                if beliefs_fetch:
                    for b_type, b_det in beliefs_fetch: beliefs_text += f"• {b_type}: {b_det}\n"
                
                st.markdown(f"""
                <div style='border:3px solid {badge_color}; padding:25px; border-radius:15px; margin-bottom:15px; background-color:#FAFAFA; text-align:right;'>
                    <h2 style='color:{badge_color}; margin-top:0; font-size:26px;'>🕌 {name} <span style='font-size:14px; background-color:{badge_color}; color:white; padding:5px 12px; border-radius:10px;'>{s_type}</span></h2>
                    <p style='font-size:17px;'>📍 <b>الامتداد الجغرافي:</b> {region} ← {province} ({loc}) | ⏳ <b>العصر:</b> {era}</p>
                    <p style='font-size:15px; color:#1E3A8A; font-weight:bold;'>🏷️ <b>الوسوم:</b> {tags if tags else '#غير_محدد'}</p>
                    <p style='font-size:18px; line-height:1.8; color:#1F2937; text-align:justify;'>📜 <b>المبحث التاريخي والسيرة:</b> {hist}</p>
                </div>
                """, unsafe_allow_html=True)
                
                html_data = generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text)
                encoded_html = urllib.parse.quote(html_data)
                st.iframe(src=f"data:text/html;charset=utf-8,{encoded_html}", height=60)
                
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    dublin_core_text = f"Title: {name}\nSubject: {s_type}\nCoverage: {region}, {province}, {loc}"
                    st.download_button(label=f"📥 تصدير بطاقة لـ {name}", data=dublin_core_text, file_name=f"Dublin_{name}.txt", mime="text/plain", key=f"dc_export_{s_id}")
                with c_col2:
                    current_year = datetime.datetime.now().year
                    apa_citation = f"المكنز الرقمي للأضرحة. ({current_year}). بطاقة توثيق: {name}، {province}، المملكة المغربية."
                    st.markdown(f"""
                    <div style='background-color:#EFF6FF; border-right:4px solid #1E3A8A; padding:15px; border-radius:8px; text-align:right; font-size:16px; color:#1E3A8A;'>
                        <b>📚 التوثيق والاقتباس (APA):</b> <code>{apa_citation}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                tab_daily, tab_anthropology, tab_bibliography = st.tabs(["📆 الطقوس والممارسات", "💭 الأنثروبولوجيا والكرامات", "📚 الخزانة والمصادر"])
                with tab_daily:
                    st.write(daily if daily else "لا توجد معطيات مسجلة.")
                    st.markdown("---")
                    st.write(annual if annual else "لا توجد معطيات مسجلة.")
                with tab_anthropology: st.write(beliefs_text if beliefs_text else "لا توجد معطيات مسجلة.")
                with tab_bibliography:
                    st.write(books if books else "لا توجد مراجع مسجلة.")
                    if creative: st.write(creative)
                    if links: st.markdown(f"🔗 **الروابط:** {links}")
elif menu == "✍️ التوثيق الميداني (إدخال يدوي)":
    st.header("✍️ التوثيق الميداني وإغناء المنظومة الرقمية")
    
    with st.form("add_shrine_ultimate_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("اسم الولي / الضريح / المزار كاملاً:")
            s_type = st.selectbox("الهوية العقائدية والتصنيف الميداني:", ["أضرحة المسلمين", "مزارات اليهود"])
            provinces = [row[0] for row in cursor.execute("SELECT province FROM geography").fetchall()]
            prov_dict = {row[1]: row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
            s_prov = st.selectbox("إقليم / عمالة المملكة المغربية:", provinces) if provinces else st.selectbox("إقليم / عمالة المملكة المغربية:", ["إقليم شفشاون"])
            s_loc = st.text_input("المدخل الجغرافي الترابي والمحلي الدقيق (الجماعة، الدوار):")
            s_era = st.selectbox("العصر التاريخي والسياسي:", ["العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"])
            s_tags = st.text_input("الوسوم والأنثروبولوجيا الدلالية مفصولة بفاصلة:")
        with col2:
            s_hist = st.text_area("📜 المبحث التاريخي والسيرة والنسب الشريف:")
            s_daily = st.text_area("🔄 الأنشطة والممارسات والطقوس اليومية:")
            s_annual = st.text_area("🎉 الأنشطة والمواسم السنوية:")
            
        st.subheader("📚 المبحث البيبليوغرافي والمصادر والمستندات العلمية")
        s_books = st.text_area("✍️ الكتب والمراجع والرسائل والأطاريح الجامعية:")
        s_creative = st.text_area("🎨 الأعمال الإبداعية المرتبطة بالمعلم:")
        s_links = st.text_area("🔗 روابط رقمية، مراجع إلكترونية:")
        
        st.subheader("💭 المبحث الأنثروبولوجي (الوظائف والاعتقاد بالكرامات)")
        b_type = st.selectbox("صنف الوظيفة والمعتقد السائد:", ['الاعتقاد بالكرامات', 'الشفاء من الأمراض', 'قضاء الحوائج وطلب الزواج', 'القداسة و الشرف', 'القداسة و الطبيعة', 'تبادل القداسة', 'وظائف اجتماعية وقبلية'])
        b_details = st.text_area("تفاصيل وحكايات الكرامة أو الوظائف القروية الحية:")
        
        if st.form_submit_button("💾 تثبيت وحفظ المعلم التراثي") and s_name:
            auto_lat, auto_lon = get_auto_coords(s_prov)
            prov_id_val = prov_dict.get(s_prov, 1)
            try:
                cursor.execute("""
                    INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (s_name, s_type, prov_id_val, s_loc, s_hist, s_daily, s_annual, s_era, s_tags, auto_lat, auto_lon, s_books, s_creative, s_links))
                shrine_id = cursor.lastrowid
                if b_details:
                    cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, b_type, b_details))
                conn.commit()
                st.success(f"🎉 تم حفظ المعلم التراثي بنجاح بكافة مباحثه!")
                st.rerun()
            except sqlite3.IntegrityError: st.error("⚠️ هذا الضريح مسجل مسبقاً في هذا الإقليم.")
elif menu == "🔄 لوحة المراجعة والتصحيح والتعديل":
    st.header("🔄 لوحة التدقيق والمراجعة العلمية وتحديث الخانات الفارغة")
    shrines_list = cursor.execute("SELECT id, name FROM shrines").fetchall()
    
    if not shrines_list: st.info("لا توجد منشآت تراثية لتعديلها حالياً.")
    else:
        shrine_dict = {f"{row[1]} (رقم: {row[0]})": row[0] for row in shrines_list}
        selected_shrine = st.selectbox("اختر المنشأة المراد تحديث خاناتها:", list(shrine_dict.keys()))
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
            term_cat = st.selectbox("تصنيف المفهوم وموقعه من خطة الفهرس للصلحاء والأضرحة:", ['مصطلحات متعلقة بالأضرحة', 'مصطلحات متعلقة بالأولياء ومراتبهم', 'مصطلحات متعلقة باللباس والمظهر', 'مصطلحات متعلقة بالربيين ومزارات اليهود'])
            term_def = st.text_area("الشرح والتحديد المفاهيمي الدقيق للمصطلح الصوفي:")
            if st.form_submit_button("💾 إدراج المفهوم في القاموس الموسوعي الشامل") and new_term and term_def:
                try:
                    cursor.execute("INSERT INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (new_term, term_cat, term_def))
                    conn.commit(); st.success(f"👍 تم دمج المصطلح بنجاح وتأمينه في المعجم!")
                    st.rerun()
                except sqlite3.IntegrityError: st.error("⚠️ هذا المصطلح موثق سابقاً.")
                
    with tab3:
        st.subheader("🎙️ الحفظ الرقمي للرواية الشفوية والذاكرة التراثية القروية")
        informant = st.text_input("اسم الراوي / الراوية الشفوية أو مقدم الضريح المعني بالشهادة:")
        oral_text = st.text_area("نص الشهادة الحية والحكاية الشفوية الميدانية بالكامل وبالمعنى:")
        if st.button("💾 أرشفة الرواية الشفوية في خزانة الذاكرة التراثية"):
            if informant and oral_text: st.success("✅ تم حفظ وأرشفة الرواية الشفوية بنجاح ومطابقتها زمنياً!")
if menu == "🎓 حول المكنز الأكاديمي":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFDF6, #F9F5E8); border: 3px double #D4AF37; padding: 35px; border-radius: 15px; text-align: center; margin-bottom: 25px;'>
        <h2 style='color: #1E3A8A; font-family: "Reem Kufi", serif; font-size: 32px; margin-top: 0;'>🎓 لوحة الشرف والتعريف الأكاديمي بالمنصة الرقمية</h2>
        <p style='font-size: 20px; color: #1F2937; line-height: 1.8; font-weight: 500;'>
            إن هذا البرنامج التراثي السيادي المتقدم هو ثمرة حية وتحويل رقمي متكامل لأطروحة نُوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.
        </p>
        <div style='background-color: #1E3A8A; color: white; padding: 10px 25px; display: inline-block; border-radius: 8px; font-weight: bold; font-size: 20px; margin: 15px auto;'>
            👨‍🎓 الباحث الدكتور: رشيد الجانبي
        </div>
        <p style='font-size: 18px; color: #4B5563; font-weight: bold; margin-bottom: 5px;'>🏛️ المضمون المؤسسي للأطروحة:</p>
        <p style='font-size: 17px; color: #1F2937; margin-top: 0;'>
            <b>جامعة ابن طفيل (القنيطرة)</b> — مركز دراسات الدكتوراه — كلية اللغات والآداب والفنون<br>
            <b>موضوع الأطروحة:</b> رقمنة التراث الشعبي المغربي "الأضرحة والمزارات" نموذجاً (السنة الجامعية: 2022/2023م).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_ar, tab_fr, tab_en = st.tabs(["🇲🇦 النبذة (العربية)", "🇫🇷 Résumé (Français)", "🇬🇧 Abstract (English)"])
    with tab_ar:
        st.markdown("<div style='background-color:#FAFAFA; padding:25px; border-right:5px solid #1E3A8A; border-radius:8px; text-align:justify;'><p style='font-size:18px; color:#1F2937;'>يكتسي التراث أهمية كبيرة في حياة الأمم والشعوب؛ فهو كاشف لعمقها الحضاري... تبرز أهمية هذه الأطروحة والدراسة العلمية والميدانية لرقمنة التراث الشعبي من خلال مكنز رقمي ذكي للمساجد والمزارات الدينية لتوفير قاعدة بيانات حيوية فائقة الدقة تخدم متطلبات البحث الأنثروبولوجي والتأريخي وعمارة المعالم التراثية الوطنية.</p></div>", unsafe_allow_html=True)
    with tab_fr:
        st.markdown("<div class='latin-text' style='background-color:#FAFAFA; padding:25px; border-left:5px solid #10B981; border-radius:8px;'><h3 style='color:#10B981;'>📝 Résumé de l'œuvre :</h3><p style='font-size:17px; color:#1F2937;'>Le patrimoine a une grande importance... C'est dans ce cadre rigoureux que s'inscrit cette thèse doctorale menée par le <b>Dr. RACHID JANEBI</b>, visant à bâtir le premier Thésaurus Numérique National dédié aux mausolées et sanctuaires du Royaume.</p></div>", unsafe_allow_html=True)
    with tab_en:
        st.markdown("<div class='latin-text' style='background-color:#FAFAFA; padding:25px; border-left:5px solid #D4AF37; border-radius:8px;'><h3 style='color:#D4AF37;'>📝 Academic Abstract :</h3><p style='font-size:17px; color:#1F2937;'>Heritage is of great importance... This platform stands as the ultimate technological fruition of the doctoral dissertation by <b>Dr. RACHID JANEBI</b>. It establishes an advanced database that provides an exhaustive list of description or indexing terms.</p></div>", unsafe_allow_html=True)

elif menu == "📬 دفتر التواصل":
    st.header("📬 دفتر التواصل وإرسال الملاحظات والتحقيق العلمي الميداني")
    st.markdown("<p style='font-size:16px; color:#4B5563;'>هل تملك تصحيحاً، رواية شفوية، أو مراجع إضافية لإغناء هذا المعلم التراثي؟ أرسل ملاحظتك سراً إلى الدكتور رشيد الجانبي للعمل بها.</p>", unsafe_allow_html=True)
    with st.form("visitor_feedback_fixed_top_form", clear_on_submit=True):
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
                <div style='background-color:#FFFFFF; border-right:4px solid #1E3A8A; padding:15px; margin-bottom:10px; text-align:right;'>
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
                                cursor.execute("UPDATE shrines SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, creative_works=?, web_links=?, historical_era=?, tags=? WHERE id=?", (s_type, str(row['exact_location']), hist_val, str(row['daily_activities']), str(row['annual_activities']), str(row['researchers_books']), str(row['creative_works']), str(row['web_links']), era_val, tags_val, existing[0]))
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
