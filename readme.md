#De-enp-ass
Converts an exported file from enpass to files with comma-separated values (.csv).
This supports logins, secure notes and credit cards and will export one csv file for each type.
It's originally written to prepare files for import to 1password but could be modified to any password manager that can import csv files.

##Usage
You must have python installed on your computer.
Download de-enp-ass.py, open up the terminal, cd to that folder and run:

```python de-enp-ass.py /path/to/exported-from-enpass.txt```

This will generate three files in the same folder as the exported enpass file:

`exported-from-enpass-logins.txt`
`exported-from-enpass-secure-notes.txt`
`exported-from-enpass-credit-cards.txt`

For importing in 1password (mac), choose file->import, use button "options" in the lower left corner. Choose .csv file and then "import credit cards", choose credit card file. Do it again for all types...

##Credit Cards
Credit cards must have a Cardholder to be recognized.

##Note
The exported txt file from enpass may require some preparation before conversion (for now). Please make sure there are at least two empty lines between each item in the file.
If it works, great!
I may update the script to be better in the future... Feel free to contribute.

##Yup
I don't take any responsibilities for stuff that might be missed during conversion. This is for anyones convenience.
