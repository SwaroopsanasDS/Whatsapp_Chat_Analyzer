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

# Set page config with light mode by default
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Custom styles for light mode
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #333333;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            color: #2C3E50;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            background-color: #00bcd4;
            color: white;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #0194a2;
        }
        .stMetric {
            background-color: #f1f1f1;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            color: #00bcd4;
        }
        .st-lottie {
            background: transparent;
        }
    </style>
""", unsafe_allow_html=True)

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
        
        # Two columns for top animations
        col1, col2 = st.columns([3, 1])
        with col1:
            st_lottie(load_lottie_local(analysis_animation_path), speed=1, width=200, height=200)
        with col2:
            st_lottie(load_lottie_local(whatsapp_animation_path), speed=1, width=200, height=200)

        # Top Stats
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.markdown("<h2 style='color:#ae81ff;'>Top Statistics</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        # Monthly Timeline
        st.markdown("<h2 style='color:#00bcd4;'>Monthly Timeline</h2>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timeline["time"], timeline["message"], color="#00bcd4", linewidth=2, alpha=0.8)
        ax.set_facecolor("white")

        # Remove all spines and ticks
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12, length=0)
        plt.xticks(rotation="vertical")

        # Set transparent background for the figure and remove any borders
        fig.patch.set_facecolor('none')  # Makes the figure background transparent
        st.pyplot(fig)

        # Daily Timeline
        st.markdown("<h2 style='color:#00bcd4;'>Daily Timeline</h2>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_timeline["only_date"], daily_timeline["message"], color="#ae81ff", linewidth=2, alpha=0.8)
        ax.set_facecolor("white")

        # Remove all spines and ticks
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12, length=0)
        plt.xticks(rotation="vertical")

        # Set transparent background for the figure and remove any borders
        fig.patch.set_facecolor('none')  # Makes the figure background transparent
        st.pyplot(fig)

        # Activity Map
        st.markdown("<h2 style='color:#00bcd4;'>Activity Map</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Most Busy Day**")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(busy_day.index, busy_day.values, color="#f39c12", edgecolor="none", alpha=0.7)
            ax.set_facecolor("white")

            # Remove all spines and ticks
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.tick_params(axis='both', which='major', labelsize=12, length=0)
            plt.xticks(rotation="vertical")
            fig.patch.set_facecolor('none')
            st.pyplot(fig)
        with col2:
            st.markdown("**Most Busy Month**")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(busy_month.index, busy_month.values, color="#9b59b6", edgecolor="none", alpha=0.7)
            ax.set_facecolor("white")

            # Remove all spines and ticks
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.tick_params(axis='both', which='major', labelsize=12, length=0)
            plt.xticks(rotation="vertical")
            fig.patch.set_facecolor('none')
            st.pyplot(fig)

        # Weekly Activity Heatmap
        st.markdown("<h2 style='color:#00bcd4;'>Weekly Activity Heatmap</h2>", unsafe_allow_html=True)
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(user_heatmap, cmap="coolwarm", ax=ax, cbar_kws={'label': 'Activity Level'}, linewidths=0, linecolor='none')
        ax.set_facecolor("white")

        # Remove all spines and ticks
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12, length=0)
        fig.patch.set_facecolor('none')
        st.pyplot(fig)

        # Busiest Users
        if selected_user == "Overall":
            st.markdown("<h2 style='color:#ae81ff;'>Most Busy Users</h2>", unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(x.index, x.values, color="#3498db", edgecolor="none", alpha=0.7)
                ax.set_facecolor("white")

                # Remove all spines and ticks
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.tick_params(axis='both', which='major', labelsize=12, length=0)
                plt.xticks(rotation="vertical")
                fig.patch.set_facecolor('none')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.markdown("<h2 style='color:#ae81ff;'>Word Cloud</h2>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        ax.set_facecolor("white")

        # Remove all spines and ticks
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12, length=0)
        fig.patch.set_facecolor('none')
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        st.markdown("<h2 style='color:#ae81ff;'>Most Common Words</h2>", unsafe_allow_html=True)

        st.dataframe(most_common_df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(most_common_df[0], most_common_df[1], color="#1abc9c", alpha=0.8)
        ax.set_facecolor("white")

        # Remove all spines and ticks
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12, length=0)
        plt.xticks(rotation="horizontal")
        fig.patch.set_facecolor('none')
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
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.pie(emoji_df["count"].head(10), labels=emoji_df["emoji"].head(10), autopct="%0.2f", startangle=140)
                ax.set_facecolor("white")

                # Remove all spines and ticks
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.tick_params(axis='both', which='major', labelsize=12, length=0)
                fig.patch.set_facecolor('none')
                st.pyplot(fig)
        else:
            st.write("No emojis found in the selected user/chat.")
