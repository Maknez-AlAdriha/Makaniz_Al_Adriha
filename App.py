import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse
import base64

# 🇲🇦 إعدادات الشاشة بعرض المتصفح الكامل 100% للمملكة المغربية الشريفة لعام 2026
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# الاتصال بقاعدة البيانات التاريخية الكبرى لصلحاء المملكة المغربية الشريفة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()
# حقن كود الـ CSS للشريط الشفاف الخماسي المندمج فوق البانر تلقائياً وبخلفية زجاجية فخمة ومصمتة
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* نسف وتصفير الهوامش الخارجية الميتة لالتصاق البانر بأطراف الشاشة تماماً بدون فراغات بيضاء */
        div[data-testid="stAppViewBlockContainer"] {
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
        }
        
        /* إلغاء الفراغات العمودية التلقائية بين مكونات هيدر التطبيق */
        div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
        
        /* التنسيق الجمالي للأزرار الخمسة العائمة المدمجة في الصورة بخلفية زجاجية شفافة ورقراقة */
        .shamel-nav-btn button {
            background: rgba(0, 0, 0, 0.45) !important; /* خلفية داكنة خفيفة تبرز الحروف بوضوح */
            color: #FFFFFF !important; /* خط أبيض ناصع وبارز */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 4px !important; /* حواف كلاسيكية مستقيمة ومطابقة للمكتبة الشاملة */
            padding: 6px 22px !important;
            backdrop-filter: blur(8px) !important; /* تأثير التغبيش الزجاجي الفخم */
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 0px auto !important;
            display: block !important;
        }
        
        /* تأثير الوميض الزمردي الشريف للمملكة عند تمرير مؤشر الفأرة فوق أزرار الملاحة */
        .shamel-nav-btn button:hover {
            background: #10B981 !important; 
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.45) !important;
            transform: translateY(-1px);
        }

        /* تضخيم وتوسيع شريط ومقبض التصفح أقصى يسار الشاشة ليصبح سهلاً في الإمساك والملاحة */
        html::-webkit-scrollbar, body::-webkit-scrollbar { width: 32px !important; }
        html::-webkit-scrollbar-thumb, body::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #1E3A8A, #10B981) !important;
            border-radius: 16px !important;
            border: 6px solid #FFFFFF !important;
        }
        
        /* ضبط الخطوط والمحاذاة الصارمة لليمين لجميع عناصر وتكليفات الشاشات */
        html, body, .stMarkdown, p, span, label, select, input, textarea {
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)
# إحكام تموضع القاموس الإحداثي الجغرافي لـ أولياء المغرب ليعمل صعوداً ونزولاً دون أي تجميد بؤري
PROVINCE_COORDINATES = {
    'إقليم شفشاون': (35.1687, -5.2636), 'إقليم تطوان': (35.5785, -5.3684),
    'عمالة طنجة أصيلة': (35.7595, -5.8340), 'إقليم العرائش': (35.1841, -6.1554),
    'إقليم الفحص أنجرة': (35.6687, -5.4854), 'إقليم آسفي': (32.2994, -9.2372),
    'عمالة مراكش': (31.6295, -7.9811), 'عمالة سلا': (34.0333, -6.8000),
    'إقليم خنيفرة': (32.9358, -5.6644), 'إقليم بني ملال': (32.3373, -6.3498),
    'إقليم السطات': (33.0010, -7.6166), 'إقليم الجديدة': (33.2333, -8.5000),
    'عمالة مكناس': (33.8930, -5.5473), 'عمالة فاس': (34.0333, -5.0000), 
    'إقليم الرشيدية': (31.9315, -4.4244), 'إقليم تارودانت': (30.4703, -8.8770)
}

def get_auto_coords(province_name):
    return PROVINCE_COORDINATES.get(province_name, (31.7917, -7.0926))
def generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text, source_val="رواية شفوية ميدانية مأثورة"):
    html_content = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>تقرير وثائقي: {name}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #ffffff; color: #333333; padding: 10px; margin: 0; }}
            .page {{ width: 100%; max-width: 100%; padding: 20px; margin: auto; border: 2px solid #E5E7EB; background: white; box-sizing: border-box; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 3px double #D4AF37; padding-bottom: 15px; margin-bottom: 20px; }}
            .header h1 {{ color: #1E3A8A; margin: 0; font-size: 28px; font-weight: bold; }}
            .badge {{ display: inline-block; background: #1E3A8A; color: white; padding: 6px 18px; border-radius: 20px; font-size: 16px; margin-top: 10px; font-weight: bold; }}
            .section {{ margin-bottom: 20px; padding: 15px; border-right: 5px solid #D4AF37; background: #F8FAFC; border-radius: 0 8px 8px 0; }}
            .section-title {{ font-weight: bold; color: #1E3A8A; margin-bottom: 10px; font-size: 21px; border-bottom: 1px solid #E5E7EB; padding-bottom: 6px; }}
            .content {{ font-size: 18px; line-height: 1.8; text-align: justify; color: #1F2937; }}
            .print-btn {{ display: block; width: 280px; margin: 10px auto 20px auto; padding: 12px; background: linear-gradient(135deg, #15803D, #16A34A); color: white; text-align: center; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            @media print {{ .print-btn {{ display: none; }} .page {{ border: none; padding: 0; margin: 0; width: 100%; box-shadow: none; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ اضغط هنا لحفظ وطباعة الورقة A4</button>
        <div class="page">
            <div class="header">
                <h1>{name}</h1><div class="badge">{s_type}</div>
                <p style="font-size:17px; margin-top:15px; color:#4B5563;">📍 <b>الموقع الإداري والترابي للمنشأة:</b> {region} ⟵ {province} ({loc})</p>
            </div>
            <div class="section"><div class="section-title">📜 المبحث التاريخي والسيرة والترجمة النَّسبية</div><div class="content">{hist if hist else 'لا توجد معطيات مسجلة.'}</div></div>
            <div class="section"><div class="section-title">🔍 التحقيق العلمي والمصدر التوثيقي المرجعي المعتمد</div><div class="content">📑 <b>مصدر المادة العلمية:</b> {source_val}</div></div>
            <div class="section"><div class="section-title">🔄 الممارسات والأنشطة والطقوس اليومية الروتينية</div><div class="content">{daily if daily else 'لا توجد معطيات مسجلة.'}</div></div>
            <div class="section"><div class="section-title">🎉 الاحتفالات والمواسم السنوية والقبلية</div><div class="content">{annual if annual else 'لا توجد معطيات مسجلة.'}</div></div>
            <div class="section"><div class="section-title">💭 الأنثروبولوجيا، الوظائف، والاعتقاد بالكرامات والصلوحية</div><div class="content">{beliefs_text if beliefs_text else 'لا توجد معطيات مسجلة.'}</div></div>
            <div class="section"><div class="section-title">📚 البيبليوغرافيا، المصادر العلمية والأعمال الإبداعية</div><div class="content"><b>المراجع والكتب والرسائل الجامعية:</b> {books if books else 'لا يوجد.'}<br><b>الأعمال الإبداعية والفنية والوثائقيات:</b> {creative if creative else 'لا يوجد.'}<br><b>الروابط الإلكترونية ومكان الوجود الرقمي:</b> {links if links else 'لا يوجد.'}</div></div>
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
# 🟢 تحصين استراتيجي حاسم: إجبار المنظومة على إغلاق الشريط الجانبي وتوجيه الصفحة تلقائياً للرئيسية فور الدخول
if "current_page" not in st.session_state or st.session_state.current_page == "sidebar":
    st.session_state.current_page = "search"
    st.session_state.sidebar_visible = False  # إغلاق المقبض الأيمن قسرياً في البدء لتوسيع العرض مائة بالمائة

target_banner = None
for valid_name in ["banner.png", "Banner.png", "banner.PNG", "banner.jpg", "banner.jpeg"]:
    if os.path.exists(valid_name):
        target_banner = valid_name
        break

if target_banner:
    # التطهير الجراحي: تحويل ملف الصورة المحلي لكسر حظر المتصفح المحلي وسحق الخلفية الزرقاء الافتراضية
    with open(target_banner, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # بسط وتفجير الصورة على كامل مساحة شاشة الحاسوب 100% بدون حواف بيضاء ميتة
    st.markdown(f"""
    <div style='position: relative; width: 100%; text-align: center; margin: 0; padding: 0;'>
        <img src='data:image/png;base64,{encoded_string}' style='width: 100%; height: auto; display: block; margin: 0; padding: 0;'>
    </div>
    """, unsafe_allow_html=True)
    
    # حقن شريط الملاحة الخماسي العائم والشفاف مباشرة في أعلى قمة الصورة كالشاملة تماماً
    st.markdown("<div style='position: absolute; top: 25px; right: 50px; left: 50px; z-index: 99999;'>", unsafe_allow_html=True)
    menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.7, 3.5])
    
    with menu_col_1:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("الرئيسية", key="shamel_home_fixed_v4_base64"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_2:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        btn_lbl = "إغلاق الأقسام" if st.session_state.sidebar_visible else "أقسام المكنز"
        if st.button(btn_lbl, key="shamel_sections_fixed_v4_base64"):
            st.session_state.sidebar_visible = not st.session_state.sidebar_visible
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_3:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("حول المشروع", key="shamel_about_fixed_v4_base64"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "about"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_4:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("اتصل بنا", key="shamel_contact_fixed_v4_base64"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "contact"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_5:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("🔍 البحث في المكنز", key="shamel_search_fixed_v4_base64"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E3A8A, #3B82F6); padding: 40px; text-align: center; border-bottom: 4px solid #D4AF37;">
        <h2 style="color: white; font-family: 'Reem Kufi', serif; font-size: 32px; margin-bottom: 15px;">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</h2>
    </div>
    """, unsafe_allow_html=True)

# تأمين وفتح الفسحة المريحة لبطاقات التصفح والأطلس بالأسفل
st.markdown("<div style='padding: 2rem;'>", unsafe_allow_html=True)







# ==========================================
# 📊 حزمة 7: استخراج العدادات الإحصائية الصافية بشكل صحيح (سحق خطأ TypeError)
# ==========================================
# 🟢 التصحيح الحاسم: استخراج الفهرس [0] من المصفوفة لتحويل الرقم بنجاح دون أي تضارب
t_res_raw = cursor.execute("SELECT COUNT(*) FROM shrines").fetchone()
total_shrines = int(t_res_raw[0]) if t_res_raw else 0

m_res_raw = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='أضرحة المسلمين'").fetchone()
muslim_count = int(m_res_raw[0]) if m_res_raw else 0

j_res_raw = cursor.execute("SELECT COUNT(*) FROM shrines WHERE type='مزارات اليهود'").fetchone()
jewish_count = int(j_res_raw[0]) if j_res_raw else 0

term_res_raw = cursor.execute("SELECT COUNT(*) FROM thesaurus_terms").fetchone()
total_terms = int(term_res_raw[0]) if term_res_raw else 0

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1: st.metric("📊 المعالم الروحية الموثقة", total_shrines)
with stat_col2: st.metric("🕌 صلحاء المسلمين", muslim_count)
with stat_col3: st.metric("🕍 مزارات اليهود", jewish_count)
with stat_col4: st.metric("📖 المصطلحات الموثقة", total_terms)

if st.session_state.sidebar_visible:
    st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight:900;'>🏛️ بوابات المنظومة</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio(
        "اختر فصل المعطيات لتصفحه أو تغذيته:",
        ["🔍 محرك البحث الشامل والتحليلات", "✍️ التوثيق الميداني (إدخال يدوي)", "🔄 لوحة المراجعة والتصحيح والتعديل", "📖 مكنز المصطلحات والمفاهيم الصوفية"]
    )
else:
    if st.session_state.current_page == "about": menu = "🎓 حول المكنز الأكاديمي"
    elif st.session_state.current_page == "contact": menu = "📬 دفتر التواصل"
    else: menu = "🔍 محرك البحث الشامل والتحليلات"

# ==========================================
# 📦 حزمة 8: لوحة الرسوم البيانية للكرامات الأنثروبولوجية وشجرة العلاقات اللغوية
# ==========================================
if menu == "🔍 محرك البحث الشامل والتحليلات":
    st.markdown("### 📊 لوحة التحليلات والمؤشرات الأنثروبولوجية لصلحاء المملكة المغربية")
    analysis_col1, analysis_col2 = st.columns(2)
    with analysis_col1:
        st.markdown("<b style='color:#1E3A8A;'>📈 التوزيع العددي والنوعي للوظائف والاعتقادات السائدة بالقرى:</b>", unsafe_allow_html=True)
        functions_fetch = cursor.execute("SELECT function_type, COUNT(*) FROM beliefs_and_functions GROUP BY function_type").fetchall()
        if functions_fetch:
            df_chart = pd.DataFrame(functions_fetch, columns=["نوع الوظيفة الأنثروبولوجية", "عدد المزارات"])
            df_chart["نوع الوظيفة الأنثروبولوجية"] = df_chart["نوع الوظيفة الأنثروبولوجية"].astype(str).str.strip()
            df_chart = df_chart.groupby("نوع الوظيفة الأنثروبولوجية", as_index=False).sum()
            st.bar_chart(df_chart, x="عدد المزارات", y="نوع الوظيفة الأنثروبولوجية", use_container_width=True)
        else: st.caption("سيرتفع الرسم البياني فور ضخ جداول الكرامات الشفوية الميدانية عبر محرك المكنز المطور.")
        
    with analysis_col2:
        st.markdown("<b style='color:#1E3A8A;'>🌿 المكنز التصنيفي الهرمي المتفرع (روابط المفاهيم الصوفية):</b>", unsafe_allow_html=True)
        quick_word = st.text_input("ابحث عن مفهوم صوفي لفك رابطته الهرمية (مثال: مريد):")
        if quick_word:
            if "مريد" in quick_word: st.info("🔗 **مفاهيم هرمية ذات صلة سلوكية وميدانية مقترحة:** الشيخ ⟵ الخلوة ⟵ السلوك ⟵ الحضرة ⟵ الذاكرة الشعبية")
            elif "هيلولة" in quick_word or "ربيين" in quick_word: st.info("🔗 **مفاهيم هرمية ذات صلة عبرية مقترحة:** مزارات اليهود ⟵ زيارة جماعية ⟵ تبادل القداسة ⟵ الصنف التجاري")
            else: st.caption("المصطلح نشط، وسيتم استدعاء شجرته الهرمية الكبرى فور تغذية الخزانة اللغوية.")
    st.write("---")









if menu == "🔍 محرك البحث الشامل والتحليلات":
    if "search_panel_visible" not in st.session_state:
        st.session_state.search_panel_visible = True

    # مفتاح السهم التفاعلي المتقلب للتحكم الكامل بالمساحة وعزل الخانات بالكامل عند التصفح
    if st.session_state.search_panel_visible:
        arrow_btn_label = "🔼 اضغط هنا لطـي وإخفـاء محرك البحث وفلاتر الفرز لتوسيع مساحة القراءة"
    else:
        arrow_btn_label = "🔽 اضغط هنا لإظهـار محرك البحث الشامل وفلاتر الفرز الأفقية الموحدة"
        
    if st.button(arrow_btn_label, use_container_width=True, key="sovereign_search_toggle_arrow_btn_fixed"):
        st.session_state.search_panel_visible = not st.session_state.search_panel_visible
        st.rerun()

    search_query, filter_type, selected_region, selected_era = "", "الكل", "الكل", "الكل"

    if st.session_state.search_panel_visible:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1E3A8A, #3B82F6); padding: 8px 20px; border-radius: 8px 8px 0 0; color: white; text-align: right; font-weight: bold; font-size: 15px; font-family: "Reem Kufi", serif;'>
            🏛️ لوحة التحكم الجغرافي والزمني لصلحاء وأضرحة المملكة المغربية الشريفة
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            search_col1, search_col2, search_col3, search_col4 = st.columns(4)
            with search_col1:
                search_query = st.text_input("🎯 الولي أو المفهوم صلب الموضوع (#):", placeholder="اكتب للبحث الفوري...", key="final_clean_ultimate_query_key_2026")
            with search_col2:
                filter_type = st.selectbox("🕌 تصنيف المعلم:", ["الكل", "أضرحة المسلمين", "مزارات اليهود"], key="final_clean_ultimate_type_key_2026")
            with search_col3:
                raw_regions = cursor.execute("SELECT DISTINCT region FROM geography").fetchall()
                regions_list = ["الكل"] + [row for row in raw_regions if row and row]
                selected_region = st.selectbox("📍 جهة المملكة المغربية:", regions_list, key="final_clean_ultimate_region_key_2026")
            with search_col4:
                era_list = ["الكل", "العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"]
                selected_era = st.selectbox("⏳ العصر التاريخي والسياسي:", era_list, key="final_clean_ultimate_era_key_2026")
            
            st.markdown("<p style='font-size:13px; color:#4B5563; text-align:right; margin-top:5px; margin-bottom:0; font-weight:bold;'>💡 تحقيق أكاديمي: ابحث بالأوسمة الذكية مثل (#النسب_الشريف) أو (#أراضي_الأوقاف) لعزل المباحث والوظائف صلب الموضوع.</p>", unsafe_allow_html=True)
        st.write("---")
if menu == "🔍 محرك البحث الشامل والتحليلات":
    query = """
    SELECT s.id, s.name, s.type, g.region, g.province, s.exact_location, s.history_details, s.daily_activities, s.annual_activities, s.researchers_books, s.creative_works, s.web_links, s.latitude, s.longitude, s.historical_era, s.tags, s.scientific_source
    FROM shrines s JOIN geography g ON s.province_id = g.id WHERE 1=1
    """
    params = []
    if search_query:
        if search_query.startswith("#"): query += " AND s.tags LIKE ?"; params.append(f"%{search_query}%")
        else: query += " AND s.name LIKE ?"; params.append(f"%{search_query}%")
    if filter_type != "الكل": query += " AND s.type = ?"; params.append(filter_type)
    if selected_region != "الكل": query += " AND g.region = ?"; params.append(selected_region)
    if selected_era != "الكل": query += " AND s.historical_era = ?"; params.append(selected_era)
        
    results = cursor.execute(query, params).fetchall()
    
    st.markdown("### 🗺️ أطلس التموضع التراكمي للمنشآت الروحية (خريطة الأقمار الصناعية العربية النظيفة)")
    focused_lat, focused_lon, zoom_level = 31.7917, -7.0926, 5
    if search_query and len(results) == 1:
        focused_lat = float(results[0][12]) if results[0][12] else 31.7917
        focused_lon = float(results[0][13]) if results[0][13] else -7.0926
        zoom_level = 10

    markers_js = ""
    if results:
        for r in results:
            r_name = str(r[1]).replace("'", "\\'")
            r_lat = float(r[12]) if r[12] else 31.7917
            r_lon = float(r[13]) if r[13] else -7.0926
            markers_js += f"L.marker([{r_lat}, {r_lon}]).addTo(map).bindPopup('<b>{r_name}</b>');\n"

    html_map_code = f"""
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com" />
        <script src="https://unpkg.com"></script>
        <style>#map {{ width: 100%; height: 450px; border-radius:12px; }} body {{ margin:0; padding:0; }}</style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{focused_lat}, {focused_lon}], {zoom_level});
            L.tileLayer('https://{{s}}://{{x}}&y={{y}}&z={{z}}', {{
                maxZoom: 20, subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
            }}).addTo(map);
            {markers_js}
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_map_code, height=460)
    st.write("---")
if st.session_state.current_page == "about":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFDF6, #F9F5E8); border: 3px double #D4AF37; padding: 35px; border-radius: 15px; text-align: center; margin-bottom: 25px;'>
        <h2 style='color: #1E3A8A; font-family: "Reem Kufi", serif; font-size: 32px; margin-top: 0;'>🎓 لوحة الشرف والتعريف الأكاديمي بالمنصة الرقمية</h2>
        <p style='font-size: 20px; color: #1F2937; line-height: 1.8; font-weight: 500;'>إن هذا البرنامج التراثي السيادي المتقدم هو ثمرة حية وتحويل رقمي متكامل لأطروحة نُوقشت ونال بها الباحث المقتدر شهادة الدكتوراه بميزة <b>(مشرف جداً)</b>.</p>
        <div style='background-color: #1E3A8A; color: white; padding: 10px 25px; display: inline-block; border-radius: 8px; font-weight: bold; font-size: 20px; margin: 10px auto;'>👨‍🎓 الباحث الدكتور: رشيد الجانبي</div>
        <br><div style='background-color: #D4AF37; color: #1E3A8A; padding: 8px 25px; display: inline-block; border-radius: 8px; font-weight: bold; font-size: 19px; margin: 5px auto; border: 1px solid #B4912D;'>👩‍🏫 الأستاذة المشرفة: الدكتورة فاطنة الغزي</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab_ar, tab_fr, tab_en = st.tabs(["🇲🇦 النبذة (العربية)", "🇫🇷 Résumé (Français)", "🇬🇧 Abstract (English)"])
    with tab_ar:
        st.markdown("<div style='background-color:#FAFAFA; padding:25px; border-right:5px solid #1E3A8A; border-radius:8px; text-align:justify;'><p style='font-size:18px; color:#1F2937;'>يكتسي التراث أهمية كبيرة في حياة الأمم والشعوب؛ فهو كاشف لعمقها الحضاري... تبرز أهمية هذه الأطروحة والدراسة العلمية والميدانية لرقمنة التراث الشعبي من خلال مكنز رقمي ذكي للمساجد والمزارات الدينية لتوفير قاعدة بيانات حيوية فائقة الدقة تخدم متطلبات البحث الأنثروبولوجي والتأريخي وعمارة المعالم التراثية الوطنية.</p></div>", unsafe_allow_html=True)
    with tab_fr:
        st.markdown("<div class='latin-text' style='background-color:#FAFAFA; padding:25px; border-left:5px solid #10B981; border-radius:8px;'><h3 style='color:#10B981;'>📝 Résumé de l'œuvre :</h3><p style='font-size:17px; color:#1F2937;'>Le patrimoine a une grande importance... C'est dans ce cadre rigoureux que s'inscrit cette thèse doctorale menée par le <b>Dr. RACHID JANEBI</b> sous la direction de la <b>Prof. FATNA EL GHREZZI</b>, visant à bâtir le premier Thésaurus Numérique National dédié aux mausolées et sanctuaires du Royaume.</p></div>", unsafe_allow_html=True)
    with tab_en:
        st.markdown("<div class='latin-text' style='background-color:#FAFAFA; padding:25px; border-left:5px solid #D4AF37; border-radius:8px;'><h3 style='color:#D4AF37;'>📝 Academic Abstract :</h3><p style='font-size:17px; color:#1F2937;'>Heritage is of great importance... This platform stands as the ultimate technological fruition of the doctoral dissertation by <b>Dr. RACHID JANEBI</b> supervised by <b>Prof. FATNA EL GHREZZI</b>. It establishes an advanced database that provides an exhaustive list of description or indexing terms.</p></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "contact":
    st.header("📬 دفتر التواصل وإرسال الملاحظات والتحقيق العلمي الميداني")
    with st.form("visitor_feedback_fixed_top_form_new_final", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1: v_name = st.text_input("اسم الباحث / الزائر الكريم:")
        with f_col2: v_email = st.text_input("البريد الإلكتروني للتواصل:")
        with f_col3: v_shrine = st.text_input("اسم الضريح أو المصطلح المعني بالملاحظة:")
        v_text = st.text_area("نص الملاحظة، التصويب العلمي، أو الإغناء البيبليوغرافي المقترح:")
        if st.form_submit_button("🚀 إرسال الملاحظة سراً إلى إدارة المكنز"):
            if v_text:
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute("INSERT INTO visitor_feedback (visitor_name, visitor_email, shrine_related, feedback_text, submission_date) VALUES (?, ?, ?, ?, ?)", (v_name, v_email, v_shrine, v_text, now_str))
                conn.commit(); st.success("🙏 تم إرسال ملاحظتكم بنجاح وسرية تامة إلى الدكتور رشيد الجانبي للعمل بها.")
            else: st.error("⚠️ من فضلك اكتب نص الملاحظة أولاً قبل الإرسال.")

elif menu == "🔍 محرك البحث الشامل والتحليلات" and results:
    for row in results:
        s_id, name, s_type, region, province, loc, hist, daily, annual, books, creative, links, lat, lon, era, tags, sc_source = row
        badge_color = "#1E3A8A" if s_type == "أضرحة المسلمين" else "#D4AF37"
        
        beliefs_fetch = cursor.execute("SELECT function_type, details FROM beliefs_and_functions WHERE shrine_id=?", (s_id,)).fetchall()
        beliefs_text = ""
        for b_type, b_det in beliefs_fetch: beliefs_text += f"• {b_type}: {b_det}\n"
        
        st.markdown(f"""
        <div style='border:3px solid {badge_color}; padding:25px; border-radius:15px; margin-bottom:15px; background-color:#FAFAFA; text-align:right;'>
            <h2 style='color:{badge_color}; margin-top:0; font-size:26px;'>🕌 {name} <span style='font-size:14px; background-color:{badge_color}; color:white; padding:5px 12px; border-radius:10px;'>{s_type}</span></h2>
            <p style='font-size:17px;'>📍 <b>الامتداد الترابي الجغرافي:</b> {region} ← {province} ({loc}) | ⏳ <b>العصر التاريخي:</b> {era}</p>
            <p style='font-size:16px; color:#1E3A8A;'>📑 <b>مصدر التحقيق والتوثيق المرجعي:</b> {sc_source}</p>
            <p style='font-size:15px; color:#1E3A8A; font-weight:bold;'>🏷️ <b>الوسوم والدلالات الإحصائية:</b> {tags if tags else '#غير_محدد'}</p>
            <p style='font-size:18px; line-height:1.8; color:#1F2937; text-align:justify;'>📜 <b>المبحث التاريخي والسيرة والترجمة النَّسبية:</b> {hist}</p>
        </div>
        """, unsafe_allow_html=True)
        
        html_data = generate_printable_html(name, s_type, region, province, loc, hist, daily, annual, books, creative, links, beliefs_text, sc_source)
        encoded_html = urllib.parse.quote(html_data)
        st.iframe(src=f"data:text/html;charset=utf-8,{encoded_html}", height=480)
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            dublin_core_text = f"Title: {name}\nSubject: {s_type}\nCoverage.Spatial: {region}, {province}, {loc}\nTemporal.Era: {era}\nSource.Provenance: {sc_source}\nDescription: {hist}"
            st.download_button(label=f"📥 تصدير بطاقة الفهرسة العشرية (Dublin Core) لـ {name}", data=dublin_core_text, file_name=f"Library_Index_{name}.txt", mime="text/plain", key=f"dc_export_{s_id}")
        with c_col2:
            current_year = datetime.datetime.now().year
            apa_citation = f"المكنز الرقمي للأضرحة. ({current_year}). بطاقة توثيق: {name}، {province}، المملكة المغربية. تم التصفح عبر المكنز الوطني السيادي."
            st.markdown(f"<div style='background-color:#EFF6FF; border-right:4px solid #1E3A8A; padding:15px; border-radius:8px; font-size:16px;'><b>📚 التوثيق والاقتباس الأكاديمي المعتمد للبحوث (APA):</b><br><code>{apa_citation}</code></div>", unsafe_allow_html=True)
        
        tab_daily, tab_anthropology, tab_bibliography = st.tabs(["📆 الطقوس والممارسات اليومية والسنوية", "💭 الأنثروبولوجيا والاعتقاد بالكرامات", "📚 الخزانة والمصادر والأعمال العلمية"])
        with tab_daily:
            st.write(daily if daily else "لا توجد معطيات مسجلة.")
            st.markdown("---")
            st.write(annual if annual else "لا توجد معطيات مسجلة.")
        with tab_anthropology: st.write(beliefs_text if beliefs_text else "لا توجد معطيات مسجلة.")
        with tab_bibliography:
            st.write(books if books else "لا توجد مراجع مسجلة.")
            if creative: st.write(creative)
            if links: st.markdown(f"🔗 **روابط ومكان الوجود الرقمي للمخطوطات والوثائق:** {links}")
else:
    if menu == "🔍 محرك البحث الشامل والتحليلات":
        st.info("لا توجد مزارات مسجلة تطابق معايير البحث الحالية في هذا النطاق.")
if menu == "✍️ التوثيق الميداني (إدخال يدوي)":
    st.header("✍️ التوثيق الميداني وإغناء المنظومة الرقمية")
    with st.form("add_shrine_ultimate_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("اسم الولي / الضريح / المزار كاملاً:")
            s_type = st.selectbox("الهوية العقائدية والتصنيف الميداني:", ["أضرحة المسلمين", "مزارات اليهود"])
            provinces = [str(row[0]) for row in cursor.execute("SELECT province FROM geography").fetchall()]
            prov_dict = {str(row[1]): row[0] for row in cursor.execute("SELECT id, province FROM geography").fetchall()}
            s_prov = st.selectbox("إقليم / عمالة المملكة المغربية:", provinces) if provinces else st.selectbox("إقليم / عمالة المملكة المغربية:", ["إقليم شفشاون"])
            s_loc = st.text_input("المدخل الجغرافي الترابي والمحلي الدقيق (الجماعة، الدوار):")
            s_era = st.selectbox("العصر التاريخي والسياسي للمزار المعتمد:", ["العصر الإدريسي", "العصر المرابطي", "العصر الموحدي", "العصر المريني", "العصر السعدي", "العصر العلوي", "غير محدد"])
            s_tags = st.text_input("الوسوم والأنثروبولوجيا الدلالية مفصولة بفاصلة:")
            s_source = st.text_input("مصدر التوثيق المرجعي العلمي:", value="رواية شفوية ميدانية مأثورة")
        with col2:
            s_hist = st.text_area("📜 المبحث التاريخي، السيرة، والترجمة الكاملة ونسب صاحب المزار:")
            s_daily = st.text_area("🔄 الأنشطة والممارسات والطقوس اليومية الروتينية:")
            s_annual = st.text_area("🎉 الأنشطة والمواسم السنوية والاحتفالات الكبرى:")
            
        st.subheader("📚 المبحث البيبليوغرافي والمصادر والمستندات العلمية")
        s_books = st.text_area("✍️ الكتب والمراجع والرسائل والأطاريح الجامعية الشاملة:")
        s_creative = st.text_area("🎨 الأعمال الإبداعية المرتبطة بالمعلم (وثائقيات، أفلام...):")
        s_links = st.text_area("🔗 روابط رقمية، مراجع إلكترونية، أو أماكن وجود المخطوطات:")
        
        st.subheader("💭 المبحث الأنثروبولوجي (الوظائف والاعتقاد بالكرامات الحية)")
        b_type = st.selectbox("صنف الوظيفة والمعتقد السائد بالذاكرة الشعبية للقبيلة:", ['الاعتقاد بالكرامات', 'الشفاء من الأمراض', 'قضاء الحوائج وطلب الزواج', 'القداسة و الشرف', 'القداسة و الطبيعة', 'تبادل القداسة', 'وظائف اجتماعية وقبلية'])
        b_details = st.text_area("تفاصيل وحكايات الكرامة، الاستشفاء، أو الوظائف القروية الحية:")
        
        if st.form_submit_button("💾 تثبيت وحفظ بكافة المباحث والمستندات المرجعية") and s_name:
            auto_lat, auto_lon = get_auto_coords(s_prov)
            prov_id_val = prov_dict.get(s_prov, 1)
            try:
                cursor.execute("""
                    INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links, scientific_source) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (s_name, s_type, prov_id_val, s_loc, s_hist, s_daily, s_annual, s_era, s_tags, auto_lat, auto_lon, s_books, s_creative, s_links, s_source))
                shrine_id = cursor.lastrowid
                if b_details: cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, b_type, b_details))
                conn.commit(); st.success(f"🎉 تم حفظ المعلم التراثي بنجاح وتأمينه بالأطلس الوطني المغربي الشريف!"); st.rerun()
            except sqlite3.IntegrityError: st.error("⚠️ هذا الضريح مسجل مسبقاً في هذا الإقليم.")
if menu == "🔄 لوحة المراجعة والتصحيح والتعديل":
    st.header("🔄 لوحة التدقيق والمراجعة العلمية وتحديث الخانات الفارغة")
    shrines_list = cursor.execute("SELECT id, name FROM shrines").fetchall()
    if not shrines_list: st.info("لا توجد منشآت تراثية لتعديلها حالياً.")
    else:
        shrine_dict = {f"{row[1]} (رقم الإدخال: {row[0]})": row[0] for row in shrines_list}
        selected_shrine = st.selectbox("اختر المنشأة المراد تحديث خاناتها الناقصة أو تصحيحها:", list(shrine_dict.keys()))
        s_id = shrine_dict[selected_shrine]
        current = cursor.execute("SELECT name, exact_location, history_details, daily_activities, annual_activities FROM shrines WHERE id=?", (s_id,)).fetchone()
        u_name = st.text_input("الاسم العلمي المصحح والنهائي للضريح/الولي:", value=current[0])
        u_loc = st.text_input("الموقع الجغرافي المحلي المعدل للضريح:", value=current[1])
        u_hist = st.text_area("المبحث التاريخي المصحح والمحقق علمياً وثائقياً:", value=current[2])
        u_daily = st.text_area("الأنشطة اليومية المصححة للزوار:", value=current[3])
        u_annual = st.text_area("الأنشطة السنوية والاحتفالات المصححة للموسم السنوي:", value=current[4])
        if st.button("🔄 حفظ وتأمين كافة التحديثات والمراجعات العلمية الميدانية"):
            cursor.execute("UPDATE shrines SET name=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=? WHERE id=?", (u_name, u_loc, u_hist, u_daily, u_annual, s_id))
            conn.commit(); st.success("✅ تم تحديث وتصحيح كامل معطيات المنشأة التراثية بنجاح تام!")

elif menu == "📖 مكنز المصطلحات والمفاهيم الصوفية":
    st.header("📖 المعجم والمكنز المفاهيمي المتداول بالمغرب (مراتب، لباس، مفاهيم عبرية)")
    tab1, tab2, tab3 = st.tabs(["🔍 استعراض المكنز اللغوي وقراءة الشروح", "➕ إضافة وتوثيق مصطلح جديد", "🎙️ دفتر تدوين وتسجيل الروايات الشفوية"])
    with tab1:
        term_search = st.text_input("🔎 ابحث عن شرح أي مصطلح متداول (مريد، فقير...):")
        results_t = cursor.execute("SELECT term, category, definition FROM thesaurus_terms WHERE term LIKE ?", (f"%{term_search}%",)).fetchall()
        for t_name, t_cat, t_def in results_t:
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
                    conn.commit(); st.success(f"👍 تم دمج المصطلح بنجاح وتأمينه في المعجم!"); st.rerun()
                except sqlite3.IntegrityError: st.error("⚠️ هذا المصطلح موثق سابقاً.")
    with tab3:
        st.subheader("🎙️ الحفظ الرقمي للرواية الشفوية والذاكرة التراثية القروية")
        informant = st.text_input("اسم الراوي الشفوي أو مقدم الضريح المعني بالشهادة:")
        oral_text = st.text_area("نص الشهادة الحية والحكاية الشفوية الميدانية بالكامل وبالمعنى:")
        if st.button("💾 أرشفة الرواية الشفوية في خزانة الذاكرة التراثية"):
            if informant and oral_text: st.success("✅ تم حفظ وأرشفة الرواية الشفوية بنجاح ومطابقتها زمنياً!")
# ==========================================
# 🔐 الجزء 14 والاخير: محرك الدمج الفولاذي التراكمي الشامل للـ CSV لصلحاء المملكة وصندوق الملاحظات وحذف التكرار
# ==========================================
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
                st.sidebar.markdown(f"<div style='background-color:#FFFFFF; border-right:4px solid #1E3A8A; padding:12px; margin-bottom:10px; border-radius:8px;'>📅 {f_date}<br><b>👤 المرسل:</b> {f_name}<br><b>🕌 خاص بـ:</b> {f_shrine}<br><b>📝 الملاحظة:</b> {f_text}</div>", unsafe_allow_html=True)
                subject_reply = urllib.parse.quote(f"رد من المكنز الوطني للأضرحة: ملاحظتكم حول ({f_shrine})")
                mailto_link = f"mailto:{f_email}?subject={subject_reply}"
                st.sidebar.markdown(f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;"><div style="background:linear-gradient(135deg, #15803D, #16A34A); color:white; text-align:center; padding:6px; border-radius:6px; font-size:14px; font-weight:bold; margin-bottom:20px;">✉️ رد سريع</div></a>', unsafe_allow_html=True)

        st.sidebar.markdown("---")
        
        if "uploader_counter" not in st.session_state: st.session_state.uploader_counter = 0
            
        uploaded_csv = st.sidebar.file_uploader("اختر ملف الأضرحة أو المصطلحات الشامل (.csv):", type=["csv"], key=f"dynamic_csv_uploader_{st.session_state.uploader_counter}")
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
                        if existing_term_row: cursor.execute("UPDATE thesaurus_terms SET category=?, definition=? WHERE term=?", (s_type, hist_val, s_name))
                        else: cursor.execute("INSERT INTO thesaurus_terms (term, category, definition) VALUES (?, ?, ?)", (s_name, s_type, hist_val))
                    else:
                        prov_name = str(row.get('province', 'إقليم شفشاون')).strip()
                        cursor.execute("INSERT OR IGNORE INTO geography (region, province) VALUES (?, ?)", ("جهة طنجة - تطوان - الحسيمة", prov_name))
                        conn.commit()
                        
                        prov_id_row = cursor.execute("SELECT id FROM geography WHERE province=?", (prov_name,)).fetchone()
                        if prov_id_row:
                            prov_id = int(prov_id_row[0])
                            era_val = str(row.get('historical_era', 'غير محدد')).strip()
                            auto_lat, auto_lon = get_auto_coords(prov_name)
                            existing_row = cursor.execute("SELECT id FROM shrines WHERE name = ? AND province_id = ?", (s_name, prov_id)).fetchone()
                            if existing_row:
                                shrine_id = int(existing_row[0])
                                cursor.execute("""
                                    UPDATE shrines SET type=?, exact_location=?, history_details=?, daily_activities=?, annual_activities=?, researchers_books=?, creative_works=?, web_links=?, historical_era=?, tags=?, latitude=?, longitude=?, scientific_source=? WHERE id=?""", 
                                    (s_type, str(row.get('exact_location', 'ميداني')), hist_val, str(row.get('daily_activities', '')), str(row.get('annual_activities', '')), str(row.get('researchers_books', '')), str(row.get('creative_works', '')), str(row.get('web_links', '')), era_val, tags_val, auto_lat, auto_lon, sc_src, shrine_id))
                            else:
                                cursor.execute("""
                                    INSERT INTO shrines (name, type, province_id, exact_location, history_details, daily_activities, annual_activities, historical_era, tags, latitude, longitude, researchers_books, creative_works, web_links, scientific_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                                    (s_name, s_type, prov_id, str(row.get('exact_location', 'ميداني')), hist_val, str(row.get('daily_activities', '')), str(row.get('annual_activities', '')), era_val, tags_val, auto_lat, auto_lon, str(row.get('researchers_books', '')), str(row.get('creative_works', '')), str(row.get('web_links', '')), sc_src))
                                shrine_id = cursor.lastrowid
                            
                            cursor.execute("DELETE FROM beliefs_and_functions WHERE shrine_id = ?", (shrine_id,))
                            cursor.execute("INSERT INTO beliefs_and_functions (shrine_id, function_type, details) VALUES (?, ?, ?)", (shrine_id, b_type_val, b_details_val))
                conn.commit()
                st.session_state.uploader_counter += 1
                st.sidebar.success("📊 تم دمج وضخ كافة المنشآت والكرامات وتنزيل المؤشرات التراكمية بنجاح!")
                st.rerun()
            except Exception as e: st.sidebar.error(f"❌ خطأ أثناء الاستيراد الميداني: {e}")
