import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Create 100 rows × 10 columns
columns = [f"Column_{i+1}" for i in range(10)]

# Simulate some messy data
data = {
    col: np.random.choice(
        [f"{col}_value_{i}" for i in range(50)] + [None, " ", "NA", "n/a"],
        100
    ) for col in columns
}

# Create DataFrame
df = pd.DataFrame(data)

# Introduce some numeric values as strings with extra spaces
df['Column_1'] = df['Column_1'].apply(lambda x: f" {x} " if pd.notna(x) else x)

# Save to Excel
df.to_excel("test_inventory.xlsx", index=False)

print("Test Excel file created: test_inventory.xlsx")
