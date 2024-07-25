Traditional programming:
- input + instruction;
- computer generate output;

What is machine learning
- give computer input and the output we want;
- the computer figures out the instructions best;

What is machine learning?
Whether we realize it or not, machine learning is all around us. From antilock braking systems, to autopilot systems in airplanes and cars, smart speakers, 
which serve as personal digital assistants, to systems that learn our movie preferences and recommend what to watch next. 
Machine learning has become ubiquitous in our lives. So what is machine learning? As you can probably tell, the term machine learning is an old one. 
It's been a while since people referred to computers as machines. To understand what machine learning is, let's discuss how it came to be. Computers, machines, 
are very good at performing repetitive tasks quickly and precisely. If we think of a computer as an assistant, which helps us accomplish rigorous and sometimes mundane tasks, 
then the traditional way of interacting with a computer is to provide it with two things. The first is some sort of data or task as input. 
The second is a set of instructions on what to do with the data or instructions on how to accomplish the task. 
The computer then follows the instructions and provides us with output or the result of the task. This is a traditional way to program a computer. 
Data and instructions as input, and we get output from the computer. In 1959, computer pioneer Arthur Samuel thought of a different approach. He wondered if computers 
could infer logic instead of being given explicit instructions. In other words, he wondered if machines could learn. This type of thinking was drastically 
different from how most computer scientists at the time thought of computers. Specifically, Arthur Samuel wondered, what if we gave a computer just input data, 
and the output or the end result of previously accomplished tasks? Could a computer figure out the best set of instructions that would yield the given output based 
on the data that was provided to it? To illustrate this idea, let's say we gave a computer the numbers on the left as input data, as well as numbers on the right as 
expected outputs. Based on Arthur Samuel's idea, could a computer figure out what mathematical operation to apply to the input to yield the output? As we give the computer 
more input and output examples, if the computer is able to gradually figure out that a simple linear combination of the input values is a close approximation of the output 
values, then we say that the computer, or machine, is learning. After we train a model, which is a model that has learned the right set of instructions for a given task, 
going forward, we simply give it input data, and to apply its internal instructions to provide us with output. What we just discussed is a type of machine learning 
known as supervised learning. Supervised learning is useful in solving problems, such as image recognition, text prediction, and spam filtering. 
A different type of machine learning is unsupervised learning. With unsupervised learning, we simply ask the machine to evaluate the input data and identify any 
hidden patterns or relationships that exist in the data. Unsupervised learning is used in movie recommendation systems, and to perform customer segmentation 
for marketing purposes. The third type of machine learning is known as reinforcement learning. In this approach, there are two primary entities, the agent and the environment. 
The agent figures out the best way to accomplish a task through a series of cycles in which the agent takes an action and receives immediate positive or negative feedback 
on the action from the environment. After a number of cycles, the agent eventually learns the optimal sequence of actions to take in order to accomplish the task at hand. 
Reinforcement learning is commonly used in computer game engines, robotics, and self-driving cars.


_____________                       _______
| 4 | 5 | 6 |                       | 16   |
| 3 | 1 | 8 |                       | 12   |
| 2 | 2 | 6 |     ->  computer <-   | 9    |
| 6 | 9 | 3 |                       | 18.5 |
_____________                       ________

Quanto maias dados de input e output forem dados mais a máquina tende a aprender.
Aqui estamos a criar um modelo e depois podemos usar esse modelo.

Isto é um tipo de machine learning -> Supervised Learning.
Usado para resolver problemas como reconhecimento de imagens, previsão de texto, e filtro Spam.

Unsupervised Learning
Passados os dados de input e a máquina tem de identificar padrões escondidos ou relações existentes nos dados de input.
Usado em recomendações de filmes, seguentação de clientes para propósitos de marking.

Reinforcement Learning
Aqui existe duas entidades primárias:
 - Agente: Tenta perceber a melhor maneira de completar uma tarefa através de uma séria de ciclos em que o agente inicia uma tarefa 
 sobre o ambiente e recebe a resposta do mesmo que pode ser positiva ou negativa.
 Após uma série de ciclos o agente aprende a melhor maneira de completar a tarefa que lhe foi atribuida.
 - Ambiente: local onde o agente tentar perceber qual a melhor maneira de compeltar a tarefa.

 Usado em jogos de computador, robótica e condução autónoma.

 O que que não é Machine Learning:
relação entre estatistica e ME. Apesar de a ME usar os fundamentos das estatisticas, vai muito alem delas.

O fundamento da ME é prever situações futuras basedo em eventos do passado. (What next?)
Modelos estatisticos são mais direcionados para para a relação, inferencia entre variaveis(what happens um var b is var a change). (What if?)

o que une estes dois conceitos é normalmente conhecido como Statistical Learning.


ME, Data mining and Optimization:
- são termos que estão de alguma maneira relacionados.

What is not machine learning?
The field of machine learning and artificial intelligence is rife with specialized terms like unsupervised learning, 
statistical learning, data mining, optimization, large language models, deep learning, statistics, supervised learning, 
reinforcement learning, data science, and generative AI, just to name a few. What do these terms really mean? Are they the same thing? 
If not, how do they relate to each other? Let's start by exploring the relationship between statistics and machine learning. 
Some might characterize machine learning as an elevated form of statistics, but it's essential to understand that while machine learning does draw extensively 
from statistical concepts, its foundation extends beyond statistics to encompass principles from information theory, calculus, algebra, engineering, and even biology. 
Referring to machine learning as glorified statistics is akin to referring to physics as glorified mathematics or architecture as glorified reclaim. 
It's crucial to emphasize that the goals and objectives of machine learning often differ from those of basic statistical modeling. 
Machine learning is mostly concerned with results in the form of predictions. In other words, the primary focus of machine learning is to predict future outcomes 
based on past events. Statistical models, on the other hand, are mostly concerned with the relationship between variables. This is known as inference. 
The statistical model, we want to understand what happens to variable B as a result of a change in variable A. The overlap between the approaches used in machine 
learning and those used in statistical modeling are sometimes broadly referred to as statistical learning. Next, let's take a look at the terms machine learning, 
data mining, and optimization. These terms refer to approaches that are closely related. They represent the different branches in the broad field of data science. 
Much like the distinction between machine learning and statistics, the contrast between machine learning and data mining revolves around their ultimate objectives. 
While machine learning prioritizes prediction by utilizing known data properties, data mining emphasizes on covering previously unknown patterns in data. 
In the field of business analytics, the traditional understanding of machine learning is often referred to as predictive analytics, data mining as descriptive analytics, 
and optimization as prescriptive analytics. We use descriptive analytics to identify patterns in historical data, predictive analytics to predict future outcomes, 
and prescriptive analytics to get a recommendation of the best course of action to take. Next, let's take a look at some of the remaining terms. 
Deep learning is one of many machine learning approaches that fall under the umbrella of what is known as supervised machine learning. Supervised learning, 
along with reinforcement learning and unsupervised learning, make up the three major branches of machine learning. 
Though often used interchangeably, machine learning is not the same thing as artificial intelligence or AI. 
Machine learning is a subfield in artificial intelligence. In other words, all machine learning is AI, but not all AI is machine learning. 
Artificial intelligence is a large field in computer science that deals with the simulation of intelligent behavior in computers. 
This includes behaviors such as visual perception, speech recognition, decision-making, and translation between languages. 
Artificial intelligence models can be categorized in several different ways. One approach is to classify them based on the type of function they perform. 
With this lens, AI models can be classified as either discriminative or generative. That is discriminative AI and generative AI. 
To illustrate the difference between these two approaches, let's compare them in the context of text analytics or natural language processing. 
Discriminative AI models are models that focus on categorizing input data or on predicting a future outcome based on historical data. 
When provided with the text of customer reviews of a local restaurant, a discriminative model can correctly label each review as either satisfied, unsatisfied, or neutral. 
It is able to determine the probability that a particular review belongs to a certain category given the input text. 
The machine learning approaches introduced in this course all fall under the discriminative AI umbrella. Generative models, on the other hand, 
are models that are designed to create new content based on user input. We can use a generative AI model to generate innovative texts, complete sentences,
 and even craft entirely fresh pieces of writing. One of the prominent generative AI methodologies gaining significant attention today are large language models, 
 also known as LLMs. LLMs are generative AI models that are really good at understanding and generating human-like text based on the input or prompts they receive. 
 For a detailed explanation of generative AI and large language models, check out my LinkedIn Learning course titled, "Generative AI: Introduction to Large Language Models."


What is supervised learning?
Supervised machine learning is a process of training a predictive model. Predictive models are machine learning models that enable us to assign a label to unlabeled data 
based on patterns learned from previously labeled historical data. If we want to predict the outcome of a new event, we can use a predictive model that has been trained on 
similar or related events to predict the outcome. To illustrate how supervised learning works, let's assume that we work in the analytics department of a local credit union. 
Our task is to develop a machine learning model that predicts loan risk. Specifically, we would like to build a model that predicts whether a particular customer will or will 
not default on a loan. Let's also assume that we already have two kinds of information about the loans our bank has previously issued. The first is 
descriptive data about each loan, such as the loan amount, the grade of the loan, the annual salary of the borrower, the purpose for the loan and so forth. 
The second type of information we have is the outcome of each previously issued loan. The outcome data is a label that tells us whether the borrower paid back the 
loan in full or whether the borrower defaulted on the loan. Before we can use a supervised machine learning model to predict the outcome of a new loan, 
we first have to train the model using historical loan data. In machine learning, we call the input the independent variables and we call the output the dependent variable. 
The independent variables and dependent variable make up what is known as a training data. If our training data consists of 10 previously issued loans by our credit union, 
then the independent variables are the loan amount, the grade of the loan and the stated purpose for the loan, while the dependent variable is outcome variable, default. 
The default variable has two levels or values. They are yes, which means the borrower failed to pay back the loan in full, and no, which means that the borrower paid the loan 
back in full. To train a model, we provide it with three independent variables and we provide it with the dependent variable or outcome as well. With these two sets of values, 
the machine learns the patterns in the data and builds a set of instructions that connect the input to the output. This set of instructions represent the trained model. 
After a model has been trained, we can evaluate how well its instructions explain the relationship between the independent variables and the dependent variable. 
One way to do this is to provide the trained model with just the input in order to see what output values it will predict. By comparing the predicted outcomes 
with the actual outcomes, we can score the performance of the model based on how many of them match. We call this the predictive accuracy of the model. 
The higher the score, the better the model is. And the lower the score, the worse the model is. One of the most popular definitions of supervised machine learning is 
that provided by Tom Mitchell. According to Mitchell, "A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, 
if its performance tasks in T, as measured by P, improves with experience E." This definition presents three components to machine learning: experience E, class of tasks T, 
and performance measure P. In our loan outcomes example, the experience is a historical loan data that we use to train the model. The task is to predict who will or will not 
default. And the performance measure is predictive accuracy, which is measured by how well the predicted and actual outcomes match. We can reword the supervised machine 
learning definition as a loan prediction model is said to learn if its ability to predict which borrowers would default on the loan T, as measured by predictive accuracy P, 
improves as it encounters more training data E.


What is reinforcement learning?
Reinforcement learning is a science of learning to make decisions from interaction or the process of learning through feedback. 
It has many applications like autonomous driving, robotics trading and gaming. Reinforcement learning is very similar to early childhood learning. 
A toddler sees something, does something, gets positive or negative feedback, then adjusts his or her future behavior accordingly. Reinforcement learning along with 
unsupervised and supervised learning form the three major branches of machine learning. Unlike unsupervised learning where the objective is to identify unknown patterns 
in unlabeled data and supervise learning where the objective is to learn patterns in previously labeled data, reinforcement learning attempts to tackle two distinct objectives. 
The first is finding previously unknown solutions to existing problems. An example of this learning objective is a machine that plays chess better than any human ever.
The second objective of reinforcement learning is finding solutions to problems that arise due to unforeseen circumstances. An example of this learning objective
is a machine that is able to find an alternative route through a terrain, after a mudslide has altered the expected route. Reinforcement learning involves true primary 
entities that repeatedly interact with each other. One of them is the agent and the other is environment. The agent interacts with the environment by taking actions. 
The environment responds to the actions of the agent by providing feedback or observations to the agent. The feedback provided by the environment comes in two forms, 
state and reward. The state describes the impact of the agent's previous actions on the environment and the possible actions the agent can take. Each action is 
associated with a numeric reward, which the agent receives as a result of taking a particular action. The agent's primary objective is to maximize the sum of rewards it 
receives over the longterm. To illustrate how reinforcement learning works. Let's consider the familiar game of tic tac toe. In the game, two players take turns playing on a 
three by three board. One player plays Xs on the other Os, until one player wins by placing three marks in the row. Diagonally, vertically or horizontally as shown here. 
Let's assume that each of the positions on the board is represented by the labels shown here A1, A2, all the way to C3. Let's also assume that the first player is not the 
agent and plays Os while the agent is a second player and plays Xs. The first move of the game could look something like this. The table to the right is known as a 
policy table. It represents states and rewards. Columns A1 to C3 are the positions on the board. While column D is a reward associated with each state. 
Each row represents an available state or action that agent can make, given that the first player has played O in position A3. one stands for player one and two 
stands for player two. Notice that column A3 is taken and is therefore grayed out and pre-filled with one. This means that the agent can play any position on the board 
except A3, given the available actions and rewards, the agents must evaluate each possible action and choose the one that yields the highest reward. This is known as 
exploitation. Since all of the actions currently have the same reward, the agent randomly decides to play B2, in the second move, if the first player plays B3, 
then the state table via shown here. Once again, the agent was choose the action that yields the highest reward. Since all of these actions have a reward of 0.5, 
the agent randomly settles on a play of C3. The process repeats a third time for player one and for player two. At the end of each player's third move, 
the environment determines that player one has won the game. This is known as a terminal state. The coin cycle of learning has ended. At the end of the learning cycle, 
because the action taken by the agent in the third move resulted in the victory, the reward associated with that action is updated by the environment from 0.5 to one in the 
policy table. This is known as a backup, using the mathematical equation, the reward associated with the agent's second move is also backed up in the policy table, 
as well as a reward associated with the agent's first move. As a result of the higher rewards associated with the sequence of actions the agent took in the first 
learning cycle, during subsequent learning cycles, if the agent encounters a state similar to the one that it encountered in the first cycle, it will choose to take the 
same action that it did in the first cycle, in order to maximize reward. This brings up an important challenge with reinforcement learning. The challenge is known as the 
exploration versus exploitation trade-off. If left unchecked, an agent will always prefer to take actions that he has tried in the past and found to be effective in 
maximizing reward. As previously mentioned, this is known as exploitation. However, in order to discover a new sequence of actions with potentially higher reward, 
the agent was try actions that it has not selected before, or that do not initially appear to maximize reward. In other words, the agent sometimes has to choose actions 
with little to no consideration for their associated reward, this is known as exploration. An agent that focuses only on exploitation will only be able to solve problems it 
has previously encountered. An agent that focuses only on exploration will not learn from prior experience. A balanced approach is needed for effective reinforcement learning.


What are the steps to machine learning?
There are six major steps in the machine learning process. The first is data collection. During the data collection step, our objective is to identify and gather 
the data we need for machine learning. For unsupervised learning, this is the unlabeled data with unknown patterns that we intend to discover. 
For supervised learning, this is the labeled historical data that we intend to use to train and evaluate our model. For reinforcement learning, this is the data that 
helps our agent learn which actions yield the most reward. If we liken the machine learning process to the process of making a delicious bowl of salad, then the data 
collection step is like gathering all the ingredients that would go into a salad into a single basket. The second step in the machine learning process is data exploration. 
Data exploration is a process of describing, visualizing, and analyzing data in order to better understand it. With data exploration, we can answer questions such as, 
how many rows and columns are in the data? What type of values are stored in the columns of the data? Are there missing, inconsistent, or duplicate values in the data? 
And are there outliers in the data? Just as we did for the previous step, if we liken the machine learning process to the process of making a bowl of salad, then the data 
exploration step is like inspecting every ingredient to make sure that it is fresh, ripe, and/or exactly what we want. The next step in the machine learning process 
is data preparation. Data preparation is the process of making sure that our data is suitable for the machine learning approach that we intend to use. 
It involves resolving data quality issues, such as missing data, noisy data, outlier data, and class imbalance. Data preparation also involves modifying or transforming 
the structure of our data in order to make it easier to work with. This includes normalizing the data, reducing the number of rows and columns in the data. 
Going back to our salad analogy, the data preparation step is when we begin to cut the vegetables we plan to use in our salad. Depending on the type of salad we want, 
we may decide to cube the vegetables, slice the vegetables, or shred the vegetables. If we plan on adding chicken to the salad, this is also the stage when we either grill, 
bake, or saute the chicken. Successful data science relies on good data. The data doesn't have to be perfect, but it should be good. The saying garbage in, 
garbage out is especially important when it comes to machine learning. Because of how important good data is, it is not unusual to spend up to 80% of our time collecting, 
exploring, and preparing data. After the data collection, exploration, and and preparation stages comes the modeling stage. Modeling is the process of choosing and 
applying the right machine learning approach that works well with the data we have and solves a problem at hand. Modeling is the most well-known stage in the machine 
learning process. In order to apply the right type of model, we must be clear about our objective. Knowing what type of machine learning we intend to do and what machine 
learning approach is capable or incapable of will go a long way in helping us be successful in this stage. In the salad analogy, the modeling stage is analogous to mixing the 
ingredients that we previously prepared. Depending on the type of salad we want, we mix more of some ingredients and less than others. We also decide which ingredients 
to include and which to avoid altogether. The fifth stage in the machine learning process is evaluation. As the name suggests, our objective in this stage is to assess 
how well the machine learning approach we chose worked. There are several ways to do this. In supervised learning, where our goal is to predict a label or value, 
we evaluate a model by measuring how well it does in predicting labels for previously unseen data. In unsupervised learning, we usually take a more subjective approach. 
A good unsupervised learning model is one that provides us with results that make sense to us. The evaluation stage is when we taste test our salad. If the salad needs more 
salt or pepper, we add some seasoning. If the salad feels a bit dry, we add some dressing. Depending on how well a model performs, we may need to build it again with slightly 
different data or with different settings. The idea here is to make a change that has a meaningful positive impact on the performance of our model. This is usually an 
iterative process. When we feel confident that the model we have is good or the best we could do given the data we have, we move on to the final stage of the machine 
learning process, actionable insight. This means identifying a potential course of action based on the result of the machine learning model. For supervised learning and 
reinforcement learning, this is the stage where we decide whether or not to deploy our model to production. In unsupervised learning, this is the stage where we decide 
what to do with the patterns identified by our model. As for our salad, this is when we decide whether or not to serve it.


Things to consider when collecting data
Data collection is the first of the six stages or steps in the machine learning process. During the data collection stage, our primary objective is to identify 
and gather the data we intend to use for machine learning. As we collect this data, there are five key considerations to keep in mind. The first is accuracy. 
For supervised machine learning problems, we use historical data that has outcome labels or response values to train the model. Ensuring that this data is accurate 
is critically important to the success of their approach. Supervised learning algorithms use this data as a baseline for the learning process. It serves as a source 
of truth upon which patterns are learned in order to make future predictions. If this data is inaccurate, then the algorithm's future predictions cannot be trusted. 
This is why this data is often referred to as ground truth data. Ground truth data can either come with an existing label based on a prior event, such as whether a 
bank customer defaulted on a loan or not, or it can require that a label be initially assigned to it by domain experts, such as whether an email is spam or not. 
Regardless of whether labels already exist or need to be assigned, we should always have a plan to validate ground truth data after it has been acquired. 
The next key consideration is relevance. The type of data we collect to describe an observation should be relevant in explaining the label or the response 
associated with the observation. For example, collecting data on the shoe size of bank card customers has no relevance in explaining whether a particular borrower will 
or will not default on the loan. Conversely, excluding information about a customer's income could have an adverse impact on the effectiveness of a model that attempts 
to predict loan outcomes. The amount of data needed to successfully train a model depends on the type of machine learning approach chosen. This is a third consideration, 
quantity. Some machine learning algorithms work well with little data while others require a large amount of data to provide meaningful results. Understand the 
characteristics of the machine learning algorithm we intend to use can provide us with guidance on how much data we need to collect. Besides quantity, 
variability in the data collected is also important. For example, if we intend to consider the income of a borrower as a predictor of loan outcome, 
then our ground truth data should include customers of sufficiently different income levels. By doing this, we allow our model to gain a broader understanding of how 
income level impacts loan outcomes. The fifth consideration is one that is often overlooked, ethics. There are several ethical issues to consider during the data 
collection process. They include privacy, security, informed consent, and bias. It is important that processes and mitigating steps be put in place to address these 
issues as part of the process of acquiring ground truth data. If bias exists in the data used to train a model, then the model would also replicate the bias in its predictions. 
As one can imagine, bias predictions could prove quite harmful, especially in situations where unfavorable decisions are being made based on a machine learning model. 
Bias in ground truth data is often non-intentional. It sometimes stems from implicit human bias in the data collection process or from the absence of existing data on 
certain subpopulations. Let's recap. The data we collect for machine learning should be accurate and relevant. We must ensure that we have enough data and that the data 
we capture is different and captures different use cases. Finally, we must be ethical in how we collect, manage, and use data.

How to import data in Python
One of the reasons why Python is such a popular programming language for machine learning is because it supports some very powerful and easy to use packages, 
which are purpose built for data analysis. One of these packages is a pandas package. The pandas package provides several easy to use functions for creating, 
structuring, and importing data. Before we can use any of these functions, we first have to import the pandas package using the import command. 
Here, the import command imports the pandas package, and we use an alias for the package. We call it pd. This allows us to refer to the functions of the package by 
simply referring to pd dot a function name. One of the ways the pandas represents data is as a series. A panda series is heterogeneous one dimensional array-like data 
structure with labeled rows. We can create a panda series from a previously created list. Given the members list, we can create a series object as follows. We're going 
to create a series object called bricks1, and we create the series object by calling the pd series, construct a function, and we pass the members list to the series. 
As you can see, the series object is made up of a set of indexes on the left and values on the right. To verify that bricks1 is a panda series, let's pass it to the type 
function to see what we get. Another way that pandas represents data is as a data frame. A pandas data frame is a heterogeneous two dimensional data structure with labeled 
rows and columns. We can think of a pandas data frame as a collection of several panda series, all sharing the same index. A data frame is very similar to a 
preadsheet or a relational database table. We can create a pandas data frame from a previously created dictionary. Given the members dictionary, we can create a 
data frame object as follows. Here, we are going to create bricks2, and bricks2 is created by calling the data frame, construct a function, and we passed with the members 
dictionary. As you can see, pandas converted the dictionary keys to column names, and it used the values for each dictionary key as the cell values in the data frame. 
To verify that bricks2 is a data frame, let's call the type function to see what it returns. There we have it. It is a data frame. We can also create a data frame 
from a previously created two dimensional list of values and a list of column names. Given the members and labels lists, we can create a data frame object as follows. 
This time, we create breaks3, we passed the data frame construct a function, the members list, as well as the labels lists, as the column names. 
Another way to create a pandas data frame, is by importing data directly from an external source. For example, we can create a data frame by importing a CSV file. 
So, let us create another that a frame, bricks4. This time, we use a pd.read_csv function, and we pass through it the file we want it to read. 
There we have it. We can also create a pandas data frame by importing a Microsoft Excel file. This time we're going to call it bricks5, and we will use the 
read_excel function, and we pass to it the name of the file we intend to read. In this example, we read from an Excel file. Note that for multi-sheet Excel files, 
the pandas read Excel function imports the first sheet by default. If we want to import a sheet other than the first one, we have to specify a 
value for the sheet name argument within the read XL function. For example, the bricks Excel file we just imported, has two sheets. The first is 
named members and the second is named summits. When we imported the file, the function imported the first sheet, which is the member sheet. 
To import the second sheet, which is the summits sheet, we make the following modification to our code. There we have it. The summits sheet. 
Besides CSV and Excel files, the pandas package allows us to import other file types, which we do not cover or go over in this tutorial. 
To get an exhaustive list of supported file types, visit the pandas documentation website.



