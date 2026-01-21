"""
Main application entry point for the Starbucks Nutritional Analysis System.

This module provides a command-line interface for analyzing Starbucks menu nutrition data.
Users can generate statistical insights, filter datasets, and interact with an LLM-powered
chat system for nutritional queries.

Features:
    - Generate descriptive statistics and comparisons
    - Filter datasets by nutritional criteria
    - Interactive chat with LLM for nutritional insights
"""

from dotenv import load_dotenv
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.data_visualizer import DataVisualizer
from src.llm_service import LLMService

def generate_stats(food_data, drinks_data):
    """
    Generate and display nutritional statistics for food and drinks datasets.
    
    Creates descriptive statistics, comparison data, and visualizations for both
    datasets. Displays results to console and saves charts as PNG files.
    
    Args:
        food_data (DataLoader): Loaded food dataset
        drinks_data (DataLoader): Loaded drinks dataset
    """
        
    # create data processor instance and add the datasets
    data_processor = DataProcessor()
    data_processor.add_datasets('food', food_data.df)
    data_processor.add_datasets('drinks', drinks_data.df)

    # calculate descriptive stats and comparison stats
    descrp_stats = data_processor.calculate_descriptive_stats()
    comparison_stats = data_processor.compare_datasets()

    # create visualizer instance and display the results
    data_visualizer = DataVisualizer()
    data_visualizer.print_descriptive_stats(descrp_stats)
    data_visualizer.print_comparison(comparison_stats, metrics=['mean', 'min'])
    data_visualizer.plot_descriptive_stats(descrp_stats, metrics=['mean'])
    data_visualizer.plot_comparison_stats_bar(comparison_stats, metrics=['mean'])

    # check for returning to menu inputs
    print("Type 'quit', 'exit' or 'q' to return to menu\n")

    while True:
        user_input = input()

        if user_input.strip().lower() in ['quit', 'exit', 'q']:
            print("Returning to menu...\n")
            break

        if user_input.strip() == "":
            continue


def filter_data_mode(food_data, drinks_data):
    """
    Interactive filtering mode for dataset exploration.
    
    Allows users to filter datasets by category, nutrient, and comparison operator.
    Results are displayed immediately and users can continue filtering or return to menu.
    
    Args:
        food_data (DataLoader): Loaded food dataset
        drinks_data (DataLoader): Loaded drinks dataset
    """
        
    # create data processor instance and add the datasets
    data_processor = DataProcessor()
    data_processor.add_datasets('food', food_data.df)
    data_processor.add_datasets('drinks', drinks_data.df)

    # check for prompted inputs
    # to exit to menu upon an invalid input
    while True:
        # get category input
        category = input("\nChoose a category to filter (food/drinks): ").strip().lower()
        if category not in data_processor.datasets:
            print("Invalid category.\n")
            return
        
        # get column input
        available_columns = [col.lower() for col in data_processor.datasets[category].columns]
        print("Here are the available columns to filter:", available_columns)
        nutrient = input("Which nutrient/column do you want to filter by? ").strip().lower()
        if nutrient not in available_columns:
            print("Invalid column.\n")
            return
        
        # get operator input
        operator = input("Operator (>, <, ==, between): ").strip()
        if operator in ['>', '<', '==']:
            value = float(input("Enter value: "))
        elif operator == "between":
            val_min = float(input("Enter min value: "))
            val_max = float(input("Enter max value: "))
            value = (val_min, val_max)
        else:
            print("Operator not recognized.\n")
            return

        # filter the dataset based on the stated inputs above
        filtered_df = data_processor.filter_dataset(category, nutrient.capitalize(), operator, value)

        # print the filtered result to console
        print("\n")
        print("="*80)
        print("FILTERED RESULTS:")
        print("="*80)
        print("\n")
        print(filtered_df)
        print(f"\nTotal rows after filtering: {len(filtered_df)}\n")
    
        # check for returning to menu inputs or continue to filter
        print("Press Enter to continue filtering, or type 'quit', 'exit' or 'q' to return to menu\n")

        user_input = input()

        if user_input.strip().lower() in ['quit', 'exit', 'q']:
            print("Returning to menu...\n")
            break


def interactive_mode(food_data, drinks_data):
    """
    Interactive chat mode with LLM for nutritional insights.
    
    Provides a conversational interface where users can ask questions about the
    nutritional data. The LLM analyzes the provided datasets and generates
    data-driven responses.
    
    Args:
        food_data (DataLoader): Loaded food dataset
        drinks_data (DataLoader): Loaded drinks dataset
    """
        
    # create the context with the provided datas
    context = f"food data:\n{food_data.df.to_string()}\n"
    context += f"drinks data:\n{drinks_data.df.to_string()}"

    # create a llm service instance
    llm = LLMService()

    print("\n====== Interactive Chat Mode ======")
    print("Feel free to ask questions about Starbuck's menu items (e.g. summarize the nutritional insights of the data, etc)")
    print("Type 'quit', 'exit' or 'q' to return to menu\n")

    # get user input for prompt, for the llm to generate a response to
    # also checks for returning to menu inputs
    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in ['quit', 'exit', 'q']:
            print("Returning to menu...\n")
            break

        if user_input.strip() == "":
            continue

        response = llm.generate_response(user_input, context)

        # print out the llm generated response to console
        print(f"\nLLM: {response}\n")


def main():
    """
    Main entry point for the application.
    
    Loads environment variables, initializes datasets, and presents a menu-driven
    interface for the user to choose between different modes.
    """
        
    # load environment variables from .env file
    load_dotenv()

    # declare the datasets path
    food_csv_path = "data/starbucks-menu-nutrition-food.csv"
    drinks_csv_path = "data/starbucks-menu-nutrition-drinks.csv"

    # create dataloader instances to load data from declared datasets path
    food_data = DataLoader(food_csv_path)
    drinks_data = DataLoader(drinks_csv_path)

    while True:
        # menu interface
        print("="*40)
        print("SIMPLE LLM-POWERED APPLICATION")
        print("="*40)
        print("Choose an option (1 or 2 or 3 or 4):")
        print("1. Generate nutritional insights")
        print("2. Filter dataset mode")
        print("3. Interactive Chat")
        print("4. Exit")
        print("="*40 + "\n")

        # get the stated choice from user input and perform accordingly
        choice = input().strip()

        if choice == "1":
            generate_stats(food_data, drinks_data)
        elif choice == "2":
            filter_data_mode(food_data, drinks_data)
        elif choice == "3":
            interactive_mode(food_data, drinks_data)
        elif choice == "4":
            print("\nGoodbye! Thank you for using the application.")
            exit()
        else:
            print("Invalid input, Please type again.\n")
            continue


# run main
main()
