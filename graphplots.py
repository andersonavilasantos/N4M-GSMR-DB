import streamlit as st
import pandas as pd
import ternary
from st_aggrid import AgGrid, GridOptionsBuilder
import dataloader  # Certifique-se de que este módulo está corretamente importado
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import plotly.graph_objects as pgo
import seaborn as sns
import numpy as np

class GraphPlots:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def ternary_plot(self):
        df_ternary = self.data[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield', 'rk.index']].copy()

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
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)

        # Pass the ax to ternary for plotting
        tax = ternary.TernaryAxesSubplot(ax=ax, scale=1)

        tax.scatter(df_ternary[['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield']].values, marker='o', color=colors, edgecolor='black')
        tax.gridlines(multiple=0.1, color="gray")
        tax.ticks(axis='lbr', multiple=0.2, linewidth=1, tick_formats="%.1f")
        tax.get_axes().axis('off')
        tax.boundary(linewidth=1.0)
        
        fontsize = 12
        tax.set_title("Ternary plot r/K-index", fontsize=16, y=1.08)
        tax.left_axis_label('Maximum biomass flux', fontsize=fontsize, offset=0.12)
        tax.right_axis_label('Growth yield', fontsize=fontsize, offset=0.12)
        tax.bottom_axis_label('Number of C-containing metabolites', fontsize=fontsize, offset=0.12)

        # Add a colorbar to indicate the rk.index values
        cbar = fig.colorbar(colormap, ax=ax, orientation='vertical', fraction=0.04, pad=0.1)
        cbar.set_label('rk.index', fontsize=12)

        return fig

    def kde_plots(self):
        df = self.data.copy()
        
        # Convert the columns to numeric
        columns_to_plot = ['max.growth.minmedia', 'num.minmedia.C.mets', 'growth.yield', 'rk.index']
        labels = {
            'rk.index': 'r/K-index',
            'max.growth.minmedia': 'Maximum biomass flux',
            'growth.yield': 'Growth yield',
            'num.minmedia.C.mets': 'Number of C-containing metabolites'
        }
        
        # Convert to float and drop NaN
        for col_name in columns_to_plot:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
        df.dropna(subset=columns_to_plot, inplace=True)

        figures = []
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

        for i in range(0, 4, 2):  # i takes values 0 and 2
            fig, axes = plt.subplots(1, 2, figsize=(8, 3)) 
            for j, ax in enumerate(axes):  # j takes values 0 and 1
                idx = i + j
                col_name = columns_to_plot[idx]
                if col_name == "growth.yield":
                    sns.kdeplot(np.log10(df[col_name]), fill=True, color=colors[idx], lw=1.5, ax=ax)
                    ax.set_xlim(np.log10(0.1), np.log10(1000))
                    ax.set_xticks(np.log10([0.1, 1, 10, 100, 1000]))
                    ax.set_xticklabels([0.1, 1, 10, 100, 1000])
                else:
                    sns.kdeplot(df[col_name], fill=True, color=colors[idx], lw=1.5, ax=ax)
                
                ax.set_title(labels[col_name], fontsize=14)
                ax.set_xlabel(labels[col_name], fontsize=12)
                ax.set_ylabel('Density', fontsize=12)
            plt.tight_layout()
            
            figures.append(fig)
        
        return figures