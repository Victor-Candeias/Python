
Classification vs. regression problems
Modeling is the fourth and most well-known stage in the machine learning process. It involves choosing and applying the appropriate machine learning approach that works 
well with the data we have and solves the problem that we intend to solve. Before we build a model, we must be clear about our objective. In supervised machine learning, 
our objective is to build a model that maps a given input, which we call the independent variables, to the given output, which we call the dependent variable. 
Depending on the nature of the dependent variable, our problem can either be called a classification problem or a regression problem. If our dependent variable is a 
categorical value such as color, yes or no, or the weather, then our model is known as a classification model. In the example shown here, we intend to use loan amount, 
loan grade, and loan purpose to predict loan default, which has categorical values of yes or no. If we intend to predict a continuous value such as age, income, or 
temperature, then our model is known as a regression model. In the example shown here, we intend to use profession, length of employment, and highest degree earned as 
predictors for income, which is a continuous value. Most popular machine learning algorithms, such as decision trees, naive Bayes, neural networks, support vector machines, 
and K-nearest neighbors can be used to solve both regression and classification problems. However, there exists a family of algorithms that are tailor-made for regression 
and regression alone. Some of them are listed here. After training a supervised machine learning model, it is important that we evaluate it to see how well suited it is to 
the problem at hand. This is the goal of the evaluation stage in the machine learning process. In order to get an unbiased evaluation of the performance of our model, 
we must train the model with a different dataset from the one we use to evaluate it. We call the data set we use to the training model the training data, and we call 
the data we use to evaluate the model the test data. During the evaluation process, we provide a model with instances of the independent variables of the test data alone 
and allow it to predict what it thinks the corresponding values of the dependent variable should be. If we are trying to solve a classification problem, 
then we use predictive accuracy as a measure of how well our model does against a test data or evaluation data. In this example, by comparing the predicted and actual 
values, we see that our model correctly predicted the labels of three out of four tests instances. Therefore, the predictive accuracy of the model is three divided by four,
 which is 0.75 or 75%. This means that going forward, we estimate that the predictions of our model will be right 75% of the time. If the problem we are trying to solve 
 is a regression problem, then we use mean absolute error as a measure of our models performance. In this example, we get the total of the absolute differences between 
 the predicted and actual income values, and divide the result by the number of test instances. This gives us 3000. This means that going forward, we estimate that the 
 predictions of our model will be off the mark by an average of about plus or minus 3000.

 How to build a machine learning model in Python
- In this exercise, we'll use a historical data set, to build a linear regression model that predicts the number of bike rentals. 
Based on weather conditions. We start by importing the Panda's package. Then we import the data into a data frame called bikes and preview it. 
Now that we have our data, let's try to understand it. First, we get a concise summary of the structure of the data. From the summary. 
We can tell that there are 731 rows in the data set and that all four columns are numeric. Next, we get summary statistics for the data. 
The statistics show the mean minimum, maximum standard deviation and present our values for the four features in the dataset. Linear regression models assume that, 
there exists a linear relationship between the predictors and the response. Let's see if this assumption holds true in our dataset, to ensure that our plot show up 
in line, we run the map plot lib inline command. Then we create a scatter plot, between the predictive variable temperature, and the response variable rentals. 
The chart shows that there is a positive linear relationship between temperature and rentals. This means that as the temperature increases, so does the number of 
bike rentals. Next, we evaluate the relationship between humidity and rentals. This chart shows that there is a negative, linear relationship between humidity and rentals. 
This means that as humidity increases, the number of bike rentals decreases, finally, we evaluate the relationship between wind speed and rentals. The chart also shows a 
negative linear relationship between wind speed and rentals. This means that the number of bike rentals decreases, as wind speed and picks up, before we build our machine 
learning model, we need to split the data into training and test sets, prior to doing this, we must first separate the dependent variable, from the independent variables. 
Let's start by creating a data frame called Y, for the dependent variable. Then we split off the independent variables, into a data frame called X. Next, 
We import the train test split function, from the SK learn model selection sub package, then we split the X and Y data frames into X train X test,
 Y train and Y test to build a linear regression model in Python, we need to import the linear regression class, from the SK learn linear model sub package. 
 We then use the function to build our model. So we use a linear regression function, within the function we call the fit method of the function, and we pass to it X train, 
 and Y train, the objective of linear regression is to estimate, the intercept and slope values for a regression line, that best fits the data. We can get the estimated 
 intercept value for a model by referring to the intercept attributes of the model. The intercept value for our regression line is 3800.68. We can also get the estimated 
 slope values, or coefficients for the regression line by referring, to the co-ed attributes of the model, the model coefficients correspond the order, in which the 
 independent variables are listed, in the training data. This means that the coefficient for temperature is 80.35. The coefficient for humidity is negative 4665.74. 
 And the coefficient for wind speed is negative 196.22. one way to evaluate a linear regression model, is by calculating the coefficient of determination, or R squared. 
 The closer this metric is to one, the better the model is. Let's get the R squared for a model. We call this score method of the model and we pass to it X test, 
 as well as Y test. The R squared value tells us that our model is able to explain 98.2% of the variability in the response values, of the test data. That is very good. 
 Another way to evaluate a linear regression model, is to evaluate how accurate it is. This means comparing the predicted values, against the actual values. First let's 
 get the models predicted response values, for the test data. We're going to call our predictions, why pred and we get the models predictions by calling the predict 
 method of the model and we pass to it, X test. Next, we import the mean absolute error function, from the SK Learn that metrics sub package and calculate the mean 
 absolute error, between the actual response values, and the predicted response values. So mean absolute error function, passed to it Y, underscore test. 
 Then we can pass to it Y, underscore pred. The mean absolute error implies that going forward. We should expect the predictions of our model, to be off the mark by an 
 average of plus or minus 194 bikes. That's pretty good. Considering the little amount of work we put into a model.

Common machine learning algorithms
During the modeling stage, it's often beneficial to experiment with multiple machine learning algorithms and to fine tune their parameters to determine which one 
performs best on our specific problem. There are several models to choose from. The specific characteristics of our data and the nature of the problem we intend to 
solve usually dictates which algorithms we can or cannot use. Let's explore a few of them. The machine learning model we built in the previous video was a linear regression 
model. It assumes that the relationship between a dependent variable and one or more independent variables is linear. As a result, the algorithm tries to find a straight 
line that does the best job of modeling this relationship using a technique known as ordinary least squares. As the name suggests, the linear regression algorithm is used 
to solve regression problems, such as predicting how many bikes customers are likely to rent based on weather conditions. Unlike linear regression, the logistic regression 
algorithm models the relationship between the independent variables and the dependent variable using an S-shaped curve known as a sigmoid curve. The curve is based on 
what is known as a logit function, which assumes a linear relationship between the predictors and the log odds of the outcome. In spite of its name, logistic regression 
is not used to solve regression problems. It's most often used for binary classification problems, such as predicting whether a customer will or will not buy a product 
based on demographic or social economic indicators. As the name suggests, a decision tree represents the relationship between the values of one or more independent 
variables and those of a dependent variable using an inverted tree-like structure made up of decision nodes and leaf nodes connected by branches. Decision trees can solve 
both classification and regression problems. Their intuitive nature makes them particularly useful in situations where transparency is crucial. For example, when building
a model that makes recommendations on loan decisions based on whether a borrower will or will not default on their loan. Inspired by biological neurons, neural networks are 
particularly effective at processing patterns of inputs and outputs using a sequence of mathematical neurons arranged in layers. This makes them invaluable for tasks such as 
image detection, speech recognition, and language translation. Neural networks are the basis of most of the recent groundbreaking advances in AI, such as deep and large 
language models. The algorithms discussed so far are all supervised machine learning algorithms, each with its particular set of strengths and weaknesses. Sometimes instead 
of using a single algorithm to solve a problem, we can bring several weak algorithms together to build a stronger and more robust model. These types of models are known as 
ensembles. Ensembles are typically used for both classification and regression tasks and are known for their resiliency and effectiveness in capturing difficult patterns in 
the data. Random forests is a common ensemble learning technique that is made up of several decision trees known as a forest trained in parallel on subsets of the data. 
In an ensemble, the allocation function determines how much of the training data to assign to each member of the ensemble, while the combination function determines how the 
output of each member is to be combined into a single output. Gradient boosting machines is another common ensemble learning technique. It is made up of several decision 
trees trained in a sequential manner where each tree tries to correct the mistakes of the previous one. Unlike supervised machine learning where the data has predictive 
variables and outcome labels, the data we use for unsupervised learning lacks predefined labels or outcome variables. The objective of unsupervised learning algorithms 
is to identify inherent patterns, structures, or groupings in data without much guidance on what to look for. Once such algorithm is k-means clustering. The algorithm 
uses an iterative approach to assign each observation in the data to one of k clusters based on similarity. The objective is to create groupings or clusters where items 
within the cluster are as similar as possible, while ensuring these items are as different as possible from items in other clusters. K-means clustering is widely used for 
tasks such as customer segmentation, document labeling, and anomaly detection. Another common approach to unsupervised machine learning is the use of association rules. 
Association rules are a set of if-then statements that describe the co-occurrence of items or events within data. They're used in a variety of domains, but are most often 
used in market basket analysis to find relationships between items that customers tend to purchase together.

