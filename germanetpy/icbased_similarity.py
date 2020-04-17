import os
import sys
import math
import numpy as np
from germanetpy.filterconfig import Filterconfig
from germanetpy.semrel_measures import SemRelMeasure


class ICBasedSimilarity:
    """
    The IC-based measures are computed based on relative frequencies of words in a large corpus. Synset frequencies
    are computed
    by adding up the frequencies of all words that belong to a Synset. These measures can not be computed between
    synsets with different word categories
    """

    def __init__(self, germanet, wordcategory, path: str, separator: str = "\t"):
        """
        The constructor of the ICBasedSimilarity class. The frequency dictionary is initialized for a given word
        category. The *jcnmaxdist* is twice the information content of two leaf nodes with the highest information
        content (MAX_IC), whose LCS is GNROOT and is needed for the jiang and conraths measure. The total_freq is the
        frequency of ROOT, so the sum of all Synset
        frequencies of the GermaNet Graph. It is needed to compute the information content.
        :type wordcategory: WordCategory
        :type germanet: Germanet
        :param germanet: The GermaNet Graph
        :param wordcategory: The word category to compute the IC-based similarities for
        :param path: The path to a frequency list containing words and their frequencies in a corpus
        :param separator: The char that separates a word and its frequency in the given frequency list,
        default is a tabulator
        """
        self._germanet = germanet
        self._synset2simplefreq = self._init_simple_freq_dic(wordcategory)
        self.create_simple_freq_dic(wordcategory, path, separator)
        self._synset2cumfreq = self.synset2simple_freq.copy()
        self._compute_cum_freq_dic()

        self._root_freq = self.synset2cumfreq[self.germanet.root.id]
        self._jcnmaxdist = 2 * -math.log10(1 / self.root_freq)

        self._synset2ic, self._most_informative_synset = self.init_ic_map()
        synset_pair = (self.most_informative_synset, self.germanet.root)
        self._normalization_dic = self.init_min_max_normalization_values(synset_pair)

    def create_simple_freq_dic(self, word_category, path: str, separator: str):
        """
        Reads in the frequency list files and stores the frequency information for each Synset in a dictionary. The keys
        are the Synset IDs. This method also adds all available Synset frequencies for the given category.
        :type word_category: WordCategory
        :param word_category: The word category
        :param path: The path to a frequency list containing words and their frequencies in a corpus
        :param separator: The char that separates a word and its frequency in the given frequency list
        """
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    for line in f:
                        parts = line.strip().split(separator)
                        # frequency of word form
                        freq = int(parts[1])
                        # word form
                        word = parts[0]
                        config = Filterconfig(word, ignore_case=False)
                        config.word_categories = [word_category]
                        synsets = config.filter_synsets(self.germanet)
                        for syn in synsets:
                            self.synset2simple_freq[syn.id] += freq
                    f.close()
                except OSError:
                    print("Could not open/read file:", path)
                    sys.exit()
        else:
            print("file %s does not exist" % path)

    def _init_simple_freq_dic(self, word_category) -> dict:
        """
        creates a dictionary of synsets of a specific word category. each synset has a default frequency of 1 (as a
        smoothing technique to avoid division by 0 when computing the information content). the root is added as a
        Synset as well
        :type word_category: WordCategory
        :param word_category: the word category
        :return: the initialized dictionary with a default frequency of 1
        """
        allsynsets_wordcat = self.germanet.get_synsets_by_wordcategory(word_category)
        allsynsets_wordcat = set([synset.id for synset in allsynsets_wordcat])
        allsynsets_wordcat.add(self.germanet.root.id)
        synset2cumfreq = dict(zip(list(allsynsets_wordcat), len(allsynsets_wordcat) * [1]))
        return synset2cumfreq

    def _compute_cum_freq_dic(self):
        """
        For each Synset in the Graph of a certain word category, add its frequency to all of its hypernyms
        """
        for synset_id, simple_freq in self.synset2simple_freq.items():
            self._cumulate(self.germanet.get_synset_by_id(synset_id), simple_freq)

    def _cumulate(self, synset, freq):
        """
        recursive method to add a simple frequency to all hypernyms of a synset
        :type freq: int
        :type synset: Synset
        :param synset: the synset to whose direct hypernyms the frequency will be added
        :param freq: the frequency
        :return: call the method until root is reached
        """
        hypernyms = synset.direct_hypernyms
        if hypernyms:
            for hypernym in hypernyms:
                self.synset2cumfreq[hypernym.id] += freq
                self._cumulate(hypernym, freq)
        else:
            return

    def init_min_max_normalization_values(self, synset_pair) -> dict:
        """
        This methods computes the minimal values (two Synsets are equal) and the maximum values (two Synsets are
        maximally apart in the graph) for normalization
        :type synset_pair: tuple(Synset, Synset)
        :param synset_pair: The Tuple of synsets that have the maximum distance in the graph
        :return: a dictionary containing the (minimum value, maximum value) for each
        semantic similarity measure.
        """
        min_res = self.resnik(synset_pair[0], synset_pair[1])
        max_res = self.resnik(synset_pair[0], synset_pair[0])
        min_lin = self.lin(synset_pair[0], synset_pair[1])
        max_lin = self.lin(synset_pair[0], synset_pair[0])
        max_jcn = self.jiang_and_conrath(synset_pair[0], synset_pair[0])
        norm_values = {
            SemRelMeasure.Resnik: (min_res, max_res),
            SemRelMeasure.Lin: (min_lin, max_lin),
            SemRelMeasure.JiangAndConrath: (0.0, max_jcn)
        }
        return norm_values

    def init_ic_map(self):
        """
        Computes the information content for each synset in GermaNet (of a given word category).
        :rtype: dict, Synset
        :return: A dictionary with a Synset and the corresponding IC, a Synset with the highest IC
        """
        synset2ic = {}
        max_ic = 0
        most_informative_synset = self.germanet.root
        for synset_id in self.synset2cumfreq.keys():
            synset = self.germanet.get_synset_by_id(synset_id)
            ic = self.get_information_content(synset)
            synset2ic[synset_id] = ic
            if ic > max_ic:
                max_ic = ic
                most_informative_synset = synset
        return synset2ic, most_informative_synset

    def get_information_content(self, synset) -> float:
        """
        The information content graduates semantic concepts from general to specific. The more specific a concept, the
        smaller the probability and thus the higher its informativeness. The information content of a semantic con-
        cept is estimated by the relative frequency of the concept in a large corpus (cumulated synset frequency)
        :type synset: Synset
        :param synset: the information content should be computed for
        :return: the information content for the given synset
        """
        assert synset.id in self.synset2cumfreq.keys(), "no frequency information for this synset available"
        synset_freq = self.synset2cumfreq[synset.id]
        return -math.log10(synset_freq / self.root_freq)

    def resnik(self, synset1, synset2, normalize: bool = False, normalized_max: float = 1.0) -> float:
        """
        Two concepts are more related the more information they share. The shared information of two
        concepts can be quantified by the information content of two concepts' lowest common subsumer.
        When several LCS are available the highest IC is returned.
        :type synset2: Synset
        :type synset1: Synset
        :param synset1: The source synset
        :param synset2: The target synset
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return: The information content of the LCS of the two given synsets.
        """
        if synset1 == synset2:
            # if the two synsets are the same, resnik is the IC of the synset
            resnik = self.get_information_content(synset1)
        else:
            lcs_list = synset1.lowest_common_subsumer(synset2)
            resnik = 0
            for lcs in lcs_list:
                ic = self.get_information_content(lcs)
                if ic > resnik:
                    resnik = ic
        if normalize:
            resnik = self.normalize(raw_value=resnik, normalized_max=normalized_max,
                                    semrel_measure=SemRelMeasure.Resnik)
        return resnik

    def jiang_and_conrath(self, synset1, synset2, normalize: float = False, normalized_max: float = 1.0) -> float:
        """
        The Jiang and Conraths measure includes knowledge about the individual information contents of each synset.
        The smaller the difference of the information content of the two synsets, the more related they are.
        :type synset1: Synset
        :type synset2: Synset
        :param synset1: The source synset
        :param synset2: The target synset
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return: The jiang and conrath relatedness measure
        """
        distance = self.get_information_content(synset1) + self.get_information_content(synset2) - 2 * self.resnik(
            synset1, synset2)
        jcn = self.jcnmaxdist - distance
        if normalize:
            jcn = self.normalize(raw_value=jcn, normalized_max=normalized_max,
                                 semrel_measure=SemRelMeasure.JiangAndConrath)
        return jcn

    def lin(self, synset1, synset2, normalize: bool = False, normalized_max: float = 1.0) -> float:
        """
        The lin measure takes the individual information contents of each synset and the information content of the
        LCS into account. The LCS with the highest information content is used for the computation.
        :type synset2: Synset
        :type synset1: Synset
        :param synset1: The source synset
        :param synset2: The target synset
        :param normalize: The relatedness value can be normalized to a number between the possible minimum of that
        measure and a given upper bound.
        :param normalized_max: The upper bound of the range the measure is normalized to.
        :return: The Lin relatedness measure
        """
        ic_lcs = self.resnik(synset1, synset2)
        lin = (2 * ic_lcs) / (self.get_information_content(synset1) + self.get_information_content(synset2))
        if normalize:
            lin = self.normalize(raw_value=lin, normalized_max=normalized_max, semrel_measure=SemRelMeasure.Lin)
        return lin

    def normalize(self, raw_value: float, normalized_max: float, semrel_measure: SemRelMeasure) -> float:
        """
        Normalizes a raw value of semantic relatedness to a value between a lower bound and the given upper bound.
        :param raw_value: The raw value
        :param normalized_max: The upper bound
        :param semrel_measure: The semantic relatedness measure, the value corresponds to.
        :return:The normalized semantic relatedness value
        """
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
    def most_informative_synset(self):
        return self._most_informative_synset

    @property
    def synset2simple_freq(self):
        return self._synset2simplefreq
