Java Code Completion using N-gram Models


This project implements an N-gram model for Java code completion. It includes scripts for data collection, preprocessing, and model training.



Project Structure

•	results.json: it is the output file from Seart tool  (https://seart-ghs.si.usi.ch) with metadata for all Java projects that match our filters.
•	clone.py: it is a script for cloning the java repositories resulted from the JSON file.
•	parse_split.py: this script for preprocessing Java code and creating the corpus that is split into three files (70% training, 10% validation, and 20% testing). Given that we prepared the corpus and split the methods into three files from a sample of (18 projects) from the whole cloned projects due to the large volume of the cloned projects.
•	n-gram.py: it is an implementation of the N-gram model with Kneser-Ney smoothing and backoff with maximum size (6).


Requirements

•	Python 3.7+

•	Required Python packages: 
   o	nltk
   o	javalang
   o	tqdm
   
Install the required packages using:
           
           pip install nltk javalang tqdm


Setup

Clone this repository: 
                       git clone https://github.com/Mostafa-Noshy/AI4SW.git


Usage

[Important]  To train n-gram model directly on our training corpus and evaluate using validation and test, you need only to clone our repo and then run the n-gram script directly but make sure to install the necessary packages. 

                     python3 n-gram.py




For building the corpus again using our preprocessing, you can follow the following steps:

Step 1: Cloning the java repositories

Run the following script:

                       python3 clone.py

This will clone the selected Java repositories and create a directory for java projects containing the cloned repositories. (Keep in mind that this will clone a large volume of java projects, which we chose later to work on only a sample of them).  


Step 2: Preprocess and Create Corpus

Run the parse_split.py script to preprocess the Java code and create the corpus. Again, we worked on only a sample of the projects (18) to prepare our corpus.

                      python3 parse_split.py

This script will extract methods from the Java files, preprocess and tokenize the code, split the data into training, validation, and test sets, and save the processed data in java_methods_train.txt, java_methods_val.txt, and java_methods_test.txt.



Step 3: Train and Evaluate the N-gram Model

Run the n-gram.py script to train the N-gram model and evaluate its performance:

                       python3 n-gram.py

This script will load the preprocessed data, train the N-gram model with Kneser-Ney smoothing, evaluate the model using perplexity on validation and test sets, and finally generate a sample code completion.




