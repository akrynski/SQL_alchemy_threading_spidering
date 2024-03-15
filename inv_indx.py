import sys
import stopwordsiso
import nltk
from nltk.tokenize import word_tokenize

if stopwordsiso.has_lang("pl"):
    from stopwordsiso import stopwords
    my_stopwords = stopwords("pl")
    # print(my_stopwords)
else:
    print("Cann't load stopwords!")


# tekst = 'W Szczczebrzeszynie chrząszcz brzmi w trzcinie Sp. z o.o., li, czy, no, że, niech, by, nie.\n Rozdział XXVI.\n Czy działa li to, czy nie?\n'.lower()
tokenizer = nltk.data.load('nltk:tokenizers/punkt/polish.pickle')
if tokenizer:
    print("tokenizer loaded")
else:
    print(f"failed to load the tokenizer")


class InvertedIndex:
    def __init__(self, doc, _stopwords, _tokenizer):
        self.doc = doc
        self.lines = 1
        self.arr = []
        self.tokenizer = _tokenizer
        self.my_stopwords = _stopwords

    def __str__(self):
        return f"My stopwords are: {self.my_stopwords},\nand the doc is {self.doc}\n"

    def Display_docs(self):
        print(self.doc)
        return self.doc

    def Number_of_docs(self):
        for word in self.doc:
            if word == '\n':
                self.lines += 1
        return self.lines

    def Split_docs(self):
        for i in range(self.lines):
            self.arr.append(self.doc.split('\n')[i])
        return self.arr

    def Tokenization(self):
        self.doc = self.doc.lower()
        # tokens = self.doc.split()
        tokens = self.tokenizer.tokenize(self.doc)
        for i in range(1):
            tokens = word_tokenize(self.doc)
        return tokens

    def Stopping(self):
        # print(f"entering method stopping()")
        # stop_words = open(
        #    'C:\\Users\\Andrzej\\Desktop\\POGRZEBANE PRZEZ COVID\\python_actual_project\\SqlAlchemy\\SqlAlchemy and multithreading\\text\\StopWords.txt',
        #    'r').read()
        stop_words = self.my_stopwords
        #stop_words = stop_words.split()
        # print(f"stopwords:\n{stop_words}")
        #NewList = []
        # Remove special characters
        tokens = self.Tokenization()
        # print(f"Tokens:\n{tokens}")
        # for doc in tokens:
        #     Newdoc = "".join(ch for ch in doc if ch.isalnum())
        #     NewList.append(Newdoc)
        # print(f"NewList: \n{NewList}")
        # Remove stopring words
        after_stopping = [token for token in tokens if token not in stop_words] # było in NewList
        # print(f"after stopping list:\n{after_stopping}")
        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        newstr = []
        for ele in after_stopping:
            if ele not in punc:
                newstr.append(ele)
                # print(ele+'\n')
        # print(f"newstr po usunięciu punktatorów:\n{newstr}")
        return newstr

    def Inverted_Index(self):
        Inverted_index = {}
        _after_stopping = self.Stopping()
        # print(f"after_stopping list:\n{_after_stopping}")
        for token in _after_stopping:
            for i in range(self.lines):
                if token in self.arr[i]:
                    if token in Inverted_index:
                        Inverted_index[token].add(i + 1)
                    else:
                        Inverted_index[token] = {i + 1}
        #print(Inverted_index)
        return Inverted_index

    def Indexer(self):
        indexer = {}
        after_stopping = self.Stopping()
        for token in after_stopping:
            for i in range(self.lines):
                if token in self.arr[i]:
                    indexer[token] = i + 1

        return indexer

    def Term_squences(self):
        indexer = self.Indexer()
        return sorted(indexer.items(), key=lambda x: x[1])

    def Sorting_Alphabetically(self):
        indexer = self.Indexer()
        return sorted(indexer.items(), key=lambda x: x[0])

    def Term_Frequency(self):
        Term_frequancy = {}
        Inverted_index = self.Inverted_Index()
        for term in Inverted_index:
            Term_frequancy[term] = term
            Term_frequancy[term] = len(Inverted_index[term])

        return Term_frequancy

    # ------------------------------------------------------------


try:
    documents = open(
        'C:\\Users\\Andrzej\\Desktop\\POGRZEBANE PRZEZ COVID\\python_actual_project\\SqlAlchemy\\SqlAlchemy and multithreading\\text\\Documents.txt').read()
    print("Document opened.")
    InvIndex = InvertedIndex(doc=documents, _stopwords=my_stopwords, _tokenizer=tokenizer)
    #InvIndex
    #print("Printing docs:\n")
    #InvIndex.Display_docs()
    # ------------------------------------------------------------

    print(f"Number of docs: {InvIndex.Number_of_docs()}\n")
    # ------------------------------------------------------------

    InvIndex.Split_docs()
    # ------------------------------------------------------------

    # InvIndex.Tokenization()
    # ------------------------------------------------------------
    print(f"After stopping(): \n")
    print(InvIndex.Stopping())
    # ------------------------------------------------------------
    print(f"Inverted index:\n")
    print(InvIndex.Inverted_Index())
    # -------------------------------------------------------------

    print(f"Indexer: \n")
    InvIndex.Indexer()
    # -------------------------------------------------------------
    print(f"Term sequences: \n")
    print(InvIndex.Term_squences())
    # -------------------------------------------------------------
    print(f"Sorted:\n")
    print(InvIndex.Sorting_Alphabetically())
    # --------------------------------------------------------------
    print(f"Term frequency:\n")
    print(InvIndex.Term_Frequency())
    # --------------------------------------------------------------
except (IOError, OSError):
    # print >> sys.stderr, "Error!", sys.exc_info()[0]
    print("Error!", sys.exc_info()[0], file=sys.stderr)
    sys.exit(1)
#finally:
#    sys.exit(0)
