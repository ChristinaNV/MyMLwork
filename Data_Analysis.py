import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from a CSV file into a pandas DataFrame
data = pd.read_csv('data.csv')

# Display basic information about the DataFrame
print(data.info())

# Display the first few rows of the DataFrame
print(data.head())

# Perform basic summary statistics
print(data.describe())

# One-hot encode categorical columns
encoded_data = pd.get_dummies(data, columns=['gender', 'location', 'education', 'occupation'])

# Create a correlation matrix and visualize it using a heatmap
correlation_matrix = encoded_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

# Create a histogram of the 'age' column
plt.figure(figsize=(8, 6))
sns.histplot(data['age'], bins=20, kde=True)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()
