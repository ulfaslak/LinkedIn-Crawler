"""Crawl your outer (2nd + 3nd degree) LinkedIn network for visits.

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
$ python crawler.py Medicine ulfaslak@gmail.com mysupersecretpassword

Important: Break the process by doing ctrl + c (multiple times is necessary).

Author: Ulf Aslak
"""

import sys
import numpy as np
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create or load book keeping file
try:
	with open('visited_users.json', 'r') as infile:
		VISITED_USERS = json.load(infile)
except IOError:
	with open('visited_users.json', 'w') as outfile:
		json.dump([], outfile)
	VISITED_USERS = []

QUERY = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]

VISITING_TIME_mu = 58.2
VISITING_TIME_sigma = 20

print QUERY
sys.exit()

def update_visited_users(visited_users, user):
	visited_users += [user]
	with open('visited_users.json', 'w') as outfile:
		json.dump(visited_users, outfile)
	return visited_users

d = webdriver.PhantomJS()
d.get('https://www.linkedin.com/')

# Log in
user_field = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-uno-reg-guest-home']/div[@class='header']/div[@class='wrapper']/form[@class='login-form']/input[@id='login-email']")
pass_field = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-uno-reg-guest-home']/div[@class='header']/div[@class='wrapper']/form[@class='login-form']/p[@class='password-wrapper']/input[@id='login-password']")

user_field.send_keys(USERNAME)
pass_field.send_keys(PASSWORD)

pass_field.send_keys(Keys.ENTER)

while True:
	try:
		d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-oz-winner']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='main']/div[@id='left-container']/div[@id='content']/div[@id='ozidentity-container']/div[@id='identity']/section[@class='member']/div/div[@class='info']/h3/a[@class='name']")
		break
	except:
		print "sleeping 0.2s..."
		sleep(0.2)

# Search for people
dropdown_button = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-oz-winner']/div[@id='header']/div[@id='top-header']/div[@class='wrapper']/div[@class='header-section first-child']/form[@id='global-search']/fieldset/div[@id='control_gen_2']/span[@class='label']/span[@class='styled-dropdown-select-all']")
dropdown_button.click()
dropdown_item = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-oz-winner']/div[@id='header']/div[@id='top-header']/div[@class='wrapper']/div[@class='header-section first-child']/form[@id='global-search']/fieldset/div[@id='control_gen_2']/ul[@class='search-selector']/li[@class='people option']")
dropdown_item.click()

search_field = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-oz-winner']/div[@id='header']/div[@id='top-header']/div[@class='wrapper']/div[@class='header-section first-child']/form[@id='global-search']/fieldset/div[@id='search-box-container']/span[@id='search-autocomplete-container']/span[@class='twitter-typeahead']/input[@id='main-search-box']")
search_field.send_keys(QUERY)
search_field.send_keys(Keys.ENTER)

# Filter to 2nd+ degree
second_connections = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='facets-col']/form[@id='refine-search']/div/ul[@class='facets']/li[@id='facet-N']/fieldset/div[@class='facet-values-container']/ol[@class='facet-values']/li[@class='facet-value'][2]/div[@class='label-container']/label[@class='facet-label']/bdi")
second_connections.click()

third_connections = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='facets-col']/form[@id='refine-search']/div/ul[@class='facets']/li[@id='facet-N']/fieldset/div[@class='facet-values-container']/ol[@class='facet-values']/li[@class='facet-value'][4]/div[@class='label-container']/label[@class='facet-label']/bdi")
third_connections.click()


while True:
	try:
		d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='results-col']/div[@id='pivot-bar-container']/div[@id='pivot-bar']/ul[@class='pivots']/li[@class='pivot'][1]")
		break
	except:
		print "sleeping 0.2s..."
		sleep(0.2)


while True:
	for i in range(10):
		skip_user = False

		try:
			user = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='results-col']/div[@id='results-container']/ol[@id='results']/li[@class='mod result idx%d people']/div[@class='bd']/h3/a[@class='title main-headline']" % i)
			user_name = user.get_attribute('innerHTML')
		except:
			print "\n---> EXCEPTION: Problem crawling user for %d." % i
			continue
		
		if user_name in VISITED_USERS:
			print "\n---> WARNING: User '%s' already visited." % user_name
			continue

		VISITED_USERS = update_visited_users(VISITED_USERS, user_name)
		print "\n################\n\nUsername:", user_name

		user.click()

		sleep_counter = 0
		while True:
			try:
				user_summary = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-nprofile_view_nonself']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='wrapper']/div[@id='profile']/div[@id='background']/div[@class='background-content ']/div[@id='background-summary-container']/div[@id='background-summary']/div[@id='summary-item']/div[@id='summary-item-view']/div[@class='summary']/p[@class='description']")
				print "\nUser summary:\n-------------\n", user_summary.get_attribute('innerHTML')[:200], "\n"
				break
			except:
				print "sleeping 0.2s..."
				sleep_counter += 1
				sleep(0.2)
				if sleep_counter > 10:
					print "\n---> WARNING: Can't get user summary."
					break

		sleep_time = abs(np.random.normal(VISITING_TIME_mu, VISITING_TIME_sigma, 1)[0])
		sleep(sleep_time)
		
		# Go back
		d.execute_script("window.history.go(-1)")

		while True:
			try:
				d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='results-col']/div[@id='pivot-bar-container']/div[@id='pivot-bar']/ul[@class='pivots']/li[@class='pivot'][1]")
				break
			except:
				print "sleeping 0.2s..."
				sleep(0.2)

	try:
		next = d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='results-col']/div[@id='results-pagination']/ul[@class='pagination']/li[@class='next']/a[@class='page-link']")
		next.click()
	except Exception as e:
		print "\n---> FATAL ERROR: Can't page!"
		print e
		break

	print "\nPaging...\n"

	while True:
		try:
			d.find_element_by_xpath("/html[@class='os-mac']/body[@id='pagekey-voltron_people_search_internal_jsp']/div[@id='body']/div[@class='wrapper hp-nus-wrapper']/div[@id='srp_main_']/div[@id='srp_container']/div[@id='results-col']/div[@id='pivot-bar-container']/div[@id='pivot-bar']/ul[@class='pivots']/li[@class='pivot'][1]")
			break
		except:
			print "sleeping 0.2s..."
			sleep(0.2)