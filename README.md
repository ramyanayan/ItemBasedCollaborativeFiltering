This is an implementation of a simple item-based collaborative filtering recommender system.

Format of data file for item
You are provided with the input data file ratings-dataset.tsv. The file consists of one rating event per line. Each rating event is of the form:

user_id\trating\tmovie_title

The user_id is a string that contains only alphanumeric characters with hyphens or spaces (no tabs). The rating is one of the float values 0.5,
1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 The movie_title is a string that may contain space characters (to separate the words). The three
fields -- user_id, rating, and the movie_title -- are separated by a single tab character (\t).

Please run <lastname>_<firstname>_collabFilter.py
  
The Ratings Prediction program should output a list of k items to recommend to the user specified as an input argument. It  should identify the k items with the highest predicted rating for this user. Be sure not to include any items that the user has already rated.

Please run python <lastname>_<firstname>_collabFilter.py <ratingsFileName> <user> <n> <k>
