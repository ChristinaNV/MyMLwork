from nltk.corpus import wordnet # import the WordNet corpus from NLTK
from nltk.util import ngrams # import ngrams function from NLTK

# Define a function to calculate the Jaccard similarity between two lists
def jaccard_similarity(a, b):
    # Generate sets of n-grams (in this case, trigrams) for each list
    a_ngrams = set(ngrams(a, n=3))
    b_ngrams = set(ngrams(b, n=3))
    # Calculate the Jaccard similarity using the formula: intersection / union
    return len(a_ngrams & b_ngrams) / len(a_ngrams | b_ngrams)

# Define a function to check if two words are synonyms
def is_synonym(word1, word2):
    # Get all synonyms of word1 from WordNet
    synonyms = wordnet.synsets(word1)
    for syn in synonyms:
        for lemma in syn.lemmas():
            # Check if word2 matches any of the synonyms
            if lemma.name() == word2:
                return True
    return False

# Define a list of synonyms to compare against
synonyms = ["full name", "wallet", "phone number", "ranking", "earnings"]

# Prompt the user to enter a word to compare against the list of synonyms
word = input("Enter a word: ")

# Initialize variables to track the closest synonym and its similarity score
max_similarity = 0
closest_word = ""

# Iterate through each synonym and calculate its similarity to the input word
for syn in synonyms:
    # If the input word is a synonym of the current synonym, use that synonym
    if is_synonym(word, syn):
        closest_word = syn
        break
    # Otherwise, calculate the Jaccard similarity between the two words
    similarity = jaccard_similarity(word, syn)
    # If the similarity score is higher than the current maximum, update the closest word and similarity score
    if similarity > max_similarity:
        max_similarity = similarity
        closest_word = syn

# Print the closest synonym to the input word
print("The closest synonym to "+word+" is "+closest_word)
