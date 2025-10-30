import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def plot_type_distribution(data):
    sns.countplot(x='type', data=data, palette='Set2')
    plt.title("Distribution of Content Type")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def plot_top_countries(data):
    top_countries = data['country'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='cool')
    plt.title("Top 10 Countries by Netflix Content")
    plt.xlabel("Count")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()


def plot_yearly_trend(data):
    data['year_added'] = data['date_added'].dt.year
    sns.countplot(x='year_added', data=data, palette='mako')
    plt.title("Netflix Content Added Over the Years")
    plt.xlabel("Year Added")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def wordcloud_titles(data):
    titles = " ".join(data['title'])
    wc = WordCloud(width=1000, height=500, background_color='black').generate(titles)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud of Netflix Titles")
    plt.tight_layout()
    plt.show()
