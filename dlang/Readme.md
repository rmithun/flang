# backend
Sample flask app to check language profanity


## Getting Started

1. Install requirments using Pip
2. Run Python init_db.py to create sqlite3 table for posts
3. Run flask server: flak run
4. Use postman to make requests to add comments:
	ex: {'paragraphs':"This is a sample \n This is a sample"}


## Things to consider:

1. The app uses better-profanity to check for any foul words
2. If the sentences service is unavailable - the comments are stored as not moderated and so the daily moderator
   can be scheudled to run in intervals to moderate the comments
3. The application used Sqlite as DB and there is not differntiation between dev db and test DB


# Must to do Improvements

1. Set up test Sqllite DB for separating DB's
2. Improve unit tests to check for the inserted data in DB
3. Make sure the test db is created and destroyed after running the tests

