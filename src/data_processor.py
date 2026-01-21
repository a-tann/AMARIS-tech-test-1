"""
Data processing module for nutritional analysis.

This module provides statistical analysis and filtering capabilities for
nutritional datasets. It calculates descriptive statistics, compares datasets,
and enables flexible data filtering.

Classes:
    DataProcessor: Processes and analyzes nutritional datasets
"""

import numpy as np

class DataProcessor:
    """
    Processes and analyzes nutritional datasets.
    
    Supports multiple datasets (e.g., food, drinks) and provides methods for
    calculating statistics, comparing datasets, and filtering data based on
    nutritional criteria.
    
    Attributes:
        datasets (dict): Dictionary of DataFrames, keyed by category name
        categories (list): List of category names in the order they were added
    """

    def __init__(self):
        """Initialize DataProcessor with empty dataset storage."""
        # initialize class member
        self.datasets = {}
        self.categories = []


    def add_datasets(self, catergory, df):
        """
        Add a dataset for a specific category.
        
        Args:
            category (str): Category name (e.g., 'food', 'drinks')
            df (pd.DataFrame): DataFrame containing nutritional data
        """
                
        self.datasets[catergory] = df # add dataset into the datasets dictionary, with the key as the category
        self.categories.append(catergory) # append to the list of categories

    def calculate_descriptive_stats(self):
        """
        Calculate descriptive statistics for all datasets.
        
        Computes standard statistics (count, mean, std, min, max, quartiles) and
        nutritional ratios (fat-to-protein, protein-to-carb, carb-to-fat) for each
        category.
        
        Returns:
            dict: Nested dictionary containing:
                - 'describe': DataFrame with descriptive statistics
                - 'ratio': Dictionary of calculated nutritional ratios
                
        Example:
            {
                'food': {
                    'describe': DataFrame(...),
                    'ratio': {'fat_to_protein': 1.43, ...}
                },
                'drinks': {...}
            }
        """
                
        stats = {}

        # for every category, compute the nutrients descriptive stats and ratio stats
        for category, nutrient in self.datasets.items():
            # count, mean, min, max
            stats[category] =  {
                'describe': nutrient.describe(),
                'ratio': {}
            }

            # ratios
            if 'Fat' in nutrient.columns and 'Protein' in nutrient.columns and 'Carb' in nutrient.columns:
                fat_sum = nutrient['Fat'].sum()
                protein_sum = nutrient['Protein'].sum()
                carb_sum = nutrient['Carb'].sum()

                stats[category]['ratio']['fat_to_protein'] = fat_sum / protein_sum
                stats[category]['ratio']['protein_to_carb'] = protein_sum / carb_sum
                stats[category]['ratio']['carb_to_fat'] = carb_sum / fat_sum

        return stats


    def compare_datasets(self, nutrients=None):
        """
        Compare nutritional metrics across all datasets.
        
        Generates comprehensive comparison statistics for specified nutrients.
        If nutrients are not specified, only common nutrients across all datasets
        are compared. Missing nutrients are represented as NaN.
        
        Args:
            nutrients (list, optional): List of nutrient names to compare.
                If None, compares only common nutrients across all datasets.
                
        Returns:
            dict: Nested dictionary structure:
                {
                    'category1': {
                        'nutrient1': {'count': ..., 'mean': ..., 'min': ..., ...},
                        'nutrient2': {...}
                    },
                    'category2': {...}
                }
                
        Note:
            Returns None if fewer than 2 datasets are available for comparison.
        """
                
        # check if there is sufficient datasets for comparison
        if len(self.datasets) < 2:
            print("Need at least 2 datasets to compare.")
            return
        
        # default nutrients if none is defined, only considers common nutrients between categories, for comparison purpose
        # otherwise the stated nutrients will be used
        # and only the stated metrics data will be used for comparison
        if nutrients is None:
            all_cols = [set(df.columns) for df in self.datasets.values()]
            nutrients = list(set.intersection(*all_cols))
        
        comparison = {}
    
        # for every category, compute the nutrients descriptive stats
        # Nan value if nutrient doesnt exist
        for category, df in self.datasets.items():
            comparison[category] = {}
            
            for nutrient in nutrients:
                if nutrient in df.columns:
                    comparison[category][nutrient] = {
                        'count': int(df[nutrient].count()),
                        'mean': round(df[nutrient].mean(), 2),
                        'median': round(df[nutrient].median(), 2),
                        'std': round(df[nutrient].std(), 2),
                        'min': round(df[nutrient].min(), 2),
                        'max': round(df[nutrient].max(), 2),
                        '25%': round(df[nutrient].quantile(0.25), 2),
                        '50%': round(df[nutrient].quantile(0.50), 2),
                        '75%': round(df[nutrient].quantile(0.75), 2)
                    }
                else:
                    comparison[category][nutrient] = {
                        'count': np.nan,
                        'mean': np.nan,
                        'median': np.nan,
                        'std': np.nan,
                        'min': np.nan,
                        'max': np.nan,
                        '25%': np.nan,
                        '50%': np.nan,
                        '75%': np.nan
                    }

        return comparison


    def filter_datasets(self, nutrient, operator, value, categories=None):
        """
        Filter multiple datasets based on nutritional criteria.
        
        Args:
            nutrient (str): Column name to filter on (e.g., 'Calories', 'Protein')
            operator (str): Comparison operator ('>', '<', '==', 'between')
            value (float or tuple): Value for comparison. For 'between', use tuple (min, max)
            categories (list, optional): List of category names to filter.
                If None, filters all categories.
                
        Returns:
            dict: Dictionary of filtered DataFrames, keyed by category name
        """
               
        # defaulted categories, if none is defined
        # otherwise the stated categories will be used
        if categories is None:
            categories = self.categories
        
        # for each category, filter the dataset based on the criteria
        # criteria is defined by the type of categories, nutrient, operator, and value
        filtered_datasets = {}
        for catergory in categories:
            filtered_datasets[catergory] = self.filter_data(self.datasets[catergory], nutrient, operator, value)

        return filtered_datasets
    

    def filter_dataset(self, catergory, nutrient, operator, value):
        """
        Helper function to filter a single dataset based on nutritional criteria.
        
        Args:
            category (str): Category name (e.g., 'food', 'drinks')
            nutrient (str): Column name to filter on
            operator (str): Comparison operator ('>', '<', '==', 'between')
            value (float or tuple): Value for comparison
            
        Returns:
            pd.DataFrame: Filtered DataFrame
            
        Raises:
            ValueError: If category doesn't exist in datasets
        """
                
        # check if theres any category to filter
        if catergory not in self.categories:
            raise ValueError(f"'{catergory}' not found in datasets")
        
        # extract the category's data and filter it
        df = self.datasets[catergory]
        return self.filter_data(df, nutrient, operator, value)
    

    @staticmethod
    def filter_data(df, nutrient, operator, value):
        """
        Helper function to apply filter criteria to a DataFrame.
        
        Static method that performs the actual filtering logic. Can be used
        independently of class instance.
        
        Args:
            df (pd.DataFrame): DataFrame to filter
            nutrient (str): Column name to filter on
            operator (str): Comparison operator ('>', '<', '==', 'between')
            value (float or tuple): Value for comparison. For 'between' operator,
                provide tuple (min_value, max_value)
                
        Returns:
            pd.DataFrame: Filtered DataFrame. Returns original DataFrame if
                operator is not recognized.
                
        Example:
            >>> filtered = DataProcessor.filter_data(df, 'Calories', '>', 300)
            >>> filtered = DataProcessor.filter_data(df, 'Protein', 'between', (10, 20))
        """

        # filter the data based on the stated nutrient, operator and value
        if operator == '>':
            return df[df[nutrient] > value]
        elif operator == '<':
            return df[df[nutrient] < value]
        elif operator == '==':
            return df[df[nutrient] == value]
        elif operator == 'between':
            return df[df[nutrient].between(value[0], value[1])]
        print("operator not recognized.")
        return df



