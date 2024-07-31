
Describe your data
Data exploration is the second of the six stages or steps in the machine learning process. Data exploration is a process of describing, visualizing, 
and analyzing data in order to better understand it. Data exploration enables us to answer questions such as how many rows and columns are in the data. 
What type of data do we have? Are there missing, inconsistent, or duplicate values in the data? In machine learning, we use certain key terms to describe the structure and 
nature of our data. The term instance refers to a row of data. An instance is an individual independent example of the concept represented by the data set. 
A data set consists of several instances. An instance is sometimes referred to as a record or an observation. In this example, each loan application is 
represented by an instance. Each instance is described by a set of attributes or features. A feature refers to a column of data. A feature is a property or 
characteristic of an instance. Features are sometimes referred to as variables. In this example, a loan customer's name, the loan amount, the loan grade, 
the loan purpose, and the loan outcome are all features of a loan instance. Features can be categorized based on the type of data they hold. A feature can be described as 
categorical. A categorical feature is an attribute that holds data stored in discreet form. Categorical features are typically limited to a reasonable set of possible values. 
In this example, customer name, grade, purpose, and default are categorical features. A feature can also be described as continuous. 
A continuous feature is an attribute that holds data stored in the form of an integer or real number. A continuous feature has an infinite number of possible values 
between its lower and upper bounds. In this example, the loan amount is a continuous feature. Other examples of continuous features include features such as temperature, 
height, weight, and age. Please note that not all numeric values are continuous. A numeric scale such as a Likert scale that goes from 1 to 5 is categorical and not continuous. 
It does not have an infinite number of possible values between its lower bound of 1 and its upper bound of 5. Features can also be categorized based on their function. 
In supervised machine learning, we use the values of a set of features known as independent variables to predict the value of another feature known as the dependent variable. 
If the dependent variable is categorical, we referred to it as the class. However, if it is continuous, we refer to it as a response. In this example, the loan outcome, 
which is the default feature, is the class. The dimensionality of a data set represents the number of features in the dataset. The higher the dimensionality of a dataset, 
the more detail we have about each instance. High dimensionality also means higher computational complexity. Sparsity and density describe the degree to which data 
exists for the features in the dataset. For example, if 20% of the values in the dataset are missing or undefined, we say that data set is 20% sparse. 
Density is the complement of sparsity. Therefore, a data set that is 20% sparse is 80% dense.

How to summarize data in Python
During the exploration, one of the best ways to understand the nature of the data at hand is to summarize it by computing aggregations, such as mean, median, 
maximum and minimum. These aggregations or statistical measures, as they're commonly referred to, are helpful in describing the general and specific characteristics of data. 
The Pandas data frame provides several easy to use methods that help us describe and summarize data. One of these methods is the info method. Given a data frame called 
washers, we can get a concise summary of its rows and columns by calling it's info method. From the output, we can tell the washers data frame has 261 rows and 18 columns. 
Five of the columns hold decimal values, three hold integer values and 10 hold textual data. If we want a sneak peek of the data stored in the data frame, we can call it's 
head method. As we can see from the output, the head method returns just the first five rows in the data frame. This provides us with a high level 
view of the data we're working with. Now that we know what the data looks like, we can start to dive a little deeper into the nature of the values. 
The describe method of a data frame is useful for this, the method returns a statistical summary of each of the columns in a data frame. It's important to note 
that the descriptive statistics returned by the describe method depends on the data type of a column. For example, let's get the descriptive statistics for the 
non-numeric brand name column in the washers data frame. To do this, we specify the column that we want, which is brand name. Then we call the describe method for this column. 
The output tells us that there are 261 non missing values in the brand name column. It also tells us that there are 22 unique washer brands in the data. Of the unique brands, 
LG is the most occurring with 50 washers listed under the LG brand. To illustrate how the describe method works for numeric columns, 
let's get a descriptive statistics for the volume column in the washers data frame. So we start by selecting the column that we want, volume. 
Then we call the describe method. From the statistics, we can tell that the average, minimum and maximum volumes of the washers in the data are 4.4, 1.9 and 6.2 cubic 
feet respectively. Instead of getting a pre-packaged list of statistical measures, we can also compute specific aggregations for certain columns in a data frame. 
The Pandas package provides several data frame methods to do this. For example, we can get a count of each unique washer brand in the data frame. We start by specifying 
the column that we want, this time around we also want the brand name. We call the value counts method, and this gives us a list. Sometimes it's more useful to get a 
percentage rather than a count. To do so, we modify the code we ran in the previous cell. Within the value counts method, we specify a value for normalize to true. 
Now we get a percentage representational distribution for each brand of washer. The output tells us that 18% of the washers in the data are Samsung washers. 
For numeric columns, we can get specific aggregations as well. For example, we can compute the average volume of washers in the dataset. So let us get the washers, 
volume column, and we compute the mean. 4.37. We can also get specific aggregations at the group level. For example, we can compute the average volume of washers by brand. 
To do this, we specify the data frame washers, call the group by method and pass to it the column on which we want to group by, which is brand name. Next, 
we specify the column we want to aggregate by, which is volume. And we call the mean method. This result is sorted by brand to help us better compare the average washer 
volumes across brands. Let's sort the data in ascending order of average volume. To do this, we make a slight modification to our code. We add a sort values method and say 
sort by volume. Now our washer mean volumes by brand is sorted by the mean volumes for each washer brand. Now we can clearly see that on an average, 
Beko washers have the smallest volume, while Midea washers have the largest volume. We can also compute more than one specific aggregation at once. For example, let's 
compute the average median minimum and maximum washer volume for each brand. To help us along the way, part of the code has already been written. What we need to do 
now is to use the dot ag method and within the method we specify the aggregations that we want. So we want the mean, we also want median. We want min and we want max. 
The methods introduced here are just the tip of the iceberg. To explore some of the other methods which are useful in summarizing data, visit the Pandas documentation site.

Visualize your data
Data exploration is a second of the six stages of steps in the machine learning process. Data exploration is a process of describing, visualizing, 
and analyzing data in order to better understand it. By exploring our data, we can answer questions such as. How many rows and columns are in the data? 
What type of data do we have? Are there missing, inconsistent, or duplicate values in the data? During data exploration, even after using sophisticated statistical 
techniques to analyze data, certain patterns are best understood when represented with a visualization. Like the popular saying goes, 
"A picture is worth a thousand words." Visualizations serve as a great tool for asking and answering questions about data. Depending on the type of question we are trying 
to answer, there are four major types of visualizations we could use. The first is a comparison visualization. Comparison visualizations are used to illustrate the 
difference between two or more items at a given point in time or over a period of time. One of the most commonly used comparison visualizations is a box plot. 
Using a box plot, we can compare the distribution of values for a continuous feature against the values of a categorical feature. For example, this box plot 
compares carbon dioxide emissions values across vehicle class. Based on the visualization, we can tell that on average pickups and vans have higher carbon emissions than
compact and midsize cars. Comparison visualizations provide insights such as the significance of a feature, the variation in the median or mean value of a feature across 
subgroups, and the existence of outliers in the values of a feature. Relationship visualizations are used to illustrate the correlation between two or more continuous 
variables. Scatter plots and line charts are two of the most commonly used relationship visualizations. They show how one variable changes in response to a change in another. 
For example, this scatter plot highlights the negative relationship between vehicle emissions levels and city mileage. Specifically, vehicles with higher city mileage ratings 
emit less carbon. Besides illustrating how two features interact with each other, relationship visualizations also provide insight into the significance of a 
feature and the existence of outliers within the values of a feature. The third type of visualization is a distribution visualization. As the name suggests, 
these types of visualizations illustrate the statistical distribution of the values of a feature. One of the most commonly used distribution visualizations is the histogram. 
With a histogram, we can figure out the most common values of a feature. For example, this histogram shows that most vehicles in the dataset have carbon emissions values 
between 300 and 700 grams per mile. Histograms visualize the spread or skewness in the values of a feature. They also highlight the presence of outliers in the data. 
A composition visualization shows the component makeup of our data. Stacked bar charts, grouped bar charts, and pie charts are three of the most commonly used composition 
visualizations. Stacked bar charts show how much a subgroup contributes to the hole. For example, based on this stacked bar chart, we can figure out the proportion of 
vehicles each year that are front wheel drive, all wheel drive, and rear wheel drive within the dataset. Besides illustrating how much a subgroup contributes to the total, 
composition visualizations can also illustrate the relative or absolute change in a subgroup composition over time.

How to visualize data in Python
Like the popular saying, "a picture is worth a thousand words." Visualizations are sometimes more useful than summary statistics in helping us understand our data. 
One of the most popular visualization packages in Python is a matplotlib package, which provides a host of powerful functions and methods that allow us to 
produce publication quality visualizations. The plot method of a Pandas dataframe provides an abstraction of the matplotlib functions. To ensure that the plots we 
create in this tutorial appear right after our code, we have to run the following command. Next, let's import and preview the data we will use for our illustrations. 
The first type of plot we create is a relationship visualization. These types of visualizations are used to illustrate the correlation between two or more continuous variables. 
Scatter plots are one of the most commonly used relationship visualizations. They show how one variable changes in response to a change in another. To create a scatter plot, 
we start with our data frame vehicles. We call the plot method within the method, we specify the value for the kind arguments as scatter, we specify a value for the X axis, 
here we choose city MPG and we specify a value for the Y axis. Here we choose CO2 emissions. The plot that we have shows that the relationship between vehicle emissions 
levels and city mileage is negative. In other words, vehicles with higher mileage ratings emit less carbon. Next, we create a distribution visualization. 
As the name suggests, distribution visualizations illustrate this statistical distribution of the values of a feature. One of the most commonly used distribution 
visualizations is the histogram. With a histogram, we can figure out which values are most common for a feature. To create a histogram, we start with our vehicles data, 
and we specify the column that we want. So here we choose CO2 emissions. Then we call the plot method. And within the method we specify the value for the kind argument 
which this time around is hissed. The plot shows that the carbon emissions values for the vehicles in the dataset range from just on the 200 grams per mile, to just over a 
thousand grams per mile. It also shows a most vehicles fall within the 300 to 700 grams per mile range. Comparison visualizations are used to illustrate the 
difference between two or more items at a given point in time or over a period of time. One of the most commonly used comparison visualizations is the box plot. 
Using a box plot, we can compare the distribution of values for a continuous feature against the values of a categorical feature. To create a box plot in Python, we must 
first create a pivot table, such that the value we want on the X axis of our plot are listed as column labels while the values we want on the Y axis of our plot are the cell 
values. To create the pivot table, we begin with our vehicles dataset. We call the pivot method. Within the method, we specify a value for the columns. 
Here we specify the value as drive, and we specify a value for the cells, which is the values argument and we specify this as CO2 emissions. Note that the value 
NAN is an acronym for not a number and is how a pan does dataframe represents missing values. The emissions values are missing for every column except the one that 
corresponds with a drive type for a particular vehicle. For example, we can tell that the first vehicle in our table is a two wheel drive vehicle while the fourth 
one is a rare wheel drive vehicle. With our data in this format, we can then create a box plot. So we have some of the code already written for us here, so we call the 
plots method and within the method, we specify kind = box plus, we want a box plot, and we also specify a figure size of 10 by six. The plot shows that on average front 
wheel drive cars have lower carbon emissions than other types of cars. Our fourth visualization is a composition visualization. These types of visualizations show the 
component makeup of data. Stacked bar charts are one of the most commonly used composition visualizations. Stacked bar charts show how much a subgroup contributes to the 
whole. To create a stacked bar chart in Python, we must first create a pivot table so that the values we want on the X axis of our plot are listed as row labels while the 
composite groups are listed as column labels. To do this, we start with a group level aggregation. So we start with our vehicles data, we grouped by year, we specify 
or select the drive, the column we want, which is drive and we call value counts to give us a unique count of values. The next thing we do is call the unstack method to 
pivot that innermost index, which is drive to column labels, unstack. Now that our data is in this format, we can create a stat bar chart. So here we call the plot method 
within the method when we specify a value for kind this time around it's bar stat = 2. We're going to stat bar chart. This will specify fixed size and by six. 
The plot shows the total number of vehicles rated by the EPA each year, as well as the proportion of front wheel, all wheel, and rear wheel vehicles that make up those numbers.

