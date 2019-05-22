from django.core.files.storage import default_storage

import string
import re
from sklearn.feature_extraction.text import CountVectorizer
import xml.dom.minidom as minidom
doc_xml = minidom.parse("inr/data/convertcsv(1).xml")

docno = doc_xml.getElementsByTagName('No')
text = doc_xml.getElementsByTagName('Lirik')
headline = doc_xml.getElementsByTagName('Judul')
penyanyi = doc_xml.getElementsByTagName('Penyanyi')

N_DOC = len(docno)
tokens_doc = []
all_sentence_doc = []
for i in range(N_DOC):
    #print (i)
    sentence_doc = headline[i].firstChild.data +' '+ text[i].firstChild.data +' '+ penyanyi[i].firstChild.data
    all_sentence_doc.append(sentence_doc)
    
# =============================================================================
# REMOVE PUNCTUATION & URL
# =============================================================================

def remove_punc_tokenize(sentence):
    tokens = []
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation," ")
    
    sentence = re.sub(r'^https?:\/\/.*[\r\n]*', '', sentence, flags=re.MULTILINE)
    for w in CountVectorizer().build_tokenizer()(sentence):
        tokens.append(w)
    return tokens

for i in range(N_DOC):
    tokens_doc.append(remove_punc_tokenize(all_sentence_doc[i]))
#     print(tokens_doc[i])

# =============================================================================
# CASE FOLDING    
# =============================================================================
def to_lower(tokens):
    tokens = [x.lower() for x in tokens]
    return tokens

for i in range(N_DOC):
    tokens_doc[i] = to_lower(tokens_doc[i])
#     print(tokens_doc[i])

# =============================================================================
# STOPWORDS
# =============================================================================
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def stop_word_token(tokens):
    tokens = [w for w in tokens if not w in stop_words]
    return tokens

for i in range(N_DOC):
    tokens_doc[i] = stop_word_token(tokens_doc[i])
    
# =============================================================================
# REMOVE NUMBER
# =============================================================================
for i in range(N_DOC):
    tokens_doc[i] = ([w for w in tokens_doc[i] if not any(j.isdigit() for j in w)])
    
# =============================================================================
# STEMMING    
# =============================================================================
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
def stemming(tokens):
    for i in range(0, len(tokens)):
        if (tokens[i] != stemmer.stem(tokens[i])):
            tokens[i] = stemmer.stem(tokens[i])
    return tokens

for i in range(N_DOC):
    tokens_doc[i] = stemming(tokens_doc[i])
    
all_tokens = []
for i in range(N_DOC):
    for w in tokens_doc[i]:
        all_tokens.append(w)

new_sentence = ' '.join([w for w in all_tokens])

for w in CountVectorizer().build_tokenizer()(new_sentence):
    all_tokens.append(w)
    
# =============================================================================
# REMOVE DUPLICATE
# =============================================================================
all_tokens = set(all_tokens)


# =============================================================================
# PROXIMITY INDEX
# =============================================================================
from itertools import count
proximity_index = {}
for token in all_tokens:
    dict_doc_position = {}
    for n in range(N_DOC):
        if(token in tokens_doc[n]):
            dict_doc_position[docno[n].firstChild.data] = [i+1 for i, j in zip(count(), tokens_doc[n]) if j == token]
    proximity_index[token] = dict_doc_position
    
import collections
proximity_index = collections.OrderedDict(sorted(proximity_index.items()))
#for key, value in proximity_index.items():
#    print (key, value)
    
# =============================================================================
# CREATE FILE TXT
# =============================================================================
file = open('index.txt','w')
for key, value in proximity_index.items():
    file.write(key+'\n')
    for key, value in value.items():
        file.write('\t'+str(key)+': ')
        for i in range (len(value)):
            file.write(str(value[i]))
            if not(i == len(value)-1):
                file.write(',')
        file.write('\n')
    file.write('\n')
file.close()

# =============================================================================
# SEARCH 
# =============================================================================
def preprocessing(query):
    stemmer = PorterStemmer()
    
    query = query.lower()
    for punctuation in string.punctuation:
        query = query.replace(punctuation," ")
        string_no_numbers = re.sub("\d+", " ", query)
        
    query = stemmer.stem(string_no_numbers)
    # return query
    # query = stemmer.stem(query)
    return query

def search(query):
    result = []
    
    query = preprocessing(query)
    
    for key,value in proximity_index[query].items():
        result.append(key)
    return result

def main(inputs):

    query = inputs

    prepros = preprocessing(query)
    # prepros


    def indexing(data, queryLenght):
        index = []
        result = []
        
        for i in range(len(data)):
            sequence = [data[i][j:] for j in range(n)]
            temp = zip(*sequence)
            lists = list(temp)
            result.append([" ".join(lists) for lists in lists])
            
        for i in range(len(result)):
            for j in range(len(result[i])):
                index.append(result[i][j])
        
        return index, result

    spl = prepros.split()
    n = len(spl)
    dic = []
    ngram_all, ngram_doc = indexing(tokens_doc, n)

    ngram_index = {}
    ngram_data = {}
    ngram_penyanyi = {}
    for token in ngram_all:
        doc_headline = []
        doc_text = []
        doc_penyanyi = []

        for i in range(N_DOC):
            if (token in ngram_doc[i]):
                doc_headline.append(headline[i].firstChild.data)
                doc_text.append(text[i].firstChild.data)
                doc_penyanyi.append(penyanyi[i].firstChild.data)
                

        ngram_index[token] = doc_headline
        ngram_data[token] = doc_text
        ngram_penyanyi[token] = doc_penyanyi
    
    retrieve = []
    if query in ngram_all:
    
        khas = (u', '.join(ngram_data[prepros]))
        retrieve.append(khas)
    
    else:
        return dic

    
    # result = []
    judul = []
    lirik = []
    nyanyi = []
    for v1,v2,v3 in zip(ngram_index[prepros],ngram_data[prepros],ngram_penyanyi[prepros]):
        # hasil = "Judul : {0}\n Lirik : {1}".format(v1,v2)
        judul.append(v1)
        lirik.append(v2)
        nyanyi.append(v3)

    for i in range(len(judul)):
        ans = {'judul' : judul[i], 'penyanyi' : nyanyi[i], 'lirik' : lirik[i]}
        dic.append(ans)

    return dic,prepros