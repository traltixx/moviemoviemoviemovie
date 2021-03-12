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

if not os.path.exists(r'movieresult.txt'):
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
						msg= part1 + ' ('+str(movieyear1)+') '+str(movie_dict[part1][0])+' +++ '+ part2 + ' ('+str(movieyear2)+') '+str(movie_dict[part2][0])+' ==>'+part1[:-3]+part2
						fp.write(msg+'\n')
						
	fp.close()		

if os.path.exists(r'movieresult.txt'):
	lines = []
	used_movies = []
	with open(r'movieresult.txt','r') as infile:
		for line in infile:
			lines.append(line)
	fpo = open(r'results.txt','w')
	for work in lines:
	#done = False
	#while not done:
		#movie = random.choice(lines)
		movie = work
		done = False
		if movie.find(' +++ ') > -1 and movie.find(' ==>') > -1:
			print movie
			movie1 = movie.split(' +++ ')[0].split(') ')[1].strip()
			movie2 = movie.split(' +++ ')[1].split(') ')[1].split(' ==>')[0].strip()
			movie1title = movie.split(' +++ ')[0].split(' (')[0].strip()
			movie2title = movie.split(' +++ ')[1].split(' (')[0].strip()
			movieanswer = movie.split(' ==>')[1].strip()
			movie1plot = ''
			movie2plot = ''
			
			with open(r"MovieSummaries\plot_summaries.txt",'r') as infile:
				for line in infile:
					if line.startswith(movie1):
						movie1plot = line.split(movie1)[1].strip()
					if line.startswith(movie2):
						movie2plot = line.split(movie2)[1].strip()
			if movie1plot != '' and movie2plot != '' and len(movie1plot.split(' ')) > 50 and len(movie2plot.split(' ')) > 50:
				done = True
	#same word
		if done:
			movie1words = movie1plot.split(' ')[30:50]
			movie2words = movie2plot.split(' ')[-50:-30]

			pos1 = -1
			position1=0
			pos2 = -1
			
			for movie1word in movie1words:	
				position2 =0	
				for movie2word in movie2words:
					if movie1word.lower() == movie2word.lower():				
						pos1 = position1
						pos2 = position2

					position2+=1
				position1+=1
			pos2 = 20-pos2

			if pos1 > -1 and pos2 > -1:

				result = ' '.join(movie1plot.split(' ')[0:30+pos1]) + ' '.join(movie2plot.split(' ')[-30-pos2:])
				
				if result.lower().find(movie1title.lower()) > -1:
					result = re.sub(movie1title,' <REDACTED> ',result,re.IGNORECASE)
				if result.lower().find(movie2title.lower()) > -1:
					result = re.sub(movie2title,' <REDACTED> ',result,re.IGNORECASE)
				fpo.write("-----------------------\n")
				fpo.write('Question :' + result + '\n')
				fpo.write('=======================\n')
				fpo.write('Answer is : '+ movieanswer+'\n')
				fpo.write("***********************\n")
	fpo.close()	

print("--- %s seconds ---" % (time.time() - start_time))