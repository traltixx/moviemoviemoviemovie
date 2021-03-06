import os
import random
import re
import time

start_time = time.time()
movie_dict={}

with open(r"MovieSummaries\movie.metadata.tsv",'r') as infile:
	for line in infile:
		if line.find('English Language') > -1:
			moviename = line.split('\t')[2]			
			if len(line.split('\t')[3]) > 4:
				movieyear = int(line.split('\t')[3][0:4])
				if movieyear > 1980:
					if moviename not in movie_dict.keys():
						movie_dict[moviename] = [line.split('\t')[0],movieyear]

list1 = movie_dict.keys()
list2 = movie_dict.keys()
fp=open(r'movieresult.txt','w')
for part1 in list1:
	for part2 in list2:
		if part1 != part2:
			if len(part1) > 4 and len(part2) > 4:
				if part1.lower()[-3:] == part2.lower()[:3] and re.findall('[a-z][a-z][a-z]',part2.lower()[:3]) != [] and re.findall('[a-z]',part1.lower()[-4]) != [] and re.findall('[a-z]',part2.lower()[3]) != []:
					movieyear1 = movie_dict[part1][1]
					movieyear2 = movie_dict[part2][1]
					msg= part1 + ' ('+str(movieyear1)+') + '+ part2 + ' ('+str(movieyear2)+') =>'+part1[:-3]+part2
					fp.write(msg+'\n')
fp.close()					

print("--- %s seconds ---" % (time.time() - start_time))