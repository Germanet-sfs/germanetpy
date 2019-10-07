# -*- coding: iso-8859-1 -*-
import numpy as np
from synset import WordCategory


class PathBasedSimilarity:
    MAXSHORTESTPATH_NOUNS = 35
    MAXSHORTESTPATH_VERBS = 28
    MAXSHORTESTPATH_ADJ = 20

    MAXDEPTH_NOUNS = 20
    MAXDEPTH_VERBS = 15
    MAXDEPTH_ADJ = 10

    def __init__(self, germanet):
        self._germanet = germanet

    def get_maxlen_by_category(self, wordcategory):
        assert isinstance(wordcategory, type(WordCategory.nomen)), "please specify a valid WordCategory"
        if wordcategory == WordCategory.nomen:
            return PathBasedSimilarity.MAXSHORTESTPATH_NOUNS
        elif wordcategory == WordCategory.verben:
            return PathBasedSimilarity.MAXSHORTESTPATH_VERBS
        else:
            return PathBasedSimilarity.MAXSHORTESTPATH_ADJ

    def get_maxdepth_by_category(self, wordcategory):
        assert isinstance(wordcategory, type(WordCategory.nomen)), "please specify a valid WordCategory"
        if wordcategory == WordCategory.nomen:
            return PathBasedSimilarity.MAXDEPTH_NOUNS
        elif wordcategory == WordCategory.verben:
            return PathBasedSimilarity.MAXDEPTH_VERBS
        else:
            return PathBasedSimilarity.MAXDEPTH_ADJ

    def path(self, synset1, synset2):
        assert synset1.word_category() == synset2.word_category(), "only synsets of the same Wordcategory can be " \
                                                                   "compared"
        maxlen = self.get_maxlen_by_category(synset1.word_category())
        pathlen = synset1.shortest_path_distance(synset2)
        path = (maxlen - pathlen) / maxlen
        return np.round(path, decimals=3)

    def wup(self, synset1, synset2):
        assert synset1.word_category() == synset2.word_category(), "only synsets of the same Wordcategory can be " \
                                                                   "compared"
        root_node = self._germanet.root()
        lcs_nodes = synset1.lowest_common_subsumer(synset2)
        depth = 0
        for n in lcs_nodes:
            dist = n.shortest_path_distance(root_node)
            if dist > depth:
                depth = dist
        pathlen = synset2.shortest_path_distance(synset1)
        wup = (2 * depth) / (pathlen + 2 * depth)
        return np.round(wup, decimals=3)

    def lch(self, synset1, synset2):
        assert synset1.word_category() == synset2.word_category(), "only synsets of the same Wordcategory can be " \
                                                                   "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        maxdepth = self.get_maxdepth_by_category(synset1.word_category())
        lch_sim = -np.log(pathlen / (2 * maxdepth))
        return np.round(lch_sim, decimals=3)
