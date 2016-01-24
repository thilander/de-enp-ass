#De-enp-ass
Converts an exported file from enpass to files with comma-separated values (.csv).
This supports logins, secure notes and credit cards and will export one csv file for each type.
It's originally written to prepare files for import to 1password but could be modified to any password manager that can import csv files.

##Remove files when done
Please remove the files after you've imported them since they contain all your passwords (like the exported file from enpass also does. Remove it!)

##Pre-usage
You must have python installed on your computer. If you have a mac it's already installed. If you run linux you already know everything ;)
If you run windows, google is your friend.

##Note
The exported txt file from enpass may require some love before conversion (for now). Please make sure there are at least two empty lines between each item in the file.

It's somewhat of a hit or miss, for me it works great but you'll need to quickly check the enpass txt file to see that the password chunks are not looking funky. If a password contains a huge note containing several empty lines, the conversion will fail.
What you can do then is to remove empty lines (the conversion script checks for two empty lines between items).

##Usage
Download de-enp-ass.py, open up the terminal, cd to that folder and run:

```python de-enp-ass.py /path/to/exported-from-enpass.txt```

This will generate three files in the same folder as the exported enpass file:

`exported-from-enpass-logins.csv`

`exported-from-enpass-secure-notes.csv`

`exported-from-enpass-credit-cards.csv`

For importing in 1password (mac), choose file->import, use button "options" in the lower left corner. 
Choose .csv file and then "import credit cards", open the credit card file.
Do it again for secure notes and logins and choose correct import in the dialog.

###What do you mean "cd to that folder"?
Move both the exported enpass txt file (we'll call it enpass.txt) and the downloaded de-enp-ass.py to your desktop. 
Then open up the terminal and run:

```
cd ~/Desktop
```

This will change directory to desktop.
Then run the script:

```
python de-enp-ass.py enpass.txt
```

Once completed (if it ran without problems) you will see three more files on the desktop.

##Credit Cards
Credit cards must have a Cardholder to be recognized.

##Eh
If it works for you, great!
I made this mainly for myself because I had a sh#t ton of passwords and would have been a pain to manually migrate, but I really wanted to migrate. I figured others might benefit of it too.
I may update the script to be better in the future... Feel free to contribute.

##Yup
I don't take any responsibilities for stuff that might be missed during conversion. This is for anyones convenience.
