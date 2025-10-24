# Netflix Data Analysis Dashboard (Centered Welcome + Cinematic UI)
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud


st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_style("whitegrid")


st.markdown("""
<style>
/* App background and font */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #0d0d0d, #000000, #1a0000);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(15, 15, 15, 0.95);
    backdrop-filter: blur(10px);
    border-right: 2px solid #E50914;
    box-shadow: 2px 0 15px rgba(229, 9, 20, 0.3);
}
[data-testid="stSidebar"] * {
    color: #fff !important;
    font-weight: 500;
}

/* Welcome Screen Center Fix */
#welcome-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: 100%;
}

/* Titles */
.main-title {
    font-size: 50px;
    font-weight: 900;
    color: #E50914;
    text-shadow: 0 0 25px rgba(229, 9, 20, 0.8);
    margin-bottom: 15px;
}
.sub-title {
    color: #ccc;
    font-size: 20px;
    margin-bottom: 40px;
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(145deg, #E50914, #b0060f);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 14px 50px;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.6);
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 40px rgba(229, 9, 20, 0.9);
}

/* Fade-in Animation */
.fade-in {
    animation: fadeIn 2s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Animated KPI Cards */
@keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(229, 9, 20, 0.3); }
    50% { box-shadow: 0 0 30px rgba(229, 9, 20, 0.8); }
    100% { box-shadow: 0 0 10px rgba(229, 9, 20, 0.3); }
}
.metric-box {
    background: linear-gradient(145deg, #141414, #0a0a0a);
    border: 1px solid rgba(229, 9, 20, 0.4);
    border-radius: 15px;
    color: white;
    padding: 18px;
    text-align: center;
    animation: pulseGlow 2.5s infinite ease-in-out;
    transition: all 0.3s ease;
}
.metric-box:hover {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(229, 9, 20, 0.9);
}

[data-testid="stTabs"] {
    background: rgba(18, 18, 18, 0.6);
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.3);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


if "start_analysis" not in st.session_state:
    st.session_state.start_analysis = False

if not st.session_state.start_analysis:
    st.markdown(
        """
        <div id="welcome-container" class="fade-in">
            <p class="main-title">🍿 Welcome to Netflix Data Analysis</p>
            <p class="sub-title">“Ready to explore the secrets behind Netflix’s global success?”</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered Button Below Text
    placeholder = st.empty()
    with placeholder.container():
        center_col = st.columns([4, 2, 4])[1]  # Centers button perfectly
        with center_col:
            if st.button("🎬 Start Exploring"):
                st.session_state.start_analysis = True
                st.rerun()
    st.stop()


data_path = "data/netflix1.csv"
if not os.path.exists(data_path):
    st.error("❌ Dataset not found in the data folder!")
    st.stop()

data = pd.read_csv(data_path)
data.drop_duplicates(inplace=True)

columns_to_check = [col for col in ['director', 'cast', 'country'] if col in data.columns]
if columns_to_check:
    data.dropna(subset=columns_to_check, inplace=True)

if 'date_added' in data.columns:
    data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')
    data['year_added'] = data['date_added'].dt.year
else:
    data['year_added'] = None

for col in ['rating', 'duration', 'listed_in']:
    if col in data.columns:
        data[col].fillna('Unknown', inplace=True)


st.sidebar.header("🎛️ Filter Netflix Data")

type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=sorted(data['type'].dropna().unique()),
    default=list(data['type'].dropna().unique())
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=sorted(data['country'].dropna().unique()),
    default=["United States", "India"]
)

if 'listed_in' in data.columns:
    all_genres = set(sum([g.split(', ') for g in data['listed_in'].dropna()], []))
    genre_filter = st.sidebar.multiselect(
        "Select Genre(s)",
        options=sorted(all_genres),
        default=[]
    )
else:
    genre_filter = []

if data['year_added'].notnull().any():
    min_year, max_year = int(data['year_added'].min()), int(data['year_added'].max())
    year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
else:
    year_range = (0, 9999)

filtered_data = data.copy()
filtered_data = filtered_data[
    (filtered_data['type'].isin(type_filter)) &
    (filtered_data['country'].isin(country_filter)) &
    (filtered_data['year_added'] >= year_range[0]) &
    (filtered_data['year_added'] <= year_range[1])
]

if genre_filter and 'listed_in' in filtered_data.columns:
    filtered_data = filtered_data[filtered_data['listed_in'].apply(
        lambda x: any(genre in x for genre in genre_filter)
    )]

st.sidebar.success(f"✅ Showing {len(filtered_data)} records after filtering")


st.markdown("### 📊 Key Insights")


col1, col2, col3, col4 = st.columns(4, gap="medium")


total_titles = len(filtered_data)
total_movies = len(filtered_data[filtered_data["type"] == "Movie"]) if "type" in filtered_data else 0
total_shows = len(filtered_data[filtered_data["type"] == "TV Show"]) if "type" in filtered_data else 0
unique_countries = filtered_data["country"].nunique() if "country" in filtered_data else 0


metric_html = """
<div style="
    background: linear-gradient(145deg, #141414, #0a0a0a);
    border: 1px solid rgba(229, 9, 20, 0.4);
    border-radius: 15px;
    color: white;
    padding: 20px;
    text-align: center;
    width: 100%;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.3);
    animation: pulseGlow 3s infinite ease-in-out;
    transition: all 0.3s ease;
">
    <h3 style="margin-bottom: 10px; font-size: 20px;">{title}</h3>
    <h2 style="font-size: 36px; margin: 0;">{value}</h2>
</div>
"""

with col1:
    st.markdown(metric_html.format(title="Total Titles", value=total_titles), unsafe_allow_html=True)
with col2:
    st.markdown(metric_html.format(title="Total Movies", value=total_movies), unsafe_allow_html=True)
with col3:
    st.markdown(metric_html.format(title="TV Shows", value=total_shows), unsafe_allow_html=True)
with col4:
    st.markdown(metric_html.format(title="Countries", value=unique_countries), unsafe_allow_html=True)


st.markdown("---")
st.markdown("### 🎥 Dataset Preview")
st.dataframe(filtered_data.head(10))


st.markdown("---")
st.markdown("### 📈 Explore Netflix Insights")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎞️ Content Type Distribution",
    "🌍 Top 10 Countries",
    "📆 Yearly Additions",
    "⭐ Rating Distribution",
    "☁️ Word Cloud",
    "🎭 Genre Insights"
])

with tab1:
    st.subheader("Movies vs TV Shows")
    if "type" in filtered_data:
        fig, ax = plt.subplots()
        sns.countplot(x="type", data=filtered_data, palette="Reds", ax=ax)
        plt.title("Distribution of Content Type")
        st.pyplot(fig)

with tab2:
    st.subheader("Top 10 Countries by Netflix Content")
    if "country" in filtered_data:
        top_countries = filtered_data["country"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index, palette="Reds_r", ax=ax)
        plt.title("Top 10 Countries")
        st.pyplot(fig)

with tab3:
    st.subheader("Netflix Content Added Over the Years")
    if "year_added" in filtered_data:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x="year_added", data=filtered_data, palette="rocket", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Yearly Content Additions")
        st.pyplot(fig)

with tab4:
    st.subheader("Ratings Breakdown")
    if "rating" in filtered_data:
        rating_counts = filtered_data["rating"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=rating_counts.values, y=rating_counts.index, palette="magma", ax=ax)
        plt.title("Top 10 Ratings")
        st.pyplot(fig)

with tab5:
    st.subheader("Word Cloud of Netflix Titles")
    if "title" in filtered_data:
        titles = " ".join(filtered_data["title"])
        wc = WordCloud(width=1000, height=500, background_color="black", colormap="Reds").generate(titles)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

with tab6:
    st.subheader("Genre Insights")
    if "listed_in" in filtered_data:
        genre_series = filtered_data["listed_in"].str.split(", ").explode().value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=genre_series.values, y=genre_series.index, palette="flare", ax=ax)
        plt.title("Top 10 Most Common Genres")
        st.pyplot(fig)


st.markdown("---")
st.markdown("### 💾 Download Filtered Dataset")
csv = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Data", csv, "filtered_netflix_data.csv", "text/csv")

st.markdown("<br><center>✨ Built with ❤️ by Nanda S.C✨</center>", unsafe_allow_html=True)
