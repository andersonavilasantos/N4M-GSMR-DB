import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import dataloader

class AdvancedSearchPage:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.filtered_data = data.copy()
        self.filters = {}

    def apply_filters(self):
        for column, selected_values in self.filters.items():
            self.filtered_data = self.filtered_data[self.filtered_data[column].isin(selected_values)]

    def display_filters(self):
        if not self.filters:
            return
        st.markdown("### Applied Filters")
        for col, vals in self.filters.items():
            st.write(f"- {col}: {', '.join(vals)}")

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
        ## Filter and Find Specific Records
        ---
        """)

        # Select multiple columns to filter
        selected_columns = st.multiselect("Select columns to filter", self.data.columns)

        # Create filters for selected columns
        for col in selected_columns:
            selected_values = st.multiselect(f"Filter by {col}", self.data[col].unique())
            if selected_values:
                self.filters[col] = selected_values

        self.display_filters()
        self.apply_filters()

        # Replace NaN with NA
        self.filtered_data.fillna("NA", inplace=True)

        # AgGrid Options
        go = GridOptionsBuilder.from_dataframe(self.filtered_data)
        go.configure_pagination(True)
        go.configure_side_bar()
        
        # Directly adding pagination settings to the grid options
        gridOptions = go.build()
        gridOptions['paginationPageSize'] = 20
        gridOptions['domLayout'] = 'autoHeight'

        AgGrid(
            self.filtered_data,
            gridOptions=gridOptions,
            height=600, 
            width='100%',
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True
        )

        # Download button for the filtered data as CSV
        csv_data = self.filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
        
        #st.markdown('<div class="footer">© 2023 MAG-based Genome-Scale Metabolic Reconstruction Database</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Sample data
    df = dataloader.load_data()

    advanced_search = AdvancedSearchPage(df)
    advanced_search.render()
