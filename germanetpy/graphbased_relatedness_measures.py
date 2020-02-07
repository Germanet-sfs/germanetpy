import numpy as np
import fastenum
from germanetpy import longest_shortest_path


class SemRelMeasure(fastenum.Enum):
    SimplePath = 1
    LeacockAndChodorow = 2
    WuAndPalmer = 3


class GraphRelatedness:

    def __init__(self, germanet, category):
        self._germanet = germanet
        self._category = category
        self._max_len, self._max_depth, synset_pair = longest_shortest_path.get_overall_longest_shortest_distance(
            germanet, category)
        self._normalization_dic = self.init_min_max_normalization_values(synset_pair)

    def simple_path(self, synset1, synset2, normalize=False, upper_bound=1.0):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        path = (self.max_len - pathlen) / self.max_len
        if normalize:
            path = self.normalize(raw_value=path, normalized_max=upper_bound, semrel_measure=SemRelMeasure.SimplePath)
        return np.round(path, decimals=5)

    def init_min_max_normalization_values(self, synset_pair):
        """
        This methods computes the minimal values (two synsets are equal) and the maximum values (two synsets are
        maximally appart in the graph) for normalization
        :param synset_pair: The Tuple of synsets that have the maximum distance in the graph
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

    def wu_and_palmer(self, synset1, synset2, normalize=False, upper_bound=1.0):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        root_node = self.germanet.root()
        lcs_nodes = synset1.lowest_common_subsumer(synset2)
        depth = 0
        for n in lcs_nodes:
            dist = n.shortest_path_distance(root_node)
            if dist > depth:
                depth = dist
        pathlen = synset2.shortest_path_distance(synset1)
        wup = (2 * depth) / (pathlen + 2 * depth)
        if normalize:
            wup = self.normalize(raw_value=wup, normalized_max=upper_bound, semrel_measure=SemRelMeasure.WuAndPalmer)
        return np.round(wup, decimals=3)

    def leacock_chodorow(self, synset1, synset2, normalize=False, upper_bound=1.0):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        lch_sim = -np.log(pathlen / (2 * self.max_depth))
        if normalize:
            lch_sim = self.normalize(raw_value=lch_sim, normalized_max=upper_bound,
                                     semrel_measure=SemRelMeasure.LeacockAndChodorow)
        return np.round(lch_sim, decimals=3)

    def normalize(self, raw_value, normalized_max, semrel_measure):
        lower_bound, upper_bound = self.normalization_dic[semrel_measure]
        return (raw_value / upper_bound) * normalized_max

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
