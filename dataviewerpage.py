import streamlit as st
import pandas as pd
import ternary
from st_aggrid import AgGrid, GridOptionsBuilder
import dataloader  # Certifique-se de que este módulo está corretamente importado
from graphplots import GraphPlots

class DataViewerPage:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def apply_filters(self, filters):
        filtered_data = self.data.copy()
        for column_name, selected_values in filters.items():
            if selected_values:
                filtered_data = filtered_data[filtered_data[column_name].isin(selected_values)]
        return filtered_data

    def render(self):
        st.markdown("""
        <style>
            
            h2, h3 {
                color: #4f8bf9;
                font-size: 1.6rem;
            }
            .footer {
                text-align: center;
                padding: 20px;
                background-color: #f1f1f1;
                font-size: 14px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        ## Filter and Explore Datasets
        ---
        """)

        # Filters at the top
        columns_to_filter = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'database']
        col_filters = st.columns(len(columns_to_filter))

        filters = {}
        filtered_data = self.data.copy()
        for col, column_name in zip(col_filters, columns_to_filter):
            with col:
                unique_values = filtered_data[column_name].unique()
                filters[column_name] = st.multiselect(f"{column_name.capitalize()}", unique_values, [])
                filtered_data = self.apply_filters(filters)

        # Replace NaN with NA
        filtered_data.fillna("NA", inplace=True)

        # AgGrid Options
        go = GridOptionsBuilder.from_dataframe(filtered_data)
        go.configure_pagination(True)
        go.configure_side_bar()
        go.configure_column("fasta.link",
            valueGetter='return data["fasta.link"]',
            cellRenderer="""function(params) {
                return '<a href="' + params.value + '" target="_blank">Download</a>';
            }""")

        gridOptions = go.build()
        gridOptions['paginationPageSize'] = 20
        gridOptions['domLayout'] = 'autoHeight'

        AgGrid(
            filtered_data,
            gridOptions=gridOptions,
            height=600,
            width='100%',
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True  # Este parâmetro pode ser necessário para a renderização de links
        )
        graph_plots = GraphPlots(filtered_data)

        col1, col2 = st.columns(2)

        with col1:
            fig = graph_plots.ternary_plot()
            st.pyplot(fig, use_container_width=True)

        with col2:
            kde_figures = graph_plots.kde_plots()
            for fig in kde_figures:
                st.pyplot(fig)

        csv_data = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

        

        st.markdown('<div class="footer">© 2023 MAG-based Genome-Scale Metabolic Reconstruction Database</div>', unsafe_allow_html=True)
@st.cache
def load_and_filter_data():
    df = dataloader.load_data()  # Carrega os dados uma única vez
    return df

if __name__ == "__main__":
    # Sample data
    df = load_and_filter_data() # Este método deve ser definido no módulo 'dataloader'

    data_viewer = DataViewerPage(df)
    data_viewer.render()
