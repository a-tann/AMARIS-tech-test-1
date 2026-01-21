"""
Data loading module for CSV nutritional data.

This module handles loading CSV files containing Starbuck's nutritional information,
with automatic encoding detection and data cleaning. It standardizes column
names and handles common CSV formatting issues.

Classes:
    DataLoader: Loads and preprocesses CSV nutritional data
"""

import os
import pandas as pd
import chardet as cd

class DataLoader:
    """
    Loads and preprocesses CSV files containing nutritional data.
    
    Automatically detects file encoding, handles missing values, and standardizes
    column names by removing units and special characters.
    
    Attributes:
        csv_path (str): Path to the CSV file
        df (pd.DataFrame): Loaded and cleaned DataFrame
    """
     
    def __init__(self, csv_path):
        """
        Initialize DataLoader and load data from CSV file.
        
        Args:
            csv_path (str): Path to the CSV file to load
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist at the specified path
        """

        # initliaze class members
        self.csv_path = csv_path
        self.df = None
        self.load_data() # load data from the provided csv path


    def load_data(self):
        """
        Load and preprocess CSV data.
        
        Performs the following operations:
        - Validates file existence
        - Detects file encoding automatically
        - Loads CSV with first column as index
        - Handles missing values (treats '-' as NaN)
        - Strips whitespace from column names
        - Removes units and special characters from column names
        
        Raises:
            FileNotFoundError: If CSV file not found at specified path
        """

        # check if the file path exist 
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found at path: {self.csv_path}")
        
        # handle formatting issues and extract the data and store in dataframe
        detected_encoding = self.detect_encoding(self.csv_path)
        self.df = pd.read_csv(self.csv_path, index_col=0, na_values='-', encoding=detected_encoding)
        self.df.columns = self.df.columns.str.strip() # strip leading/trailing whitespace from column names
        self.df.columns = self.df.columns.str.replace(r'\s*\(.*\)|[.]', '', regex=True) # standardise the column names, by removing anything in parentheses


    @staticmethod
    def detect_encoding(csv_path):
        """
        Helper function to detect the character encoding of a CSV file.
        
        Uses the chardet library to automatically detect the file encoding,
        which helps handle files with different character sets (UTF-8, Latin-1, etc.).
        
        Args:
            csv_path (str): Path to the CSV file
            
        Returns:
            str: Detected encoding (e.g., 'utf-8', 'ISO-8859-1')
        """

        with open(csv_path, 'rb') as f:
            return cd.detect(f.read())['encoding']