"""
05-Matplotlib Homework
"""
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
# Study data files
mouse_metadata_path = '.\Instructions\Pymaceuticals\data\Mouse_metadata.csv'
study_results_path = '.\Instructions\Pymaceuticals\data\Study_results.csv'
# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path) 
# Combine the data into a single datase
merged_df = pd.merge(mouse_metadata, study_results, how='inner', on='Mouse ID')
# Display the data table for preview
print('\nRecords after merge:')
print(merged_df)
# Checking the number of mice.
print('\nNumber of mice after merge: ' + str(merged_df['Mouse ID'].count())+'\n')
# Getting the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
dupRows_df = merged_df[merged_df.duplicated(['Mouse ID', 'Timepoint'])]
print('\nDuplicate records with same Mouse IDs and Timepoints:')
print(dupRows_df)
# Optional: Get all the data for the duplicate mouse ID. 
allDupRows_df = merged_df[merged_df.duplicated(['Mouse ID'])]
print('\nDuplicate records with same Mouse IDs:')
print(allDupRows_df)
# Create a clean DataFrame by dropping the duplicate mouse by its ID.
cleaned_merged_df = merged_df.drop_duplicates('Mouse ID')
# Checking the number of mice in the clean DataFrame.
print('\nNumber of Mice after clean: ' + str(cleaned_merged_df['Mouse ID'].count())+'\n')
# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen
# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 
# mean, median, variance, standard deviation, and SEM of the tumor volume. 
mean = merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()
median = merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()
variance = merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()
stdDev = merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()
sem = merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()
summary_df = pd.DataFrame({'Mean': mean, 'Median': median, 'Variance': variance, 'Std Dev': stdDev, 'SEM': sem})
summary_df
# Assemble the resulting series into a single summary dataframe.
merged_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].describe()
# Generate a bar plot showing the total number of unique mice tested on each drug regimen using pandas.
drug_df = pd.DataFrame(merged_df.groupby(['Drug Regimen']).count()).reset_index()
drugs_df = drug_df[['Drug Regimen', 'Mouse ID']]
drugs_df = drugs_df.set_index('Drug Regimen')
drugs_df.plot(kind='bar', figsize=(10,4))
plt.xlabel('Drug Regimen')
plt.ylabel('Count')
plt.title('#Mice in each Regimen')
plt.show()
plt.tight_layout()
# Generate a bar plot showing the total number of unique mice tested on each drug regimen using pypl
drug_ls = summary_df.index.tolist()
drugCount_ls = (merged_df.groupby(['Drug Regimen'])['Age_months'].count()).tolist()
x_axis = np.arange(len(drugCount_ls))
x_axis = drug_ls
plt.figure(figsize=(10,4))
plt.xlabel('Drug Regimen')
plt.ylabel('Count')
plt.title('#Mice in each Regimen')
plt.bar(x_axis, drugCount_ls, color='g', alpha=0.5, align='center')
# Generate a pie plot showing the distribution of female versus male mice using pandas
gender_df = pd.DataFrame(merged_df.groupby(["Sex"]).count()).reset_index()
gender_df=gender_df[['Sex','Mouse ID']]
plt.figure(figsize=(10,4))
axis = plt.subplot(121, aspect='equal')
gender_df.plot(kind='pie', y = 'Mouse ID', ax=axis, autopct='%1.2f%%',
              startangle=90,labels=gender_df['Sex'], legend=False)
plt.title('% Female vs Male Mice')
plt.ylabel('')
# Generate a pie plot showing the distribution of female versus male mice using pyplot
genderCount = (merged_df.groupby(['Sex'])['Age_months'].count()).tolist()
labels = ['Females', 'Males']
plt.pie(genderCount, autopct='%1.2f%%', startangle=90, labels=labels)
