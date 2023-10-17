import streamlit as st
from streamlit_option_menu import option_menu
from homepage import HomePage
from dataviewerpage import DataViewerPage
import dataloader
from advancedsearch import AdvancedSearchPage
from contact import ContactPage
from helppage import HelpPage
from interactivechart import InteractiveChartPage

# Defina a configuração da página como a primeira chamada
st.set_page_config(layout="wide")

# CSS para estilização
st.markdown("""
<style>
    body {
        font-family: "Arial", sans-serif;  /* Fonte padronizada */
        color: #fff;
        background-color: #4f8bf9;
    }
    h1, h2, h3 {
        font-weight: bold;  /* Títulos em negrito */
    }
    h1 {
        color: #ffaa1c;
        margin-top: 0px !important;
    }
    a {
        text-decoration: none;  /* Remover sublinhado dos links */
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 95%;
        background-color: white;
        padding: 10px 0;
    }
    .footer p {
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def display_info():
    st.markdown("## Subtitle")
    st.write("Explore bacterial and archaeal metagenome-assembled genome (MAG) based genome-scale metabolic reconstructions (GSMRs).")
    
    st.markdown("### About")
    st.write("""
    We developed the MAG-based Genome-Scale Metabolic Reconstruction Database to facilitate the selection and download of the metagenome-assembled genome (MAG) based genome-scale metabolic reconstructions that were created from MAGs deposited in the [CLUE-TERRA consortium](https://www.ufz.de/index.php?en=47300) and the [Earth's microbiome genomic catalog (GEM)](https://doi.org/10.1038/s41587-020-0718-6).

    The MAG-based Genome-Scale Metabolic Reconstruction Database (Release 1.0) contains the [GTDB-tk determined taxonomic classifications](https://doi.org/10.1093/bioinformatics/btac672), MAG quality and technical data from [CheckM](https://doi.org/10.1101%2Fgr.186072.114) and the [BioInfoTools BBMap genome statistics tool](https://github.com/BioInfoTools/BBMap/blob/master/sh/stats.sh), and metabolic reconstruction quality parameters from [MEMOTE](https://www.nature.com/articles/s41587-020-0446-y) for 68,679 MAG-based metabolic reconstructions.

    The Quick Search and Advanced Search tabs allow users to select MAG-based metabolic reconstructions of interest. The download tool allows easy download of the source MAG sequence assemblies and the resulting genome-scale metabolic reconstructions.
    """)

def display_footer():
    st.write("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("nfdi4microbiota_Logo_new.png", width=200)
    with col2:
        st.image("ufz_med_trans.png", width=300)
    with col3:
        st.image("uni_leipzig_logo_trans.png", width=285)
    with col4:
        st.image("icmc_big_trans.png", width=222)
    
    footer_html = """
        <style>
            .footer {
                display: flex;
                justify-content: center;  /* Centralizar texto */
                align-items: center;
            }
            .footer p {
                font-size: 14px;  /* Tamanho menor de fonte */
                color: #888;  /* Cor de fonte cinza */
            }
        </style>
        <div class="footer">
            <hr style="margin-top: 0;">
            <p>© 2023 MAG-based Genome-Scale Metabolic Reconstruction Database</p>
        </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

df = dataloader.load_data()

st.title("MAG-based Genome-Scale Metabolic Reconstruction Database")

menu_items = ["Home", "Quick Search", "Advanced Search", "Help", "Contact", "Interactive Graphics"]
icons_list = ['house', 'eye', 'search', 'question-circle', 'envelope', 'bar-chart']

if 'page' not in st.session_state:
    st.session_state.page = "Home"

selected_page = option_menu(None, menu_items, icons=icons_list, menu_icon="bars", default_index=menu_items.index(st.session_state.page), orientation="horizontal")
st.session_state.page = selected_page

if st.session_state.page == "Home":
    display_info()
elif st.session_state.page == "Quick Search":
    data_viewer = DataViewerPage(df)
    data_viewer.render()
elif st.session_state.page == "Advanced Search":
    advanced_search_page = AdvancedSearchPage(df)
    advanced_search_page.render()
elif st.session_state.page == "Help":
    help_page = HelpPage()
    help_page.render()
elif st.session_state.page == "Contact":
    contact_page = ContactPage()
    contact_page.render()
elif st.session_state.page == "Interactive Graphics":
    interactive_page = InteractiveChartPage(df)
    interactive_page.render()

# Exiba o rodapé
display_footer()
