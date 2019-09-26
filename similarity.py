import numpy as np
from germanet import Germanet
from synset import Synset, WordCategory


class Similarity:

    MAXSHORTESTPATH_NOUNS = 35
    MAXSHORTESTPATH_VERBS = 28
    MAXSHORTESTPATH_ADJ = 20

    def __init__(self, germanet):
        self._germanet = germanet


    def get_maxlen_by_category(self, wordcategory):
        assert isinstance(wordcategory, type(WordCategory.nomen)), "please specify a valid WordCategory"
        if wordcategory == WordCategory.nomen:
            return Similarity.MAXSHORTESTPATH_NOUNS
        elif wordcategory == WordCategory.verben:
            return Similarity.MAXSHORTESTPATH_VERBS
        else:
            return Similarity.MAXSHORTESTPATH_ADJ

    def path(self, synset1, synset2):
        assert synset1.word_category() == synset2.word_category(), "only synsets of the same Wordcategory can be compared"
        maxlen = self.get_maxlen_by_category(synset1.word_category())
        pathlen = synset1.shortest_path_distance(synset2)
        path = (maxlen-pathlen)/maxlen
        return np.round(path, decimals=3)

    def wup(self, synset1, synset2):
        root_node = self._germanet.root()
        print(root_node)
        lcs_nodes = synset1.lowest_common_subsumer(synset2)
        depth = 0
        for n in lcs_nodes:
            dist = n.shortest_path_distance(root_node)
            if dist > depth:
                depth = dist
        pathlen = synset2.shortest_path_distance(synset1)
        print(pathlen)
        wup = (2*depth) / (pathlen + 2 * depth)
        return np.round(wup, decimals=3)


if __name__ == '__main__':
    g = Germanet('data')
    root = g.get_synset_by_id('s51001')
    s = Similarity(g)
    s1 = g.get_synset_by_id("s50944")
    s2 = g.get_synset_by_id("s50915")
    print(s.wup(s1, s2))