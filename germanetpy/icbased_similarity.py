import os
import sys
from pathlib import Path
import numpy as np
from germanetpy.synset import WordCategory
from germanetpy.filterconfig import Filterconfig


class ICBasedSimilarity:
    """
    These measure are computed based on relative frequencies of words in a large corpus. Synset frequencies are computed
    by adding up the frequencies of all words that belong to a synset. These measures can be computed between synsets
    with different word categories
    """

    def __init__(self, germanet):
        """
        The constructor of the ICBasedSimilarity class. The frequency dictionary for each word category are initialized.
        The *jcnmaxdist* is twice the IC of two leaf nodes with the highest IC (MAX _IC ), whose LCS is GNROOT and is
        needed for the jiang and conraths measure. The total_freq is the frequency of ROOT, so the sum of all synset
        frequencies of the Germanet Graph. It is needed to compute the information content.
        :param germanet: The Germanet Graph
        """
        self._germanet = germanet
        self._freqdic_verbs, verb_freq = self.read_freq_dic(WordCategory.verben)
        self._freqdic_nouns, noun_freq = self.read_freq_dic(WordCategory.nomen)
        self._freqdic_adj, adj_freq = self.read_freq_dic(WordCategory.adj)
        self._total_freq = verb_freq + noun_freq + adj_freq
        self._jcnmaxdist = 2 * -np.log(1 / self.total_freq)

    def read_freq_dic(self, word_category):
        """
        Reads in the frequency list files and stores the frequency information for each synset in a dictionary. The keys
        are the synset IDs. This method also adds all available synset frequencies for the given category.
        :param word_category: [WordCategory] The word category
        :return: [dict], [int]:  A dictionary with (synset id : frequency) and the overall frequency
        """
        cumfreq = 0
        fname = str(Path(__file__).parent.parent) + "/data/freq_" + str(word_category).replace("WordCategory.",
                                                                                               "") + ".txt"
        synset2freq = {}
        if os.path.exists(fname):
            with open(fname, "r") as f:
                try:
                    for line in f:
                        parts = line.strip().split("\t")
                        freq = int(parts[1])
                        word = parts[0]
                        config = Filterconfig(word, ignore_case=False)
                        config.word_categories = [word_category]
                        lexunits = config.filter_lexunits(self.germanet)
                        if lexunits:
                            for unit in lexunits:
                                synset_id = unit.synset.id
                                if synset_id in synset2freq.keys():
                                    synset2freq[synset_id] += freq
                                else:
                                    synset2freq[synset_id] = freq
                                cumfreq += freq
                    f.close()
                except OSError:
                    print("Could not open/read file:", fname)
                    sys.exit()
        else:
            print("file %s does not exist" % fname)
        return synset2freq, cumfreq

    def _lookup_synset_freq(self, synset):
        """
        Looks up the frequency for a synset id in the corresponding dictionary. If the synset is not in the dictionary,
        the frequency is 0.
        :param synset: [Synset] The source synset
        :return: [int] The cumulated frequency for a synset.
        """
        if synset.word_category == WordCategory.nomen:
            return self.freqdic_nouns.get(synset.id, 0)
        if synset.word_category == WordCategory.verben:
            return self.freqdic_verbs.get(synset.id, 0)
        else:
            return self.freqdic_adj.get(synset.id, 0)

    def get_synset_freq(self, synset):
        """
        This method returns the cummulated frequency for a given synset. That is adding all frequencies of all words
        that are part of the given synset.
        :param synset: [Synset] the source synset
        :return: [int] the cumulated synset frequency
        """
        hyponyms = synset.all_hyponyms()
        hyponym_freqs = [self._lookup_synset_freq(hyponym) for hyponym in hyponyms]
        hyponym_freqs.append(self._lookup_synset_freq(synset))
        return sum(hyponym_freqs)

    def get_information_content(self, synset):
        """
        The information content graduates semantic concepts from general to specific. The more specific a concept, the
        smaller the probability and thus the higher its informativeness. The information content of a semantic con-
        cept is estimated by the relative frequency of the concept in a large corpus (cumulated synset frequency)
        :param synset: [Synset] the information content should be computed for
        :return: [float] the information content for the given synset
        """
        synset_freq = self.get_synset_freq(synset)
        assert synset_freq > 0, "no frequency information for this synset available"
        return -np.log(synset_freq / self.total_freq)

    def resnik(self, synset1, synset2):
        """
        Two concepts are more related the more information they share. The shared information of two
        concepts can be quantified by the information content of two concepts' lowest common subsumer.
        When several LCS are available the highest IC is returned.
        :param synset1: [Synset] The source synset
        :param synset2: [Synset] The target synset
        :return: [float]: The information content of the LCS of the two given synsets.
        """
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
        The closer smaller the difference of the information content of the two synsets, the more related they are.
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

    @property
    def germanet(self):
        return self._germanet

    @property
    def total_freq(self):
        return self._total_freq

    @property
    def freqdic_nouns(self):
        return self._freqdic_nouns

    @property
    def freqdic_verbs(self):
        return self._freqdic_verbs

    @property
    def freqdic_adj(self):
        return self._freqdic_adj

    @property
    def jcnmaxdist(self):
        return self._jcnmaxdist
