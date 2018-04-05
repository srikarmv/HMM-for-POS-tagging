from nltk.corpus import brown
from nltk.tokenize import TweetTokenizer
import random,math,sys,os,re 
import numpy as np

def tokenize(filename):
    '''
    Declare a list of lists for each file and return the list of lists.
    '''
    line_list = []
    
    '''
    Define the regex for compiling only alpha-numeric characters.
    '''

    regex = re.compile('[\W]+')

    #Scraping through the text file
    with open(filename, 'r') as f:
        for line in f:
            line = line.split(' ')
            
            if line[0].startswith("#"):
                continue
            #Only alpha-numeric characters
            for i, word in enumerate(line):
                line[i] = re.sub('[^a-zA-Z0-9]+', '', line[i])
                
                #Convert it into lowercase
                line[i] = line[i].lower()
                #If empty string is processed
                if line[i]=='':
                    del line[i]
            #print line

            if not line:
                continue
            
            line_list.append(line)

    return line_list            


line_list = tokenize('./movies.txt')
word_list = []
for line in line_list:
	for word in line:
		if word not in word_list:
			word_list.append(word)



def normalize_matrix(a,s):
	sum = 0.
	for i in s:
		for j in s:
			sum += a[i][j]
		sum += a[i]['f']
	for i in s:
		for j in s:
			a[i][j] = a[i][j]/sum
		a[i]['f'] = a[i]['f']/sum

def normalize_b(b,s):
	sum = 0.
	for i in s:
		for word in word_list:
			sum += b[i][word]
	for i in s:
		for word in word_list:
			b[i][word] = b[i][word]/sum 

def forward(a,b,pi,line,s):
	alpha = {}

	for i, word in enumerate(line):
		if word == '':
			del line[i]

	for i in range(1,len(line)+1):
		alpha[i] = {}

	#Initialization step:
	for i in s:
		alpha[1][i] = pi[i]*b[i][line[0]]

	#Induction step:
	for t in range(2,len(line)+1):
		for j in s:
			alpha[t][j] = 0.
			for i in s: 
				alpha[t][j] += alpha[t-1][i]*a[i][j]
			alpha[t][j] = alpha[t][j]*b[j][line[t]]

	#Termination step:
	i = len(line)+1
	for j in s:
		alpha[i] += alpha[i-1][j]*a[j]['f']
	return alpha	
	
def backward(a,b,pi,line,s):
	beta = {}
	
	for i, word in enumerate(line):
		if word == '':
			del line[i]

	for i in range(1,len(line)+1):
		beta[i] = {}

	#Initialization step:
	for i in s:
		beta[len(line)][i] = 1

	#Induction step:
	for t in range(len(line)-1,0,-1):
		for i in s:
			for j in s:
				beta[t][i] += a[i][j]*beta[t+1][j]
			beta[t][i] = beta[t][i]*b[i][line[t]]

	#Termination step:
	beta[0] = 0.
	for i in s:
		beta[0] = beta[1][i]*pi[i]

	return beta

def viterbi(a,b,pi,line,s):
	eta = {}

	for i, word in enumerate(line):
		if word == '':
			del line[i]

	for i in range(1,len(line)+1):
		eta[i] = {}

	#Initialisation step:
	for i in s:
		eta[1][i] = pi[i]*b[i][line[0]]
	
	#Recursion step:
	for t in range(2,len(line)+1):
		for j in s:
			for i in s:
				eta[t][j] += eta[t-1][i]*a[i][j]
			eta[t][j] = eta[t][j]*b[j][line[t]]

	return eta

			##States (s):
s = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"]

			##Output alphabet (V):
V = word_list

			##Transition probabilities (a):
a = {}
for i in s:
	a[i] = {}
	for j in s:
		a[i][j] = random.random()
	a[i]['f'] = random.random()

normalize_matrix(a,s)
#print a

			##Emission probabilities (b):
b = {}
for i in s:
	b[i] = {}
	for word in word_list:
		b[i][word] = random.random()

normalize_b(b,s)
#print b

			##Pi:
pi = {}
sum = 0.
for i in s:
	pi[i] = random.random()
	sum += pi[i]
for i in s:
	pi[i] = pi[i]/sum 
#print pi

			## Alpha computation:

alpha = {}
#alpha = forward(a,b,pi,line_list[0],s)
