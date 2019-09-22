import sys
import string
import re
import json
import itertools
import collections
import glob
import os
import itertools
import operator
from decimal import *
from itertools import combinations

document = str(sys.argv[1])
USER = str(sys.argv[2])
N = int(sys.argv[3])
k = int(sys.argv[4])

MovieUserlist=[]
linelist = []
movies = {}

afinnfile = open(document)
for line in afinnfile:
	line = line.strip()
	linelist = line.split("\t")
	MovieUserlist.append(linelist)
	if linelist[2] not in movies:
		movies[linelist[2]] = []
	movies[linelist[2]].append(linelist[0])

# for key in MovieUserlist:
# 	movieset.add(key[2])

movieuserdic={}
for key in MovieUserlist:
	if key[0] not in movieuserdic:
		movieuserdic[key[0]]=[]
MovieUser = {}
for key in MovieUserlist:
	if key[0] not in MovieUser:
		MovieUser[key[0]]={}
for key in MovieUserlist:
	MovieUser[key[0]].update({key[2]:float(key[1])})
movielist = sorted(movies.keys())
for key in MovieUser:
	for movie in movielist:
		if movie in MovieUser[key].keys():
			movieuserdic[key].append(float(MovieUser[key][movie]))
		else:		
			movieuserdic[key].append(float(0))
			
if USER not in movieuserdic.keys():
	print" Wrong user entered, User not in the input data list provided. Please Enter the right user and re-run the program"
	sys.exit()

similarity = {}
for pair in combinations(movielist, 2):
	pair = tuple(sorted(pair))
	movie_i = pair[0]
	movie_j = pair[1]
	co_rated_users = set(movies[movie_i]) & set(movies[movie_j])
	if len(co_rated_users)==0:
		similarity[pair] = 0
		continue
	averageJ=[]
	averageI=[]
	for user in co_rated_users:
		averageI.append(MovieUser[user][movie_i])
		averageJ.append(MovieUser[user][movie_j])
	ave_i=sum(averageI)/len(co_rated_users)
	ave_j=sum(averageJ)/len(co_rated_users)
	N_I = []
	N_J = []
	for user in co_rated_users:
		N_I.append(MovieUser[user][movie_i] - ave_i)
		N_J.append(MovieUser[user][movie_j] - ave_j)
	numerator_fraction=0.0
	for i,j in zip(N_I,N_J):
		numerator_fraction+=(i*j)
	denominator_fraction1=0.0
	denominator_fraction2=0.0
	for i in N_I:
		denominator_fraction1+=i**2
	for j in N_J:
		denominator_fraction2+=j**2
	denominator_fraction= (denominator_fraction1*denominator_fraction2)**0.5
	similarity[pair] = 0 if denominator_fraction==0 else numerator_fraction/denominator_fraction

def predictMovieRating(movie, similarity, MovieUser):
	rated_movies = MovieUser[USER].keys()
	rated_movie_pairs =[]
	for rated_movie in rated_movies:
		rated_movie_pairs.append(tuple(sorted([movie, rated_movie])))
	relevant_similarity =[]
	for wij in rated_movie_pairs:
		relevant_similarity.append((wij, similarity[wij]))
	relevant_similarity = sorted(relevant_similarity,key=lambda x: x[0])
	relevant_similarity = sorted(relevant_similarity, key=lambda x: x[1], reverse=True)
	if len(relevant_similarity)>N:
		relevant_similarity = relevant_similarity[0:N]
	neighbourhood_movie=[]
	for wij in relevant_similarity:
		neighbourhood_movie.append(wij[0][(wij[0].index(movie)-1)%2])	
	numerator_fraction =0
	for n_movie,win in zip(neighbourhood_movie, relevant_similarity):
		numerator_fraction+= (MovieUser[USER][n_movie] * similarity[win[0]])
	denominator_fraction=0
	for win in relevant_similarity:
		denominator_fraction+= abs(similarity[win[0]])
	if denominator_fraction==0:
		return 0
	else:
		return numerator_fraction/denominator_fraction

def iterative_bfs(graph, start):
	bfs_tree = {start: {"parents":[], "children":[], "level":0}}
	q = [start]
	while q:
		current = q.pop(0)
		for v in graph[current]:
			if not v in bfs_tree:
				bfs_tree[v] = {"parents":[current], "children":[], "level": bfs_tree[current]["level"] + 1}
				bfs_tree[current]["children"].append(v)
				q.append(v)
			else:
				if bfs_tree[v]["level"] > bfs_tree[current]["level"]:
					bfs_tree[current]["children"].append(v)
					bfs_tree[v]["parents"].append(current)
	return bfs_tree

unrated_movies = set(movielist).difference(set(MovieUser[USER].keys()))
predictions = {}
for movie in unrated_movies:
	predictions[movie] = predictMovieRating(movie, similarity, MovieUser)
predictions = collections.OrderedDict(sorted(predictions.items()))
sorted_predictions = sorted(predictions.items(), key=operator.itemgetter(1),reverse=True)[:k]
for x,y in sorted_predictions:
	print "%s %.5f"%(x,y)	
