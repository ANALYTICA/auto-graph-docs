from keybert import KeyBERT

with open('if1120.txt', 'r') as fh:
    doc1 = fh.read()
with open('if1120sd.txt', 'r') as fh:
    doc2 = fh.read()



doc3 = """
         Supervised learning is the machine learning task of learning a function that
         maps an input to an output based on example input-output pairs. It infers a
         function from labeled training data consisting of a set of training examples.
         In supervised learning, each example is a pair consisting of an input object
         (typically a vector) and a desired output value (also called the supervisory signal).
         A supervised learning algorithm analyzes the training data and produces an inferred function,
         which can be used for mapping new examples. An optimal scenario will allow for the
         algorithm to correctly determine the class labels for unseen instances. This requires
         the learning algorithm to generalize from the training data to unseen situations in a
         'reasonable' way (see inductive bias).
      """
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(doc1)
#print("text: \n", doc1)
print("keywords:  \n", keywords)

keywords2 = kw_model.extract_keywords(doc2)
#print("text: \n", doc1)
print("keywords:  \n", keywords2)

keywords3 = kw_model.extract_keywords(doc3)
#print("text: \n", doc1)
print("keywords:  \n", keywords3)

import spacy
nlp = spacy.load("en_core_web_md")
#nlp = spacy.load("en_core_web_md")


docs1 = [doc1,doc3]
docs2 = [doc2]

#docs1 = [
#        'The person wears red T-shirt.', 
#        'This is a red dress.', 
#        "The mechanic went to work."
#        ]

#docs2 = [
#        'I fixed the car.', 
#        'This fancy suit is red.', 
#        'He ate lunch.', 
#        "I don't like driving."
#        ]

def compare(lst1, lst2):
    for s1 in lst1:
        e1 = nlp(s1)
        for s2 in lst2:
            sim = e1.similarity(nlp(s2))
            #print(s1, " ", s2, " ", "similarity: ", sim)
            print("similarity: ", sim)

compare(docs1, docs2)
