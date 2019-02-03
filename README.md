# Information-Retrieval-System
Final Project:
Goal: Design and build your information retrieval systems, evaluate and compare their performance levels in terms of retrieval effectiveness

SYNOPSIS:

This readme file has references and detailed information regarding how to setup, compile and run the programs in the assignment.
The progrms are discussed below in brief:
-- Task1: Building our own search engines with Query likelihood, BM25, tf-idf and Lucene model.
-- Task2: Implementing pseudo-relevance feedback for query expansion on one of the above mentioned models.
-- Task3: Using the same base search engine, implementing stopping and stemming seperately on any three baselines of choice.We have selected BM25, Query likelihood, tf-idf.
-- Phase2: Snippet Generation and query term highlighting.
-- Phase3: Evaluation in form of MAP, MRR, P@K for k=5 and 20, Precision and Recall.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INSTALLATION GUIDE:

-- Download python 2.7.x from https://www.python.org/download/releases/2.7/
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add two new variables in 'PATH' -> [Home directory of Python]; [Home directory of Python]\Scripts
-- Open Command Prompt and upgrade pip using the following command: 'python -m pip install -U pip'
-- To check whether you have pip installed properly, just open the command prompt and type 'pip'
-- It should not throw an error, rather details regarding pip will be displayed.
-- Install BeautifulSoup by using the command 'pip install beautifulsoup4'
-- If for some reason the installation fails due to the absence of certain package, just install that package using 'pip install name_of_that_package'
-- Install Colorama by downloading colorama-0.3.7.zip file from https://pypi.python.org/pypi/colorama#downloads
-- Open the unzipped folder and open a command prompt in that location and write the given command - 'C:\Python27\python.exe setup.py install'
-- Install JAVA SE6 or above if not already installed in the system from http://www.oracle.com/technetwork/java/javase/index-137561.html#windows
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add new variable in 'PATH' -> [Home directory of Java]\jdk[version number]\bin;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

GENERAL INSTRUCTIONS:

-- Each search model folder contains a sub-folder 'cacm'. This folder contains the 3204 raw documents provided for this project :-
    -- Navigate through phase 1 task1 to each of the models folder.
	-- Giving the path of that folder, run the python file 'Parser.py' by using the command 'python Parser.py' in  command prompt
	-- The corpus will be generated from the cacm documents present in 'cacm' and be stored in 'corpus' folder document wise. And a processed query file named 'query.txt' will be generated from the raw query file 'cacm.query' in the respective folder itself for each of the models in phase 1.
-- Once the Parser.py has parsed all the raw documents, run 'indexer.py' by using the command 'python indexer.py' in  command prompt.
-- Once the indexer.py has been run, a model respective doc score would be generated inside the 'output_score' folder.
-- Copy and paste these respective score txts inside phase 3 folder to get the desired evaluation results of the score of the search model.
-- Run 'Evaluation.py' by using the command 'Python Evaluation.py' in command prompt.
-- For each score model, Precision_and_Recall txt and P@K=5, P@K=20 txts would be generated.
-- The code for Lucene implementation is provided in 'lucene' folder of Lucene along with all the jars needed for the code to run inside folder 'java_jars'
-- Lucene.jar is the runnable jar of the given code which can work independently from a command prompt and doesn't need any IDE setup or dependency on the jars. One can run this executable jar by running the given command in a command prompt 'java -jar Lucene.jar'

-- For Snippet Generation, kindly follow the previous steps of generating corpus using Parser.py and then generating document score query by executing 'indexer.py' and then run the snippet.py. 'Snippet.py' prints the snippets along with the document names and highlights the query terms with white background and black foreground.
