# LinkedIn Crawler

Crawl your outer (2nd + 3nd degree) LinkedIn network for visits.

Provide search QUERY, USERNAME and PASSWORD, where QUERY should be a word
you want the people you crawl to have in their description, e.g. "Medicine",
"Data", "Civil Engineering". Run the script from its directory in Terminal.

What it does: The crawler logs in, searches for people and uses the QUERY 
parameter, checks the 2nd and 3rd degree checkboxes, then spends on average 
around 1 minute at each profile that the result returns, to simulate real 
behavior (in case anyone is looking). If it starts acting up you have probably
exceeded the LinkedIn monthly search limit. For that reason I recommend you
use this script only a little bit (breaking it after a couple of pages using
ctrl + c) or only use it by the end of the month since search quota restarts
on the 1st of each month.

Usage example
-------------
$ python crawler.py "Electrical Engineering" ulfaslak@gmail.com mysupersecretpassword

Important: Break the process by doing ctrl + c (multiple times is necessary).

Author: Ulf Aslak
