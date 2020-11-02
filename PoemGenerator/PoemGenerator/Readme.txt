The code can be runned into a single fashion: as an python program.  We also will explain how we formed the executable from the python program.

The python start file is the PoemGenerator which is within the Code folder and this folder Code needs to be in the same directory as the folder Data_Output, as the inspiring set ( in the form of a json file) is stored. After running the program X( argument 2 ) new poems with Y ( argument 3 ) are generated and can be displayed in a webviewer. This can be done by any webexplorer by opening the file poems.html. This will show the ten newly generated poems. Each of them with their own Title and centered around the middle of the page.

The python program can be runnend within a appropriate python 3.7 enviroment with the following package installed:
- the NLTK module for the different corpusses as input for the inspiring set
- the Regex module for the usage of regular expressions.
- the Json module for the useage of the json-format for the inspiring set and the ease of making this corpus setuo.
- the pronouncing module for a good indication which words in the corpus rhyme with each other in order to create a rhyming poem.
- the numpy package, for standard numpy array's.

Within the python program, the program operates with three variables that can be either given as parameters or given to the program if executed. Being a True or False question if you need to download the corpus ( only needed the first time.) The second parameter will be how many poems should be generated. And the third will be the parameters of how many couplets a poems should contain.