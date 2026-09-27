import pandas as pd

# Dataset loaded 
df = pd.read_csv("dataset/sales_dataset.csv")

# Display basic information
print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

#Checking the missing values
print("\nMissing Values:")
print(df.isnull().sum())

#Checking the duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Cleaning column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

#Removed duplicate rows
df = df.drop_duplicates()

#Removed completely empty rows
df = df.dropna(how="all")

#Displed information after cleaning
print("\nAfter Cleaning:")
print("Dataset Shape:", df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# now saved the cleaned dataset
df.to_csv("dataset/cleaned_sales_data.csv", index=False)

print("\nCleaned dataset saved successfully!")