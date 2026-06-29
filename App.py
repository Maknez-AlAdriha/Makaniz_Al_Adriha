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
            top: 0px !important; /* الالتصاق التام والصريح بسقف الشاشة فوق حافة الصورة العلوية */
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

        /* تقييد الارتفاع بالبكسل الثابت وتفعيل الـ Scroll قسرياً لكلا النافذتين وعناصرهما الداخلية بحرف D الكبير */
        div[data-testid="stDialog"], 
        div[data-testid="stDialog"] > div, 
        div[data-testid="stDialog"] .stForm, 
        div[data-testid="stDialog"] div[data-testid="stVerticalBlock"] {{
            max-height: 520px !important;
            overflow-y: auto !important;
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
        
        /* تنسيق الألواح البانورامية المضيئة لأقسام المكنز الثلاثة صلب الواجهة المفتوحة */
        .section-card-panel {{
            background: rgba(255, 255, 255, 0.95) !important;
            border-right: 6px solid #064E3B !important;
            border-radius: 8px !important;
            padding: 20px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }}
        .section-card-title {{
            font-family: "Reem Kufi", serif !important;
            color: #1E3A8A !important;
            font-size: 22px !important;
            font-weight: bold !important;
            margin-bottom: 10px !important;
            border-bottom: 1px solid #D4AF37 !important;
            padding-bottom: 5px !important;
        }}
    </style>
""", unsafe_allow_html=True)
# ==========================================
# دالات النوافذ المنبثقة التفاعلية للمشروع وبوابة التغذية الرقمية الفولاذية
# ==========================================

# 1. الدالة المنبثقة التفاعلية للتعريف بالأطروحة ونبذة عن المشروع بعد التحيين المنقح وصفر أخطاء ترتيب
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
        
        # زر الإرسال الممتد أفقياً بنجاح وثبات
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
                st.error("⚠️ منظومة الأمان تمنع الإرسال, يرجى كتابة بريدك الإلكتروني ونص الرسالة أولاً.")
# ==========================================
# 🟢 محرك لوحة الانتقاء الحركي لأقسام المكنز الثلاثة الشامخة (بدون ملفات خارجية)
# ==========================================
def show_maknez_sections_dashboard():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#FFFFFF; font-family:\"Reem Kufi\", serif; text-shadow:2px 2px 4px rgba(0,0,0,0.8); font-size:32px;'>🏛️ الأروقة والأقسام الميدانية الموثقة للمكنز الوطني</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#FFFFFF; font-family:\"Tajawal\", sans-serif; text-shadow:1px 1px 3px rgba(0,0,0,0.7); font-size:18px;'>تصفح وجرد وتحميل مفردات المباحث التاريخية والأنثروبولوجية للأطروحة الجامعية لعام 2026</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. رواق صلحاء وأولياء الإسلام بالمغرب
    st.markdown("<div class='section-card-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-card-title'>🕌 رواق صلحاء وأولياء الإسلام بالمملكة المغربية الشريفة</div>", unsafe_allow_html=True)
    st.markdown("<p>يحتوي هذا الرواق على الجرد والتحقيق الميداني الشامل لكافة الأضرحة والمنشآت الروحية التابعة لصلحاء المسلمين عبر جهات وأقاليم المملكة التاريخية.</p>", unsafe_allow_html=True)
    
    shrines_muslim = cursor.execute("""
        SELECT s.name, g.province, s.historical_era, s.scientific_source 
        FROM shrines s JOIN geography g ON s.province_id = g.id 
        WHERE s.type = 'أضرحة المسلمين' ORDER BY s.id DESC""").fetchall()
        
    if not shrines_muslim:
        st.info("لم يتم ضخ معطيات المسلمين حالياً؛ استخدم بوابة الإدارة لرفع ملفات الـ CSV.")
    else:
        df_m = pd.DataFrame(shrines_muslim, columns=["اسم المعلم الروحي الشريف", "الإقليم / العمالة التاريخية", "العصر التاريخي", "المصدر العلمي المعتمد"])
        st.dataframe(df_m, use_container_width=True, hide_index=True)
        csv_m = df_m.to_csv(index=False).encode('utf-8')
        st.download_button("📥 قذف وتحميل تقرير رواق المسلمين بالكامل (CSV)", data=csv_m, file_name="رواق_أضرحة_المسلمين_المغرب.csv", mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # 2. رواق مزارات اليهود المغاربة
    st.markdown("<div class='section-card-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-card-title'>📜 رواق مزارات وتراث اليهود المغاربة المشترك</div>", unsafe_allow_html=True)
    st.markdown("<p>قسم منقح ومنعزل يضم التوثيق والبيبليوغرافيا التاريخية الخاصة بمزارات اليهود المغاربة، تجسيداً لقيم التعددية الثقافية والوفاء العلمي الميداني صلب مادة الأطروحة.</p>", unsafe_allow_html=True)
    
    shrines_jew = cursor.execute("""
        SELECT s.name, g.province, s.historical_era, s.scientific_source 
        FROM shrines s JOIN geography g ON s.province_id = g.id 
        WHERE s.type = 'مزارات اليهود' ORDER BY s.id DESC""").fetchall()
        
    if not shrines_jew:
        st.info("لم يتم ضخ معطيات مزارات اليهود حالياً؛ استخدم بوابة الإدارة لرفع ملفات الـ CSV المخصصة.")
    else:
        df_j = pd.DataFrame(shrines_jew, columns=["اسم المعلم / الضريح", "الإقليم الجغرافي", "العصر والعهد التاريخي", "المصدر والتحقيق الميداني"])
        st.dataframe(df_j, use_container_width=True, hide_index=True)
        csv_j = df_j.to_csv(index=False).encode('utf-8')
        st.download_button("📥 قذف وتحميل تقرير رواق مزارات اليهود (CSV)", data=csv_j, file_name="رواق_مزارات_اليهود_المغاربة.csv", mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. المكنز اللغوي ومصطلحات الصوفية والأنثروبولوجيا
    st.markdown("<div class='section-card-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-card-title'>📖 القاموس الاصطلاحي ومكنز المفاهيم الصوفية والأنثروبولوجية</div>", unsafe_allow_html=True)
    st.markdown("<p>معجم هجائي قاموسي شامل لتعريف المصطلحات والمفاهيم الكبرى الواردة في الأطروحة لتسهيل الاستطلاع والفهم على الباحثين وطلاب العلم.</p>", unsafe_allow_html=True)
    
    terms_data = cursor.execute("SELECT term, category, definition FROM thesaurus_terms ORDER BY term ASC").fetchall()
    if not terms_data:
        st.info("القاموس الاصطلاحي فارغ حالياً؛ قُم بضخ المفاهيم المتبقية عبر رفع ملف CSV يحمل وسم المعجم.")
    else:
        df_t = pd.DataFrame(terms_data, columns=["المصطلح / المفهوم المحقق", "الصنف / التصنيف العلمي", "التعريف والمضمون التوثيقي المعتمد"])
        st.dataframe(df_t, use_container_width=True, hide_index=True)
        csv_t = df_t.to_csv(index=False).encode('utf-8')
        st.download_button("📥 قذف وتحميل معجم المصطلحات بالكامل (CSV)", data=csv_t, file_name="معجم_المصطلحات_الصوفية_والأنثروبولوجية.csv", mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للواجهة الرئيسية للمكنز الشريف", use_container_width=True, key="back_to_home_from_sec_dashboard"):
        st.query_params.clear()
        st.rerun()
# 3. الدالة المنبثقة السيادية لبوابة الإدارة ودعم الاستيراد المتعدد للمللفات والتقارير الإحصائية وسحق الـ tuple نهائياً
@st.dialog("بوابة إدارة وتغذية المكنز الوطني")
def show_admin_dashboard_popup():
    st.markdown("<div class='popup-header-title'>🔐 نظام التغذية الرقمية والاستيراد التراكمي الشامل</div>", unsafe_allow_html=True)
    developer_key = st.text_input("أدخل رمز العبور السيادي لتنشيط صلاحيات الإشراف:", type="password", key="popup_dev_key_fixed_v14")
    
    if developer_key == "MAROC_2026":
        st.success("🔓 تم فتح صلاحيات الإدارة السيادية للمكنز بنجاح!")
        st.markdown("---")
        
        # صندوق الرسائل والملاحظات في القمة العليا ليكون مرئياً فوراً أمام الدكتور رشيد دون تمرير
        st.markdown("<h4 style='color: #1E3A8A; font-weight: bold; margin-bottom: 10px;'>📬 صندوق الملاحظات ورسائل الباحثين الحية:</h4>", unsafe_allow_html=True)
        feedbacks = cursor.execute("SELECT visitor_name, visitor_email, shrine_related, feedback_text, submission_date FROM visitor_feedback ORDER BY id DESC").fetchall()
        
        if not feedbacks:
            st.info("الصندوق فارغ حالياً؛ لا توجد رسائل أو تذكيرات واردة من الزوار في قاعدة البيانات.")
        else:
            for index, (f_name, f_email, f_shrine, f_text, f_date) in enumerate(feedbacks):
                st.markdown(f"""
                <div style='background-color:#FFFFFF; border-right:4px solid #1E3A8A; padding:12px; margin-bottom:10px; border-radius:8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <span style='color:#6B7280; font-size:13px;'>📅 {f_date}</span><br>
                    <b>👤 اسم المرسل:</b> {f_name}<br>
                    <b>📌 الموضوع:</b> {f_shrine}<br>
                    <b>📝 نص الرسالة الترابية:</b> {f_text}
                </div>
                """, unsafe_allow_html=True)
                
                # فتح الـ Gmail وحقن البيانات تلقائياً بأمر الملاحة الصافي الصرف المانع للصفحة البيضاء
                subject_reply = urllib.parse.quote(f"رد من المكنز الوطني للأضرحة: ملاحظتكم حول ({f_shrine})")
                body_reply = urllib.parse.quote(f"المرسل الكريم {f_name}،\n\nنشكركم على تواصلكم العلمي الميداني مع المكنز الوطني للأضرحة بالمغرب لعام 2026.\nلقد تم تسجيل ملاحظتكم بنجاح صلب المنظومة وجاري مراجعتها وتحقيقها علمياً.\n\nمع تحيات،\nإدارة المكنز الوطني الشريف.\nالدكتور رشيد الجانبي")
                mailto_link = f"mailto:{f_email}?subject={subject_reply}&body={body_reply}"
                
                st.markdown(f'<a href="{mailto_link}" target="_self" style="text-decoration:none;"><div style="background:linear-gradient(135deg, #15803D, #16A34A); color:white; text-align:center; padding:8px; border-radius:6px; font-size:14px; font-weight:bold; margin-bottom:20px; box-shadow: 0 2px 5px rgba(22,163,74,0.2);">✉️ رد سريع ومباشر لبريد الباحث {f_name}</div></a>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<h4 style='color: #1E3A8A; font-weight: bold; margin-bottom: 10px;'>📥 بوابة ضخ ملفات الـ CSV التراكمية:</h4>", unsafe_allow_html=True)
