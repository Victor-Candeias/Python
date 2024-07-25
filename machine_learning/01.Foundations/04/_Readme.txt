
Common data quality issues
An ideal dataset is one that has no missing values and has no values that deviates from the expected. Such a dataset hardly exists, if at all. In reality, 
most datasets have to be transformed or have data quality issues that need to be dealt with prior to being used for machine learning. 
This is what the third stage in the machine learning process is all about, data preparation. Data preparation is a process of making sure that our data is suitable 
for the machine learning approach that we choose to use. In computing, the saying, "Garbage in, garbage out," is used to express the idea that incorrect or poor quality 
input will invariably result in incorrect or poor quality output. This concept is fundamentally important in machine learning. 
If proper care is not taken on the front-end to properly deal with data quality issues before building the model, then the model output will be unreliable, 
misleading, or simply wrong. One of the most commonly encountered data quality issues is that of missing data. There are several reasons why data could be missing. 
They include changes in data collection methods, human error, bias, or simply the lack of reliable input. Before we resolve missing data, we should attempt to 
understand why the data is missing and if there is a pattern to the missing values. There are several approaches to dealing with missing data. One approach is to 
simply remove all instances with features that have a missing value. Another is to use an indicated value, so just NA, unknown, or negative one to represent missing values. 
An alternative approach is to use a method known as imputation. Imputation is this use of a systematic approach to fill in missing data by using the most probable 
substitute value. There are several approaches to imputation. One of which is known as median imputation. With median imputation, we can resolve the missing value in the 
amount column by replacing the missing value with a median of the non-missing values. Another common data quality problem is that of outliers. 
An outlier is a data point that is significantly different from other observations within the dataset. Outliers manifest either as instances with characteristics 
different from most other instances or as values of a feature that are unusual with respect to the typical values for the feature. Before we decide what to do with the 
outlier data, we must first understand why it exists and whether it is useful towards our machine learning goal. Supervised machine learning algorithms learn by identifying 
rules or estimating the function that explains the value of the dependent variable based on the values of the independent variables. If the values of the dependent 
variable are categorical, we refer to them as class labels and the proportion of examples that belong to each class label is known as a class distribution. 
For most real world problems, the class distribution of the historical data is not uniform. For example, the vast majority of people who take out loans pay them back. 
This means the historical loan datasets will typically have a lot more examples of people who repay their loans than examples of people who default on their loans. 
This phenomenon is known as class imbalance. Class imbalance is a well-known data quality problem in machine learning. If not properly accounted for, class imbalance can 
lead to rather misleading results because the machine learning model we build will not have an equal shot at learning the patterns that correspond to each class label. 
There are several ways to resolve class imbalance. One approach is to under sample the majority class. This means that we randomly remove some of the instances of the 
majority class in an attempt to even the class distribution.

How to resolve missing data in Python
During the exploration, we may find that some of our data is missing or incomplete. Missing data could arise as a result of changes in data collection methods, 
human error, bias, or simply the lack of reliable input. There are several ways to deal with missing data in Python. To illustrate how to deal with missing values, 
let's import a sample student dataset from an Excel spreadsheet and preview it. We can see that there are missing values in several of the columns in our data frame 
in order to list the rows of missing values for a particular column, we make use of the isnull method of a Pandas data frame to create a filter or a mask. 
For example, we can list a rows in the data frame with missing state values as follows. Mask, students, data frame, specify the column we want, which is state, 
called the isnull method, and we output our mask. The mask object is a series object, a boolean series object, to be more precise. The rows of the series 
correspond to those of the students data frame. The values of the series are true if the corresponding state value is missing, and false if the value is not missing. 
We can use this series as a mask to filter the students data frame. To do so, specify students, data frame, and we index by mask. What we now have are all the 
rows in the students data frame with missing values in the state column. After we identify the rows with missing values in our data, we could decide to simply remove them. 
The dropna method of a Pandas data frame allows us to do this. For example, to drop any rows with missing values in the students data frame, we do the following. Students, 
dropna method. We are now left with six rows with no missing values. That means we dropped 14 rows. As you can probably tell, this approach is rather extreme. Most often, 
what we really want is to remove rows with missing data for certain columns only. For example, we could decide to remove the rows with missing values in just the state 
and zip columns. To do so, we specify two arguments for the dropna method. The first is subset. The subset arguments we set to the columns that we want, state and zip. 
The how arguments we specify as all. Instead of dropping 14 rows, as we did in the previous example, the only rows dropped now are the first two rows in the data frame, 
which have missing values for both the state and zip columns. These are rows with index values of zero and one. We could also decide to drop columns with missing data 
instead of rows with missing data. For example, to drop any columns with missing values in the students data frame, we do the following. Students, dropna, we specify a 
value for the access argument as one. That leaves us with five columns that have no missing values. This is an extreme approach as well. Most often, what we really 
want is to only drop columns with a certain number of missing values. For example, let's say we decide to remove any columns with 50% of the rows missing. 
Since we had 20 rows in our original data, we set the threshold to 10, as follows. Within our dropna method, we specify two arguments. The first is access to go to one. 
The second is the thresh argument. We set this to 10. This time only the minor column is removed because it had less than 50% non-missing values. 
Instead of dropping rows or columns with missing data, we could also decide to replace the missing values with something else. The fillna method of a Pandas data 
frame allows us to do this. For example, there are three missing values in the gender column of the students data frame. To replace the missing values in the column with 
female, we do the following. Within our fillna method, we specify a dictionary, the dictionary key, it will be the column we want, which is gender, and the value for the key, 
for the dictionary, is female, the value we want to replace. So when we run this now we now have all the missing gender values replaced with female. 
Instead of using a literal value to replace missing data, we could also use a function. For example, to replace the missing values in the age column, 
with a median of the non missing values, we do the following. Within the fillna method, we specify a dictionary once more. The key is age and that the value is students 
age median. This means replace the missing age values with a median age value for the non missing rows. The fillna method allows us to replace all missing values 
within the column, all within the row. However, if our objective is to replace missing values on a cell by cell basis, we use a different approach. 
For example, let's say we want to replace the missing zip code for Granger Indiana with 46530. This is row index six. The first thing we do is select the cell or 
cells that we want by creating a mask that describes the data. Let us create the mask. We call it mask, and our masks are going to have two parts to it. 
The first is the logic for the city. So we say students specify the column. City is equal to Granger. The second part students column is state. This is equal to Indiana.
Next, we apply the mask as a row filter using the dot loc operator. So we say students dot loc in this index by mask, specify every column, this returns 
all rows for row index six, which is what we wanted. Note that in the syntax of the loc operator, mask specifies the rows we want and the colon specifies 
that we want all columns. Using the loc operator, we can update the value of the zip column alone, as follows. Students dot loc, our mask, this time we want just a zip 
column and we give a value to it, which is 46530. I'll output a beta, so we can see what we got. There we have it. We see that row six now has a zip code of 46530. 
Now that we've resolved the zip code for Granger, Indiana, we can also do the same for Niles, Michigan, which is row index 14. The current zip code is 49120. 
Let's resolve it as well.

Normalizing your data
An ideal dataset is one that has no missing values and has no values that deviate from the expected. Such a dataset hardly exists, if at all. In reality, 
most data sets have to be transformed or have data quality issues that need to be dealt with prior to being used for machine learning. This is what the third stage in 
the machine learning process is all about, data preparation. Data preparation is a process of making sure that our data is suitable for the machine learning approach 
that we choose to use. Specifically data preparation involves modifying or transforming the structure of our data in order to make it easier to work with. 
One of the most common ways to transform this structure of data is known as normalization or standardization. The goal of normalization is to ensure that the values of a 
feature share a particular property, this often involves scaling the data to fall within a small or specified range. Normalization is required by certain machine 
learning algorithms, it reduces the complexity of our models and can make our results easier to interpret. There are several ways to normalize data. 
The first is known as z-score normalization. Z-score normalization, which is also known as zero mean normalization, gets its name from the fact that the 
approach results in normalized values to have a mean of zero and a standard deviation of one. Given an original value V of feature F the normalized value 
for the feature V' is computed as V minus the feature mean denoted as F bar, divided by the standard deviation of the feature, Sigma F. 
To illustrate how z-score normalization works, let's consider the feature with five values shown here. The mean of these values is 40,800, and if the deviation is 33,544. 
To normalize the fourth value we subtract 40,800 from 40,000 and divide the result by 33,544. This yields negative 0.024, using the same approach for the other values 
of the feature, the normalized values will now be -0.859, - 0.5, - 0.322, - 0.024 and 1.705. Note that the mean of the normalized values is zero and the standard 
deviation is one. In most instances, z-score normalization works well. However, some problems and certain machine learning algorithms require that our data have a 
lower and upper bound such as zero and one. For that we need min-max normalization. With min-max normalization, we transform the original data to a new scale defined by 
user defined lower and upper bounds. Most often the new boundary and values are zero and one, mathematically this transformation is represented as shown here where V' is a 
normalized value, V is original value, minF is the minimum value for the feature, maxF is the maximum value for the feature, upperF is a user defined upper bound and lowerF 
is user defined lower bound. To illustrate how min-max normalization works let's consider the same set of five values. Assuming that we set the upper bound to one and 
the lower bound to zero, to normalize the third value, 30,000, we apply the min-max normalization formula, which yields 0.209. Using the same approach for the remaining 
four values, the min-max normalized values for the feature will now be 0, 0.14, 0.209, 0.326 and 1. Z-score and min-max normalization are usually suitable when there are 
no significant outliers in our data. If there are outliers in our data, a more suitable approach is log transformation. With log transformation we replaced the values 
of the original data with its logarithm as shown here, where V is original value for the feature and V' is a normalized value. The logarithm used for log transform can 
be the natural logarithm log base 10 or log base two. This is generally not critical, however, it is important to note that log transformation works only for values that 
are positive. A plan log transformation to the fifth value in our example data, we get 4.991, applied to the rest of the values we now have 4.079, 4.380, 4.477, 4.602 and 
4.991. Notice that this approach minimize the distance between the original outlier values, 12,000 and 98,000 and the rest of the data.

How to normalize data in Python
- Part of the objective of data preparation, is to transform our data in order to make it more suitable for machine learning. 
During this step, we often have to restructure some of our data, so right. It conforms to a particular characteristic. This is known as normalization. 
There are several ways to normalize data in Python, to illustrate how to normalize data let's import and preview a sample vehicles emissions data set into a data 
frame called vehicles. Our goal is to normalize the CO2 emissions column. So let's get descriptive statistics for that column, vehicles specify the column that we want, 
which is CO2 emissions. And we call it that describe method to augment our understanding of the summary statistics. Let's also create a histogram that shows the distribution 
of values for the CO2 emissions column, the histogram visualizes, what we already see in the summary statistics, the carbon emissions values in the dataset have minimum, 
and maximum values of 29 and 1269.57 respectively. They also have mean and median values of 476.55 and 467.74 Respectively. 
This scikit-learn package provides several functions for transforming data in Python for min-max normalization. We first import the min-max scaler object from, 
the SK learn pre-processing sub package, to from SK learn, dot pre-processing, we import the min max scaler object. Next, we use the fit transform method of, 
the object to normalize our data. So we're going to call on new data CO2 emissions on the score MM. And it's going to be the min-max scaler object, 
the fit on the squad transform method within the method. We passed away, the data we want to transform, which is vehicles, and we want the CO2 emissions column. 
And then we output our results. Notice that our result is a nonPareil. We can convert it back to a data frame by using the pandas, data frame, construct a function. 
So let us right back CO2 emissions, the MM and a call the PD that data frame, construct a function. Then the function we're going to pass to it. Two things, our original data,
CO2 emissions, M M, and the value for the columns arguments, which this time around will be just a list of the column name that we want, which is CO2 emissions. 
And we output our data. Once more. Now we can get summary statistics for our normalized data frame, so to do so we call the data frame CO2 emissions, on the score, MM. 
And we call the describe method of the data frame. We can also visualize it, which is what we have here based on the summary statistics and the visualization. 
We see that the minimum value is now zero, while the maximum value is one. That is what we expect for min-max normalization. However, notice that compared to the original 
data, even though the scale of the X axis changed, the basic structure or shape of the histogram, remains the same, that is also expected for z-score normalization, 
We import the standard scaler object from the SK learn pre-processing sub package. So from SK learn that pre processing, we import standard scaler. Next, we normalize our 
data, convert it to a data frame and compute summary statistics like we did. In the previous example, finally, we visualize the data as well. As expected, 
the basic structure of the histogram remained intact. Even with the change to the scale of the X axis. This time, we also notice that our minimum and maximum values, 
are negative 3.8 and 6.7 respectively. Also note that the standard deviation is one, and the mean is effectively zero.

Sampling your data
As we prepare our data for machine learning, we sometimes have to reduce the number of rows in our data or split the data into two or more partitions. 
We do this because the data we have is too large or too complex to use in it's current form, or because we need to hold on to some of our data for later use. 
In Supervised Machine Learning, our goal is to create a model that maps a given input, which we call independent variables, to the given output, which we call the 
dependent variable. In order to properly evaluate whether our model is learning, we have to get an unbiased estimation of its performance using data that it has not 
previously seen. To do this, we must first split our previously labeled historical data into training and test datasets. We hold out the test data and use the training 
data to build or train our model. Then we evaluate our models performance using the test data. There are several ways to split data for this purpose. The most common 
approach is known as sampling. Sampling is a process of selecting a subset of the instances in a dataset as a proxy for the whole. In statistical terms, the original 
data set is known as the population, while the subset is known as a sample. Sampling comes in several flavors. To illustrate some of them, let's use a fictional population 
of 20 students. 12 women, and eight men. From this population, we intend to create a sample of five students. The first sampling approach we illustrate is random sampling 
without replacement. In this approach, we begin by randomly selecting a student from the population. For example, we select student number 11. Then we select student nine. 
Notice that as we select students from the population, they are no longer part of the pool of students from which we can select. Next, we select student 15, student 19, 
and finally student three. This is random sampling without replacement. The next type of sampling is known as random sampling with replacement. In this approach, 
we also randomly select students from the population. However, there is one key difference. Before I tell you what it is, let's see if you notice on your own. 
Let's begin by randomly selecting the first four students. The first student we select is student 11, then student nine, student five, and then student 19. Have you noticed a 
difference yet? I'm sure you have. As we select students from the population, they remain part of the pool of students from which we can select in subsequent trials. 
This is the replacement part of random sampling with replacement. As you can imagine, this means that we could potentially select the same student more than once for our 
sample. This is exactly what happens here. Student nine is selected twice for the sample. This may seem like an odd way to sample data, but it actually is a very important 
technique in machine learning known as bootstrapping. Bootstrapping is often used to evaluate and estimate the feature performance of a supervised machine learning model 
when we have very little data. The next sampling approach is known as stratified random sampling. Stratified random sampling is a modification of the simple random 
sampling approach and ensures that the distribution of values for a particular feature within the sample matches the distribution of values for the same feature in the 
overall population. To do this, the instances in the original data, the population, are first divided into homogenous subgroups known as strata. In our example, 
let's assume that we intend to stratify based on gender. This means that we first need to group our population by gender, recall that our goal is to create a sample of 
five students out of the 20 students in our population. In other words, our sample should be a fourth of the students in the population. This also means that our 
sample should be a fourth of the students from each stratum or group. Since we have 12 women in the population, we randomly select three women for our sample. 
And since we have eight men in the population, we randomly select two men for our sample. Notice that the sample has the same three to two gender distribution of women 
to men as the overall population. That is the benefit of this sampling approach.

How to sample data in Python
- Prior to training the supervised machine learning model, we usually have to split the roles in our data into training and test sets using one of several sampling approaches. 
To illustrate how to split data using sampling, let's import and preview a dataset of vehicles evaluated by the EPA between the years 1984 and 2018. Before we split our data, 
you must first separate the dependent variable from the independent variables. If we assume that the CO2 emissions column is a dependent variable, then we can create a data 
frame called Y based on that column alone. To do this, we create a string variable called response for the name of the dependent variable column, CO2 emissions. Next, 
we create our data frame by sub-setting based on this variable. And we preview our data frame. To create a data frame of the independent variables, 
we first create a list called predictors of all the columns in the vehicles data frame. So we need our list called predictors, using the list command. Now the vehicles, 
not columns. That gives us a list of all the columns in the vehicles data set. Next, we remove the CO2 emissions column from the list. Let's remove, you're going to 
recall the remove method, pass to it, the column name, and let's see what we have. That gives us all the columns except the CO2 emissions column. Using predictors,
we can now create a data frame called X based on the remaining columns in the list, the independent variables. So we call it X, let's go to vehicles. We can preview 
our X data frame. Perfect. The first approach we use to split our data is simple, random sampling. The train test split function from the SK learn model selection sub 
package allows us to do this. Let's import it. Next, we pass our independent variables, X and dependent variable Y to the function which we transfer datasets. We call data 
sets X underscore train, X underscore tests, Y underscore train, and Y underscore test and the train test split function. We pass to it X and Y. The X train data frame 
holds the independent variables of the training set. It has 27,734 rows and 11 columns. The Y train data frame holds the dependent variables of the training set. 
It also has 27,734 rows but one column. The X test data frame holds the independent variables of the test set. It has 9,245 rows and 11 columns. Finally, 
the Y test data frame holds the dependent variables of the test set. It also has 9,245 rows, but one column. The original data has 36,979 rows. This means that the 9,245 
rows in the two test sets represent 25% of the original data. By default, the train test split function allocates 25% of the original data to the test set. 
If we want to override this behavior, we can do so by setting either the train size argument or the test size argument of the function. For example, we can allocate 
40% of the original data to the test set as follows: within our train test split function We specify an additional argument called tests underscore size, and we set 
it to 0.4. We see that 14,792 rows are now assigned to the test set. That is 40% of the 36,979 rows from the original dataset. The second approach we use to split 
our data is stratified random sampling. With this approach, our objective is to maintain the same distribution of values for a specific column between the original 
training and test data. To contrast the two sampling approaches, let's split our data once again, using simple random sampling. This time, we want 1% of the original 
data allocated to the test set. Notice that in our code, we also said the random state argument. This helps ensure that the result in this tutorial are reproducible 
by you and me at a later time. If our objective for using stratified random sampling is to maintain the same distribution of values for the drive column, between 
the original training and test sets, then let's get the distribution for the drive column in the original data. So that's X, specify the column we want, which is drive, 
and we get the value counts. Within the value counts method we specify normalize is equal to true, and that gives us the distribution of values for the drive column. 
We do the same for the test set, which was created based on simple random sampling. Use X underscore test, specify the column we want, which is drive, the value counts 
method within the method we're supposed to specify that normalize is equal to true. Let me get our distribution of values. Looking at the two distributions, we notice that 
there is a small but noticeable difference in the values. Now, let's split the data using stratified random sampling. Stratifying by drive. To do so, we specify an 
additional argument stratify, and we specify the column we want to stratify by, which happens to be drive, and we can run our code. Once again, we can get the distribution 
for the drive column within the test data. Looking at these two distributions, X test and the original X drive distribution, we can see the distribution of values for 
the drive column in the test set created by stratified random sampling, more closely mimics the original data above.

Reducing the dimensionality of your data
As we prepare our data for machine learning, we sometimes have to reduce the size or complexity of our data. There are several ways to do this. 
One approach is sampling, which helps us reduce the number of rows in our data. Another approach is dimensionality reduction. As the name suggests, 
dimensionality reduction is simply the reduction in the number of features or dimensions in a dataset. Dimensionality reduction is an important step in the
machine learning process because it helps reduce the time and storage required to process data. It improves data visualization and model interpretability. 
It also helps avoid the curse of dimensionality. The curse of dimensionality is a phenomenon in machine learning that describes the eventual reduction in the 
performance of a model as a dimensionality of the training data increases. Specifically, as we increase the number of features that we use to build a model, 
we eventually also have to increase the number of instances in the training data. If we don't do this, the performance of our model will eventually degrade. 
The reality is that we are not always able to sufficiently increase the number of instances in any given data set. As a result, we should sometimes focus our attention 
on reducing the dimensionality of our data in order to mitigate the impact of the curse of dimensionality. In other words, we need to identify the optimal number of 
features to use. There are two common approaches to dimensionality reduction. They are feature selection and feature extraction. The idea behind feature selection is to 
identify the minimal set of features that result in the model performance reasonably close to that obtained by a model trained in all the features. The assumption with 
feature selection is that some of the features or independent variables are either redundant or irrelevant and can be removed without having much of an impact on the 
performance of the model. This is why feature selection is sometimes referred to as variable subset selection. To illustrate how this works, let's assume that our 
goal is to build a supervised machine learning model that uses the six independent variables of loan amount, loan grade, loan purpose, income, age, and credit 
score to predict loan outcomes. With feature selection, we identify a subset of the features that result in the model that performs almost as well or possibly better 
than one built with all six original features. With feature extraction, our goal is to use mathematical functions to transform a dataset with high dimensionality 
to one with low dimensionality, or like feature selection, where the final set of features is a subset of the original set of features. The feature extraction 
process results in a final set of features that are completely different from the original set. The new features are simply a projection of the original ones. 
This is why feature extraction is also known as feature projection. To illustrate how feature extraction works, let's also assume that our goal is to build a 
supervised machine learning model that uses the independent variable shown here to predict loan outcomes, which is the default dependent variable. With feature extraction, 
we apply a mathematical transformation that creates these three new features from the original ones. Feature extraction is a very efficient approach to dimensionality reduction. 
However, it does present one notable disadvantage. As you can see in this example, the values for the newly created features are not easy to interpret and may 
not make much sense to a user.

