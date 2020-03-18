import os
import sys
from pathlib import Path
import math
from germanetpy.synset import WordCategory
from germanetpy.filterconfig import Filterconfig
import numpy as np
from germanetpy.semrel_measures import SemRelMeasure


class ICBasedSimilarity:
    """
    These measure are computed based on relative frequencies of words in a large corpus. Synset frequencies are computed
    by adding up the frequencies of all words that belong to a synset. These measures can be computed between synsets
    with different word categories
    """

    def __init__(self, germanet, wordcategory):
        """
        The constructor of the ICBasedSimilarity class. The frequency dictionary for each word category are initialized.
        The *jcnmaxdist* is twice the IC of two leaf nodes with the highest IC (MAX _IC ), whose LCS is GNROOT and is
        needed for the jiang and conraths measure. The total_freq is the frequency of ROOT, so the sum of all synset
        frequencies of the Germanet Graph. It is needed to compute the information content.
        :param germanet: The Germanet Graph
        """
        self._germanet = germanet
        self._synset2cumfreq = self._init_cumfreq_dic(wordcategory)
        self.read_freq_dic(wordcategory)
        self._root_freq = self.synset2cumfreq[self.germanet.root.id]
        self._jcnmaxdist = 2 * -math.log10(1 / self.root_freq)

        self._synset2ic, self._most_informative_lcs = self.init_ic_map()
        print("most informative synset that can be lcs : ")
        print(self.most_informative_lcs)
        print("IC of root : ")
        print(self.synset2ic[self.germanet.root.id])
        synset_pair = (self.most_informative_lcs, self.germanet.root)
        self._normalization_dic = self.init_min_max_normalization_values(synset_pair)
        print(self.normalization_dic)

    def read_freq_dic(self, word_category):
        """
        Reads in the frequency list files and stores the frequency information for each synset in a dictionary. The keys
        are the synset IDs. This method also adds all available synset frequencies for the given category.
        :param word_category: [WordCategory] The word category
        :return: [dict], [int]:  A dictionary with (synset id : frequency) and the overall frequency
        """
        fname = str(Path(__file__).parent.parent) + "/data/freq_" + str(word_category).replace("WordCategory.",
                                                                                               "") + ".txt"
        # dublicates = {"s100884", "s103294", "s63247", "s65510", "s72107", "s92539", "s53033", "s3109", "s310"}
        duplicates = {"l112255", "ll506", "l4545", "l123935", "l88444"}
        if os.path.exists(fname):
            with open(fname, "r") as f:
                try:
                    for line in f:
                        parts = line.strip().split("\t")
                        # frequency of word form
                        freq = int(parts[1])
                        # word form
                        word = parts[0]
                        # extract all lexunits that have that wordform
                        config = Filterconfig(word, ignore_case=False)
                        config.word_categories = [word_category]
                        lexunits = config.filter_lexunits(self.germanet)
                        # for each lexunit retrieve the corresponding synset
                        if lexunits:
                            for unit in lexunits:
                                if unit.id not in duplicates:
                                    self._update_synset_freq(unit.synset, freq)
                    f.close()
                except OSError:
                    print("Could not open/read file:", fname)
                    sys.exit()
        else:
            print("file %s does not exist" % fname)

    def _init_cumfreq_dic(self, word_category):
        allsynsets_wordcat = self.germanet.get_synsets_by_wordcategory(word_category)
        allsynsets_wordcat = set([synset.id for synset in allsynsets_wordcat])
        allsynsets_wordcat.add(self.germanet.root.id)
        synset2cumfreq = dict(zip(list(allsynsets_wordcat), len(allsynsets_wordcat) * [1]))
        return synset2cumfreq

    def _update_synset_freq(self, synset, freq):
        hypernyms = synset.all_hypernyms()
        # add freq to synset
        self.synset2cumfreq[synset.id] += freq
        # add frequency to each hypernym
        for hyper in hypernyms:
            self.synset2cumfreq[hyper.id] += freq

    def init_min_max_normalization_values(self, synset_pair):
        """
        This methods computes the minimal values (two synsets are equal) and the maximum values (two synsets are
        maximally appart in the graph) for normalization
        :param synset_pair: The Tuple of synsets that have the maximum distance in the graph
        :return: a dictionary [SemRelMeasure : (int, int)] containing the (minimum value, maximum value) for each
        semantic similarity measure.
        """
        min_res = self.resnik(synset_pair[0], synset_pair[1])
        max_res = self.resnik(synset_pair[0], synset_pair[0])
        min_lin = self.lin(synset_pair[0], synset_pair[1])
        max_lin = self.lin(synset_pair[0], synset_pair[0])
        min_jcn = self.jiang_and_conrath(synset_pair[0], synset_pair[1])
        max_jcn = self.jiang_and_conrath(synset_pair[0], synset_pair[0])
        norm_values = {
            SemRelMeasure.Resnik: (min_res, max_res),
            SemRelMeasure.Lin: (min_lin, max_lin),
            SemRelMeasure.JiangAndConrath: (min_jcn, max_jcn)
        }
        return norm_values

    def init_ic_map(self):
        synset2ic = {}
        max_ic = 0
        most_informative_lcs = self.germanet.root
        for synset_id in self.synset2cumfreq.keys():
            synset = self.germanet.get_synset_by_id(synset_id)
            ic = self.get_information_content(synset)
            synset2ic[synset_id] = ic
            if len(synset.direct_hyponyms) >= 2:
                if ic > max_ic:
                    max_ic = ic
                    most_informative_lcs = synset
        return synset2ic, most_informative_lcs

    def get_information_content(self, synset):
        """
        The information content graduates semantic concepts from general to specific. The more specific a concept, the
        smaller the probability and thus the higher its informativeness. The information content of a semantic con-
        cept is estimated by the relative frequency of the concept in a large corpus (cumulated synset frequency)
        :param synset: [Synset] the information content should be computed for
        :return: [float] the information content for the given synset
        """
        assert synset.id in self.synset2cumfreq.keys(), "no frequency information for this synset available"
        synset_freq = self.synset2cumfreq[synset.id]
        return -math.log10(synset_freq / self.root_freq)

    def resnik(self, synset1, synset2):
        """
        Two concepts are more related the more information they share. The shared information of two
        concepts can be quantified by the information content of two concepts' lowest common subsumer.
        When several LCS are available the highest IC is returned.
        :param synset1: [Synset] The source synset
        :param synset2: [Synset] The target synset
        :return: [float]: The information content of the LCS of the two given synsets.
        """
        if synset1 == synset2:
            # if the two synsets are the same, return the IC of the synset
            return self.get_information_content(synset1)
        lcs_list = synset1.lowest_common_subsumer(synset2)
        current_IC = 0
        for lcs in lcs_list:
            ic = self.get_information_content(lcs)
            if ic > current_IC:
                current_IC = ic
        return current_IC

    def jiang_and_conrath(self, synset1, synset2):
        """
        The Jiang and Conraths measure includes knowledge about the individual information contents of each synset.
        The smaller the difference of the information content of the two synsets, the more related they are.
        :param synset1: [Synset] The source synse
        :param synset2: [Synset] The target synset
        :return: [float]: The jiang and conrath relatedness measure
        """
        distance = self.get_information_content(synset1) + self.get_information_content(synset2) - 2 * self.resnik(
            synset1, synset2)
        return self.jcnmaxdist - distance

    def lin(self, synset1, synset2):
        """
        The lin measure takes the individual information contents of each synset and the information conent of the
        LCS into account. The LCS with the highest information content is used for the computation.
        :param synset1: [Synset] The source synset
        :param synset2: [Synset] The target synset
        :return: [float]: The Lin relatedness measure
        """
        ic_lcs = self.resnik(synset1, synset2)
        return (2 * ic_lcs) / (self.get_information_content(synset1) + self.get_information_content(synset2))

    def normalize(self, raw_value, normalized_max, semrel_measure):
        lower_bound, upper_bound = self.normalization_dic[semrel_measure]
        return np.round(((raw_value - lower_bound) / (upper_bound - lower_bound)) * normalized_max, decimals=5)

    @property
    def germanet(self):
        return self._germanet

    @property
    def root_freq(self):
        return self._root_freq

    @property
    def synset2cumfreq(self):
        return self._synset2cumfreq

    @property
    def jcnmaxdist(self):
        return self._jcnmaxdist

    @property
    def normalization_dic(self):
        return self._normalization_dic

    @property
    def synset2ic(self):
        return self._synset2ic

    @property
    def most_informative_lcs(self):
        return self._most_informative_lcs


if __name__ == '__main__':
    from germanetpy.germanet import Germanet

    germanet_data = Germanet("/Users/nwitte/PycharmProjects/germanetpy/data")

    ic = ICBasedSimilarity(germanet_data, WordCategory.nomen)
    ic = ICBasedSimilarity(germanet_data, WordCategory.verben)
    ic = ICBasedSimilarity(germanet_data, WordCategory.adj)
