"""
Data visualization module for nutritional analysis.

This module provides methods for displaying and visualizing nutritional data,
including text-based statistics displays and matplotlib-based charts.

Classes:
    DataVisualizer: Creates text displays and charts for nutritional data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataVisualizer:
    """
    Visualizes nutritional data through text displays and charts.
    
    Provides methods for:
    - Printing formatted descriptive statistics
    - Printing dataset comparisons
    - Generating descriptive statistics visualizations
    - Generating comparison visualizations
    """

    def __init__(self):
        """Initialize DataVisualizer."""
        pass


    def print_descriptive_stats(self, datasets_dict):
        """
        Print formatted descriptive statistics for all datasets.
        
        Displays basic statistics (count, mean, std, min, max, quartiles) and
        calculated ratios for each category in a readable format.
        
        Args:
            datasets_dict (dict): Dictionary containing statistics for each category.
                Expected structure: {
                    'category': {
                        'describe': pd.DataFrame,
                        'ratio': {'ratio_name': value, ...}
                    }
                }
        """
                
        # check if theres any descriptive stats to display
        if len(datasets_dict) == 0:
            print("No data to display.\n")
            return
        

        # print the descriptive stats, one for every category
        for catergory, stats_df in datasets_dict.items():
            print("\n")
            print("="*80)
            print(f"{catergory.upper()} DESCRIPTIVE STATISTICS")
            print("="*80)

            print("\nBasic Statistics:")
            print(stats_df['describe'].round(2))

            print("\nRatios:")
            for ratio_name, ratio_value in stats_df['ratio'].items():
                print(f"  {ratio_name:<16}: {ratio_value:.2f}")


    def print_comparison(self, comparison_dict, metrics=None):
        """
        Print side-by-side comparison of datasets.
        
        Displays comparison tables for specified metrics, making it easy to
        compare nutritional values across categories.
        
        Args:
            comparison_dict (dict): Comparison data from DataProcessor.compare_datasets()
            metrics (list, optional): List of metrics to display
                (e.g., ['mean', 'min', 'max']). If None, displays all available metrics.
        """
               
        # check if theres any comparison stats to display
        if len(comparison_dict) == 0:
            print("No comparison data to display.")
            return
        
        # title
        print("\n")
        print("="*80)
        print("DATASETS COMPARISON")
        print("="*80)

        # default metrics if none is defined
        # otherwise the stated metrics will be used
        # and only the stated metrics data will be displayed
        if metrics == None:
            metrics = ['count', 'mean', 'std', 'min', 'max', '25%', '50%', '75%']

        # get the list of catergories and nutrients
        categories = list(comparison_dict.keys())
        nutrients = list(comparison_dict[categories[0]].keys())

        # for every metric, print the comparison of nutrients between categories
        for metric in metrics:
            to_print = {}
            for category in categories:
                    to_print[category] = {}

                    for nutrient in nutrients:
                        to_print[category][nutrient] = comparison_dict[category][nutrient][metric]

            to_print_df = pd.DataFrame(to_print)

            print("\n")
            print("-"*80)
            print(f"{metric.upper()} COMPARISON") # subtitle
            print("-"*80)
            print(to_print_df)

        print("\n")


    def plot_descriptive_stats(self, datasets_dict, metrics=None, output_filename = "descriptive_stats_bar_chart.png"):
        """
        Create bar chart visualizations of descriptive statistics.
        
        Generates grouped bar charts showing specified metrics for each nutrient,
        with one subplot per category. Charts are saved as PNG files and displayed.
        
        Args:
            datasets_dict (dict): Statistics dictionary from calculate_descriptive_stats()
            metrics (list, optional): Metrics to plot (e.g., ['mean', 'max']).
                If None, plots all available metrics.
            output_filename (str, optional): Filename for saved chart.
                Default is 'descriptive_stats_bar_chart.png'
        """
         
        # check if theres any descriptive stats to plot
        n = len(datasets_dict)
        if n == 0:
            print("No data to plot.\n")
            return
        
        # create subplots based on the number of categories
        rows = n
        cols = 1
        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
        
        # for single subplots, axes is just a single object, rather than an array
        # to be able to index it later on, we need to convert it into a list
        if n == 1:
            axes = [axes]

        # default metrics
        # otherwise the stated metrics will be used
        # and only the stated metrics data will be displayed
        if metrics == None:
            metrics = ['count', 'mean', 'std', 'min', 'max', '25%', '50%', '75%']
        
        # plot the descriptive stats bar chart for every catergory
        for i, (category, stats_df) in enumerate(datasets_dict.items()):
            ax = axes[i]

            describe_df = stats_df["describe"]
            self.plot_single_dataset_stats_bar(ax, category, describe_df, metrics) # helper function to plot each subplots

        # auto adjust subplot spacing to prevent overlapping of details
        plt.tight_layout()
        
        # save the figure to the state output filename
        # if none is state, a default filename will be used
        plt.savefig(output_filename, dpi=200) 
        print(f"Bar chart generated for comparison statistics, successfully saved as {output_filename}\n")

        # show the figure to screen
        plt.show()
    

    @staticmethod
    def plot_single_dataset_stats_bar(ax, category, describe_df, metrics):
        """
        Helper function to plot grouped bar chart for a single dataset's statistics.
        
        Helper method that creates a bar chart with nutrients on x-axis and
        different metrics shown as grouped bars.
        
        Args:
            ax (matplotlib.axes.Axes): Subplot axes to draw on
            category (str): Category name for the title
            describe_df (pd.DataFrame): DataFrame from pd.DataFrame.describe()
            metrics (list): List of metric names to plot
        """

        # extract the available nutrients columns
        nutrients = describe_df.columns.tolist()

        # compute bar width and positions based on the number of nutrients and metrics
        num_nutrients = len(nutrients)
        num_metrics = len(metrics)
        x_pos = np.arange(num_nutrients) # creates the position for each nutrients on the x axis
        bar_width = 0.8 / num_metrics # bar width for each of the metric for the nutrient

        # define the available colors for the bar of the bar chart
        colors = ["#ff0000", "#0033ff", "#00ff00", "#ff8000", "#ff0080", "#8000ff", "#fffb00", "#00f7ff"]

        # for each metric, plot the bar
        for i, metric in enumerate(metrics):
            if metric in describe_df.index:
                values = [describe_df.loc[metric, nutrient] for nutrient in nutrients] # extract metrics value for all the available nutrient column
                offset = (i - num_metrics/2) * bar_width + bar_width/2 # compute the bar offset to center around the x axis
                ax.bar(x_pos + offset, values, bar_width, label=metric.capitalize(), color=colors[i]) # plot the bar with the values, offset and color

        # formatting
        ax.set_xlabel('Nutrients', fontsize=10, fontweight='bold')
        ax.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax.set_title(f'{category.upper()} - NUTRITIONAL STATISTICS', fontsize=13, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(nutrients)

        ax.legend(loc='best') # ensures the best location for legend to prevent it from overlapping/covering data
        ax.grid(axis='y') # create grid along the y axis for easier visual reading


    def plot_comparison_stats_bar(self, comparison_dict, metrics=None, output_filename = "comparison_stats_bar_chart.png"):
        """
        Creates bar chart comparing datasets across metrics.
        
        Generates side-by-side bar charts comparing categories for each metric.
        Each subplot shows one metric with nutrients on x-axis and categories
        as grouped bars.
        
        Args:
            comparison_dict (dict): Comparison data from DataProcessor.compare_datasets()
            metrics (list, optional): Metrics to plot. If None, plots all metrics.
            output_filename (str, optional): Filename for saved chart.
                Default is 'comparison_stats_bar_chart.png'
        """

        # check if theres any comparison stats to plot
        if len(comparison_dict) == 0:
            print("No comparison data to plot.")
            return
        
        # default metrics
        # otherwise the stated metrics will be used
        # and only the stated metrics data will be displayed
        if metrics == None:
            metrics = ['count', 'mean', 'std', 'min', 'max', '25%', '50%', '75%']

        # create subplots
        num_metrics = len(metrics)
        rows = 1
        cols = num_metrics
        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
        
        # for single subplots, axes is just a single object, rather than an array
        # to be able to index it later on, we need to convert it into a list
        if num_metrics == 1:
            axes = [axes]
        
        # extract the available catergories and nutrients
        categories = list(comparison_dict.keys())
        first_category_dict = list(comparison_dict.values())[0]
        nutrients = list(first_category_dict.keys())
        
        # for each metric, plot a comparison bar chart
        for i, metric in enumerate(metrics):
            ax = axes[i]
            self.plot_single_comparison_metric(ax, comparison_dict, categories, nutrients, metric)
        
        # auto adjust subplot spacing to prevent overlapping of details
        plt.tight_layout()

        # save the figure to the state output filename
        # if none is state, a default filename will be used
        plt.savefig(output_filename, dpi=200)
        print(f"Bar chart generated for comparison statistics, successfully saved as {output_filename}\n")

        # show the figure to screen
        plt.show()        


    @staticmethod
    def plot_single_comparison_metric(ax, comparison_dict, categories, nutrients, metric):
        """
        Helper function to plot comparison bar chart for a single metric.
        
        Helper method that creates a grouped bar chart comparing categories
        for one specific metric across all nutrients.
        
        Args:
            ax (matplotlib.axes.Axes): Subplot axes to draw on
            comparison_dict (dict): Full comparison data structure
            categories (list): List of category names
            nutrients (list): List of nutrient names
            metric (str): Metric name to plot (e.g., 'mean', 'max')
        """
                
        # compute bar width and positions based on the number of nutrients and categories
        num_nutrients = len(nutrients)
        num_categories = len(categories)
        x_pos = np.arange(num_nutrients) # creates the position for each nutrients on the x axis
        bar_width = 0.8 / num_categories # bar width for each of the categories
        
        # define the available colors for the bar of the bar chart
        colors = ["#ff0000", "#0033ff", "#00ff00", "#ff8000", "#ff0080", "#8000ff", "#fffb00", "#00f7ff"]
        
        # for each category, plot the bar
        for i, category in enumerate(categories):
            values = [comparison_dict[category][nutrient].get(metric, np.nan) for nutrient in nutrients] # extract metrics value for all the available nutrient column for that category, NaN value if metric doesnt exist
            offset = (i - num_categories/2) * bar_width + bar_width/2
            ax.bar(x_pos + offset, values, bar_width, label=category.capitalize(), color=colors[i])
        
        # formatting
        ax.set_xlabel('Nutrients', fontsize=10, fontweight='bold')
        ax.set_ylabel(f'{metric.capitalize()} Value', fontsize=10, fontweight='bold')
        ax.set_title(f'{metric.upper()} COMPARISON', fontsize=13, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(nutrients)

        ax.legend(loc='best') # ensures the best location for legend to prevent it from overlapping/covering data
        ax.grid(axis='y') # create grid along the y axis for easier visual reading


