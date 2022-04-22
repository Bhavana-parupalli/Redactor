## Author: Bhavana Parupalli
## Email: parupallibhavana123@ou.edu
# Changes
## Packages installed
```bash 
from commonregex import commonregex
```
* Small amount of Features Found - Names --- I changed the code in such a way that matcher is going to check for patterns with proper noun followed by comma(,) followed by proper noun and replaces the particular names with u"\u2588". Moreover, the redacted document is converted to nlp doc and again the document is checked for names if present using .ents and if labels of entities is 'PERSON' then it is appended into names_list and finally, the names_list if looped and the names in the document is replaced using u"\u2588". 
* Small amount of Features Found - Gender --- I added some other genders into the g_list. If the genders in the g_list present in the document then those genders are replaced with u"\u2588".
* Missing/No Features Found - Phone Number --- I changed the entire code in the phone_numbers() function. I used commonregex. Firstly, the document is converted to commonregex document and then if any phone numbers appear in the regex document. Each phone number will be looped and if every digit in the phone number lies in between 0-9 then count will be incremented, else if '.' occurs then the loop will break. After looping through all the phone numbers. If count==10 or else 11 because phone numbers consists of 10 digits and some numbers may have +1 at the beginning. Therefore, if the count==10 or 11 those phone numbers will be appended into a phone_list. Furthermore, commonregex will take Fax, voice along with other numbers, in order to avoid this i have implemented if else statement. Finally, the phone_list is looped and replaces the phone numbers present in the document with u"\u2588".
* Small amount of Features Found - Concept --- I tried to change the concept function. But could not find better one than the previous approach.
* Small amount of Features Found - Dates --- I used commonregex to get the dates from the document. Firstly, the document is converted into commonregex document and using '.dates' the dates will be extracted from the document and all the dates are appended into a dates_list. Finally, the dates_list is looped and respective dates in the document are being replaced using u"\u2588".
* Missing Stats --- Earlier i hardcoded the directory name. Now, i changed the code, so that any file name is given the stats output will be stored in that file.
* File names not re-assigned correctly --- I have changed the code so that after redaction each input file will be saved with 'input file name.redacted' extension in the output files folder.
* Output files not stored in respective folder --- I corrected the code so that output files will be correctly saved in the output folder.
* Missing Bugs & Assumptions --- In names function in some cases if surname and firstname are seperated by comma(,) it is not considering it as single name. It is taking surname as one name and the first name as another name. I have mentioned assumptions for all the functions in the readme earlier.
