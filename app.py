
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import helper
import preprocessor
# Page Configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS
st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

div[data-testid="stMetric"]{
    background-color:#262730;
    border-radius:12px;
    padding:15px;
    border:1px solid #444;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Title
# ==========================================================

st.markdown(
    "<h1 style='text-align:center;'>📱 WhatsApp Chat Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("⚙ Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload WhatsApp Chat",
    type=["txt"]
)

# ==========================================================
# Read Chat
# ==========================================================

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # --------------------------------------------
    # User List
    # --------------------------------------------

    user_list = df['user'].unique().tolist()

    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()

    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "👤 Select User",
        user_list
    )

    show = st.sidebar.button(
        "🚀 Analyze Chat",
        use_container_width=True
    )


    # Show Dashboard


    if show:

        (
            num_messages,
            words,
            media,
            links
        ) = helper.fetch_stats(
            selected_user,
            df
        )

        # ========================================
        # Dashboard Heading
        # ========================================

        st.markdown(
            "## 📊 Dashboard Overview"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "💬 Messages",
                f"{num_messages:,}"
            )

        with col2:

            st.metric(
                "📝 Words",
                f"{words:,}"
            )

        with col3:

            st.metric(
                "🖼 Media",
                f"{media:,}"
            )

        with col4:

            st.metric(
                "🔗 Links",
                f"{links:,}"
            )

        st.markdown("---")

        # Most Busy Users & Word Cloud


        col1, col2 = st.columns([1, 1])


        # Most Busy Users


        with col1:

            st.markdown("## 👥 Most Busy Users")

            if selected_user == "Overall":

                x, busy_df = helper.most_busy_users(df)

                fig, ax = plt.subplots(figsize=(7, 5))

                bars = ax.bar(
                    x.index,
                    x.values,
                    color="#4F8BF9"
                )

                ax.set_xlabel("Users", fontsize=11)

                ax.set_ylabel("Messages", fontsize=11)

                ax.set_title("Most Active Members")

                plt.xticks(rotation=35)

                for bar in bars:

                    height = bar.get_height()

                    ax.text(
                        bar.get_x() + bar.get_width()/2,
                        height,
                        int(height),
                        ha='center',
                        va='bottom',
                        fontsize=10
                    )

                st.pyplot(fig, use_container_width=True)

                st.markdown("### 📋 Contribution (%)")

                st.dataframe(
                    busy_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "Busy User Analysis is available only for Overall Chat."
                )

        # -----------------------------------------------------
        # Word Cloud
        # -----------------------------------------------------

        with col2:

            st.markdown("## ☁️ Word Cloud")

            wc = helper.create_wordcloud(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(7,7))

            ax.imshow(wc)

            ax.axis("off")

            st.pyplot(
                fig,
                use_container_width=True
            )

        st.markdown("---")

        # =====================================================
        # Top 25 Most Common Words
        # =====================================================

        st.markdown("## 📖 Top 25 Most Common Words")

        common_df = helper.most_common_words(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(11,7))

        ax.barh(
            common_df[0],
            common_df[1],
            color="#00A896"
        )

        ax.invert_yaxis()

        ax.set_xlabel("Frequency")

        ax.set_ylabel("Words")

        ax.set_title("Top 25 Most Used Words")

        st.pyplot(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        # =====================================================
        # Chat Timeline
        # =====================================================

        st.markdown("## 📈 Chat Timeline")

        col1, col2 = st.columns(2)

        # ---------------- Monthly Timeline -------------------

        with col1:

            st.subheader("📅 Monthly Timeline")

            timeline = helper.monthly_timeline(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(8,5))

            ax.plot(
                timeline['time'],
                timeline['message'],
                marker='o',
                linewidth=3,
                color="#4F8BF9"
            )

            plt.xticks(rotation=45)

            ax.set_xlabel("Month")

            ax.set_ylabel("Messages")

            ax.grid(alpha=0.3)

            st.pyplot(
                fig,
                use_container_width=True
            )

        # ---------------- Daily Timeline ---------------------

        with col2:

            st.subheader("📆 Daily Timeline")

            daily = helper.daily_timeline(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(8,5))

            ax.plot(
                daily['only_date'],
                daily['message'],
                color="#00A896",
                linewidth=2
            )

            ax.set_xlabel("Date")

            ax.set_ylabel("Messages")

            ax.grid(alpha=0.3)

            st.pyplot(
                fig,
                use_container_width=True
            )

        st.markdown("---")

        # =====================================================
        # Activity Map
        # =====================================================

        st.markdown("## 📊 Activity Map")

        col1, col2 = st.columns(2)

        # ---------------- Busy Month --------------------------

        with col1:

            st.subheader("📅 Most Busy Month")

            month = helper.month_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(8,5))

            bars = ax.bar(
                month.index,
                month.values,
                color="#FF9F1C"
            )

            plt.xticks(rotation=35)

            ax.set_ylabel("Messages")

            for bar in bars:

                y = bar.get_height()

                ax.text(
                    bar.get_x()+bar.get_width()/2,
                    y,
                    int(y),
                    ha='center'
                )

            st.pyplot(
                fig,
                use_container_width=True
            )

        # ---------------- Busy Day --------------------------

        with col2:

            st.subheader("📅 Most Busy Day")

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(8,5))

            bars = ax.bar(
                busy_day.index,
                busy_day.values,
                color="#8E44AD"
            )

            plt.xticks(rotation=35)

            ax.set_ylabel("Messages")

            for bar in bars:

                y = bar.get_height()

                ax.text(
                    bar.get_x()+bar.get_width()/2,
                    y,
                    int(y),
                    ha='center'
                )

            st.pyplot(
                fig,
                use_container_width=True
            )

        st.markdown("---")

        # =====================================================
        # Heat Map
        # =====================================================

        st.markdown("## 🔥 Weekly Activity Heatmap")

        heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(16,6))

        sns.heatmap(
            heatmap,
            cmap="YlGnBu",
            linewidths=.5,
            annot=True,
            fmt=".0f",
            ax=ax
        )

        ax.set_xlabel("Time Interval")

        ax.set_ylabel("Day")

        st.pyplot(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        st.success("✅ Analysis Completed Successfully!")