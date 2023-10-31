import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

class DataAvailability:
    def __init__(self):
        pass  # No data passed for the data availability page
    
    def render(self):
        st.markdown("""
        ## Data Availability 
        Welcome to the MAG-based Genome-Scale Metabolic Reconstruction Database Data Availability. This platform is designed to 
        facilitate the selection and download of the metagenome-assembled genome (MAG) based genome-scale metabolic reconstructions 
        sourced from the CLUE-TERRA consortium and the Earth's microbiome genomic catalog (GEM). Note that the genomes from 
        the CLUE-TERRA consortium will also be available on the Sequence Read Archive (SRA) for download in the coming months.

          ### Downloads
        - [Download Metabolic Reconstructions](https://www.ufz.de/record/dmp/archive/14296/en/)
        - [Download CLUE-TERRA Database](https://www.ufz.de/record/dmp/archive/14295/de/)

        """)

        st.write(
            f'<style>.dataframe tbody tr:nth-child(even) {{ background-color: #fffae6; }}</style>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    data_availability_page = DataAvailability()
    data_availability_page.render()
