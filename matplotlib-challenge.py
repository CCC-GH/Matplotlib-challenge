'''
05-Matplotlib Homework
'''
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd

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
drugs_df.plot(kind='bar', figsize=(10,4),legend=False)
plt.xlabel('Drug Regimen')
plt.ylabel('Count')
plt.title('#Mice in each Regimen (pandas)')
plt.tight_layout()
# Generate a bar plot showing the total number of unique mice tested on each drug regimen using pyplot
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
gender_df = pd.DataFrame(merged_df.groupby(['Sex']).count()).reset_index()
gender_df = gender_df[['Sex','Mouse ID']]
plt.figure(figsize=(10,4))
axis = plt.subplot(121, aspect='equal')
gender_df.plot(kind='pie', y = 'Mouse ID', ax=axis, autopct='%1.2f%%',
              startangle=90,labels=gender_df['Sex'], legend=False)
plt.title('% Female vs Male Mice (pandas)')
plt.ylabel('')
# Generate a pie plot showing the distribution of female versus male mice using pyplot
genderCount = (merged_df.groupby(['Sex'])['Age_months'].count()).tolist()
labels = ['Females', 'Males']
plt.pie(genderCount, autopct='%1.2f%%', startangle=90, labels=labels)
plt.axis("equal")
# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin
# Start by getting the last (greatest) timepoint for each mouse
sort_df = merged_df.sort_values(['Drug Regimen', 'Mouse ID', 'Timepoint'], ascending=True)
last_df = sort_df.loc[sort_df['Timepoint'] == 45]
# Merge this group df with the original dataframe to get the tumor volume at the last timepoint
# Put treatments into a list for for loop (and later for plot labels)
last_df.head().reset_index()
capo_df = last_df[last_df['Drug Regimen'].isin(['Capomulin'])]
capo_df.head().reset_index()
capo_obj = capo_df.sort_values(['Tumor Volume (mm3)'], ascending=True).reset_index()
capo_obj = capo_obj['Tumor Volume (mm3)']
capo_obj
quartiles = capo_obj.quantile([.25,.5,.75])
lowQ = quartiles[0.25]
upQ = quartiles[0.75]
iqr = upQ - lowQ
print(f'Lower quartile of temp: {round(lowQ,2)}')
print(f'Upper quartile of temp: {round(upQ,2)}')
print(f'Interquartile range of temp: {round(iqr,2)}')
print(f'Median of temp: {round(quartiles[0.5],2)}')
low_b = lowQ - (1.5*iqr)
up_b = upQ + (1.5*iqr)
print(f'Values below {round(low_b,2)} are possible outliers')
print(f'Values above {round(up_b,2)} are possible outliers')
# Generate a box plot of the final tumor volume of each mouse across four regimens of interest
box, axis = plt.subplots()
axis.set_title('Final Tumor Volume in Capomulin Regimen')
axis.set_ylabel('Final Tumor Volume (mm3)')
axis.boxplot(capo_obj)
plt.show()
ram_df = last_df[last_df['Drug Regimen'].isin(['Ramicane'])]
ram_df.head().reset_index()
ram_obj = ram_df.sort_values(['Tumor Volume (mm3)'], ascending=True).reset_index()
ram_obj = ram_obj['Tumor Volume (mm3)']
ram_obj
# Generate a line plot of tumor volume vs. time point for a mouse treated with Capomulin
capomulin_df = merged_df.loc[merged_df["Drug Regimen"] == "Capomulin"]
capomulin_df = capomulin_df.reset_index()
capomulin_df.head()
# Generate a scatter plot of average tumor volume vs. mouse weight for the Capomulin regimen
weight_df = capomulin_df.loc[:, ["Mouse ID", "Weight (g)", "Tumor Volume (mm3)"]]
avg_capo = pd.DataFrame(weight_df.groupby(["Mouse ID", "Weight (g)"])["Tumor Volume (mm3)"].mean()).reset_index()
avg_capo = avg_capo.rename(columns={"Tumor Volume (mm3)": "Average Volume"})
avg_capo.plot(kind="scatter", x="Weight (g)", y="Average Volume", grid=True, figsize=(4,4), title="Weight vs. Average Tumor Volume")
# Generate a box plot of the final tumor volume of each mouse across four regimens of interest
box, axis = plt.subplots()
axis.set_title("Final Tumor Volume in Capomulin Regimen")
axis.set_ylabel("Final Tumor Volume (mm3)")
axis.boxplot(capo_obj)
# Calculate the correlation coefficient and linear regression model 
# for mouse weight and average tumor volume for the Capomulin regimen
mouse_weight = avg_capo.iloc[:,0]
avg_tumor_volume = avg_capo.iloc[:,1]
# We then compute the Pearson correlation coefficient between "Mouse Weight" and "Average Tumor Volume"
# correlation = st.pearsonr(mouse_weight,avg_tumor_volume)
# print(f'Correlation is: {round(correlation[0],2)}')
# import linregress
from scipy.stats import linregress
x_value = avg_capo['Weight (g)']
y_value = avg_capo['Average Volume']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_value, y_value)
regress_value = x_value * slope + intercept
line_eq = 'y = ' + str(round(slope,2)) + 'x + ' + str(round(intercept,2))
plt.scatter(x_value, y_value)
plt.plot(x_value,regress_value,'r-')
plt.annotate(line_eq,(3,10), fontsize=15, color='red')
plt.xlabel('Mouse Weight')
plt.ylabel('Avg Tumor Volume')
plt.show()