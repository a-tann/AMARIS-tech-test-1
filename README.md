# Simple LLm-powered Application (AMARIS-tech-test-1)

A Python-based LLM-powered application for analyzing Starbucks menu nutrition data. This tool provides statistical insights, data filtering capabilities, and an interactive chat interface powered by the Groq LLM API.

## Features

- **Descriptive Statistics**: Generate comprehensive nutritional statistics for food and drinks
- **Dataset Comparison**: Compare nutritional metrics across different menu categories
- **Data Visualization**: Create bar charts comparing nutritional aspects
- **Interactive Filtering**: Filter datasets based on nutritional criteria
- **LLM-Powered Chat**: Ask natural language questions about nutritional data

## Project Structure

```
AMARIS-tech-test-1/
├── data/
│   ├── starbucks-menu-nutrition-food.csv
│   └── starbucks-menu-nutrition-drinks.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── data_visualizer.py
│   └── llm_service.py
├── .env
├── main.py
├── README.md
└── requirements.txt
```

## Installation

### 1. Extract and Open Project

Extract `AMARIS-tech-test-1.zip` and open the folder in Visual Studio Code. Then open the command prompt terminal

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Ensure you're in the project root directory and the virtual environment is activated, then run:
```bash
python main.py
```

### Menu Options

The application presents a menu with 4 options:
```
========================================
SIMPLE LLM-POWERED APPLICATION
========================================
Choose an option (1 or 2 or 3 or 4):
1. Generate nutritional insights
2. Filter dataset mode
3. Interactive Chat
4. Exit
========================================
```

#### 1. Generate Nutritional Insights
- Displays descriptive statistics (count, mean, std, min, max, quartiles)
- Shows nutritional ratios (fat-to-protein, protein-to-carb, carb-to-fat)
- Generates bar chart visualizations
- Saves charts as PNG files

#### 2. Filter Dataset Mode
Interactive filtering by:
- Category (food/drinks)
- Nutrient column (Calories, Fat, Protein, etc.)
- Operator (>, <, ==, between)
- Value or range

**Example:**
```
Choose a category to filter (food/drinks): food
Here are the available columns to filter: ['calories', 'fat', 'carb', 'fiber', 'protein']
Which nutrient/column do you want to filter by? fat
Operator (>, <, ==, between): <
Enter value: 3
```

#### 3. Interactive Chat
- Ask natural language questions about the menu data
- Get AI-powered insights and summaries
- Example queries:
  - "What drinks have the highest sugar content?"
  - "Compare average calories between food and drinks"
  - "Which food items are under 400 calories?"

#### 4. Exit
Closes the application

## Module Descriptions

### `data_loader.py`
- Loads CSV files with automatic encoding detection
- Handles missing values and formatting issues
- Standardizes column names

### `data_processor.py`
- Calculates descriptive statistics
- Compares datasets across categories
- Filters data based on criteria
- Computes nutritional ratios

### `data_visualizer.py`
- Prints formatted statistics to console
- Creates bar chart visualizations
- Generates comparison charts
- Saves charts as PNG files

### `llm_service.py`
- Interfaces with Groq LLM API
- Generates natural language responses
- Provides nutritional insights using AI

## Dependencies

- `groq>=0.4.2` - LLM API client
- `python-dotenv>=1.0.0` - Environment variable management
- `pandas>=2.1.0` - Data manipulation
- `numpy>=1.26.0` - Numerical operations
- `matplotlib>=3.8.0` - Data visualization
- `chardet>=5.0.0` - Character encoding detection

## Output Files

The application generates the following output files:
- `descriptive_stats_bar_chart.png` - Nutritional statistics visualization
- `comparison_stats_bar_chart.png` - Dataset comparison visualization

## Example Interactions

### Descriptive Statistics Example
```
================================================================================
FOOD DESCRIPTIVE STATISTICS
================================================================================

Basic Statistics:
       Calories     Fat    Carb   Fiber  Protein
count    113.00  113.00  113.00  113.00   113.00
mean     356.64   16.35   41.49    2.85    11.47
std      127.71    8.30   15.80    2.89     8.46
min       90.00    0.00    5.00    0.00     1.00
25%      280.00    9.00   31.00    1.00     5.00
50%      360.00   17.00   42.00    2.00     8.00
75%      450.00   23.00   53.00    3.00    19.00
max      650.00   37.00   80.00   21.00    34.00

Ratios:
  fat_to_protein  : 1.43
  protein_to_carb : 0.28
  carb_to_fat     : 2.54


================================================================================
DRINKS DESCRIPTIVE STATISTICS
================================================================================

Basic Statistics:
       Calories    Fat   Carb  Fiber  Protein  Sodium
count     92.00  92.00  92.00  92.00    92.00   92.00
mean     135.16   2.34  24.74   0.45     4.15   57.93
std       93.85   3.89  15.21   1.42     5.69   68.38
min        0.00   0.00   0.00   0.00     0.00    0.00
25%       60.00   0.00  14.75   0.00     0.00   10.00
50%      130.00   0.00  25.50   0.00     1.00   15.00
75%      190.00   4.12  35.00   0.00     8.25  115.00
max      430.00  26.00  64.00   8.00    20.00  240.00

Ratios:
  fat_to_protein  : 0.56
  protein_to_carb : 0.17
  carb_to_fat     : 10.59
```

### Comparison Statistics Example
```
================================================================================
DATASETS COMPARISON
================================================================================


--------------------------------------------------------------------------------
MEAN COMPARISON
--------------------------------------------------------------------------------
            food  drinks
Fiber       2.85    0.45
Fat        16.35    2.34
Carb       41.49   24.74
Protein    11.47    4.15
Calories  356.64  135.16
```

### Filtering Example
```
Choose a category to filter (food/drinks): food
Here are the available columns to filter: ['calories', 'fat', 'carb', 'fiber', 'protein']
Which nutrient/column do you want to filter by? fat
Operator (>, <, ==, between): <
Enter value: 3
```

```
================================================================================
FILTERED RESULTS:
================================================================================


                                                  Calories  Fat  Carb  Fiber  Protein
Cinnamon Raisin Bagel                                  270  1.0    58      3        9
Plain Bagel                                            280  1.5    56      2        9
Classic Whole-Grain Oatmeal                            160  2.5    28      4        5
Hearty Blueberry Oatmeal                               220  2.5    43      5        5
Berry Trio Yogurt                                      240  2.5    39      3       14
Fresh Blueberries and Honey Greek Yogurt Parfait       240  2.5    42      2       14
Seasonal Fruit Blend                                    90  0.0    24      4        1

Total rows after filtering: 7
```

### Chat Example
```
You: which drink items have the highest sugar content?
LLM: LLM: To determine the drink items with the highest sugar content, we need to look at the carbohydrate (Carb) column in the drinks data, as sugar is a type of carbohydrate. Since the exact sugar content is not provided, we'll use the Carb column as a proxy.

Based on the provided data, the top 5 drink items with the highest carbohydrate content are:   

1. Strawberry Acai Starbucks Refreshers™ Beverage - 18.0g
2. Tazo® Bottled Black Mango - 38.0g
3. Tazo® Bottled Giant Peach - 37.0g
4. Tazo® Bottled Tazoberry - 38.0g
5. Tazo® Bottled Brambleberry - 35.0g

However, if we consider the drinks with the highest carb content per serving, we should also look at the Frappuccino® Blended Coffee drinks. Although their data is mostly missing, the Cinnamon Dolce Frappuccino® Blended Coffee has a carb content of 64.0g, and the Mocha Frappuccino® Blended Coffee has a carb content of 60.0g.

Please note that the data for many drink items is missing, so this analysis is limited to the available data.
```

