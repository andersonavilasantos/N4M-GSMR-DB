import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import dataloader
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import ternary

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


        # Ternary Plot
        df_ternary = self.filtered_data[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield', 'rk.index']].copy()

        # Convert to float
        for column in df_ternary.columns:
            df_ternary[column] = pd.to_numeric(df_ternary[column], errors='coerce')

        # Drop NaN values
        df_ternary.dropna(inplace=True)

        # Normalize the data
        df_ternary[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield']] = df_ternary[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield']].div(df_ternary[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield']].sum(axis=1), axis=0)

        # Normalize the rk.index values for color mapping
        norm = mcolors.Normalize(vmin=df_ternary['rk.index'].min(), vmax=df_ternary['rk.index'].max())
        colormap = cm.ScalarMappable(norm=norm, cmap=cm.RdYlGn)
        colors = df_ternary['rk.index'].apply(lambda x: colormap.to_rgba(x))

        # Create a figure using matplotlib
        fig, ax = plt.subplots(figsize=(5, 3.5), dpi=150)  # Ajustado para tornar o plot menor

        # Pass the ax to ternary for plotting
        tax = ternary.TernaryAxesSubplot(ax=ax, scale=1)

        tax.scatter(df_ternary[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield']].values, marker='o', color=colors, edgecolor='black')
        tax.gridlines(multiple=0.1, color="gray")

        # Adiciona os números aos eixos
        tax.ticks(axis='lbr', multiple=0.2, linewidth=1, tick_formats="%.1f")

        tax.get_axes().axis('off')
        tax.boundary(linewidth=1.0)

        # Set labels for the axes
        # Set labels for the axes
        fontsize = 12
        tax.set_title("Ternary plot with coordinates of the individual r/K-index features", fontsize=16, y=1.08)
        tax.left_axis_label('Maximum biomass flux', fontsize=fontsize, offset=0.12)  # Ajustado para corresponder aos rótulos definidos em tax.ticks()
        tax.right_axis_label('Growth yield', fontsize=fontsize, offset=0.12)  # Ajustado para corresponder aos rótulos definidos em tax.ticks()
        tax.bottom_axis_label('Number of C-containing metabolites', fontsize=fontsize, offset=0.12)  # Ajustado para corresponder aos rótulos definidos em tax.ticks()

        # Add a colorbar to indicate the rk.index values
        cbar = fig.colorbar(colormap, ax=ax, orientation='vertical', fraction=0.04, pad=0.1)
        cbar.set_label('rk.index', fontsize=12)

        st.pyplot(fig, use_container_width=False)

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
