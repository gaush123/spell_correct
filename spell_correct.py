
# coding: utf-8

# In[1]:


# =========================
# Importing necessary libraries
# =========================
import re
from collections import Counter
from wordsegment import load, segment


# =========================
# Importing Flask and celery library
# =========================
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

def words(text): return re.findall(r'\w+', text.lower())


# =========================
# Loading base text file for word verification
# =========================
WORDS = Counter(words(open('big.txt').read()))



# In[2]:


def remove_emoji(string):
    """removal of emojis and other symbols"""
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)



def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 

    "Most probable spelling correction for word."
    word = remove_emoji(word)
    #try:
    load()
    word_list = segment(word)
    word_list = known(word_list)
    word_list = [word for word in word_list if len(word) > 3]
    if len(word_list) == 0:
        word_list = [word]
        
    result = []
    for word in word_list:
        result.append(sorted(candidates(word), key=P, reverse = True))
    return result
    

def candidates(word): 
    "Generate possible spelling corrections for word."
    #return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return [w for w in words if w in WORDS]

def edits1(word):
    "All edits that are one edit away from `word`."
    
    #print(word)
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[3]:


# =========================
# Declare Flask API
# =========================
app = FlaskAPI(__name__)

@app.route("/spellCorrect", methods=['GET', 'POST'])

def spelling_correction():
    """
    List or create notes.
    """
    print(correction('spel@@ing'))
    print(correction('korrectud'))
    if request.method == 'POST':
        data = request.get_json() #fetching data from POST request
        

        # ==============================
        # Reading data from Client POST
        # ==============================

        word = data['word']
        result = correction(word)
        return result


if __name__ == '__main__':
   app.run(debug = True)

