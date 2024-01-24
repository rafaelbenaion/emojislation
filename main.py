# -------------------------------------------------------------------------------------------------------- #
# TATIA, Final Project - Emojislation                                                                      #
# -------------------------------------------------------------------------------------------------------- #
# 30 Jan 2024, Université Côte d'Azur.                                                                     #
# Charafeddine Achir & Rafael Baptista.                                                                    #
# -------------------------------------------------------------------------------------------------------- #

import numpy as np
import emoji
import spacy
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
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

with open('glove.6B.300d.txt', 'r', encoding='utf-8') as f:  # Opening the GloVe vectors file

    for line in tqdm(f, total=400000):  # Looping through each line

        parts = line.split()  # Splitting the line into parts
        word = parts[0]  # The first part is the word
        vec = np.array([float(v) for v in parts[1:]], dtype='f')  # The rest of the parts are the vector

        nlp.vocab.set_vector(word,vec)

# -------------------------------------------------------------------------------------------------------- #
#   Function to calculate the cosine similarity between two vectors.                                       #
# -------------------------------------------------------------------------------------------------------- #
doc_vectors = np.array([nlp(emoji).vector for emoji in e_l])


# -------------------------------------------------------------------------------------------------------- #
# Function to calculate the cosine similarity between two vectors.                                         #
# -------------------------------------------------------------------------------------------------------- #

def most_similar(vectors, vec):
    cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))  # Defining the cosine similarity function
    dst = np.dot(vectors, vec) / (norm(vectors) * norm(vec))  # Calculating the cosine similarity

    return (np.argsort(-dst))[0], max(dst)  # The index of the most similar emoji and the similarity score

# -------------------------------------------------------------------------------------------------------- #
# Data source generated with GPT-4.                                                                        #
# -------------------------------------------------------------------------------------------------------- #
# We needed a large number of simple sentences to the project, so we used GPT-4 to generate sentences that #
# are from English foreign language textbooks, for their simplicity.                                       #
#--------------------------------------------------------------------------------------------------------- #

sentences = [
    "love hearts apple",
    "Sunny weather today",
    "Happy birthday celebration",
    "Delicious food served",
    "Running fast wind",
    "Sleeping cat quietly",
    "Coffee morning routine",
    "Books stack library",
    "Music brings joy",
    "Travel world adventure",
    "The cat is sleeping.",
    "She is reading a book.",
    "The sun is shining.",
    "He is writing a letter.",
    "The dog is barking.",
    "They are playing soccer.",
    "I am eating an apple.",
    "She is drinking water.",
    "The baby is crying.",
    "We are watching a movie.",
    "The birds are singing.",
    "He is running fast.",
    "The door is closed.",
    "She is cooking dinner.",
    "The phone is ringing.",
    "They are dancing together.",
    "I am learning English.",
    "The car is moving.",
    "She is wearing a dress.",
    "The flowers are blooming.",
    "He is swimming in the pool.",
    "They are riding bicycles.",
    "I am drawing a picture.",
    "The train is arriving.",
    "She is playing the piano.",
    "The glass is full.",
    "He is driving a car.",
    "They are speaking French.",
    "I am taking a bath.",
    "The moon is bright.",
    "She is tying her shoes.",
    "The clock is ticking.",
    "He is climbing a tree.",
    "They are making a cake.",
    "I am writing an email.",
    "The river is flowing.",
    "She is jumping rope.",
    "The window is open.",
    "He is fixing the bike.",
    "They are planting flowers.",
    "I am brushing my teeth.",
    "The stars are twinkling.",
    "She is feeding the cat.",
    "The light is on.",
    "He is cutting the grass.",
    "They are building a sandcastle.",
    "I am listening to music.",
    "The leaves are falling.",
    "She is washing the dishes.",
    "The book is on the table.",
    "He is painting a picture.",
    "They are studying math.",
    "I am making a sandwich.",
    "The snow is melting.",
    "She is ironing clothes.",
    "The bus is late.",
    "He is tying a tie.",
    "They are playing chess.",
    "I am riding a horse.",
    "The kettle is boiling.",
    "She is cleaning the room.",
    "The baby is sleeping.",
    "He is peeling an orange.",
    "They are hiking in the woods.",
    "I am shopping for groceries.",
    "The bird is flying.",
    "She is playing guitar.",
    "The bell is ringing.",
    "He is baking bread.",
    "They are watching the sunrise.",
    "I am watering the plants.",
    "The fish are swimming.",
    "She is taking a selfie.",
    "The alarm is sounding.",
    "He is playing basketball.",
    "They are visiting a museum.",
    "I am reading a magazine.",
    "The cat is purring.",
    "Simple phrase traduction.",
]

# -------------------------------------------------------------------------------------------------------- #
# For each sentence, look up for to-be verbs or articles and replace them with a space                     #
# -------------------------------------------------------------------------------------------------------- #
# After testing, we found that the most similar emojis are found when the sentence is simplified.          #
# So we will remove the to-be verbs and articles from each sentence.                                       #
# -------------------------------------------------------------------------------------------------------- #

words_to_replace = [" are ", " is ", " am ", " a ", " an "]  # Words to be replaced with a space

updated_sentences = [sentence for sentence in sentences]  # Replacing the specified words in each sentence

for i, sentence in enumerate(updated_sentences):  # Looping through each sentence
    for word in words_to_replace:
        sentence = sentence.replace(word, " ")
    updated_sentences[i] = sentence

updated_sentences  # Displaying the updated sentences

# -------------------------------------------------------------------------------------------------------- #
# Using the GloVe vectors to find the most similar emojis for each sentence.                               #
# -------------------------------------------------------------------------------------------------------- #

for sentence in updated_sentences:  # Looping through each sentence
    l = []

    for w in sentence.split(" "):  # Looping through each word in the sentence
        v = nlp(w.lower()).vector  # Getting the vector for the word
        ms, sim = most_similar(doc_vectors, v)  # Getting the most similar emoji

        # ------------------------------------------------------------------------------------------------ #
        # Defining a threshold for the similarity score to filter out emojis that are not similar enough.  #
        # ------------------------------------------------------------------------------------------------ #

        if (sim > 0.0115):  # If the similarity score is greater than the threshold
            word = emo_get[ms]  # Get the emoji for the most similar emoji
            l.append(emoji.emojize(word, language='alias'))  # Append the emoji to the list

    #print(sentence)
    #display(HTML('<font size="+2">{}</font>'.format(' '.join([x for x in l]))))  # Displaying the emojis

    # ---------------------------------------------------------------------------------------------------- #
    # Writing the emojis and the sentences to a html file for further validation.                          #
    # ---------------------------------------------------------------------------------------------------- #

    # Write the emojis and the senteces to a html file
    with open('emojis.html', 'a', encoding='utf-8') as f:
        f.write('<font size="+2">{}</font>'.format(' '.join([x for x in l])))
        f.write('<br>')
        f.write(sentence)
        f.write('<input type="checkbox"/>')
        f.write('<br>')
        f.write('<br>')
        f.write('<br>')
