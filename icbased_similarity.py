# -*- coding: iso-8859-1 -*-
import numpy as np
from synset import WordCategory
from germanet import Germanet


class ICBasedSimilarity:

    def __init__(self, germanet):

        self._germanet = germanet
        self._freq_dic, self._cumfreq = self.read_freq_dic()

    def read_freq_dic(self):
        freq_dic = {}
        categories = ["adj", "verbs", "nouns"]
        for cat in categories:
            for line in open("data/freq_" + cat + ".txt", "r"):
                parts = line.strip().split("\t")
                freq = parts[0]
                word = parts[1]
                if word not in freq_dic:
                    freq_dic[word] = freq
        germanet_freqs = {}
        cumfreq = 0
        for unit in self.germanet.lexunits.values():
            word = unit.orthform.lower()
            if word in freq_dic.keys():
                frequency = freq_dic[word]
                germanet_freqs[word] = int(frequency)
                cumfreq += int(frequency)
        return germanet_freqs, cumfreq

    def get_synset_freq(self, synset):
        hyponyms = synset.all_hyponyms()
        cumfreq = 0
        for hyponym in hyponyms:
            word_frequencies = [self.freq_dic[unit.orthform.lower()] for unit in hyponym.lexunits if
                                unit.orthform.lower() in self.freq_dic.keys()]
            cumfreq += sum(word_frequencies)
        word_frequencies = [self.freq_dic[unit.orthform.lower()] for unit in synset.lexunits if
                            unit.orthform.lower() in self.freq_dic.keys()]
        cumfreq += sum(word_frequencies)
        return cumfreq

    def get_IC(self, synset):
        synset_freq = self.get_synset_freq(synset)
        assert synset_freq > 0, "no frequency information for this synset available"
        return -np.log(synset_freq / self.cumfreq)

    def res(self, synset1, synset2):
        lcs_list = synset1.lowest_common_subsumer(synset2)
        current_IC = 0
        for lcs in lcs_list:
            ic = self.get_IC(lcs)
            if ic > current_IC:
                current_IC = ic
        return current_IC

    def jcn(self, synset1, synset2):
        jcnmaxdist = 2 * -np.log(1 / self.cumfreq)
        distance = self.get_IC(synset1) + self.get_IC(synset2) - 2 * self.res(synset1, synset2)
        return jcnmaxdist - distance

    def lin(self, synset1, synset2):
        ic_lcs = self.res(synset1, synset2)
        return (2 * ic_lcs) / (self.get_IC(synset1) + self.get_IC(synset2))

    @property
    def germanet(self):
        return self._germanet

    @property
    def cumfreq(self):
        return self._cumfreq

    @property
    def freq_dic(self):
        return self._freq_dic


if __name__ == '__main__':
    g = Germanet("./data")
    s = ICBasedSimilarity(g)
    print(s.cumfreq)
    apfel = g.get_synset_by_id("s39494")
    apfelbaum = g.get_synset_by_id("s39183")
    print(apfelbaum, apfel)
    print(s.get_synset_freq(apfel))
    print(s.get_IC(apfel))
    print(s.get_IC(apfelbaum))
    print(s.res(apfel, apfelbaum))
    print(s.jcn(apfel, apfelbaum))
    print(s.lin(apfel, apfelbaum))
