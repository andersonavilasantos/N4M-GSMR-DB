import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

class HelpPage:
    def __init__(self):
        pass  # No data passed for the help page
    
    def render(self):
        st.markdown("""
        ## Help Page
        Welcome to the MAG-based Genome-Scale Metabolic Reconstruction Database Help Page. Here, you'll find information on how to use the database effectively.

        ### 1. Home
        The MAG-based Genome-Scale Metabolic Reconstruction Database user interface is divided into "Quick search" and "Advanced search" sections to help users choose a section that better fits their needs. The first section, “Quick search”, holds the full content of the databases’ current version, as well as the ability to filter the samples through their main characteristics. The “Advanced search” section dynamically generates filters for all the available features of the complete dataset, allowing the user to search for specific attributes.

        ### 2. How to use the Quick search?
        The “Quick Search” is available for users to access the full content of MAG-based Genome-Scale Metabolic Reconstruction Database and filter the dataset according to the main available features.

        - **Example usage:**
            - All MAGs and metabolic reconstructions are included in the “Quick Search” section, including the ones without valid features.
            - One can filter the entries by using the available main filters or typing in the search box at the top of the table.
            - You can further explore your selection by clicking the “Visualize” button. After filtering, you can download the data of your selected entries as a comma-separated values (.csv) file.

        ### 3. How to use the Advanced search?
        The “Advanced Search” tab dynamically generates filters for all the available features of the complete dataset since not all the filters are present in the “Quick Search” tab. The checkbox allows the users to decide if they want to filter out samples with missing values for the selected attributes.

        - **Example usage:**
            - Click on “Search and add filters” and a window will open.
            - One can search for the available features either by name or by category. Click “Add filter” once you found the filters you would like to use.
            - Use the selected features to subset the MAGs and metabolic reconstructions.
            - Click the available checkbox if you would like to keep the samples with missing values.
            - You can further filter the entries by typing in the search box placed at the top right of the table or by using the filter boxes present at the top of each column.
            - You can further explore your selection by clicking the “Visualize” button.
            - After filtering your dataset, you can download the data of your selected entries as a comma-separated values (.csv) file.

        ### 4. How to download a metagenome-assembled genome?
        We do not store the MAG sequence assemblies in our database. However, we created a graphical user interface (GUI) and script that makes it easy to download them directly from a data table downloaded from the database. You can find the GUI/script on the GitHub page of our research group [https://github.com/mdsufz].

        - **Usage:**
            - You may use our Python scripts on all operating systems. For Windows (Win10), we recommend using the Windows executable provided for easy use without installing Python or any dependencies. To use it, when executing download_gui.exe, you have to select the file with the mgsmrdb_selected_dataset.csv and execute it. You can download the graphical user interface for Windows by clicking on the “Download assemblies” button located on the other tabs of the database.

        ### 5. How to download a metabolic reconstruction?
        We do not store the metabolic reconstructions in our database. However, we created a graphical user interface (GUI) and script that makes it easy to download them directly from a data table downloaded from the database. You can find the GUI/script on the GitHub page of our research group [https://github.com/mdsufz].

        - **Usage:**
            - You may use our Python scripts on all operating systems. For Windows (Win10), we recommend using the Windows executable provided for easy use without installing Python or any dependencies. To use it, when executing download_gui.exe, you have to select the file with the mgsmrdb_selected_dataset.csv and execute it. You can download the graphical user interface for Windows by clicking on the “Download reconstructions” button located on the other tabs of the database.

        ### 6. What does each attribute of the database mean?
        To understand the meaning of each attribute in the database, refer to the table below:

        """)

        # Load the CSV file into a DataFrame
        csv_filename = "resource.data.headers.csv"
        df = pd.read_csv(csv_filename, sep='\t')  # Use '\t' as the separator
     

        # Customize the table style
        st.table(df)

        st.write(
            f'<style>.dataframe tbody tr:nth-child(even) {{ background-color: #fffae6; }}</style>',
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    help_page = HelpPage()
    help_page.render()
