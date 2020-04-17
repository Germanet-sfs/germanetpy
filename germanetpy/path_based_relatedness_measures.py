import math
import numpy as np
from germanetpy import longest_shortest_path
from germanetpy.semrel_measures import SemRelMeasure


class PathBasedRelatedness:
    """
    These measures use the GermaNet Graph to compute the shortest Paths between two concepts. These concepts have to
    have the same word category. The path lengths are normalized in different ways (depending on the measure). The path
    lengths are computed taking only the hypernymy / hyponymy relations into account
    """

    def __init__(self, germanet, category, max_len: int = None, max_depth: int = None, synset_pair=None):
        """
        This is the constructor of the PathBasedRelatedness class. The class needs the germanet Graph and a word
        category specified. The parameter max_len, max_depth and synset_pair are optional. If not given they will be
        computed online which can be time-consuming, especially for nouns.
        :type synset_pair: tuple(Synset, Synset)
        :type category: WordCategory
        :type germanet: Germanet
        :param germanet: The Germanet Graph
        :param category: WordCategory
        :param max_len: the longest shortest path distance between any of the corresponding synsets
        :param max_depth the maximum depth of any corresponding synset
        :param synset_pair a pair of synsets that has the longest shortest path distance
        """
        self._germanet = germanet
        self._category = category
        if max_len and max_depth and synset_pair:
            self._max_len = max_len
            self._max_depth = max_depth
        else:
            self._max_len, self._max_depth, synset_pair = longest_shortest_path.get_longest_possible_shortest_distance(
                germanet, category)
        self._normalization_dic = self.init_min_max_normalization_values(synset_pair)

    def simple_path(self, synset1, synset2, normalize: bool = False, normalized_max: float = 1.0) -> float:
        """
        This measure computes the pathlength and normalizes it by the longest possible shortest path between any two
        nodes of the corresponding word category.
        :type synset2: Synset
        :type synset1: Synset
        :param synset1: The source synset
        :param synset2: The target synset the source synset is compared to
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of 
        that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return: : The normalized path length between two synsets
        """
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        path = (self.max_len - pathlen) / self.max_len
        if normalize:
            path = self.normalize(raw_value=path, normalized_max=normalized_max,
                                  semrel_measure=SemRelMeasure.SimplePath)
        return np.round(path, decimals=5)

    def init_min_max_normalization_values(self, synset_pair):
        """
        This methods computes the minimal values (two synsets are equal) and the maximum values (two synsets are
        maximally appart in the graph) for normalization
        :param synset_pair: (Synset, Synset) The Tuple of synsets that have the maximum distance in the graph
        :return: a dictionary [SemRelMeasure : (int, int)] containing the (minimum value, maximum value) for each
        semantic similarity measure.
        """
        min_wup = self.wu_and_palmer(synset_pair[0], synset_pair[1])
        max_wup = self.wu_and_palmer(synset_pair[0], synset_pair[0])
        min_path = self.simple_path(synset_pair[0], synset_pair[1])
        max_path = self.simple_path(synset_pair[0], synset_pair[0])
        min_lch = self.leacock_chodorow(synset_pair[0], synset_pair[1])
        max_lch = self.leacock_chodorow(synset_pair[0], synset_pair[0])
        norm_values = {
            SemRelMeasure.SimplePath: (min_path, max_path),
            SemRelMeasure.WuAndPalmer: (min_wup, max_wup),
            SemRelMeasure.LeacockAndChodorow: (min_lch, max_lch)
        }
        return norm_values

    def wu_and_palmer(self, synset1, synset2, normalize: bool = False, normalized_max: float = 1.0) -> float:
        """
        This methods computes the semantic relatedness by taking the path length into account, normalizing by taking
        the depth of the LCS. If there are several possible LCS, the one with the largest depth is taken into account.
        :type synset2: Synset
        :type synset1: Synset
        :param synset1: The source synset
        :param synset2: The target synset the source synset is compared to
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return: : The wu and palmer relatedness measure
        """
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        root_node = self.germanet.root
        lcs_nodes = synset1.lowest_common_subsumer(synset2)
        depth = 0
        for n in lcs_nodes:
            current_depth = n.shortest_path_distance(root_node)
            if current_depth > depth:
                depth = current_depth
        pathlen = synset2.shortest_path_distance(synset1)
        wup = (2 * depth) / (pathlen + 2 * depth)
        if normalize:
            wup = self.normalize(raw_value=wup, normalized_max=normalized_max, semrel_measure=SemRelMeasure.WuAndPalmer)
        return np.round(wup, decimals=5)

    def leacock_chodorow(self, synset1, synset2, normalize: bool = False, normalized_max: float = 1.0) -> float:
        """
        This method implements the leackock and chodorow relatedness measure. For the path distance and depth,
        node count is used.
        :type synset2: Synset
        :type synset1: Synset
        :param synset1: The source synset
        :param synset2: The target synset the source synset is compared to
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return:: The leackock and chodorow relatedness measure
        """
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2) + 1
        lch_sim = -math.log10(pathlen / (2 * (self.max_depth + 1)))
        if normalize:
            lch_sim = self.normalize(raw_value=lch_sim, normalized_max=normalized_max,
                                     semrel_measure=SemRelMeasure.LeacockAndChodorow)
        return np.round(lch_sim, decimals=5)

    def normalize(self, raw_value: float, normalized_max: float, semrel_measure: SemRelMeasure) -> float:
        """
        Normalizes a raw value of semantic relatedness to a value between a lower bound and the given upper bound.
        :param raw_value: The raw value
        :param normalized_max: The upper bound
        :param semrel_measure: The semantic relatedness measure, the value corresponds to.
        :return: The normalized semantic relatedness value
        """
        lower_bound, upper_bound = self.normalization_dic[semrel_measure]
        return np.round(((raw_value - lower_bound) / (upper_bound - lower_bound)) * normalized_max, decimals=5)

    @property
    def germanet(self):
        return self._germanet

    @property
    def max_len(self):
        return self._max_len

    @property
    def max_depth(self):
        return self._max_depth

    @property
    def category(self):
        return self._category

    @property
    def normalization_dic(self):
        return self._normalization_dic
