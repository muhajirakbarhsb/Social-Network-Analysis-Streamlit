import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import numpy as np


# Load data
data = pd.read_csv("sna.csv")
data['date'] = pd.to_datetime(data['date']).dt.date

# Set page title
st.set_page_config(page_title="Social Network Analysis")

# Set page layout
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
from pyvis.network import Network
net = Network(notebook=True, width='700px', height='700px', bgcolor='#222222', font_color='white')

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
components.html(HtmlFile.read(), height=700, width = 700)
            
            
