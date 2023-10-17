import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dataloader
import plotly.express as px  

class InteractiveChartPage:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.chart_types = ['Bar Chart', 'Scatter Plot', 'Box Plot', 'Sunburst Chart', 'Genome Quality Bar Plot', 'Metabolism Histogram']
        self.selected_chart_type = None
        self.x_column = None
        self.y_column = None
        self.plot_functions = {
            'Bar Chart': self.plot_bar_chart,
            'Scatter Plot': self.plot_scatter_plot,
            'Box Plot': self.plot_boxplot,
            'Sunburst Chart': self.plot_sunburst_chart,
            'Genome Quality Bar Plot': self.plot_genome_quality_bar_plot,
            'Metabolism Histogram': self.plot_metabolism_histogram
        }

    def render(self):
        st.title('Interactive Chart Page')
        self.selected_chart_type = st.selectbox('Select chart type:', self.chart_types)
        
        available_x_columns = self.get_available_columns_for_x()
        self.x_column = st.selectbox('Select X-axis column:', available_x_columns)
        
        if self.selected_chart_type in ['Scatter Plot', 'Box Plot']:
            available_y_columns = self.get_available_columns_for_y()
            self.y_column = st.selectbox('Select Y-axis column:', available_y_columns)
        elif self.selected_chart_type == 'Sunburst Chart':
            self.sunburst_columns = st.multiselect('Select hierarchical columns:', self.data.columns, default=self.data.columns[:2].tolist())


        if st.button('Generate Chart'):
            self.generate_chart()

    def get_available_columns_for_x(self):
        if self.selected_chart_type in ['Scatter Plot', 'Box Plot']:
            return [col for col in self.data.columns if self.is_numeric(col)]
        elif self.selected_chart_type == 'Genome Quality Bar Plot':
            return ['mag']  # Example, based on your data structure
        elif self.selected_chart_type == 'Metabolism Histogram':
            return ['mets_coverage']  # Example, based on your data structure
        return list(self.data.columns)

    def get_available_columns_for_y(self):
        if self.selected_chart_type in ['Scatter Plot', 'Box Plot']:
            return [col for col in self.data.columns if self.is_numeric(col)]
        return []

    def generate_chart(self):
        valid, error_msg = self.validate_columns()
        if not valid:
            st.warning(error_msg)
            return

        st.subheader(f'{self.selected_chart_type} for columns: {self.x_column} vs {self.y_column if self.y_column else ""}')
        self.plot_functions[self.selected_chart_type]()


    def validate_columns(self):
        if self.selected_chart_type == 'Scatter Plot':
            if not (self.is_numeric(self.x_column) and self.is_numeric(self.y_column)):
                return False, "Both X and Y columns must be numeric for a scatter plot."
        elif self.selected_chart_type == 'Box Plot':
            if not self.is_numeric(self.y_column):
                return False, "The Y column must be numeric for a box plot."
        return True, ""

    def is_numeric(self, column):
        return self.data[column].dtype in ['int64', 'float64']

    def plot_bar_chart(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        top_12 = self.data[self.x_column].value_counts().nlargest(12).index
        filtered_data = self.data[self.data[self.x_column].isin(top_12)]
        sns.countplot(data=filtered_data, x=self.x_column, order=top_12, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

    def plot_scatter_plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=self.data, x=self.x_column, y=self.y_column, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

    def plot_boxplot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=self.data, x=self.x_column, y=self.y_column, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

    # As seguintes funções foram adicionadas para as visualizações propostas:
    
    def plot_sunburst_chart(self):
        if len(self.sunburst_columns) < 2:
            st.warning("Please select at least two hierarchical columns for the sunburst chart.")
            return
        fig = px.sunburst(self.data, path=self.sunburst_columns, maxdepth=-1)
        st.plotly_chart(fig)

    def plot_genome_quality_bar_plot(self):
        fig = px.bar(self.data, x='mag', y=['completeness', 'contamination', 'quality.score'])
        st.plotly_chart(fig)

    def plot_metabolism_histogram(self):
        fig = px.histogram(self.data, x='mets_coverage')
        st.plotly_chart(fig)

if __name__ == '__main__':
    data = dataloader.load_data()
    page = InteractiveChartPage(data)
    page.render()
