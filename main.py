# imports
import read
import collect
import plot as plt
import matplotlib.pyplot as plot
import analytics


# candidate selection.  Set to True to access this user
read_file = ''
user = ''
if(False):
    user = 'realdonaldtrump'
    read_file = 'your_path_and_filename_here'
elif(True):
    user = 'ewarren'
    read_file = 'your_path_and_filename_here'
elif(False):
    user = 'PeteButtigieg'
    read_file = 'your_path_and_filename_here'

try:
    # user menu
    selection = str(input('Input option:\n'
                        '     (c: collect)\n'
                        '     (con: continue_loading)\n'
                        '     (r: output stored dates\n'
                        '     (p: plot)\n'
                        '     (com: common words)\n'
                        '     (u: update)\n'
                        '     (w: select common word to plot)\n'
                        '>>> '))

    if selection == 'c':        # collect tweets.  For loading most recent tweets into set file
        collect.collect(read_file, user, int(input('Input number of tweets to collect:   ')))

    elif selection == 'con':    # continue loading tweets for a selected user (from the oldest tweet stored on)
        lastID = int(read.read(read_file)[-1][0])
        num_collect = str(input('Default collect num? Default runs to rate limit (y/n): '))
        if num_collect == 'y':                                                  # input parsing
            collect.continue_loading(lastID, read_file, user)
        elif num_collect == 'n':
            collect.continue_loading(lastID, read_file, user, int(input('Num tweets to collect: ')))
        else:
            print('Invalid input.  Rerun and try again...')

    elif selection == 'p':      # plots the 10 most commonly used words for specified user. Option to change the moving average size
        avg_len = 7
        stored_struct = read.read(read_file)                                    # get data struct from storage file
        print('Num tweets stored: ', len(stored_struct))
        if input("\nCustom moving average length?(y/n)") == 'y':
            avg_len = int(input('Input moving average length (1-9 odd): \n'))   # get moving average size
        plt.common_word_plot(stored_struct, user, avg_len)                      # function to plot 10 most common words

    elif selection == 'r':      # outputs the date of every tweet stored for specified user
        stored_struct = read.read(read_file)                                    # get data struct from storage file
        for i in range(len(stored_struct)):                                     # print all stored tweet dates
            print(stored_struct[i][1])
        print('\nNumber of tweets stored: ', len(stored_struct))                # output number of tweets stored

    elif selection == 'com':    # outputs the 50 most commonly used words for the specified user
        stored_struct = read.read(read_file)                                    # get data struct from storage file
        word_list = analytics.common_words(stored_struct, 100)                   # get most common words
        print('\n')
        for i in word_list:                                                     # output common words
            print(i)

    elif selection == 'u':      # checks for and stores any tweets newer than the most recent stored one
        most_recent_ID = int(read.read(read_file)[0][0])                        # get ID of most recent tweet
        collect.update(most_recent_ID, read_file, user)                         # update with more recent tweets

    elif selection == 'w':      # select any number of 50 most commonly used words and plot them together (raw data)
        # load struct and initialize
        stored_struct = read.read(read_file)                                    # get data struct from storage file
        common_list = analytics.common_words(stored_struct, 50)                 # get most common words
        date_list = []
        words_selection_list = []

        # common word selection
        print("\nMost common words in tweets by", user, ':\n')                  # output common word selection options
        for i in range(len(common_list)):
            print(i + 1, ' ', common_list[i])                                   # i + 1. Python subscripts start at 0

        # input list parsing
        inp = int(input("\nInput corresponding number to select a word (separate multiplte entries with ','):\n\n"))
        input_list = inp.split(",")                                             # parse input into list
        input_list = list(map(int, input_list))     # cast list to int
        for val in input_list:
            val -= 1                                # make up for earlier selection number adjustment


        for in_put in input_list:
            words_selection_list.append(common_list[in_put])

        # output
        word_data_matrix = analytics.conv_to_daily(stored_struct, words_selection_list, date_list)

        for word_num in range(len(input_list)):
            output_list = [int(word_data_matrix[x][word_num]) for x in range(len(word_data_matrix))]
            label = common_list[input_list[word_num]]
            plot.plot(range(len(date_list)), output_list, label=label)

        plot.xlabel('Tweet Date')
        plot.ylabel('Word Count')
        plot.legend()
        plot.show()


    else:
        print('Invalid input... rerun program and try again')
except(TypeError):
    print('Invalid type input. Program ending...')
except Exception:
    print('unknown error.  Ending now...')



