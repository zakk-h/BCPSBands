import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('BCPS Bandmasters - Sheet1.csv')

# Define replacement values and replace 'N/A' and 'C/O'
na_replacement = 2
co_replacement = 2
# Replace 'N/A' specifically in the SR column
data['SR'] = data['SR'].replace('N/A', na_replacement)

# Replace 'C/O' across all columns in the dataframe
data = data.replace('C/O', co_replacement)

# Function to parse the "Grade Level"
def parse_grade_level(grade_level):
    if ',' in str(grade_level):
        x, y = map(float, grade_level.split(','))
        return 0.4 * x + 0.6 * y
    else:
        return float(grade_level)

data['Grade Level'] = data['Grade Level'].apply(parse_grade_level)
data[['J1', 'J2', 'J3', 'SR']] = data[['J1', 'J2', 'J3', 'SR']].apply(pd.to_numeric, errors='coerce')
data['Objective'] = 10 + (data['Grade Level']**1.5 * (15 - data['J1'] - data['J2'] - data['J3'])) - data['SR']**2

# Define feeder relationships
feeder_relationships = {
    'Draughn': ['Heritage'],
    'East Burke High': ['East Burke Middle'],
    'Freedom': ['Table Rock', 'Walter Johnson'],
    'Patton': ['Liberty']
}

# Function to plot objective functions
def plot_objective_functions(data, schools, title, function_type):
    plt.figure(figsize=(12, 8))
    for school, feeders in schools.items():
        # High school data
        high_school_data = data[data['School'] == school]
        feeders_data = data[data['School'].isin(feeders)]
        
        # Group and plot for the high school
        if function_type == 'max':
            hs_data = high_school_data.groupby('Year')['Objective'].max()
            label_hs = f'{school} Max'
        elif function_type == 'avg':
            hs_data = high_school_data.groupby('Year')['Objective'].mean()
            label_hs = f'{school} Avg'
        
        plt.plot(hs_data.index, hs_data.values, label=label_hs, marker='o')
        
        # Group and plot for the feeder schools
        if not feeders_data.empty:
            if function_type == 'max':
                feeders_data = feeders_data.groupby('Year')['Objective'].max()
                label_feeders = f'{school} Feeders Max'
            elif function_type == 'avg':
                feeders_data = feeders_data.groupby('Year')['Objective'].mean()
                label_feeders = f'{school} Feeders Avg'
                
            plt.plot(feeders_data.index, feeders_data.values, label=label_feeders, linestyle='--', marker='x')

    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Objective Function')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot for maximum objective functions
plot_objective_functions(data, feeder_relationships, 'Maximum Objective Functions for High Schools and Their Feeder Middle Schools', 'max')

# Plot for average objective functions
plot_objective_functions(data, feeder_relationships, 'Average Objective Functions for High Schools and Their Feeder Middle Schools', 'avg')