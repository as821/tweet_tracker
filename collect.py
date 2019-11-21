
def collect(write_file, user, num_tweets=500):


    # tweepy set up and authorization
    import tweepy
    auth = tweepy.AppAuthHandler( 'your_consumer_key', 'your_secret_key')
    api = tweepy.API(auth)

    # pickle set up/import
    import pickle

    # user selection
    name = user    # select user
    results = api.user_timeline(name)   # collect initial round of tweets

    # initializations
    data_size = int(num_tweets)
    tweet_ids = []
    storage_struct = []     # empty list.  will fill with tuples in while loop
    next_tweet = int(0)

    try:
        while len(storage_struct) < data_size:    # user controlled iterations      input() == 'y'
            if next_tweet != 0:  # all iterations but the first
                next_tweet -= 1   # max_id: Returns statuses with ID less than (older than) or equal to specified ID."
                results = api.user_timeline(name, max_id = next_tweet)

            for tweet in results:   # collect tweet IDs from user_timeline
                tweet_ids.append(tweet.id)

            for _id in tweet_ids:    # pass through  .get_status method to allow for full_text option
                obj = api.get_status(_id, tweet_mode = 'extended')
                _tuple = obj.id, obj.created_at, obj.full_text   # make tuple for tweet storage entry
                storage_struct.append(_tuple)                  # append tweet tuple to storage_struct

            next_tweet = storage_struct[-1][0]               # oldest tweet in storage.  set for next iteration
            tweet_ids.clear()           # clear collected tweet IDs for next iteration

            # output for observer
            print( 'num stored: ', end='')
            print(len(storage_struct))
    except tweepy.error.RateLimitError:
        print('Rate limit reached.  Storing struct now...')
    except Exception:
        print('unkown exception caught.  Storing struct now...')

    # output after while() ends     (for future reference.  can be used to add more old data later on)
    print('num tweets stored: ', end='')
    print(len(storage_struct))
    print('oldest tweet date: ', end='')
    print(storage_struct[-1][1])
    print('oldest id: ', end='')
    print(next_tweet)

    if len(storage_struct) > 0:
        # pickling storage of list of tuples
        filename = write_file   # note: no file extension
        pickle_file = open(filename, 'wb')  # wb allows writing to binary file. 'W' clears file contents
        pickle.dump(storage_struct, pickle_file, pickle.HIGHEST_PROTOCOL)   # pickle write to file method
        pickle_file.close()     # close file
    print('Processing and storage complete...')





# continue_loading function     1126134364436406272
def continue_loading(last_id, write_file, user, num_tweets=1000):
    # tweepy set up and authorization
    import tweepy
    auth = tweepy.AppAuthHandler('your_consumer_key', 'your_secret_key')
    api = tweepy.API(auth)

    # pickle set up/import
    import pickle
    import read

    # avoid warnings about outputting values before assignment (exception handling issues)
    storage_struct = read.read(write_file)
    next_tweet = int(last_id)
    initial_struct_size = len(storage_struct)

    try:
        # initializations
        data_size = int(num_tweets)
        tweet_ids = []
        struct_length_store = []
        terminate_size = initial_struct_size + data_size

        # user selection
        name = user  # select user

        # loop through queries
        while len(storage_struct) < terminate_size:
            next_tweet -= 1  # max_id: Returns statuses with ID less than (older than) or equal to specified ID."
            results = api.user_timeline(name, max_id=next_tweet)

            for tweet in results:  # collect tweet IDs from user_timeline
                tweet_ids.append(tweet.id)

            for _id in tweet_ids:  # pass through  .get_status method to allow for full_text option
                obj = api.get_status(_id, tweet_mode='extended')
                _tuple = obj.id, obj.created_at, obj.full_text  # make tuple for tweet storage entry
                storage_struct.append(_tuple)  # append tweet tuple to storage_struct

            tup = storage_struct[-1]  # oldest tweet in storage
            next_tweet = tup[0]  # set next for following iteration of tweets
            tweet_ids.clear()  # clear collected tweet IDs for next iteration

            # output for observer
            print('num stored: ', end='')
            print(len(storage_struct))


            # handle when max tweet query date hit
            struct_length_store.insert(0, len(storage_struct))
            if len(struct_length_store) > 3:
                struct_length_store.pop()

            # average == len, break
            if len(struct_length_store) == 3:
                _sum = struct_length_store[0] + struct_length_store[1] + struct_length_store[2]
                average = _sum / 3
                if average == len(storage_struct):
                    break


    except tweepy.error.RateLimitError:
        print('Rate limit reached.  Storing struct now...')
    except Exception:
        print('unkown exception caught.  Storing struct now...')

    # output after while() ends     (for future reference.  can be used to add more old data later on)
    print('num tweets stored: ', end='')
    print(len(storage_struct))
    print('oldest tweet date: ', end='')
    print(storage_struct[-1][1])
    print('oldest id: ', end='')
    print(next_tweet)

    if initial_struct_size < len(storage_struct):
        # pickling storage of list of tuples
        filename = write_file  # note: no file extension
        pickle_file = open(filename, 'wb')  # wb allows writing to binary file. 'W' automactically clears contents
        pickle.dump(storage_struct, pickle_file, pickle.HIGHEST_PROTOCOL)  # pickle write to file method
        pickle_file.close()  # close file
    else:
        next_tweet += 1   # account for -= above
    print('Processing and storage complete...')






def update(most_recent_id, write_file, user):
    # tweepy set up and authorization
    import tweepy
    auth = tweepy.AppAuthHandler('your_consumer_key', 'your_secret_key')
    api = tweepy.API(auth)

    # pickle set up/import
    import read
    import pickle

    # initializations
    tweet_ids = []                              # tweet_id list initialization
    storage_struct = read.read(write_file)      # read in stored data structure from file
    initial_struct_size = len(storage_struct)   # length of original data structure
    recent_addition = int(most_recent_id)
    initial_first = storage_struct[0][0]        # stores newest pre-update tweet ID
    no_new = False                              # still new tweets to add
    count = 0                                   # record number of infinite loop iterations
    new_tweet_subscript = 0                     # stores subscript of new tweet to be added...
                                                # ...(newest to oldest until original newest ID found)

    try:
        while True:
            print('Most recently added tweet id: ', storage_struct[new_tweet_subscript - 1][0],
                  "\n\tDate: ", storage_struct[new_tweet_subscript - 1][1])

            # determine which user_timeline version to cLL
            if count > 0:                                          # execute on all iterations but first
                results = api.user_timeline(user, max_id=recent_addition)   # only query for tweets older than most recent addition
            else:                                                   # execute only on first iteration
                results = api.user_timeline(user)                   # queries for most recent tweets
            count += 1                                              # increment counter to record num. iterations


            # loop through tweet IDs from results[]
            for tweet in results:
                if tweet.id == initial_first:                      # collect until find original newest tweet
                    print('no_new true')
                    no_new = True
                    break
                tweet_ids.append(tweet.id)                          # append on extended tweet request list


            # pass through .get_status method to allow for full_text option
            for _id in tweet_ids:
                obj = api.get_status(_id, tweet_mode='extended')     # query for extended tweet version
                tup = obj.id, obj.created_at, obj.full_text         # make tuple for tweet storage entry
                storage_struct.insert(new_tweet_subscript, tup)     # insert tweet tuple at front of storage_struct
                new_tweet_subscript += 1                            # increment subscript count for each new tweet added


            # maintenance for next iteration
            tweet_ids.clear()                                       # clear collected tweet IDs for next iteration
            recent_addition = storage_struct[new_tweet_subscript - 1][0]# set new max_id for next iteration...
                                                                        #... - 1 because is incremented for next round already


            # output for observer
            print('num new stored: ', len(storage_struct)-initial_struct_size)

            # terminate infinite loop
            if no_new:                                            # no more new tweets to get, break
                break


    except tweepy.error.RateLimitError:
        print('\nRate limit reached.  Storing struct now...')
    except:
        print('\nunkown exception caught.  Storing struct now...')

    # output after while() ends     (for future reference.  can be used to add more old data later on)
    print('num tweets stored: ', len(storage_struct))
    print('newest tweet date: ', storage_struct[0][1])
    print('newest id: ', storage_struct[0][0])

    if initial_struct_size < len(storage_struct):
        # pickling storage of list of tuples
        filename = write_file                                               # note: no file extension
        pickle_file = open(filename, 'wb')                                  # wb : writing to binary file. 'W' clears contents
        pickle.dump(storage_struct, pickle_file, pickle.HIGHEST_PROTOCOL)   # pickle write to file method
        pickle_file.close()                                                 # close file
    else:
        print('\nNothing new to add...')

    print('\nProcessing and storage complete...')
