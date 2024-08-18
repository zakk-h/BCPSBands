import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('BCPS Bandmasters - Sheet1.csv')

# Define replacement values for N/A and C/O
na_replacement = 2.2
co_replacement = 2.3

# Replace 'N/A' and '-1' specifically in the SR column
data['SR'] = data['SR'].replace(['N/A', '-1'], na_replacement)
data['SR'] = data['SR'].fillna(na_replacement)

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

# Function to compute the objective function
def compute_objective(grade_level, j1, j2, j3, sr):
    return (grade_level**(grade_level/2)) * (50 - (j1**j1) - (j2**j2) - (j3**j3) - (sr**sr))

# Calculate the objective function
data['Objective'] = compute_objective(
    data['Grade Level'], data['J1'], data['J2'], data['J3'], data['SR']
)

# Apply a square root transformation and normalize
data['Objective'] = np.sqrt(data['Objective'] - data['Objective'].min() + 1)

# Define feeder relationships
feeder_relationships = {
    'Draughn': ['Heritage'],
    'East Burke High': ['East Burke Middle'],
    'Freedom': ['Table Rock', 'Walter Johnson'],
    'Patton': ['Liberty']
}

# Function to get average objective from middle schools in the preferred order: 2 years ago, 3 years ago, 1 year ago
def get_feeder_avg_objective(high_school, year):
    feeder_schools = feeder_relationships.get(high_school, [])
    previous_years = [year - 2, year - 3, year - 1]  # Preferred order of years: 2, 3, 1
    for yr in previous_years:
        feeder_data = data[(data['School'].isin(feeder_schools)) & (data['Year'] == yr)]
        if not feeder_data.empty:
            return feeder_data['Objective'].mean()
    return np.nan  # Return NaN if no data is found

# Compute the relative performance
relative_performance = []
for year in sorted(data['Year'].unique()):
    for high_school in feeder_relationships.keys():
        high_school_data = data[(data['School'] == high_school) & (data['Year'] == year)]
        if not high_school_data.empty:
            feeder_avg = get_feeder_avg_objective(high_school, year)
            if not np.isnan(feeder_avg):
                for index, row in high_school_data.iterrows():
                    relative_score = row['Objective'] / feeder_avg
                    relative_performance.append({'Year': year, 'School': high_school, 'Relative Performance': relative_score})

# Create DataFrame for relative performance
relative_performance_df = pd.DataFrame(relative_performance)

# Plotting
plt.figure(figsize=(12, 6))
for school in feeder_relationships.keys():
    school_data = relative_performance_df[relative_performance_df['School'] == school]
    plt.plot(school_data['Year'], school_data['Relative Performance'], label=school, marker='o')
plt.title('Relative Performance of High Schools to Their Feeder Middle Schools')
plt.xlabel('Year')
plt.ylabel('Relative Performance')
plt.legend()
plt.grid(True)
plt.show()
