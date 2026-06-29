import streamlit as st
import os
import base64

# 🇲🇦 1. Configuration de la page étendue à 100% (Plein écran)
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# 🎨 2. Injection du style CSS pour fixer le menu de la "Chamila" en haut de l'image
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* Suppression totale des marges blanches pour coller l'image aux bords de l'écran */
        div[data-testid="stAppViewBlockContainer"] {
            max-width: 100% !important;
            width: 100% !important;
            padding: 0rem !important; 
        }
        
        /* Neutralisation des espaces verticaux entre les blocs Streamlit */
        div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
        
        /* Style des boutons horizontaux épurés et discrets inspiré de la Maktaba Chamila */
        .shamel-nav-btn button {
            background: rgba(0, 0, 0, 0.5) !important; /* Fond sombre translucide pour détacher le texte */
            color: #FFFFFF !important; /* Texte blanc pur */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 4px !important; /* Coins carrés classiques style officiel */
            padding: 6px 24px !important;
            backdrop-filter: blur(5px) !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer;
            margin: 0px auto !important;
            display: block !important;
        }
        
        /* Effet au survol : Éclat Vert Émeraude National */
        .shamel-nav-btn button:hover {
            background: #10B981 !important; 
            color: #FFFFFF !important;
            border-color: #10B981 !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.45) !important;
            transform: translateY(-1px);
        }

        /* Alignements linguistiques généraux */
        html, body, .stMarkdown, p, span, label {
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# 🏢 3. Encodage et affichage de la bannière royale en plein écran (Base64 sécurisé)
banner_path = "banner.png"

if os.path.exists(banner_path):
    with open(banner_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Projection de l'image de fond
    st.markdown(f"""
    <div style='position: relative; width: 100%; text-align: center; margin: 0; padding: 0;'>
        <img src='data:image/png;base64,{encoded_string}' style='width: 100%; height: auto; display: block; margin: 0; padding: 0;'>
    </div>
    """, unsafe_allow_html=True)
    
    # Incrustation du menu horizontal sur la gauche tout en haut de l'image
    st.markdown("<div style='position: absolute; top: 25px; right: 50px; left: 50px; z-index: 99999;'>", unsafe_allow_html=True)
    menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.7, 3.5])
    
    with menu_col_1:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("الرئيسية", key="btn_home"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_2:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("أقسام المكنز", key="btn_sections"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_3:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("حول المكنز", key="btn_about"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_4:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("اتصل بنا", key="btn_contact"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_5:
        st.markdown("<div class='shamel-nav-btn'>", unsafe_allow_html=True)
        if st.button("🔍 شعار البحث في المكنز", key="btn_search"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown('<div style="background-color:#1E3A8A; color:white; padding:40px; text-align:center; font-family:\'Reem Kufi\'; font-size:24px;">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</div>', unsafe_allow_html=True)
