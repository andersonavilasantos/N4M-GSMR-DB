import streamlit as st
import pandas as pd
import ternary
from st_aggrid import AgGrid, GridOptionsBuilder
import dataloader  # Certifique-se de que este módulo está corretamente importado
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

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

        # Ternary Plot
        df_ternary = filtered_data[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield', 'rk.index']].copy()

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
      
        csv_data = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

        

        st.markdown('<div class="footer">© 2023 MAG-based Genome-Scale Metabolic Reconstruction Database</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Sample data
    df = dataloader.load_data()  # Este método deve ser definido no módulo 'dataloader'

    data_viewer = DataViewerPage(df)
    data_viewer.render()
