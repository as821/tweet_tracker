import collections
from textblob import TextBlob



# data analytics
def common_words(stored_struct, num_return=10):        # most common words
    # words to exclude
    # (questionable removals: 'ONE', 'BIG', 'BAD', 'LOOK', 'US'(could mean U.S.), 'WIN', 'TODAY', 'NEW', 'FIRST',
    # 'NOTHING', 'MAKE', 'FUTURE', 'PUBLIC', 'SERVICE', 'PRESIDENT', 'PETE'', 'SOUTH', 'BEND', 'MICHAEL')
    exclude_list = ['A', 'THE', 'I', 'AND', 'WE', 'IS', 'WAS', 'ARE', 'YOU', 'AS', 'FOR', 'IN', 'TO', 'HAS',
                    'BEEN', 'MY', 'IT', 'MY', 'OUR', 'YOUR', 'THERE', 'WITH', 'OF', 'BE', 'THAT', 'ON', 'WILL', 'HAVE',
                    '&AMP', '&AMP;', 'THEY', 'AT', 'NOT', '-', 'BY', 'RT', 'OR', 'DO', 'SO', 'HE', 'HER', 'THEIR',
                    'BUT', 'MORE', 'FROM', 'HIS', 'HERS', 'THIS', 'WHO', 'ALL', 'VERY', 'THIS', 'THAN', 'AN', 'ABOUT',
                    'WHO', 'NO', 'NOW', 'JUST', 'GET', 'WOULD', 'WANT', 'MANY', 'BACK', 'BEING', 'SHOULD', 'WERE',
                    'NEVER', 'WHICH', 'UP', 'EVEN', 'WHAT', 'OTHER', 'WHEN', 'MUCH', 'ONLY', 'ME', 'IF', 'ONE', 'AFTER',
                    'OUT', 'MUST', 'BIG', 'CAN', "DON'T", 'OVER', 'DOING', 'INTO', 'GOING', 'AM', 'BECAUSE', 'TWO',
                    'LIKE', 'HAD', 'ANY', 'DID', 'KNOW', 'HOW', 'GETTING', 'THEM', 'WHY', 'EVER', 'WHY', 'MOST', 'GO',
                    'LOOK', 'BIG,', 'GOT', 'TAKE', 'THANK', 'KEEP', 'IT.', 'HERE', 'EVERY', 'END', 'NEED', 'WAY', 'TOO',
                    'SEE', 'ACROSS', 'WIN', 'TODAY', '–', '—', 'DAY', 'US', 'THESE', 'NEW', 'DONE', 'FIRST', 'LAST',
                    'MADE', 'HIM', 'BAD', 'AGAINST', 'AGAIN', 'GOOD', 'NOTHING', 'BEFORE', 'SHE', 'SOME', 'LONG',
                    'WELL', 'TOTAL', 'HARD', 'JOIN', 'GLAD', 'JOIN', 'EVERYONE', 'TIME', 'PEOPLE', 'PLAN', 'CLEAR',
                    'STAND', 'REAL', 'DOWN', 'SURE', 'STOP', 'THANKS', 'CITY', 'LIVE', 'LOOKING', 'COME', 'NEXT',
                    'STATE', 'MORNING', 'COULD', 'YEAR', 'ITS', 'BEST', 'THOSE', 'WEEK', 'HOME', 'LOVE', 'WHERE',
                    'THINK', 'NIGHT', 'MAKE', 'BETTER', 'TALK', 'VOTE', 'YEARS', 'IMPORTANT', 'PROUD', 'FORWARD',
                    'ALSO', 'OFF', 'PART', 'ANOTHER', 'THEN', 'OFFICE', 'CENTER', 'TEAM', 'LEADERS', 'WORK', 'HELP',
                    'FUTURE', 'TONIGHT', 'CHANCE', 'PUBLIC', 'LOCAL', 'AROUND', 'LIFE', 'SAYS', 'THING', 'COMING',
                    'CONGRATULATIONS', 'WATCH', 'THROUGH', 'NEWS', 'FAMILY', 'THINGS', 'CITIES', 'RESIDENTS',
                    'SOMETHING', 'CAMPAIGN', 'NATIONAL', 'MEETING', 'HONOR', 'SIDE', 'SINCE', 'REALLY', 'HEAR',
                    'WELCOME', 'PARTY', 'LOT', 'EVENING', 'READY', 'MAKING', 'SAY', 'PLEASE', 'MEET', 'STORY', 'NEEDS',
                    'SERVICE', 'GREAT', 'COMMUNITY', 'SUPPORT', 'PRESIDENT', 'MAYOR', 'COUNTRY', 'HOPE', 'AMERICAN',
                    'AMERICA', 'AMERICANS', 'UNITED', 'PETE', 'SOUTH', 'BEND', 'STATES', 'SAID', 'FAR',
                    'HUNT', 'WORLD', 'STRONG', 'JOB', '“THE', 'LAW', 'UNDER', 'FACT', 'SOON', 'TODAY,', 'ALWAYS',
                    'OTHERS', 'COUNTRIES', 'USA', '', 'INCLUDING', 'LEFT', 'WHITE', 'OPEN', 'WONDERFUL', 'NORTH',
                    'CROOKED', 'SENATOR', 'FLORIDA', 'GIVE', 'ALREADY', 'WHILE', 'CRISIS', 'BOTH', 'ANYTHING',
                    'TOGETHER', 'RECORD', 'RIGHT', 'HISTORY', 'DEAL', 'DRUGS', 'NUMBERS', 'TRULY', 'TRYING', 'JOHN',
                    'HIGH', 'TRUE', 'TOTALLY', 'YORK', 'SAME', 'PUT', 'SUCH', 'COMPANIES', 'TREMENDOUS', 'CORRUPT',
                    'BECOME', 'SHOW', 'RADICAL', 'BUILT', 'INCREDIBLE', 'DESPITE', 'CONTINUE', 'NATION', 'LARGE',
                    'HAPPEN', 'GENERAL', 'HAPPY', 'LAWS', 'ALMOST', 'POLITICAL', 'BOOK', 'YESTERDAY', 'ANGRY', 'PLACE',
                    'MAY', 'CALLED', 'BETWEEN', 'PAID', 'MARKET', 'RUN', 'TOLD', 'TRULY', 'LOW', 'ECONOMIC', 'REMEMBER',
                    'MAJOR', 'HAVING', 'PATROL', 'DONALD', 'WON', 'CLOSE', 'PROTECT', 'BEAUTIFUL', 'FANTASTIC',
                    'JUSTICE', 'START', 'BRING', 'LITTLE', 'YET', 'BELIEVE', 'CALIFORNIA', 'DURING', 'GOVERNMENT',
                    'WITHOUT', 'PM', 'HIGHLY', 'LET', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ALONG',
                    'WRONG', 'JAMES', 'BUILD', 'FULL', 'COMPLETE', 'FAST', 'CALL', 'AGO', 'EVIDENCE', 'PAY', 'STEEL',
                    'UNTIL', 'ALLOWED', 'LEAVING', 'DOES', 'NEEDED', 'SPOKE', 'PRIME', 'MICHAEL', 'CASE', 'PROBLEM',
                    'ENDORSEMENT', 'GREATEST', 'TAKEN', 'LIVES', 'TAKING', 'BUSINESS', 'WOW', 'AMAZING', 'TERRIBLE',
                    'TOMORROW', 'ACT', 'MINISTER', 'MAN', 'WOMEN', 'FEDERAL', 'ELSE', 'SECRETARY', 'FORMER', 'FIX',
                    'MILLION', 'BILLION', 'NUMBER', 'BILLIONS', 'REASON', 'WORSE', 'AGREE', 'RIDICULOUS',
                    'PENNSYLVANIA', 'FAMILIES', 'GONE', 'READ', 'TOOK', 'BADLY', 'WANTS', 'USE', 'FINALLY','LEADERSHIP',
                    'BIGGEST', 'LOST', 'CARE', 'CHANGE', 'VOTES', 'SECOND', 'COMMITTEE', 'CONGRESSMAN', 'MASSIVE',
                    'QUICKLY']



    counter = collections.Counter()                                             # create Counter instance
    for i in range(len(stored_struct)):                                         # loop through storage struct
        tweet_text = stored_struct[i][2]                                        # collect tweet text
        word_list = tweet_text.split()                                          # split into words
        cap_word_list = [word.upper() for word in word_list]                    # words uppercase, capital letters: no skew
        valid_list = []                                                         # avoid .pop from the array being read from

        for x in range(len(cap_word_list)):                                     # test for excluded words
            word = cap_word_list[x]
            cap_word_list[x] = ''.join(c for c in word if c not in '#?:!/;.,()')   # strips specified characters from strs
            if (cap_word_list[x] not in exclude_list) and not ("’" in cap_word_list[x] ) \
                                                      and not ("@" in cap_word_list[x] ) \
                                                      and not ("'" in cap_word_list[x] ):  # to remove contractions/usernames
                valid_list.append(cap_word_list[x])
        counter.update(valid_list)                                              # update Counter instance

    most_common_word = [x[0] for x in counter.most_common(num_return)]
    return most_common_word



# sentiment calculation function
def sentiment(stored_struct):
    tweet_sentiments = []
    for i in range(len(stored_struct)):             # loop through storage struct
        tweet_text = stored_struct[i][2]            # collect tweet text
        blob = TextBlob(tweet_text)                 # TextBlob instance
        sentiment_tup = blob.sentiment[0], blob.sentiment[1]    # extracting values from Sentiment object tuples
        tweet_sentiments.append(sentiment_tup)      # append tuple to list

    print('tweet_sentiments[] size: ', end='')      # output size
    print(len(tweet_sentiments))

    # averaging sentiment/polarity scores
    sent_sum = 0
    polarity_sum = 0
    for _tuple in range(len(tweet_sentiments)):
        sent_sum += tweet_sentiments[_tuple][1]
        polarity_sum += tweet_sentiments[_tuple][0]
    sent_av = sent_sum / len(tweet_sentiments)
    polarity_av = polarity_sum / len(tweet_sentiments)

    print('polarity average (-1 to 1):  ', end='')
    print(polarity_av)
    print('sentiment average (0 to 1):  ', end='')
    print(sent_av)

    return tweet_sentiments



# word count generator
def word_counter(tweet_text, common_words_list, word_count_list):
    word_list = tweet_text.split()                          # split into words
    cap_word_list = [word.upper() for word in word_list]    # words uppercase, capital letters: no skew

    for x in range(len(cap_word_list)):                     # strip syntactical stuff
        word = cap_word_list[x]
        cap_word_list[x] = ''.join(c for c in word if c not in '?:!/;.')  # strips specified characters from strs

    for word in cap_word_list:
        if word in common_words_list:
            word_index = common_words_list.index(word)
            word_count_list[word_index] += 1  # increment word counter if specified word is in word list

    return word_count_list


# moving average function
def moving_average(word_date_matrix, output_matrix, subscript_value, num_words, num_days=7):
    averaged_date = [0 for t in range(num_words)]
    low_lim = 0
    upper_lim = 0


    if num_days != 1:
        low_lim = 0-int(num_days/2)
        upper_lim = int(num_days/2) + 1


        for g in range(low_lim, upper_lim):
            for h in range(num_words):              # for word, sum word-specific values over length of moving average
                averaged_date[h] += word_date_matrix[subscript_value + g][h]

        for i in range(num_words):                  # divide by length of moving average
            averaged_date[i] /= num_days
    else:
        for h in range(num_words):              # for word, sum word-specific values over length of moving average
            averaged_date[h] = word_date_matrix[subscript_value][h]

    output_matrix[subscript_value] = [averaged_date[x] for x in range(num_words)]   # list comp to avoid duplicates



def conv_to_daily(storage_struct, words, date_list):

    # fill date list with number of independent days in tweet storage
    for tweet in range(len(storage_struct)):
        if tweet == 0:                                  # avoids accessing [-1] (-1 is valid in python, but to be safe)
            date_list.append(storage_struct[tweet][1])   # append date of first tweet
            continue
        if storage_struct[tweet][1].day != storage_struct[tweet - 1][1].day:  # if date is different from tweet before...
            date_list.append(storage_struct[tweet])


    # zero the date/word structure to store date-specific word counts
    word_date_matrix = []
    for date in range(len(date_list)):
            word_date_matrix.append([0 for x in range(len(words))])     # 2D matrix of zeroed word_count lists for each date


    # loop through tweets and add to date-specific word counts.  Format below allows for multiple tweets per day
    prev = storage_struct[-1][1]                             # "start" date
    date_count = 0                                          # date subscript
    for count in range(len(storage_struct)):                 # loop through all tweets
        if storage_struct[-1 - count][1].day == prev.day:    # if same day,
            # loop through tweet contents. if word in words[], ++ word count.  Return/assign updated word count
            current_date_word_count = word_date_matrix[date_count]
            word_date_matrix[date_count] = word_counter(storage_struct[-1 - count][2],     # tweet_text
                                                        words,                            # common_word_list
                                                        current_date_word_count)          # date/word count

        else:                                               # different days (month/year irrelevant)
            prev = storage_struct[-1 - count][1]                                                 # record next "prev"
            date_count += 1                                                                     # count for next date
            current_date_word_count = word_date_matrix[date_count]                              # after date_count++
            word_date_matrix[date_count] = word_counter(storage_struct[-1 - count][2],     # tweet_text
                                                        words,                            # common_word_list
                                                        current_date_word_count)          # date/word count
    return word_date_matrix
