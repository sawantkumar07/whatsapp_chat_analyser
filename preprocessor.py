

def preprocess(data):

    # Regular expression for WhatsApp exported chat
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[AaPp][Mm]\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # Convert string date to datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%Y, %I:%M %p - '
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    # Separate user and message
    for message in df['user_message']:

        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) >= 3:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    # Remove extra column
    df.drop(columns=['user_message'], inplace=True)

    # ----------------------------
    # Date Features
    # ----------------------------

    df['only_date'] = df['date'].dt.date

    df['year'] = df['date'].dt.year

    df['month_num'] = df['date'].dt.month

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day

    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    # ----------------------------
    # Create Time Period
    # Example:
    # 00-01
    # 01-02
    # ...
    # 23-00
    # ----------------------------

    period = []

    for hour in df[['day_name', 'hour']]['hour']:

        if hour == 23:
            period.append("23-00")

        elif hour == 0:
            period.append("00-01")

        else:
            period.append(f"{hour:02d}-{hour+1:02d}")

    df['period'] = period

    return df
