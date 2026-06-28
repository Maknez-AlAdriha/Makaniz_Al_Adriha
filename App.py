import streamlit as st
import sqlite3
import pandas as pd
import os
import datetime
import shutil
import io
import urllib.parse

# 🇲🇦 1. Configuration de la page étendue à 100% de la largeur du navigateur (Année 2026)
st.set_page_config(page_title="المكنز الوطني للأضرحة والمزارات بالمغرب", layout="wide")

# Connexion stable au référentiel SQL de l'أطروحة
conn = sqlite3.connect("maroccan_shrines_ultimate_thesaurus.db", check_same_thread=False)
cursor = conn.cursor()

# 🎨 2. Injection du style CSS pour intégrer le menu horizontal de la "Chamila" tout en haut de l'image
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
        
        /* Alignement horizontal fluide du menu en haut (Overlaid Ribbon) */
        .shamel-nav-btn button {
            background: rgba(0, 0, 0, 0.35) !important; /* Fond sombre translucide très fin */
            color: #FFFFFF !important; /* Texte blanc pur texturé */
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700 !important;
            font-size: 17px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 4px !important; /* Coins légèrement carrés style classique */
            padding: 6px 22px !important;
            backdrop-filter: blur(5px) !important; /* Effet de flou sur l'arrière-plan de l'image */
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
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
            transform: translateY(-1px);
        }

        /* Tonalités de la barre de défilement latérale */
        html::-webkit-scrollbar, body::-webkit-scrollbar { width: 32px !important; }
        html::-webkit-scrollbar-thumb, body::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #1E3A8A, #10B981) !important;
            border-radius: 16px !important;
            border: 6px solid #FFFFFF !important;
        }
        
        /* Alignements linguistiques généraux */
        html, body, .stMarkdown, p, span, label, select, input, textarea {
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# 🏢 6. Déploiement de l'image de fond et superposition du menu d'accès aux fiches
banner_path = "banner.png"
if os.path.exists(banner_path):
    # Conteneur parent relatif pour verrouiller l'alignement
    st.markdown("<div style='position: relative; width: 100%;'>", unsafe_allow_html=True)
    
    # Création du ruban de navigation (Incrustation en haut à gauche de l'image)
    # Laisse l'espace libre au centre pour afficher la calligraphie et à droite pour le drapeau
    menu_col_1, menu_col_2, menu_col_3, menu_col_4, menu_col_5, _ = st.columns([1.1, 1.3, 1.3, 1.2, 1.7, 3.5])
    
    with menu_col_1:
        st.markdown("<div class='shamel-nav-btn' style='position: absolute; top: 20px; z-index: 999;'>", unsafe_allow_html=True)
        if st.button("الرئيسية", key="shamel_home_fixed"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_2:
        st.markdown("<div class='shamel-nav-btn' style='position: absolute; top: 20px; z-index: 999;'>", unsafe_allow_html=True)
        btn_lbl = "إغلاق الأقسام" if st.session_state.sidebar_visible else "أقسام المكنز"
        if st.button(btn_lbl, key="shamel_sections_fixed"):
            st.session_state.sidebar_visible = not st.session_state.sidebar_visible
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_3:
        st.markdown("<div class='shamel-nav-btn' style='position: absolute; top: 20px; z-index: 999;'>", unsafe_allow_html=True)
        if st.button("حول المشروع", key="shamel_about_fixed"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "about"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_4:
        st.markdown("<div class='shamel-nav-btn' style='position: absolute; top: 20px; z-index: 999;'>", unsafe_allow_html=True)
        if st.button("اتصل بنا", key="shamel_contact_fixed"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "contact"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with menu_col_5:
        st.markdown("<div class='shamel-nav-btn' style='position: absolute; top: 20px; z-index: 999;'>", unsafe_allow_html=True)
        if st.button("🔍 البحث في المكنز", key="shamel_search_fixed"):
            st.session_state.sidebar_visible = False
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Projection plein écran de votre magnifique visuel national
    st.image(banner_path, use_container_width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown('<div style="background-color:#1E3A8A; color:white; padding:40px; text-align:center; font-family:\'Reem Kufi\'; font-size:28px;">المَكْنِزُ الوَطَنِيُّ لِلأَضْرِحَةِ وَالمَزَارَاتِ بِالمَغْرِبِ</div>', unsafe_allow_html=True)

# Isolation hermétique de l'espace inférieur pour accueillir les fiches A4 et l'atlas
st.markdown("<div style='padding: 2rem;'>", unsafe_allow_html=True)
