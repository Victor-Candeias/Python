import pandas as pd

# how to summarize data um python

# open file
washers = pd.read_csv("washers.csv")

# how to describe a DataFrame
# Concise summary of rows and columns
# washers.info()

#
#<class 'pandas.core.frame.DataFrame'>
#RangeIndex: 261 entries, 0 to 260
#Data columns (total 18 columns):
# #   Column         Non-Null Count  Dtype  
#---  ------         --------------  -----  
# 0   ID             261 non-null    int64  
# 1   BrandName      261 non-null    object 
# 2   ModelNumber    261 non-null    object 
# 3   UPC            261 non-null    object 
# 4   Configuration  261 non-null    object 
# 5   Features       202 non-null    object 
# 6   Market         261 non-null    object 
# 7   Volume         261 non-null    float64
# 8   IMEF           261 non-null    float64
# 9   MinimumIMEF    261 non-null    float64
# 10  EnergyUse      261 non-null    int64
# 11  IWF            261 non-null    float64
# 12  MaximumIWF     261 non-null    float64
# 13  WaterUse       261 non-null    int64
# 14  DateAvailable  261 non-null    object
# 15  DateCertified  261 non-null    object
# 16  Countries      261 non-null    object
# 17  MostEfficient  261 non-null    object
#dtypes: float64(5), int64(3), object(10)
#memory usage: 36.8+ KB

# if we want get a resume view of the DataFrame
# we can look at the first rows
# print(washers.head())

#         ID BrandName   ModelNumber          UPC  ... DateAvailable DateCertified              Countries  MostEfficient
# 0  2342279        GE  GTW845C*N***            1  ...        8/5/19       7/31/19  United States, Canada             No
# 1  2331684        GE  GUD27EE*N***  84691844198  ...      12/10/18      11/30/18          United States             No
# 2  2331685        GE  GUD27EE*N***  7.57638E+11  ...      12/10/18      11/30/18                 Canada             No
# 3  2331687        GE  GUD27GE*N***  84691844181  ...      12/10/18      11/30/18          United States             No
# 4  2331686        GE  GUD37EE*N***  7.57638E+11  ...      12/10/18      11/30/18                 Canada             No

# [5 rows x 18 columns]

# get a statics view of a non numeric column of the DataFrame
# print(washers[["BrandName"]].describe())

#        BrandName
# count        261 - non missing values
# unique        22 - unique values
# top           LG - this is the most occurrence
# freq          50

# get a statics view of a numeric column of the DataFrame
# print(washers[["Volume"]].describe())

#            Volume
# count  261.000000
# mean     4.374713
# std      0.965866
# min      1.900000
# 25%      4.300000
# 50%      4.500000
# 75%      5.000000
# max      6.200000

# get a specific aggregations of a numeric column of the DataFrame
# count of each unique Brand of the DataFrame
# print(washers[["BrandName"]].value_counts())

# BrandName      
# LG                 50
# GE                 49
# Samsung            47
# Kenmore            30
# Whirlpool          26
# Maytag             18
# Electrolux          7
# Asko                4
# Bosch               4
# Miele               4
# Beko                3
# Crosley             3
# Blomberg            3
# Amana               2
# Magic Chef          2
# Fisher & Paykel     2
# Midea               2
# Insignia            1
# GE Adora            1
# Inglis              1
# Haier               1
# Gaggenau            1
# Name: count, dtype: int64

# count of each unique Brand of the DataFrame in percentage
# print(washers[["BrandName"]].value_counts(normalize=True))

# BrandName      
# LG                 0.191571
# GE                 0.187739
# Samsung            0.180077
# Kenmore            0.114943
# Whirlpool          0.099617
# Maytag             0.068966
# Electrolux         0.026820
# Asko               0.015326
# Bosch              0.015326
# Miele              0.015326
# Beko               0.011494
# Crosley            0.011494
# Blomberg           0.011494
# Amana              0.007663
# Magic Chef         0.007663
# Fisher & Paykel    0.007663
# Midea              0.007663
# Insignia           0.003831
# GE Adora           0.003831
# Inglis             0.003831
# Haier              0.003831
# Gaggenau           0.003831
# Name: proportion, dtype: float64

# avarage value of the column value
# print(washers[["Volume"]].mean())

# Volume    4.374713
# dtype: float64

# How to get group level aggregations
# print(washers.groupby('BrandName')[['Volume']].mean())

#                    Volume
# BrandName
# Amana            4.250000
# Asko             2.525000
# Beko             2.133333
# Blomberg         2.300000
# Bosch            2.200000
# Crosley          4.400000
# Electrolux       3.785714
# Fisher & Paykel  2.400000
# GE               4.328571
# GE Adora         4.200000
# Gaggenau         2.200000
# Haier            2.400000
# Inglis           4.300000
# Insignia         4.800000
# Kenmore          4.796667
# LG               4.596000
# Magic Chef       2.700000
# Maytag           4.988889
# Midea            5.200000
# Miele            2.300000
# Samsung          4.729787
# Whirlpool        4.453846

# How to get group level aggregations order by
# print(washers.groupby('BrandName')[['Volume']].mean().sort_values(by = 'Volume'))

# 	                   Volume
# BrandName
# Beko             2.133333
# Bosch            2.200000
# Gaggenau         2.200000
# Miele            2.300000
# Blomberg         2.300000
# Haier            2.400000
# Fisher & Paykel  2.400000
# Asko             2.525000
# Magic Chef       2.700000
# Electrolux       3.785714
# GE Adora         4.200000
# Amana            4.250000
# Inglis           4.300000
# GE               4.328571
# Crosley          4.400000
# Whirlpool        4.453846
# LG               4.596000
# Samsung          4.729787
# Kenmore          4.796667
# Insignia         4.800000
# Maytag           4.988889
# Midea            5.200000

print(washers.groupby('BrandName')[['Volume']].agg(['mean','median','min','max']))

#                    Volume
#                      mean median  min  max
# BrandName
# Amana            4.250000   4.25  4.2  4.3
# Asko             2.525000   2.70  2.0  2.7
# Beko             2.133333   2.00  1.9  2.5
# Blomberg         2.300000   2.50  1.9  2.5
# Bosch            2.200000   2.20  2.2  2.2
# Crosley          4.400000   4.50  4.2  4.5
# Electrolux       3.785714   4.30  2.4  4.4
# Fisher & Paykel  2.400000   2.40  2.4  2.4
# GE               4.328571   4.50  2.2  5.2
# GE Adora         4.200000   4.20  4.2  4.2
# Gaggenau         2.200000   2.20  2.2  2.2
# Haier            2.400000   2.40  2.4  2.4
# Inglis           4.300000   4.30  4.3  4.3
# Insignia         4.800000   4.80  4.8  4.8
# Kenmore          4.796667   4.80  2.4  6.2
# LG               4.596000   4.50  2.3  5.8
# Magic Chef       2.700000   2.70  2.7  2.7
# Maytag           4.988889   4.90  4.4  6.2
# Midea            5.200000   5.20  5.2  5.2
# Miele            2.300000   2.30  2.3  2.3
# Samsung          4.729787   4.80  2.2  5.6
# Whirlpool        4.453846   4.50  2.0  5.3