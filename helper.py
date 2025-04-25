from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    
    if selected_user != "Overall":
        df =  df[df["user"] == selected_user]
        
    num_messages = df.shape[0]
    

    words = []
    for message in df["message"]:
        words.extend(message.split())
        
    #fetch number of media messages
    num_media_messages = df[df["message"].str.contains("omitted", case=False, na=False)].shape[0]

    # Count links
    url_pattern = r"(https?://\www\.\S+)"
    num_links = df["message"].str.contains(url_pattern, na=False).sum()
    
    return num_messages, len(words), num_media_messages, num_links
    
   
def most_busy_users(df):
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={"index": "name", "user": "percent"})
    return x, df


def create_wordcloud(selected_user, df):
    
    with open("stopwords.txt", encoding='utf-8') as f:
        stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
         
    system_keywords = [
        "created group",
        "added",
        "left",
        "removed",
        "changed the subject",
        "changed this group",
        "changed their phone number"
    ]

    pattern = '|'.join(system_keywords)
    temp = df[~df["message"].str.contains("omitted|" + pattern, case=False, na=False)]
     
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    temp["message"] = temp["message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc





def most_common_words(selected_user, df):
    
    # Load stop words
    with open("stopwords.txt", encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    # Filter by user
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # Remove system-generated messages
    system_keywords = [
        "created group", "added", "left", "removed",
        "changed the subject", "changed this group", "changed their phone number"
    ]
    pattern = '|'.join(system_keywords)
    temp = df[~df["message"].str.contains("omitted|" + pattern, case=False, na=False)]

    # Extract words excluding stopwords
    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Get top 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    
    # Filter by user
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        
    # Set column names explicitly
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=["emoji", "count"])
    
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))
        
    timeline["time"] = time
        
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    df["only_date"] = pd.to_datetime(df["date"]).dt.date
        
    daily_timeline = df.groupby("only_date").count()["message"].reset_index()
    
    return daily_timeline
    
    
def week_activity_map(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    return df["day_name"].value_counts()

def month_activity_map(selected_user, df):
    

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    return df["month"].value_counts()

def activity_heatmap(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


    
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    activity_heatmap = df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    