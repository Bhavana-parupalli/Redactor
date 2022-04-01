# cs5293sp22-project1

# Project Title

A brief description of what this project does and who it's for

## Author: Bhavana Parupalli
## Email: parupallibhavana123@ou.edu
## Packages installed
```bash
pipenv install spacy
import spacy
import glob
import argparse 
import pytest
import re
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
```
## project1
### project1.py
The project1.py file contains 9 different methods reading text from different input files, extracting names, dates, phone numbers, genders, address, sentences and replacing these redacted information with block character and finally writing these modified text into new text files.
#### inputfiles(file)
Firstly, in the readctor.py glob function accepts multiple .txt files and then using extend function all the files are added into a list. Finally, looping the list and passing each file to the inputfiles function. 
The inputfiles fnction will take the file as argument and opens and read the .txt file and return the document.
#### names(document)
The names function receives the document followed by converting that text document to nlp document. As names are considered as proper nouns in POS(parts of speech) i created a pattern as, if one word from the nlp_doc whose POS is PROPN(proper noun) or if two words whose POS is PROPN which are side by side, the matcher function will check the nlp_doc for such patterns if exists then it return the start and end index along with match id. Then looping through this start and end index and if label of this elements is PERSON then the names will be appended into the names_list. Followed by sorting the list in descending order. Finally, looping through the names_list and if the names exists in the document then it will be replaced with the '\u2588' using replace function and then returning the redacted document along with the names_list. Assumptions made in this step are it can only redact first name and first name followed by last name and last name followed by first name.
#### dates(document)
The dates function takes the redacted names document as argument. I have written a regular expression for finding dates which are in the format mm/dd/yyyy if this pattern exists in the document then dates will be appended into the dates_list. Moreover, i have also included a pattern for finding the dates in the format 'day month year'. If pattern appears in such a way, whose POS is NUM followed by POS is PROPN followed by POS is NUM then this dates also will be appended into the dates_list. Finally, looping through the dates_list and replacing the dates in the document with '\u2588' and dates_list. Assumptions made in this step are it will handle only 2 types of date formats for instance (02/13/2020) and (20 jan 2022).
#### phone_numbers(document)
The phone_numbers function takes the redacted names, dates document as argument. Then i have created a pattern using ORTH and SHAPE. The matcher function looks for the given pattern in the nlp_doc and then it is appended into the phone_list.  Finally, looping through the phone_list, and thereby replacing the phone numbers in the document with '\u2588' and return the redacted document and phone_list. Assumptions made in this step are the phone_numbers can only handle (ddd) ddd-dddd and (ddd) ddd dddd formats. For this i have used OP(optional) parameter whhile creating the pattern.
#### gender(document)
The gender function takes the redacted names, dates, and phone_numbers document as argument. Followed by, i created a list which contains multiple genders. Then i looped through the nlp_doc if any of the word in nlp_doc is PRON(pronoun) and if the word exists in the gender list or else if the word is in the gender list then the word will be appended into a new list. Finally, the genders list is looped and replaces the genders present in the document using '\u2588' and return the redacted document and gender_list. Assumptions made in this step are it can only redact the genders present in the list. I have only added few genders based on my input files.
#### address(document)
The address function takes the redacted names, dates, phone_numbers, and genders document as argument. Then i have created a pattern using POS if NUM, PROPN, PROPN, PROPN, PUNCT, PROPN. If any such type of pattern appears in the nlp_doc. Then that address will be appended into the address_list. Additionally, using entity function in all the entities are extracted from the nlp_doc and if the label of the entities is GPE(Location) then those also will be appended into the address_list. Finally, address list is looped and the respective addresses and locations in the document are replacedusing '\u2588' and return the redacted document and address_list. Assumptions made in this step are it can only handle addresses of mentioned pattern type.
#### concept(document, w)
The concept function takes the names, dates, phone_numbers, genders, and address redacted document as arguments along with the word. I created a phrases list which consists of synonyms of the given word. Followed by this phrases list is added into a pattern list, and then phrase_matcher will search for the word in the nlp_doc. If word exist then the entire sentences in the nlp_doc is appended into the sentences_list. Finally, looping through the sentences_list and replacing sentences in the document with '\u2588' and return the redacted document and sentences_list.
#### output(document, filename, path)
The output function takes the names, dates, phone_numbers, genders, address, and sentences redacted document as arguments as well as filename and path. Then it will create a filename.redaced document in the files directory. Finally, opens the .redacted file and writing the document into the file.
#### stats(doc_stats, a, filename, w)
The stats function takes the .txt input document, a represents args.stats, filenames, and word as arguments. The stats function calls all the above functions and append length of list returned by each function into a stats_list. Finally, if args.stats='stdout' the stats_list will be looped and the output will be printed in the console, else a file names stderrfilename will be created in the stderr directory for each input file, opens and writes into the file.
### redactor.py
In redactor.py project1 is imported. Firstly, using args.input the input files are added into a list using extend function and then the list is looped each time it makes function calls to all the functions present in the project1.py.
### redactor.py execution
After connecting to the instance using SSH.

Clone the repository: git clone https://github.com/Bhavana-parupalli/cs5293sp22-project1

Give the following command in command line.
```bash
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'web' \
                    --output 'files/' \
                    --stats stderr
```
## tests
### test_1.py
The test_1.py contains different test cases to test the functions present inside the project1.py. The test_1.py returns the passed and failed test cases.
