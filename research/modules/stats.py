import textacy
import collections
from textacy import text_stats as ts
class DocStats():
    def __init__(self, doc):
        self.stats = {}
        self.ngrams = {}
        self.title = doc._.meta["title"]

        self.stats_available = dict(
            basics = [
                "n_sents", "n_words", "n_unique_words",
                "n_chars_per_word", "n_chars", "n_long_words",
                #language dependent: "n_syllables_per_word", "n_syllables", "n_monosyllable_words", "n_polysyllable_words",
                      "entropy"
                     ],
            counts = ["morph", "tag", "pos", "dep"],
            diversity = ["ttr", "log_ttr", "segmented_ttr", "mtld", "hdd"],
            readability = ["automated_readability_index",
                                         "automatic_arabic_readability_index", 
                                         "coleman_liau_index",
                           #language dependent "flesch_kincaid_grade_level", "flesch_reading_ease", 
                           "gulpease_index",
                           #lang dependent "gunning_fog_index", 
                           "lix", "mu_legibility_index",
                           #lang dependent "perspicuity_index", "smog_index" 
                          ]
        )
    def getNgrams(self, doc, min=2, max=15):
        doc_ngrams = {}
        for n in range(min,max):
            doc_ngrams.setdefault(n, dict())
            ngrams_list = list(textacy.extract.basics.ngrams(doc, n=n))
            doc_ngrams[n]["list"] = ngrams_list
            doc_ngrams[n]["count"] = collections.Counter([ span.text for span in ngrams_list ])
        self.ngrams = doc_ngrams
        #counter = collections.Counter([ span.text for span in stats_corpora["docs_normalized"][doc]["ngrams"][n] ])

    def topNgrams(self, nn=[2], top=5):
        top_ngrams = []
        for n in nn:
            for ngram in self.ngrams[n]["count"].most_common(top):
                top_ngrams.append(
                    dict(n=n , ngram=ngram[0], freq=ngram[1])
                ) # tuple: (n, list of top n-grams)
        return top_ngrams
    
    def getStats(self, doc):        
        for module in self.stats_available.items():
            #print("tu jestem: ", module)
            if module[0] == "basics":
                self.stats.setdefault("basics", {})
                for m in module[1]:
                    try:
                        #print(getattr(ts.basics, m)(doc))
                        self.stats["basics"].setdefault(m, getattr(ts.basics, m)(doc))
                    except (Exception, RuntimeError) as e:
                        print("error: ", m)
                        print(e)
                        pass
            elif module[0] == "counts":
                self.stats.setdefault("counts", {})
                for m in module[1]:
                    try:
                        self.stats["counts"].setdefault(m, getattr(ts.counts, m)(doc))
                    except (Exception, RuntimeError) as e:
                        print("error: ", m)
                        print(e)
                        pass
            elif module[0] == "diversity":
                self.stats.setdefault("diversity", {})
                for m in module[1]:
                    #print(m)
                    try:
                        self.stats["diversity"].setdefault(m, getattr(ts.diversity, m)(doc))
                    except (Exception, RuntimeError) as e:
                        print("error: ", m)
                        print(e)
                        pass
            elif module[0] == "readability":
                self.stats.setdefault("readability", {})
                for m in module[1]:
                    #print(m)
                    try:
                        self.stats["readability"].setdefault(m, getattr(ts.readability, m)(doc))
                    except (Exception, RuntimeError) as e:
                        print("exc: ", m)
                        print(e)
                        pass
        #self.stats = doc_stats

class CorpusStats():
    def __init__(self, name):
        self.name = name
        self.docs = []
    
    def getStats(self, corpus):
        for doc in corpus:
            document = DocStats(doc)
            document.getNgrams(doc)
            document.getStats(doc)
            self.docs.append(document)