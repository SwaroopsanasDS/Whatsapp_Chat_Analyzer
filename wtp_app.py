import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import json
from streamlit_lottie import st_lottie

# Load Lottie animation from a local file
def load_lottie_local(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Page config
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Custom Styles
st.markdown("""
    <style>
        .stApp {
            background-color: #0f0f0f;
            color: #f5f5f5;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
        }
        .css-18e3th9 {
            padding-top: 1rem;
        }
        .stButton > button {
            background-color: #00bcd4;
            color: white;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #0194a2;
        }
    </style>
""", unsafe_allow_html=True)

plt.style.use("dark_background")

# Sidebar
st.sidebar.markdown(
    "<h2 style='color:#00bcd4; font-family:Segoe UI;'>WhatsApp Chat Analyzer</h2>",
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df["user"].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        # Load Lottie animations
        analysis_animation_path = "animations/analysis_loader.json"
        whatsapp_animation_path = "animations/loader.json"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st_lottie(load_lottie_local(analysis_animation_path), speed=1, width=200, height=200)
        with col2:
            st_lottie(load_lottie_local(whatsapp_animation_path), speed=1, width=200, height=200)

        # Top Statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.markdown("<h2 style='color:#ae81ff;'>Top Statistics</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        # Monthly Timeline
        st.markdown("<h2 style='color:#00bcd4;'>Monthly Timeline</h2>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color="cyan")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Daily Timeline
        st.markdown("<h2 style='color:#00bcd4;'>Daily Timeline</h2>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["message"], color="magenta")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Activity Map
        st.markdown("<h2 style='color:#00bcd4;'>Activity Map</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Most Busy Day**")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color="violet")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.markdown("**Most Busy Month**")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # Heatmap
        st.markdown("<h2 style='color:#00bcd4;'>Weekly Activity Heatmap</h2>", unsafe_allow_html=True)
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, cmap="mako", ax=ax)
        st.pyplot(fig)

        # Most Busy Users
        if selected_user == "Overall":
            st.markdown("<h2 style='color:#ae81ff;'>Most Busy Users</h2>", unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.markdown("<h2 style='color:#ae81ff;'>Word Cloud</h2>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        st.markdown("<h2 style='color:#ae81ff;'>Most Common Words</h2>", unsafe_allow_html=True)
        st.dataframe(most_common_df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color="skyblue")
        plt.xticks(rotation="horizontal")
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.markdown("<h2 style='color:#ae81ff;'>Emoji Analysis</h2>", unsafe_allow_html=True)
        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                plt.rcParams['font.family'] = 'Segoe UI Emoji'
                fig, ax = plt.subplots()
                ax.pie(emoji_df["count"].head(10), labels=emoji_df["emoji"].head(10), autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.write("No emojis found in the selected user/chat.")
