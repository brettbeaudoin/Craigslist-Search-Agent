#!/usr/bin/python
#################################################################################
#
#  Created by Brett Beaudoin, February 2012
#  Twitter: @BrettBeaudoin
#  http://brettbeaudoin.com
#
#################################################################################
from urllib import FancyURLopener, quote_plus
import re

# Variables
# TODO: pass these in as arguments
region = "washingtondc"
minAsk = 500
maxAsk = 3500
query = "(moving | box) (truck | van) -parting -parts"

# Constants
delimStart = "~START~"
delimEnd = "|"
itemStart = "<p class=\"row\">"
itemEnd = "</div>"
spanStart = "<p class=\"row\">"
spanEnd = "</div>"
url = "http://%s.craigslist.org/search/?catAbb=sss&minAsk=%d&maxAsk=%d&query=%s" % (region, minAsk, maxAsk, quote_plus(query))
replaceStrings = [("\n", " "), ("\t", " "), ("  ", " "), ("<p class=\"row\">", delimStart), ("</p>", delimEnd)]
results = []

# Reg-Ex Patterns
patItems = re.compile(r"(?<=%s)([^|]*)(?=%s)" % (delimStart, delimEnd))
patSpan = re.compile(r"(?<=</span>)(.*)(?=<span)")
patUrl = re.compile(r"http[^\"']+(?=[\"'])")
patDate = re.compile("[JFMASOND]{1}[a-z]{2}\s+\d+(?=\s)")
patPrice = re.compile(r"(?<=\$)([^\<]*)(?=<)")
patDesc = re.compile(r"(?<=\">)([^\<]*)(?=<)")

try:
	# Get the HTML
	opener = FancyURLopener({})
	req = opener.open(url)
	html = req.read()
	html = html[html.find(itemStart):]
	html = html[0:html.find(itemEnd)-1]

	# Clean up the HTML
	for pair in replaceStrings:
		while html.find(pair[0]) >= 0:
			html = html.replace(pair[0], pair[1])

	# Parse the results
	for item in re.findall(patItems, html):
		"""
		Example:
		<p class="row">
			<span class="ih" id="images:5Ic5Kf5H23L43I63N1c2ffc52eab0d5a11a35.jpg">&nbsp;</span>
			 Feb 15 - <a href="http://washingtondc.craigslist.org/nva/cto/2852408672.html">great box truck w/ ramp -</a>
			 $3500<font size="-1"> (springfield)</font> <small class="gc"><a href="/cto/">owner</a></small> <span class="p"> pic</span><br class="c">
		</p>
		"""
		try:
			span = re.search(patSpan, item).group(0).strip()
			"""
			Example:
				 Feb 15 - <a href="http://washingtondc.craigslist.org/nva/cto/2852408672.html">great box truck w/ ramp -</a>
				 $3500<font size="-1"> (springfield)</font> <small class="gc"><a href="/cto/">owner</a></small>
			"""
			url = re.search(patUrl, span).group(0)
			date = re.search(patDate, span).group(0)
			price = re.search(patPrice, span).group(0)
			desc = re.search(patDesc, span).group(0)
			results.append({"date": date, "price": price, "desc": desc, "url": url})
		except:
			pass
	
	print results
except Exception, err:
	print "Error: %s" % str(err)











