import pandas as pd
import os
from os import path
import pymssql

# delete files
if path.exists("filtered_grouped_data.csv"):
    # get the path to the file in the current directory
    src = path.realpath("filtered_grouped_data.csv")
    
    # delete
    os.remove(src)

df = pd.read_csv("ExportTargetone_0.csv")

# df = pd.DataFrame(data)

# Group by TransStartNum and filter groups containing at least one row with Account 410
filtered_groups = df.groupby('TransStartNum').filter(lambda x: (x['Account'] == 410).any())

# Display the filtered result
print(filtered_groups)

