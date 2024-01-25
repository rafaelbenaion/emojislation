# -------------------------------------------------------------------------------------------------------- #
# TATIA, Final Project - Emojislation                                                                      #
# -------------------------------------------------------------------------------------------------------- #
# 30 Jan 2024, Université Côte d'Azur.                                                                     #
# Charafeddine Achir & Rafael Baptista.                                                                    #
# -------------------------------------------------------------------------------------------------------- #

import numpy as np
import emoji
import spacy
from emo_uni import emo_list,emo_get
from tqdm import tqdm
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load('en_core_web_sm')

# -------------------------------------------------------------------------------------------------------- #
# Converting the emoji list to lowercase and replacing the underscores with spaces.                        #
# -------------------------------------------------------------------------------------------------------- #
# #Processing the emoji's textual representation to make it easier to work with.                           #
# -------------------------------------------------------------------------------------------------------- #

e_l=[]                                                                                       #List of emojis

for i in emo_list:                                                              # Looping through each emoji
    e_l.append(str(i.replace("_"," ")).lower())                          # Converting the emoji to lowercase

e_l[1:10]

# -------------------------------------------------------------------------------------------------------- #
# Function to convert a word to its corresponding emoji.                                                   #
# -------------------------------------------------------------------------------------------------------- #

print(emoji.emojize('TATIA is :thumbs_up:'))

# -------------------------------------------------------------------------------------------------------- #
# The models use 300d Glove vectors trained on the Wikipedia corpus as word embeddings.                    #
# -------------------------------------------------------------------------------------------------------- #

with open('glove.6B.300d.txt', 'r', encoding='utf-8') as f:                 # Opening the GloVe vectors file

    for line in tqdm(f, total=400000):                                           # Looping through each line

        parts = line.split()                                                 # Splitting the line into parts
        word = parts[0]                                                         # The first part is the word
        vec = np.array([float(v) for v in parts[1:]], dtype='f')      # The rest of the parts are the vector

        nlp.vocab.set_vector(word,vec)

# -------------------------------------------------------------------------------------------------------- #
#   Function to calculate the cosine similarity between two vectors.                                       #
# -------------------------------------------------------------------------------------------------------- #
doc_vectors = np.array([nlp(emoji).vector for emoji in e_l])

# -------------------------------------------------------------------------------------------------------- #
# Function to calculate the cosine similarity between two vectors.                                         #
# -------------------------------------------------------------------------------------------------------- #

def most_similar(vectors, vec):
    cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))    # Defining the cosine similarity function
    dst = np.dot(vectors, vec) / (norm(vectors) * norm(vec))             # Calculating the cosine similarity

    return (np.argsort(-dst))[0], max(dst)    # The index of the most similar emoji and the similarity score

# -------------------------------------------------------------------------------------------------------- #
# Data source generated with GPT-4.                                                                        #
# -------------------------------------------------------------------------------------------------------- #
# We needed a large number of simple sentences to the project, so we used GPT-4 to generate sentences that #
# are from English foreign language textbooks, for their simplicity.                                       #
#--------------------------------------------------------------------------------------------------------- #

sentences = [
"The sun is rising early.",
"Birds are chirping outside.",
"The coffee is brewing.",
"Children are playing in the park.",
"The train is arriving on time.",
"She is reading a novel.",
"He is cooking breakfast.",
"The flowers are blooming brightly.",
"I am learning to paint.",
"They are watching a comedy show.",
"The teacher is explaining the lesson.",
"The cat is chasing the mouse.",
"We are planning a trip.",
"The car is parked outside.",
"The stars are shining tonight.",
"He is tying his shoes.",
"She is writing a letter.",
"The baby is laughing.",
"The dog is wagging its tail.",
"They are celebrating a birthday.",
"I am jogging in the morning.",
"The bell is ringing at school.",
"The cake is baking in the oven.",
"He is playing the guitar.",
"She is dancing ballet.",
"The book is on the shelf.",
"Birds are building a nest.",
"The moon is full tonight.",
"The fish are swimming in the pond.",
"He is fixing the bicycle.",
"She is planting flowers.",
"The sun is setting.",
"They are having a barbecue.",
"I am taking photographs.",
"He is drawing a picture.",
"She is making a salad.",
"The children are flying kites.",
"The phone is ringing.",
"He is washing the car.",
"She is studying for exams.",
"The leaves are turning red.",
"I am riding a horse.",
"The snow is falling.",
"He is shoveling the driveway.",
"She is feeding the birds.",
"The boat is sailing on the lake.",
"I am writing a story.",
"The wind is blowing the leaves.",
"He is playing chess.",
"She is knitting a sweater."
]

# -------------------------------------------------------------------------------------------------------- #
# For each sentence, look up for to-be verbs or articles and replace them with a space                     #
# -------------------------------------------------------------------------------------------------------- #
# After testing, we found that the most similar emojis are found when the sentence is simplified.          #
# So we will remove the to-be verbs and articles from each sentence.                                       #
# -------------------------------------------------------------------------------------------------------- #

words_to_replace = [" are ", " is ", " am ", " a ", " an "]              # Words to be replaced with a space

updated_sentences = [sentence for sentence in sentences]    # Replacing the specified words in each sentence

for i, sentence in enumerate(updated_sentences):                             # Looping through each sentence
    for word in words_to_replace:
        sentence = sentence.replace(word, " ")
    updated_sentences[i] = sentence

updated_sentences                                                         # Displaying the updated sentences

# -------------------------------------------------------------------------------------------------------- #
# Using the GloVe vectors to find the most similar emojis for each sentence.                               #
# -------------------------------------------------------------------------------------------------------- #

for sentence in updated_sentences:                                           # Looping through each sentence
    l = []

    for w in sentence.split(" "):                                # Looping through each word in the sentence
        v = nlp(w.lower()).vector                                          # Getting the vector for the word
        ms, sim = most_similar(doc_vectors, v)                              # Getting the most similar emoji

        # ------------------------------------------------------------------------------------------------ #
        # Defining a threshold for the similarity score to filter out emojis that are not similar enough.  #
        # ------------------------------------------------------------------------------------------------ #

        if (sim > 0.0115):                           # If the similarity score is greater than the threshold
            word = emo_get[ms]                                    # Get the emoji for the most similar emoji
            l.append(emoji.emojize(word, language='alias'))                   # Append the emoji to the list

    #print(sentence)
    #display(HTML('<font size="+2">{}</font>'.format(' '.join([x for x in l]))))  # Displaying the emojis

    # ---------------------------------------------------------------------------------------------------- #
    # Writing the emojis and the sentences to a html file for further validation.                          #
    # ---------------------------------------------------------------------------------------------------- #

    # Write the emojis and the senteces to a html file
    with open('emojis.html', 'a', encoding='utf-8') as f:
        f.write('<font size="+2">{}</font>'.format(' '.join([x for x in l])))
        f.write('<br><br>')
        f.write(sentence)
        f.write(' <input type="checkbox"/>')
        f.write('<br>')
        f.write('<br>')
        f.write('<br>')

# -------------------------------------------------------------------------------------------------------- #
# Function to translate a sentence to emojis.                                                              #
# -------------------------------------------------------------------------------------------------------- #
def translator(sentence):

    l = []

    for w in sentence.split(" "):                                # Looping through each word in the sentence

        v = nlp(w.lower()).vector                                          # Getting the vector for the word
        ms, sim = most_similar(doc_vectors, v)                              # Getting the most similar emoji

        # ------------------------------------------------------------------------------------------------ #
        # Defining a threshold for the similarity score to filter out emojis that are not similar enough.  #
        # ------------------------------------------------------------------------------------------------ #

        if (sim > 0.0115):                           # If the similarity score is greater than the threshold
            word = emo_get[ms]                                    # Get the emoji for the most similar emoji
            l.append(emoji.emojize(word, language='alias'))                   # Append the emoji to the list

    # For each emoji in the list, transform in a single html string
    html = '<font size="+2">{}</font>'.format(' '.join([x for x in l]))
    
    return html