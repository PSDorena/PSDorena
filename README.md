This README is an overivew and technical guide to our NLP project for Codeup.

For this project, we will be scraping data from GitHub repository README files. The goal will be to build a model that can predict what programming language a repository is, given the text of the README file. We decided to use repositories that were connected to the examination of the Titanic DB set.

ACQUIRE:

So, mid-way through the scraping process, we were provided the necessary code to access Github's API. This set of code was is introduced in the acquire_titanic.py file. Our code generates approximately 180 entries into a .json file. There are several important steps that the user will need to input:

    An env.py file is necessary to run the code in the acquire file. The env file should include:

    A github token. This token can be made by going onto Github and requesting a token. For further instructions, google "Getting Github token"

    A variable called github username, where the variable is set to your Github username as a string.


PREP:

All prep work was done through the functions that are included in the prep.py file located in the repository. Each step of the cleaning process was captured in a dataframe that is produced in the jupyter notebook. It is important to note that an extra list of stop words that can be modulated as necessary for further exploration into building a better model for the data. 

EXPLORATION:

The first step of the exploration process was to eliminate any instances of an entry that did not contain a README. This dropped the total number of entries from 180 to ~ 170. Intial exploration revealed the first error of using repositories that were centered around a learner's dataset. There was a marked skew in the langauges used in favor of Jupyter Notebook and Python. 70 percent of the data entries were comprised of the two languages. Given that a Jupyter Notebook is often use for python coding, it is reasonable to assume that the skew towards python is higher than what the data reveal. Additionally, any language that had one entry had to be eliminated due to the fact that it could not be split in a train/test split. Analyzed text for the first modeling was drawn from the 'clean' column in the dataframe. 

Organizing the text data led to the conclusion that there were are number of stop words that needed to be added to the personalized stopword list. Most of the words associated with the titanic dataset, including the word 'titanic', were excluded to create greater distinction between programming languages. The analyzation of bigrams also provided insight into the removal of certain stopwords, like 'machine' and 'learning'. 

Modeling:

We utilized several different classification models to find the best fit for our data. The first model was a standard logistic regression model. The model returned an accuracy of 56% on the training data, but under performed on the test data, returning just 48%. With a baseline of around 50%, this meant that the initial model did not perform better than the baseline. The next model was a simplified decision tree model that returned a 51% accuracy score on the test data, which improved (albeit slightly) from the baseline model. The decision tree also yielded the smallest change in accuracy from training to test data. Both Random Forest and KNN yielded promising returns o the training data but wilted when exposed to the test data.

Important Notes for the modeling data:

All defaults are used except where noted. All random states are 123.

 Decision Tree had a max depth of 2 and and random state of 123.

KNN uses a K of 5. 


