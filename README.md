# tweet_tracker
Collects, analyze, and graph tweet trends from a specified user

To complete before running program: 

    Fill in lines 12-20 in main.py with full path to storage files for tweet information. If/else structure here decides which        user to load tweets from.
    Obtain Twitter developer credentials and input consumer key and secret key into collect.py line 7.
    
    
Menu options: 
  c: Collect.  Run this command the first time the program is run for a specific user.  If this is run with a storage file that has other information, stored information will be overwritten.
  
  con: Continue.  Run this command to continue loading a user's old tweets.  Twitter has a stream limit, forcing this command to load tweets roughly 800-1000 at a time.  If a check for newer tweets is desired, run the 'u' menu option.
  
  r:  Prints all the stored tweet dates from the storage file specified in main.py lines 12-20.
  
  p: Plots a user's common word usage over time.  Can specify a moving average filter length to better display longer-term trends in thinking.  Default is a 7 day filter.

  com: Common words.  Outputs most commonly used words in a stored tweet file.
  
  u: Update.  Loads all of a user's most recent tweets beginning at the most recent stored tweet.
  
  w: Plot the use of one specified word over the course of all stored tweets for specified user.
