# Scam Scanner in Python

### Originally written June 2011, ported over to Python in 2013

### Note: I wrapped this in a GUI partly to teach myself the wx library 
### 	but also because this needs to be made for the end-user if it's going to be used at all

### The Scam Scanner can be used to scan websites for specified criteria and assigns a score for the number of criteria items found.
### Innocuous criteria can be specified and will be ignored.

### Important note: although I call this the scam scanner (for the original reason I wrote it), it could easily have a number of applications ranging from:
###	* monitoring criminal activity
###	* political candidate / group research, especially for messaging and issue cohesion
###	* monitoring websites for racist, misogynist, homophobic, transphobic, and xenophobic hate speech
###	* and many more.  If you use it in a novel way, tell me how you're using the scanner!

## To use:

### 1) Create a criteria file in .csv, .tsv, .xls, or .xlsx format. The Scam Scanner will scan each website for this criteria.
###	1a) Each criteria category should occupy one column in the first (header) row.
###	1b) Each criteria item should appear in the rows grouped under its category header.
###	1c) See criteria_file_example.csv for example.

### 2) (Optional) Create a innocuous-criteria file in plaintext (.txt) format. The Scam Scanner will ignore the innocuous-criteria when scanning the websites.
###	2a) Write each innocuous-criteria item on its own line.
###	2b) See innocuous_criteria_file_example.txt for example.

### 3) Create a websites file in plaintext (.txt) format. The Scam Scanner will scan each of these websites for the criteria specified above.
###	3a) Write each website to scan on its own line.
###	3b) See website_file_example.txt for example. (the first site is a test page; the second page is innocuous and should have no scam score)

### 4) Choose how many levels of the website to scan: just the homepage, every page, or somewhere in between.

### 5) Choose how long to wait in between scanning each page.

### 6) Choose whether to save the results as a quick-view spreadsheet, a fully-detailed HTML report, or both.

### 7) (Optional, Advanced) Name the user-agent to use while scanning websites.

### 8) (Optional, Advanced) Name the referral-string to use while scanning websites.

### 9) (Optional, Advanced) Set the proxy IP and port number if desired.

### 10) (Optional, Advanced) (NOT YET IMPLEMENTED) Set the TinEye API Key to use.

### 11) (Optional, Advanced) Choose whether to pull the WHOIS information for each website.

### 12) (Optional, Advanced) Select the list of rightsholders to check each domain for WIPO-type domain name violations (see http://www.wipo.int/amc/en/domains/guide/); create the file in plaintext (.txt) format.
###	12a) Write each rightsholder on its own line.
###	12b) See rightsholders_file_example.txt for example.

### 13) Run and see the results!
###	13a) See results_example.csv for sample results (compare to your results to double-check everything works)
###	13b) See results_example.html for sample results (compare to your results to double-check everything works)


