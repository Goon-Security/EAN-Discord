import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import analysis



def get_all_scripts(url):
	try:
		source = requests.get(url).text
	except:
		return []


	soup = BeautifulSoup(source, "html.parser")


	all_script_links = {}
	initial_script_links = []

	#get script links in homepage
	for script in soup.find_all("script"):
	    if script.attrs.get("src"):

	        #if the tag has the attribute 'src'
	        script_url = urljoin(url, script.attrs.get("src"))
	        initial_script_links.append(script_url)



	#search found scripts for more javascript files
	for script_link in initial_script_links:

		try:
			content = requests.get(script_link).text
		except:
			continue


		if script_link not in all_script_links:
			all_script_links[script_link] = {'requested': True, 'content': content}


		#this will part of a parser for specific frontends, this is just a taste
		if "require.config" in content:
			base_path = "/".join(script_link.split("/")[:-1])

			for match in re.findall("\'\/(.*?)\'", content):
				url = urljoin(base_path, match) + ".js"
				
				if url not in all_script_links:
					all_script_links[url] = {'requested': False, 'content': content}


	return all_script_links






def get_all_tokens(url):
	all_tokens = []
	token_data = []

	#parse script files for tokens
	script_links = get_all_scripts(url)

	for script_link in script_links:

		#get all script data
		script_data = script_links[script_link]
		if script_data['requested'] == False:
			content = requests.get(script_link).text

			script_data['requested'] == True
			script_data['content'] == content

		tokens = analysis.string_analysis(script_data['content'])


		#add unique tokens to main list
		for token in tokens:
			if token not in all_tokens: 
				all_tokens.append(token)
				token_data.append({'url': script_link, 'token': token, 'source': script_data['content']})

	return token_data
