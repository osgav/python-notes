#!/usr/bin/env python

import re
import sys
import subprocess



# function that takes text to be searched, and a list of regex patterns
# to search the text for

def test_patterns(text, patterns=[]):
	
	# empty list to be populated with match strings
	# and returned by the function
	matches = []

	# iterate through patterns passed in	
	for pattern in patterns:
		print "Matching pattern %s" % pattern.pattern
		# for each match found by the current pattern
		for match in re.findall(pattern, text):
			# add the match the the list 'matches'
			matches.append(match)
	return matches

if __name__ == "__main__":
	
	if sys.argv < 2:
		print 'usage: python firefox_patterns.py <filename>'
	else:
	
		# open user-provided list of useragents
		useragentsfile = open(sys.argv[1], 'r')
		useragents = useragentsfile.read()

		# compile firefox regex pattern
		pattern1 = re.compile(r'Firefox\S+\s')

		# get matches for firefox regex pattern "pattern1" within
		# the user-provided file of useragents
		# (invoke test_patterns function)
		matches = test_patterns(useragents, [pattern1,])

		
		# set up subprocesses for equivalent of piping matches
		# into ' | cut -f1 -d. | sort | uniq -c | sort -rn' at the CLI
		
		cut_cmd = subprocess.Popen(['cut', '-f1', '-d.'],
					stdin=subprocess.PIPE,
					stdout=subprocess.PIPE,
					)

		# link STDIN to cut_cmd's STDOUT
		sort_cmd = subprocess.Popen('sort',
                                        stdin=cut_cmd.stdout,
                                        stdout=subprocess.PIPE,
                                        )

		# link STDIN to sort_cmd's STDOUT
                uniq_cmd = subprocess.Popen(['uniq', '-c'],
                                        stdin=sort_cmd.stdout,
                                        stdout=subprocess.PIPE,
                                        )
		
		# link STDIN to uniq_cmd's STDOUT
                sort_cmd_2 = subprocess.Popen(['sort', '-rn'],
                                        stdin=uniq_cmd.stdout,
                                        stdout=subprocess.PIPE,
                                        )

		# end this madness!
                end_of_pipe = sort_cmd_2.stdout

		# test_patterns function returns a list, but process.communicate(...)
		# requires a string or buffer..
                matchdump = "\n".join(matches)
		
		# send matchdump (string containing matches for firefox regex pattern)
		# to STDIN for cut_cmd
                cut_cmd.communicate(matchdump)

		# print lines from STDOUT of last command - sort_cmd_2
                for line in end_of_pipe:
                        print '\t', line.strip()

