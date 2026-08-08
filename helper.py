
# --------------------------------------------------------
# URL Extractor Object
# --------------------------------------------------------
from urlextract import URLExtract
extract = URLExtract()


# --------------------------------------------------------
# Total Messages, Words, Media and Links
# --------------------------------------------------------
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total Messages
    num_messages = df.shape[0]

    # Total Words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Total Media
    num_media_message = df[df['message'].str.contains("<Media omitted>", na=False)].shape[0]

    # Total Links
    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_links = len(links)

    return num_messages, len(words), num_media_message, num_links


# --------------------------------------------------------
# Most Busy Users
# --------------------------------------------------------
def most_busy_users(df):

    x = df['user'].value_counts().head()

    percent = (
        round((df['user'].value_counts() / df.shape[0]) * 100, 2)
        .reset_index()
    )

    percent.columns = ['Name', 'Percent']

    return x, percent


# --------------------------------------------------------
# Word Cloud
# --------------------------------------------------------
def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    temp = temp[
        ~temp['message'].str.contains("<Media omitted>", na=False)
    ]

    # Read stop words
    stop_words = set()

    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        for word in f.readlines():
            stop_words.add(word.strip())

    cleaned_messages = []

    for message in temp['message']:

        current_words = []

        for word in message.lower().split():

            if word not in stop_words:

                current_words.append(word)

        cleaned_messages.append(" ".join(current_words))

    wc = WordCloud(
        width=500,
        height=500,
        background_color="white",
        min_font_size=10
    )

    df_wc = wc.generate(" ".join(cleaned_messages))

    return df_wc


# --------------------------------------------------------
# Top 25 Most Common Words
# --------------------------------------------------------
def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    temp = temp[
        ~temp['message'].str.contains("<Media omitted>", na=False)
    ]

    stop_words = set()

    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        for word in f.readlines():
            stop_words.add(word.strip())

    words = []

    for message in temp['message']:

        for word in message.lower().split():

            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(25)
    )

    return most_common_df

# --------------------------------------------------------
# Monthly Timeline
# --------------------------------------------------------
def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    timeline.sort_values(['year', 'month_num'], inplace=True)

    time = []

    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


# --------------------------------------------------------
# Daily Timeline
# --------------------------------------------------------
def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily = df.groupby('only_date').count()['message'].reset_index()

    return daily


# --------------------------------------------------------
# Most Busy Month
# --------------------------------------------------------
def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# --------------------------------------------------------
# Most Busy Day
# --------------------------------------------------------
def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


# --------------------------------------------------------
# Hourly Activity Heatmap
# --------------------------------------------------------
def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    heatmap = heatmap.reindex(day_order)

    return heatmap
