import pandas as pd
import re
df = pd.read_csv("E:\\Coding\\Fleet\\CSV_FILES\\truck_transformed.csv")
def clean_fuel_tank(value):
    value = str(value)
    value = value.replace("\n", " ")
    value = value.strip()
    nums = re.findall(r"\d+\.?\d*", value)
    if not nums:
        return None
    nums = [float(x) for x in nums]
    return max(nums)

def clean_mileage(value):
    value = str(value)
    nums = re.findall(r"\d+\.?\d*", value)
    if not nums:
        return None
    nums = [float(x) for x in nums]
    return sum(nums) / len(nums)


df["fuel_tank_liters"] = df["fuel_tank"].apply(clean_fuel_tank)
df["mileage_kmpl"] = df["mileage"].apply(clean_mileage)
df = df[
    [
        "brand",
        "model",
        "fuel_type",
        "fuel_tank_liters",
        "mileage_kmpl"
    ]
]

df.to_csv(
    "E:\\Coding\\Fleet\\CSV_FILES\\truck_cleaned.csv",
    index=False
)

print(df.head(10))
