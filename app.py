import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------
st.set_page_config(
    page_title="CineScope | IMDb Movie Explorer",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM DESIGN
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #111a2e 55%, #15152b 100%);
    color: #f4f6fb;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #f7f8fc;
}
.hero {
    padding: 34px 38px;
    border-radius: 22px;
    background: linear-gradient(115deg, #252e52, #49316c 58%, #873f67);
    border: 1px solid rgba(255,255,255,.12);
    margin-bottom: 24px;
}
.hero-kicker {
    color: #d8d5ff;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(30px, 4vw, 48px);
    line-height: 1.12;
    font-weight: 800;
    margin: 10px 0;
    color: white;
}
.hero-copy {
    color: #e2e4f3;
    font-size: 15px;
    max-width: 700px;
}
.section-label {
    color: #aeb8d8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.12);
    padding: 18px 20px;
    border-radius: 17px;
}
div[data-testid="stMetricLabel"] {
    color: #bfc8e2;
}
div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-family: 'Manrope', sans-serif;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,.05);
    padding: 7px;
    border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #d8def0;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: #7656d8 !important;
    color: white !important;
}
.stButton > button, .stFormSubmitButton > button {
    border: 0;
    border-radius: 10px;
    background: linear-gradient(100deg, #7656d8, #a45cc5);
    color: white;
    font-weight: 700;
    padding: 10px 18px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    border: 0;
    color: white;
    filter: brightness(1.12);
}
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 12px;
    overflow: hidden;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 12px;
}
[data-testid="stSidebar"] {
    background: #10182a;
}
.small-note {
    color: #aab4ce;
    font-size: 13px;
}
.footer {
    color: #929db8;
    text-align: center;
    font-size: 12px;
    padding: 28px 0 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("ToP 250 movies on imdb in 2026.csv")

    def to_list(value):
        if isinstance(value, list):
            return value
        if pd.isna(value):
            return []
        try:
            result = ast.literal_eval(value)
            return result if isinstance(result, list) else [result]
        except (ValueError, SyntaxError):
            return [str(value)]

    for column in ["genres", "countriesOfOrigin"]:
        if column in data.columns:
            data[column] = data[column].apply(to_list)

    for column in ["averageRating", "numVotes", "grossWorldwide"]:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    return data

try:
    df = load_data()
except FileNotFoundError:
    st.error("I couldn't find the CSV file. Keep the dataset in the same folder as app.py.")
    st.stop()

required_columns = [
    "primaryTitle", "genres", "countriesOfOrigin",
    "averageRating", "numVotes", "grossWorldwide"
]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    st.error("The dataset is missing these required columns: " + ", ".join(missing_columns))
    st.stop()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Your personal movie discovery space</div>
    <div class="hero-title">CineScope <span style="color:#e6b9ff;">✦</span></div>
    <div class="hero-copy">
        Explore the IMDb Top 250, compare ratings, discover genres and find
        your next great movie — all in one place.
    </div>
</div>
""", unsafe_allow_html=True)

st.success("The movie collection is ready. Choose a section below and start exploring.")

# -------------------------------------------------
# Q1 - DATASET EXPLORATION
# -------------------------------------------------
with st.expander("📁 Dataset overview — loading and preparation", expanded=False):
    st.markdown('<div class="section-label">A quick look at the data</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)
    a, b = st.columns(2)
    a.metric("Rows", f"{df.shape[0]:,}")
    b.metric("Columns", f"{df.shape[1]:,}")
    st.write("**Column names**")
    st.write(", ".join(df.columns))
    st.write("**Column data types**")
    st.dataframe(df.dtypes.astype(str).rename("Data type"), use_container_width=True)
    st.write("**Missing values in each column**")
    st.dataframe(df.isna().sum().rename("Missing values"), use_container_width=True)

st.markdown('<div class="section-label">At a glance</div>', unsafe_allow_html=True)
st.header("The numbers behind the movies")

# Q2 - KPI METRICS
k1, k2, k3, k4 = st.columns(4)
k1.metric("Movies in the list", f"{len(df):,}")
k2.metric("Average IMDb rating", f"{df['averageRating'].mean():.2f}/10")
k3.metric("Highest rating", f"{df['averageRating'].max():.1f}/10")
k4.metric("Total votes", f"{df['numVotes'].fillna(0).sum():,.0f}")

st.divider()

# -------------------------------------------------
# Q3 - VISUAL ANALYTICS
# -------------------------------------------------
st.markdown('<div class="section-label">Explore the collection</div>', unsafe_allow_html=True)
st.header("Movie analytics")

genre_tab, rating_tab, votes_tab, gross_tab = st.tabs([
    "🎭 Genres", "⭐ Ratings", "💬 Votes", "💰 Box office"
])

with genre_tab:
    genre_data = df.explode("genres")
    genre_counts = genre_data["genres"].dropna().value_counts()
    st.subheader("Which genres show up most?")
    st.caption("A movie can belong to more than one genre, so each genre is counted separately.")
    st.bar_chart(genre_counts, color="#9b83f5", use_container_width=True)

with rating_tab:
    st.subheader("How are movie ratings distributed?")
    ratings = df["averageRating"].dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#17213a")
    ax.set_facecolor("#17213a")
    ax.hist(ratings, bins=10, color="#a78bfa", edgecolor="#17213a")
    ax.set_xlabel("IMDb rating", color="white")
    ax.set_ylabel("Number of movies", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#64708e")
    ax.grid(axis="y", alpha=.18)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with votes_tab:
    st.subheader("Ratings compared with audience votes")
    st.caption("Each dot represents one movie.")
    st.scatter_chart(
        df.dropna(subset=["averageRating", "numVotes"]),
        x="averageRating",
        y="numVotes",
        color="#c084fc",
        use_container_width=True
    )

with gross_tab:
    st.subheader("Top 10 movies by worldwide gross")
    gross_data = df.dropna(subset=["grossWorldwide"]).nlargest(10, "grossWorldwide")
    if not gross_data.empty:
        st.bar_chart(
            gross_data.set_index("primaryTitle")["grossWorldwide"],
            color="#c084fc",
            use_container_width=True
        )
        st.dataframe(
            gross_data[["primaryTitle", "grossWorldwide", "averageRating"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Worldwide gross information is not available in this dataset.")

st.divider()

# -------------------------------------------------
# Q4 - EXTRA DATASET INFORMATION
# -------------------------------------------------
with st.expander("ℹ️ About this dashboard"):
    st.write(
        "This dashboard uses the supplied IMDb Top 250 Movies dataset. "
        "It includes movie titles, genres, countries of origin, ratings, "
        "vote counts and worldwide gross collections."
    )
    st.write(f"Currently loaded: **{len(df)} movie records** across **{len(df.columns)} columns**.")

# -------------------------------------------------
# Q5 - INTERACTIVE MOVIE EXPLORER
# -------------------------------------------------
st.markdown('<div class="section-label">Find something to watch</div>', unsafe_allow_html=True)
st.header("Movie explorer")
st.write("Narrow down the list using the filters. You can combine them to find a closer match.")

all_genres = sorted({g for values in df["genres"] for g in values if str(g).strip()})
all_countries = sorted({c for values in df["countriesOfOrigin"] for c in values if str(c).strip()})

filter_defaults = {
    "explorer_genre": "All genres",
    "explorer_countries": [],
    "explorer_rating": (0.0, 10.0),
    "explorer_votes": 0,
    "explorer_title": "",
    "explorer_sort": "Highest rated first"
}

if "explorer_reset_ready" not in st.session_state:
    st.session_state.explorer_reset_ready = False

if st.button("↺ Reset explorer filters"):
    for key, value in filter_defaults.items():
        st.session_state[key] = value
    st.rerun()

left, right = st.columns(2)
with left:
    selected_genre = st.selectbox(
        "Genre",
        ["All genres"] + all_genres,
        key="explorer_genre"
    )
    selected_countries = st.multiselect(
        "Country of origin",
        all_countries,
        key="explorer_countries"
    )
    selected_rating = st.slider(
        "IMDb rating range",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1,
        key="explorer_rating"
    )
with right:
    minimum_votes = st.number_input(
        "Minimum number of votes",
        min_value=0,
        step=1000,
        key="explorer_votes"
    )
    title_search = st.text_input(
        "Search by movie title",
        placeholder="For example, The Godfather",
        key="explorer_title"
    )
    sort_choice = st.radio(
        "Sort by IMDb rating",
        ["Highest rated first", "Lowest rated first"],
        horizontal=True,
        key="explorer_sort"
    )

filtered = df.copy()

if selected_genre != "All genres":
    filtered = filtered[filtered["genres"].apply(lambda values: selected_genre in values)]

if selected_countries:
    filtered = filtered[
        filtered["countriesOfOrigin"].apply(
            lambda values: any(country in values for country in selected_countries)
        )
    ]

filtered = filtered[
    filtered["averageRating"].between(selected_rating[0], selected_rating[1], inclusive="both")
]
filtered = filtered[filtered["numVotes"].fillna(0) >= minimum_votes]

if title_search.strip():
    filtered = filtered[
        filtered["primaryTitle"].str.contains(title_search.strip(), case=False, na=False)
    ]

filtered = filtered.sort_values(
    "averageRating",
    ascending=(sort_choice == "Lowest rated first")
)

st.metric("Movies matching your filters", f"{len(filtered):,}")
st.dataframe(
    filtered[["primaryTitle", "genres", "countriesOfOrigin", "averageRating", "numVotes", "grossWorldwide"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------
# Q6 - SESSION STATE AND SEARCH FORM
# -------------------------------------------------
st.markdown('<div class="section-label">A more personal search</div>', unsafe_allow_html=True)
st.header("Search for a movie")

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "movie_search_message" not in st.session_state:
    st.session_state.movie_search_message = ""

with st.form("movie_preferences_form"):
    movie_query = st.text_input(
        "Movie title",
        placeholder="Type a movie name..."
    )
    preferred_genre = st.selectbox(
        "Preferred genre",
        ["All genres"] + all_genres
    )
    preferred_rating = st.slider(
        "Minimum IMDb rating",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )
    search_submitted = st.form_submit_button("Find my movie")

if search_submitted:
    if not movie_query.strip():
        st.session_state.selected_movie = None
        st.session_state.movie_search_message = "Please enter a movie title to search."
    else:
        matches = df[
            df["primaryTitle"].str.contains(movie_query.strip(), case=False, na=False)
            & (df["averageRating"] >= preferred_rating)
        ]

        if preferred_genre != "All genres":
            matches = matches[
                matches["genres"].apply(lambda values: preferred_genre in values)
            ]

        if not matches.empty:
            st.session_state.selected_movie = matches.sort_values(
                "averageRating", ascending=False
            ).iloc[0].to_dict()
            st.session_state.movie_search_message = "Found a movie that matches your preferences."
        else:
            st.session_state.selected_movie = None
            st.session_state.movie_search_message = "No movie matched all those preferences. Try changing a filter."

if st.session_state.movie_search_message:
    if st.session_state.selected_movie is not None:
        st.success(st.session_state.movie_search_message)
    else:
        st.info(st.session_state.movie_search_message)

if st.session_state.selected_movie is not None:
    movie = st.session_state.selected_movie
    st.subheader(movie["primaryTitle"])
    info1, info2, info3 = st.columns(3)
    info1.metric("IMDb rating", f"{movie['averageRating']:.1f}/10")
    info2.metric("Number of votes", f"{movie['numVotes']:,.0f}")
    info3.write("**Genre**")
    info3.write(", ".join(movie["genres"]) if movie["genres"] else "Not available")
    if isinstance(movie.get("description"), str) and movie["description"].strip():
        st.write(movie["description"])
    if isinstance(movie.get("url"), str) and movie["url"].startswith("http"):
        st.link_button("View on IMDb ↗", movie["url"])

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
    CINESCOPE · IMDb TOP 250 MOVIES · BUILT WITH PYTHON & STREAMLIT
</div>
""", unsafe_allow_html=True)
