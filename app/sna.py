import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import numpy as np
import requests
import streamlit.components.v1 as components

# Load data
data = pd.read_csv("sna.csv")
data = data.drop_duplicates()
data['date'] = pd.to_datetime(data['date']).dt.date


class Tweet(object):  ## embedd the tweet
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=700)

def central_component(): ## function to make sna in center
    container = st.container()
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        components.html(HtmlFile.read(), height=700)
        
def influential_tweet(relationship_df, df):  ## to make influentional tweet
    df2 = relationship_df.to.value_counts().rename_axis('username').reset_index(name='counts')
    df2 = df2.head(3)
    df3 = df[['id', 'username', 'replyCount', 'tweet_url']]
    newdf = df2.merge(df3, how='right', on=['username'])
    newdf = newdf.dropna()
    newdf  = newdf.sort_values(by=[ 'replyCount', 'counts',],ascending=False)
    newdf = newdf.head(3)
    url = newdf['tweet_url'].unique()
    return url


# Set page title
st.set_page_config(page_title="Social Network Analysis", layout="wide")

# Set page layout
st.write('<style>h1{text-align: center;}</style>', unsafe_allow_html=True)
st.title("Social Network Analysis")


# Show date slider
min_date = data['date'].min()
max_date = data['date'].max()
selected_date_range = st.slider('Select date range', min_date, max_date, (min_date, max_date))

# Convert slider values back to datetime objects
start_date = pd.to_datetime(selected_date_range[0]).date()
end_date = pd.to_datetime(selected_date_range[1]).date()

# Filter data based on selected date range
df = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
df = df.head(1500)
df_reply = df[['inReplyToUser','username']][df['tweet_type'] == 'reply']
# Sort the cases with a->b and b->a
relationship_df = pd.DataFrame(np.sort(df_reply.values, axis = 1), columns = ['from','to'])
relationship_df["value"] = 1
relationship_df = relationship_df.groupby(["from","to"], sort=False, as_index=False).sum()
G = nx.from_pandas_edgelist(relationship_df, 
                            source = "from", 
                            target = "to", 
                            edge_attr = "value", 
                            create_using = nx.Graph())
net = Network(width='100%', height='700px', bgcolor='#e2e2e3', font_color='black')
#net = Network(notebook=True, bgcolor='#222222', font_color='white')

node_degree = dict(G.degree)
nx.set_node_attributes(G, node_degree, 'size')

net.from_nx(G)
#net.show('sumbar_streamlit.html')
try:
        net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
except:
        net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
#components.html(HtmlFile.read(), height=700, width = 1400)
central_component()
            

url = influential_tweet(relationship_df=relationship_df, df=df)
st.write('<style>h1{text-align: center;}</style>', unsafe_allow_html=True)
st.title('Most Influential Tweet')    
cols=st.columns(3)
with cols[0]:
    a = Tweet(url[0]).component()
with cols[1]:
    b = Tweet(url[1]).component()
with cols[2]:
    c = Tweet(url[2]).component()

    
# for x in url:
#     t = Tweet(x).component()