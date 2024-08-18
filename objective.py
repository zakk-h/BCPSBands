import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
data = pd.read_csv('BCPS Bandmasters - Sheet1.csv')

# Define replacement values for N/A and C/O
na_replacement = 2.2
co_replacement = 2.3

# Replace 'N/A' and '-1' specifically in the SR column
data['SR'] = data['SR'].replace(['N/A', '-1'], na_replacement)
data['SR'] = data['SR'].fillna(na_replacement)

# Replace 'C/O' across all columns in the dataframe
data = data.replace('C/O', co_replacement)

# Handle the Grade Level column for cases "x,y"
def parse_grade_level(grade_level):
    if ',' in str(grade_level):
        x, y = map(float, grade_level.split(','))
        return 0.4 * x + 0.6 * y
    else:
        return float(grade_level)

data['Grade Level'] = data['Grade Level'].apply(parse_grade_level)

# Convert J1, J2, J3, and SR to numeric
data[['J1', 'J2', 'J3', 'SR']] = data[['J1', 'J2', 'J3', 'SR']].apply(pd.to_numeric, errors='coerce')

# Function to compute the objective function
def compute_objective(grade_level, j1, j2, j3, sr):
    return (grade_level**(grade_level/2)) * (50 - (j1**j1) - (j2**j2) - (j3**j3) - (sr**sr))

# Calculate the objective function
data['Objective'] = compute_objective(
    data['Grade Level'], data['J1'], data['J2'], data['J3'], data['SR']
)

# Apply a square root transformation and normalize
data['Objective'] = np.sqrt(data['Objective'] - data['Objective'].min() + 1)
min_obj = data['Objective'].min()
max_obj = data['Objective'].max()
data['Normalized Objective'] = (data['Objective'] - min_obj) / (max_obj - min_obj) * 100
data['Normalized Objective'] = (100 + data['Normalized Objective']) / 2

# Define high schools and middle schools
high_schools = ['East Burke High', 'Patton', 'Draughn', 'Freedom']
middle_schools = set(data['School']) - set(high_schools)

# Filter data for high schools and middle schools
high_school_data = data[data['School'].isin(high_schools)]
middle_school_data = data[data['School'].isin(middle_schools)]

# Function to plot data
def plot_school_data(df, title):
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle(title)

    # Average of entries per year
    avg_data = df.groupby(['Year', 'School'])['Normalized Objective'].mean().unstack().plot(ax=axes[0], marker='o')
    axes[0].set_title('Average Normalized Objective per Year')
    axes[0].set_ylabel('Average Normalized Objective')
    axes[0].grid(True)

    # Maximum of entries per year
    max_data = df.groupby(['Year', 'School'])['Normalized Objective'].max().unstack().plot(ax=axes[1], marker='o')
    axes[1].set_title('Maximum Normalized Objective per Year')
    axes[1].set_ylabel('Maximum Normalized Objective')
    axes[1].grid(True)

    # Layout adjustment
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Plot for high schools
plot_school_data(high_school_data, 'High Schools Objective Function Analysis')

# Plot for middle schools
plot_school_data(middle_school_data, 'Middle Schools Objective Function Analysis')

plt.show()
