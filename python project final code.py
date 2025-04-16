# ----------------------------------------------
# 📊 Hospital Directory Analysis Project
# ----------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("C:/Users/DELL/Downloads/hospital_directory.csv", low_memory=False)

# ----------------------------------------------
# Objective 1: State-wise Hospital Distribution
# ----------------------------------------------
df_state = df.dropna(subset=['State'])
state_counts = df_state['State'].value_counts().reset_index()
state_counts.columns = ['State', 'Hospital Count']
state_counts = state_counts.sort_values(by='Hospital Count', ascending=False)

plt.figure(figsize=(14, 8))
sns.barplot(data=state_counts, x='Hospital Count', y='State', hue='State', palette='viridis', legend=False)
plt.title('State-wise Distribution of Hospitals in India', fontsize=16)
plt.xlabel('Number of Hospitals')
plt.ylabel('State / UT')
plt.tight_layout()
plt.show()

# Pie Chart: Top 10 States by Hospital Count
top_states = state_counts.head(10)
plt.figure(figsize=(8, 8))
plt.pie(top_states['Hospital Count'], labels=top_states['State'], autopct='%1.1f%%', startangle=140)
plt.title("Top 10 States by Hospital Count (Pie Chart)")
plt.axis('equal')
plt.show()

# ----------------------------------------------
# Objective 2: Hospital Type Distribution
# ----------------------------------------------
df_cat = df.dropna(subset=['Hospital_Category'])
hospital_type_counts = df_cat['Hospital_Category'].value_counts().reset_index()
hospital_type_counts.columns = ['Hospital Type', 'Count']

plt.figure(figsize=(10, 6))
sns.barplot(data=hospital_type_counts, x='Count', y='Hospital Type', hue='Hospital Type', palette='Set2', legend=False)
plt.title('Distribution of Hospitals by Type', fontsize=16)
plt.xlabel('Number of Hospitals')
plt.ylabel('Hospital Type')
plt.tight_layout()
plt.show()

# State-wise hospital category heatmap
state_hospital_type = df_cat.groupby(['State', 'Hospital_Category']).size().unstack().fillna(0)
plt.figure(figsize=(16, 10))
sns.heatmap(state_hospital_type, cmap='YlGnBu', linewidths=0.5)
plt.title('State-wise Distribution of Hospital Types', fontsize=16)
plt.xlabel('Hospital Type')
plt.ylabel('State')
plt.tight_layout()
plt.show()

# ----------------------------------------------
# Objective 3: Data Cleaning & Missing Value Handling
# ----------------------------------------------
important_columns = [
    'Hospital_Name',
    'Address_Original_First_Line',
    'Telephone',
    'Mobile_Number',
    'Total_Num_Beds'
]

# Step 1: Show missing data percentages
missing_percent = df[important_columns].isnull().mean() * 100
missing_df = missing_percent.reset_index()
missing_df.columns = ['Column', 'Missing Percentage']

plt.figure(figsize=(8, 5))
sns.barplot(data=missing_df, x='Missing Percentage', y='Column', palette='rocket', hue='Column', legend=False)
plt.title('Missing Data Percentage in Important Fields')
plt.tight_layout()
plt.show()

# Step 2: Cleaning
df_cleaned = df.dropna(subset=['Hospital_Name']).copy()
df_cleaned['Telephone'] = df_cleaned['Telephone'].fillna('Not Available')
df_cleaned['Mobile_Number'] = df_cleaned['Mobile_Number'].fillna('Not Available')
df_cleaned['Total_Num_Beds'] = pd.to_numeric(df_cleaned['Total_Num_Beds'], errors='coerce').fillna(0).astype(int)

# Step 3: Confirm cleaning
print("\n✅ Data cleaned! Remaining null values in important columns:\n")
print(df_cleaned[important_columns].isnull().sum())

# ----------------------------------------------
# Objective 4: Exploratory Data Analysis (EDA)
# ----------------------------------------------

# Summary Statistics of Bed Data
print("\n📌 Summary of Total Number of Beds:\n")
print(df_cleaned['Total_Num_Beds'].describe())

# Histogram: Total Number of Beds
plt.figure(figsize=(8, 4))
sns.histplot(df_cleaned['Total_Num_Beds'], bins=30, kde=True, color='skyblue')
plt.title("Distribution of Total Number of Beds")
plt.xlabel("Total Beds")
plt.ylabel("Number of Hospitals")
plt.tight_layout()
plt.show()

# Top 10 States by Total Beds
top_states_beds = df_cleaned.groupby('State')['Total_Num_Beds'].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=top_states_beds, x='Total_Num_Beds', y='State', hue='State', palette='Blues_r', legend=False)
plt.title("Top 10 States with Most Hospital Beds")
plt.xlabel("Total Beds")
plt.ylabel("State")
plt.tight_layout()
plt.show()

# ----------------------------------------------
# Objective 5: Dashboard - Visual Summary
# ----------------------------------------------

hospital_types = df_cleaned['Hospital_Category'].value_counts()
top_states_hospitals = df_cleaned['State'].value_counts().head(10)

sns.set_style("whitegrid")
plt.figure(figsize=(14, 10))

# Subplot 1: Top 10 States by Total Beds
plt.subplot(2, 2, 1)
sns.barplot(data=top_states_beds, x='Total_Num_Beds', y='State', hue='State', palette='Blues_r', legend=False)
plt.title("Top 10 States by Total Hospital Beds")
plt.xlabel("Total Beds")
plt.ylabel("State")

# Subplot 2: Pie Chart - Hospital Category
plt.subplot(2, 2, 2)
plt.pie(hospital_types, labels=hospital_types.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribution of Hospital Categories")
plt.axis('equal')

# Subplot 3: Histogram - Bed Distribution
plt.subplot(2, 2, 3)
sns.histplot(df_cleaned['Total_Num_Beds'], bins=30, kde=False, color='orange')
plt.title("Distribution of Total Number of Beds")
plt.xlabel("Total Beds")
plt.ylabel("Number of Hospitals")

# Subplot 4: Top 10 States by Hospital Count
plt.subplot(2, 2, 4)
sns.barplot(x=top_states_hospitals.values, y=top_states_hospitals.index, hue=top_states_hospitals.index, palette='Greens_r', legend=False)
plt.title("Top 10 States by Number of Hospitals")
plt.xlabel("Number of Hospitals")
plt.ylabel("State")

# Final Layout
plt.suptitle("Hospital Data Visual Dashboard", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
