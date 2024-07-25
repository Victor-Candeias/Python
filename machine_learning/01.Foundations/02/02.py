import pandas as pd

print("The panda series")

members1 = ["Brazil", "Russia", "India", "China", "South Africa"]

bricks1 = pd.Series(members1)
print(bricks1)
print(bricks1[1])

print(type(bricks1))

print("\nThe panda data frame 1\n")

members2 = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
        "capital": ["Brasilia", "Moscow", "New Delhi", "Beijing", "Pretoria"],
        "gdp": [2750, 1658, 3202, 15270, 370],
        "literacy":[.944, .997, .721, .964, .943],
        "expectancy": [76.8, 72.7, 68.8, 76.4, 63.6],
        "population": [210.87, 143.96, 1367.09, 1415.05, 57.4]}

bricks2 = pd.DataFrame(members2)
print(bricks2)
print(type(bricks2))

print("\nThe panda data frame 2\n")

members3 = [["Brazil", "Brasilia", 2750, 0.944, 76.8, 210.87],
                     ["Russia", "Moscow", 1658, 0.997, 72.7, 143.96],
                     ["India", "New Delhi", 3202, 0.721, 68.8, 1367.09],
                     ["China", "Beijing", 15270, 0.964, 76.4, 1415.05],
                     ["South Africa", "Pretoria", 370, 0.943, 63.6, 57.4]]
labels = ["country", "capital", "gdp", "literacy", "expectancy", "population"]

bricks3 = pd.DataFrame(members3, columns=labels)
print(bricks3)
print(type(bricks3))

print("\nThe panda data frame 3\n")

bricks4 = pd.read_csv("brics02.csv")
print(bricks4)
print(type(bricks4))

print("\nThe panda data frame 4\n")

bricks5 = pd.read_excel("brics02.xlsx")
print(bricks5)
print(type(bricks5))

print("\nThe panda data frame 5\n")

bricks5 = pd.read_excel("brics02.xlsx", sheet_name="Summits")
print(bricks5)
print(type(bricks5))