import pandas as pd

def content_distribution(data):
    """Movies vs TV Shows count"""
    return data['type'].value_counts()

def top_countries(data, n=10):
    """Top countries producing content"""
    return data['country'].value_counts().head(n)

def top_directors(data, n=10):
    """Top directors by number of titles"""
    return data['director'].value_counts().head(n)

def content_over_time(data):
    """Yearly trend of content added"""
    # Extract the year from 'date_added'
    data['year_added'] = data['date_added'].dt.year
    return data['year_added'].value_counts().sort_index()
