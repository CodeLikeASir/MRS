To use the Reddit scrapper, open a terminal, go to the files location and insert:
python MRS.py "SUBREDDIT" MODE "KEYWORD" "START_DATE" "END_DATE" NUMBER_OF_ANALYZED_POSTS

SUBREDDIT: name of the subreddit
MODE: 0 to scan flairs, 1 to scan for keyword in titles
KEYWORD: Word to look for
START_DATE: First date for posts to be added, Format: YYYY-MM-DD, example: 2020-01-01
END_DATE: Last date for posts to be added
NUMBER_OF_ANALYZED_POSTS (OPTIONAL): Number of analyzed top posts (>= number of results)

Don't forget the " before and after the subreddit and the keyword