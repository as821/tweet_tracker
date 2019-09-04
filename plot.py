import matplotlib.pyplot as plot
import analytics

# plotting data
def plot_sentiment_graph(stored_struct):
    sent_calc_data = analytics.sentiment(stored_struct)

    polarity_only = [sent_calc_data[i][0] for i in range(len(sent_calc_data))]
    sentiment_only = [sent_calc_data[val][1] for val in range(len(sent_calc_data))]

    tweet_dates = [stored_struct[sub][1] for sub in range(len(stored_struct))]

    plot.scatter(tweet_dates, sentiment_only, color='r')
    plot.scatter(tweet_dates, polarity_only, color='g')

    plot.xlabel('Tweet Date')
    plot.ylabel('Sentiment Score')
    plot.show()


# plot progression of common word usage over time
def common_word_plot(stored_struct, user, mv_average_length):
    # want a line for each commonly used word plotted over time with a couple day moving average to show thoughts/focus

    # use lines similar to first ~30 in analytics.common words.
    # analyze tweets on daily basis and display as an average of the 7 days surrounding it (3 before, 3 after)
    # input results of 7-day moving average into list for output to graph (y axis)
    # y-axis: time in days

    words = analytics.common_words(stored_struct)       # collect common words
    date_list = []
    word_date_matrix = analytics.conv_to_daily(stored_struct, words, date_list)


    # moving average set up
    # zero output array
    output_matrix = []
    for date in range(len(date_list)):
        output_matrix.append([0 for x in range(len(words))])  # 2D matrix of zeroed word_count lists for each date

    # calculate moving average
    upper_lim = int(mv_average_length/2) + 1
    for val in range(len(word_date_matrix)):
        if val < mv_average_length | val + upper_lim >= len(word_date_matrix):
            output_matrix[val] = [0 for t in range(len(words))]
        else:    # not sufficient data...
            analytics.moving_average(word_date_matrix, output_matrix, val, len(words), mv_average_length)


    # moving average output
    num_days = len(output_matrix)
    for word_num in range(len(words)):  # loop through matrix and plot word values
        selected_word_list = [output_matrix[x][word_num] for x in range(num_days)]
        plot.plot(range(num_days), selected_word_list, label=words[word_num])




    # plot formatting
    plot_save_file = ''
    # title planning
    if user == 'realdonaldtrump':
        plot.title("Trump Common Word Usage (Twtter)")
        plot_save_file = '/Users/andrewstange/Desktop/PythonProjects/twitter_data/common_word_plots/trump_common_word_mvavg'
    elif user == 'ewarren':
        plot.title("Warren Common Word Usage (Twtter)")
        plot_save_file = '/Users/andrewstange/Desktop/PythonProjects/twitter_data/common_word_plots/warren_common_word_mvavg'
    elif user == 'PeteButtigieg':
        plot.title("Buttigieg Common Word Usage (Twtter)")
        plot_save_file = '/Users/andrewstange/Desktop/PythonProjects/twitter_data/common_word_plots/buttigieg_common_word_mvavg'


    plot.xlabel('Tweet Date')
    plot.ylabel('Word Count')
    plot.legend()
    fig = plot.gcf()
    plot.show()
    fig.savefig(plot_save_file, dpi=200)



def plot_set(x_set, y_set, label=''):
    plot.plot(x_set, y_set, label=label)

    plot.xlabel('Tweet Date')
    plot.ylabel('Word Count')
    plot.legend()
    fig = plot.gcf()    # not used, but here for future expansion of function
    plot.show()
