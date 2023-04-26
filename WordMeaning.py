import spacy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define the text to be processed
text = "The cat sat on the mat and the dog barked. The sun was shining but it started to rain. I am hungry, therefore I am going to eat."

# Tokenize the text using spaCy
doc = nlp(text)

# Define the transition words and their meanings
TRANSITIONWORDS = {
    "and": "Addition / Extension",
    "but": "Contrast",
    "or": "Alternative",
    "because": "Explanation / Cause",
    "therefore": "Conclusion / Result"
}

# Define a function to find the children of a token in the dependency tree
def get_children(token):
    return [child for child in token.children]

# Define a function to recursively find all children of a given list of tokens
def find_children(tokens):
    children = []
    for token in tokens:
        children.extend(get_children(token))
    if children:
        children += find_children(children)
    return children

# Define a function to get the root of a given token
def get_root(token):
    if token.dep_ == "ROOT":
        return token
    else:
        return get_root(token.head)

# Define a function to get the meaning of a given transition word
def get_transition_meaning(word):
    return TRANSITIONWORDS.get(word, "Unknown")


# Create a networkx graph to represent the dependency tree
G = nx.DiGraph()

# Iterate over each token in the document
for token in doc:
    # Add the token to the graph
    G.add_node(token.i, label=token.text, pos=token.pos_, dep=token.dep_, head=token.head.i)
    # Add an edge between the token and its head
    if token.dep_ != "ROOT":
        G.add_edge(token.head.i, token.i)
        
# Find the transition words in the text
transition_words = []
for token in doc:
    if token.text in TRANSITIONWORDS:
        transition_words.append(token)

# Group the tokens based on their relation to the transition words
token_groups = []
for word in transition_words:
    root = get_root(word)
    children = find_children([root])
    group = [root] + children
    token_groups.append(group)

# Build a list of nodes and edges for the visualization
nodes = []
edges = []
for group in token_groups:
    meaning = get_transition_meaning(group[0].text)
    for token in group:
        nodes.append((token.i, {"label": token.text, "pos": token.pos_, "dep": token.dep_}))
        if token.dep_ != "ROOT":
            edges.append((token.head.i, token.i, {"label": token.dep_}))
    edges.append((group[0].i, group[-1].i, {"label": meaning}))

# Build a dataframe with the edges
df = pd.DataFrame(edges, columns=["from", "to", "label"])


# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to')

# Create a dictionary that maps node IDs to node labels
node_labels = {}
for node in G.nodes:
    node_labels[node] = doc[node].text

# Plot the graph with node labels
nx.draw(G, labels=node_labels, with_labels=True)
plt.show()