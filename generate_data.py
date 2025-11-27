import pandas as pd

data = {
    'Hours': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Score': [15, 28, 42, 54, 68, 75, 82, 94, 98, 99]
}

df = pd.DataFrame(data)
df.to_excel('test_data.xlsx', index=False)
print("test_data.xlsx created")
