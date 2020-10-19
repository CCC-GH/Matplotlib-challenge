'''
05-Matplotlib Homework
'''
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
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
#
# Checking the number of mice.
print('\nNumber of mice after merge: ' + str(merged_df['Mouse ID'].count())+'\n')
#
# Getting the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
dupRows_df = merged_df[merged_df.duplicated(['Mouse ID', 'Timepoint'])]
print('\nDuplicate records with same Mouse IDs and Timepoints:')
print(dupRows_df)
#
# Optional: Get all the data for the duplicate mouse ID. 
allDupRows_df = merged_df[merged_df.duplicated(['Mouse ID'])]
print('\nDuplicate records with same Mouse IDs:')
print(allDupRows_df)
# Create a clean DataFrame by dropping the duplicate mouse by its ID.
cleaned_merged_df = merged_df.drop_duplicates('Mouse ID')
# Checking the number of mice in the clean DataFrame.
print('\nNumber of Mice after clean: ' + str(cleaned_merged_df['Mouse ID'].count())+'\n')
#
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
#
# Generate a bar plot showing the total number of unique mice tested on each drug regimen using pandas
drug_df = pd.DataFrame(merged_df.groupby(['Drug Regimen']).count()).reset_index()
drugs_df = drug_df[['Drug Regimen', 'Mouse ID']]
drugs_df = drugs_df.set_index('Drug Regimen')
drugs_df.plot(kind='bar', legend=False)
plt.xlabel('Drug Regimen')
plt.ylabel('Data Points')
plt.title('#Mice in each Regimen (pandas)')
plt.show()
# Generate a bar plot showing the total number of unique mice tested on each drug regimen using pyplot
drug1_df = merged_df.groupby('Drug Regimen').count()['Tumor Volume (mm3)']
drugs1_df = pd.DataFrame(drug1_df)
plt.xdata = drugs1_df.plot.bar(legend=False)
plt.xlabel('Drug Regimen')
plt.ylabel('Data Points')
plt.title('#Mice in each Regimen (pyplot)')
plt.show()
#
# Generate a pie plot showing the distribution of female versus male mice using pandas
gender_df = pd.DataFrame(merged_df.groupby(["Sex"]).count()).reset_index()
gender_df=gender_df[['Sex','Mouse ID']]
plt.figure(figsize=(10,4))
axis = plt.subplot(121, aspect='equal')
gender_df.plot(kind='pie', y = 'Mouse ID', ax=axis, autopct='%1.2f%%',
              startangle=90,labels=gender_df['Sex'], legend=False)
plt.title('% Female vs Male Mice (pandas)')
# Null label to match other chart
plt.ylabel('')
plt.show()
# Generate a pie plot showing the distribution of female versus male mice using pyplot
genderCount = (merged_df.groupby(['Sex'])['Age_months'].count()).tolist()
labels = ['Female', 'Male']
plt.pie(genderCount, autopct='%1.2f%%', startangle=90, labels=labels)
plt.title('% Female vs Male Mice (pyplot)')
plt.show()
#
# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin
# Start by getting the last (greatest) timepoint for each mouse
sort_df = merged_df.sort_values(['Drug Regimen', 'Mouse ID', 'Timepoint'], ascending=True)
last_df = sort_df.loc[sort_df['Timepoint'] == 45]
# Merge this group df with the original dataframe to get the tumor volume at the last timepoint
# Capomulin
cap_df = merged_df.loc[merged_df["Drug Regimen"] == "Capomulin",:]
cap_max = cap_df.groupby('Mouse ID').max()['Timepoint']
cap_max_df = pd.DataFrame(cap_max)
cap_max_merge = pd.merge(cap_max_df,merged_df,on=("Mouse ID","Timepoint"),how="left")
# Ramicane
ram_df = merged_df.loc[merged_df["Drug Regimen"] == "Ramicane", :]
ram_max = ram_df.groupby('Mouse ID').max()['Timepoint']
ram_max_df = pd.DataFrame(ram_max)
ram_max_merge = pd.merge(ram_max_df,merged_df,on=("Mouse ID","Timepoint"),how="left")
# Infubinol
inf_df = merged_df.loc[merged_df["Drug Regimen"] == "Infubinol", :]
inf_max = inf_df.groupby('Mouse ID').max()['Timepoint']
inf_max_df = pd.DataFrame(inf_max)
inf_max_merge = pd.merge(inf_max_df,merged_df,on=("Mouse ID","Timepoint"),how="left")
# Ceftamin
cef_df = merged_df.loc[merged_df["Drug Regimen"] == "Ceftamin", :]
cef_max = cef_df.groupby('Mouse ID').max()['Timepoint']
cef_max_df = pd.DataFrame(cef_max)# Put treatments into a list for for loop (and later for plot labels)
cef_max_merge = pd.merge(cef_max_df,merged_df,on=("Mouse ID","Timepoint"),how="left")
#
# Capomulin
cap_tumors = cap_max_merge["Tumor Volume (mm3)"]
cap_quart = cap_tumors.quantile([.25,.5,.75])
cap_lowerq = cap_quart[0.25]
cap_upperq = cap_quart[0.75]
cap_iqr = cap_upperq-cap_lowerq
cap_lower = cap_lowerq - (1.5*cap_iqr)
cap_upper = cap_upperq + (1.5*cap_iqr)
print(f"Capomulin outliers below {round(cap_lower,2)} and above {round(cap_upper,2)}")
# Ramicane
ram_tumors = ram_max_merge["Tumor Volume (mm3)"]
ram_quart = ram_tumors.quantile([.25,.5,.75])
ram_lowerq = ram_quart[0.25]
ram_upperq = ram_quart[0.75]
ram_iqr = ram_upperq-ram_lowerq
ram_lower = ram_lowerq - (1.5*ram_iqr)
ram_upper = ram_upperq + (1.5*ram_iqr)
print(f"Ramicane outliers below {round(ram_lower,2)} and above {round(ram_upper,2)}")
# Infubinol
inf_tumors = inf_max_merge["Tumor Volume (mm3)"]
inf_quart = inf_tumors.quantile([.25,.5,.75])
inf_lowerq = inf_quart[0.25]
inf_upperq = inf_quart[0.75]
inf_iqr = inf_upperq-inf_lowerq
inf_lower = inf_lowerq - (1.5*inf_iqr)
inf_upper = inf_upperq + (1.5*inf_iqr)
print(f"Infubinol outliers below {round(inf_lower,2)} and above {round(inf_upper,2)}")
# Ceftamin
cef_tumors = cef_max_merge["Tumor Volume (mm3)"]
cef_quart = cef_tumors.quantile([.25,.5,.75])
cef_lowerq = cef_quart[0.25]
cef_upperq = cef_quart[0.75]
cef_iqr = cef_upperq-cef_lowerq
cef_lower = cef_lowerq - (1.5*cef_iqr)
cef_upper = cef_upperq + (1.5*cef_iqr)
print(f"Ceftamin outliers below {round(cef_lower,2)} and above {round(cef_upper,2)}")
#
# Generate a box plot of the final tumor volume of each mouse across four regimens of interest
# Capomulin
cap_box, cap_axis = plt.subplots()
cap_axis.set_title('Capomulin Drug')
cap_axis.set_ylabel('Final Tumor Volume')
cap_axis.boxplot(cap_tumors)
plt.show()
# Ramicane
ram_box, ram_axis = plt.subplots()
ram_axis.set_title('Ramicane Drug')
ram_axis.set_ylabel('Final Tumor Volume')
ram_axis.boxplot(ram_tumors)
plt.show()
# Infubinol
inf_box, inf_axis = plt.subplots()
inf_axis.set_title('Infubinol Drug')
inf_axis.set_ylabel('Final Tumor Volume')
inf_axis.boxplot(inf_tumors)
plt.show()
# Ceftamin
cef_box, cef_axis = plt.subplots()
cef_axis.set_title('Ceftamin Drug')
cef_axis.set_ylabel('Final Tumor Volume')
cef_axis.boxplot(cef_tumors)
plt.show()
# Generate a line plot of tumor volume vs. time point for a mouse treated with Capomulin
cMouse_df = merged_df.loc[merged_df["Mouse ID"] == "m601"]
cMouse_df = cMouse_df.reset_index()
xAxis = cMouse_df["Timepoint"]
yAxis = cMouse_df["Tumor Volume (mm3)"]
plt.title('Mouse m601 Treated with Capomulin')
plt.xlabel('Time Point (days)')
plt.ylabel('Tumor Volume (mm3)')
plt.plot(xAxis,yAxis,linewidth=2, markersize=15)
plt.show()
#
# Generate a scatter plot of average tumor volume vs. mouse weight for the Capomulin regimen
capomulin_df = merged_df.loc[merged_df["Drug Regimen"] == "Capomulin"]
capomulin_df = capomulin_df.reset_index()
weight_df = capomulin_df.loc[:, ["Mouse ID", "Weight (g)", "Tumor Volume (mm3)"]]
avg_capo = pd.DataFrame(weight_df.groupby(["Mouse ID", "Weight (g)"])["Tumor Volume (mm3)"].mean()).reset_index()
avg_capo = avg_capo.rename(columns={"Tumor Volume (mm3)": "Average Volume"})
avg_capo.plot(kind="scatter", x="Weight (g)", y="Average Volume", grid=True, figsize=(6,4), title="Weight vs. Average Tumor Volume")
plt.show()
#
# Calculate the correlation coefficient and linear regression model 
# for mouse weight and average tumor volume for the Capomulin regimen
from scipy.stats import linregress
x_value = avg_capo['Weight (g)']
y_value = avg_capo['Average Volume']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_value, y_value)
regress_value = x_value * slope + intercept
line_eq = 'y = ' + str(round(slope,2)) + 'x + ' + str(round(intercept,2))
plt.scatter(x_value, y_value)
plt.plot(x_value,regress_value,'r-')
plt.annotate(line_eq,(15,10),fontsize=15,color='red')
plt.xlabel('Mouse Weight')
plt.ylabel('Avg Tumor Volume')
plt.show()