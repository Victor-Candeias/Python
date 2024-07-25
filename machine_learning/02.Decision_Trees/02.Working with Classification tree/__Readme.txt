In this exercise, we'll use a sample loans data set to build a classification tree that predicts 
whether a borrower will default or not default on a new loan. Before we get started, note that this 
video is the first in a three video sequence, that explains how to build, visualize, and prune a 
classification tree. We start by importing the Pandas package. Then we import the data into a data 
frame called loan and preview it to make sure that the input worked as expected. Now that we have 
our data, let's try to understand it. First, we get a concise summary of the structure of the data 
by calling the info method of the data frame. From the summary, we can tell that there are 30 
instances in the dataset by looking at the range index. We can also tell that there are three 
features in the dataset. Looking at the D type column of the summary, we see that the income and 
loan amount columns hold integer values while the default column holds text, AKA object. Next, 
we get summary statistics for the data by calling the described method of the data frame. 
From the statistics, we see that the minimum income value in the data is five. While the maximum 
value is 34. Note that these values are in the thousands. So what we're seeing here is $5,000 
and $34,000. Likewise, the average loan amount is $51,967. Next, let's also visually explore 
the data by creating a few plots. To ensure that our plots show up in line, we run the map plot 
lib in line command. Then, we import two packages, mapplotlib pyplot and the seaborne package. 
The first plot we create is a boxplot. This is a plot to show the difference in annual income 
between those that did not default, which is no, and those that did default, which is yes The plot 
shows that those that did not default on their loans tend to have a higher annual income. 
Next, let's create another boxplot to show the difference in loan amount between those that 
did not default on their loans and those that did. This chart shows that those that defaulted on 
their loans tend to have borrowed a little slightly more than those that did not. Finally, 
let's create a scatter plot to look at the relationship between income and loan amount. 
This chart doesn't show a clear linear relationship between those two variables. 
There isn't much we can really infer from it, so we can move on now. Before we build our 
classification tree though, we need to split the data into training and test sets. 
Prior to doing so, we must first separate the dependent variable from the independent variables. 
Let's start by creating a data frame called Y for the dependent variable, which is default. 
Then we also do the same and create a second data frame called X for the independent variables, 
income and loan amount. Now that we have our two data frames, we need to now build our model. 
We can now split our data, before we do so, we have to import the train test split function 
from the SK learn model selections package. Using this, we can split the data, the X and Y data frames, 
into X_train X_test, Y_train and Y_test. Note that here we set train size to 0.8. 
This means we want 80% of the original data to become the training data, while 20% becomes the 
test data. We also set stratify as y which means we want the data splits using stratified 
random sampling based on the values of y. Finally, we set random state to 1234, simply so we get 
the same results every time we do the split. Now that our data is split, the shape attribute of 
the X_train and X_test data frames tell us how many instances, or records, are in each data frame. 
We can see that we have 24 instances in the training set and six instances in the test set. 
To build a classification tree in Python, we need to import the decision tree classifier class 
from the SK learn tree sub package. We then instant sheet an object from the class. 
We call the object classifier. Now that we have an object, we can build or fit a classification 
tree model using the training data. To evaluate and estimate the future performance of our model, 
we can now see how this model fits against the test data. To do so, we pass the test data to the 
score method of the model. This returns the accuracy of the model against the test data. Hmm, a 
classification tree is only able to accurately explain 50% of the relationship between the independent 
variables and a dependent variable within the test data. That's no better than a coin toss. 
We can do better. Over the course of the next two videos, we will visualize this tree then attempt 
to improve its performance. I'll see you there.
