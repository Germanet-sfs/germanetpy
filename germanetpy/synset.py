from collections import defaultdict
import math
import fastenum


class ConRel(fastenum.Enum):
    """
    This Enum class contains the conceptual relations (short: ConRel) that synsets can have to other synsets.
    For a description of each relation look at
    http://www.sfs.uni-tuebingen.de/GermaNet/relations.shtml#Conceptual%20Relations
    """
    has_hypernym = 1
    has_hyponym = 2
    has_component_meronym = 3
    has_component_holonym = 4
    has_member_meronym = 5
    has_member_holonym = 6
    has_substance_meronym = 7
    has_substance_holonym = 8
    has_portion_meronym = 9
    has_portion_holonym = 10
    entails = 11
    is_entailed_by = 12
    is_related_to = 13
    causes = 14


class WordCategory(fastenum.Enum):
    """
    This Enum class contains the three part-of-speech tags (WortCategory), a Synset can have in GermaNet.
    adj = adjective, nomen = noun, verben = verb
    """
    adj = 1
    nomen = 2
    verben = 3


class WordClass(fastenum.Enum):
    """
    This Enum class contains the semantic wordclasses / semantic fields  a Synset can have in GermaNet.
    For a detailed description see:
    http://www.sfs.uni-tuebingen.de/GermaNet/germanet_structure.shtml#Tops
    """
    Allgemein = 1
    Bewegung = 2
    Gefuehl = 3
    Geist = 4
    Gesellschaft = 5
    Koerper = 6
    Menge = 7
    natPhaenomen = 8
    Ort = 9
    Pertonym = 10
    Perzeption = 11
    privativ = 12
    Relation = 13
    Substanz = 14
    Verhalten = 15
    Zeit = 16
    Artefakt = 17
    Attribut = 18
    Besitz = 19
    Form = 20
    Geschehen = 21
    Gruppe = 22
    Kognition = 23
    Kommunikation = 24
    Mensch = 25
    Motiv = 26
    Nahrung = 27
    natGegenstand = 28
    Pflanze = 29
    Tier = 30
    Tops = 31
    Koerperfunktion = 32
    Konkurrenz = 33
    Kontakt = 34
    Lokation = 35
    Schoepfung = 36
    Veraenderung = 37
    Verbrauch = 38


class Synset:
    """
    This class holds a Synset object. A synset in GermaNet contains several lexical units and holds specific relations
    to other synsets, for example a synset can have hypernyms or hyponyms.
    """

    def __init__(self, id, word_category, word_class):
        """

        :param id: [String] Every synset has a unique identifier.
        :param word_category: [WordCategory] Every synset has exactly one part-of-speech
        :param word_class: [WordClass] Every synset has exactly one semantic class
        """
        self._id = id
        self._word_category = word_category
        self._word_class = word_class
        self._paraphrase = ""
        self._lexunits = []
        self._relations = defaultdict(set)
        self._incoming_relations = defaultdict(set)
        self._direct_hypernyms = self._relations[ConRel.has_hypernym]
        self._direct_hyponyms = self._relations[ConRel.has_hyponym]

    def __repr__(self):
        lexunit_list = [f'{unit.orthform}' for unit in self._lexunits]
        lexunit_str = ', '.join(lexunit_list)
        return f'Synset(id={self._id}, lexunits={lexunit_str})'

    def add_lexunit(self, unit):
        """
        Adds a lexical unit that part of this synset to the list of lexical units
        :param unit: The lexUnit object to be added
        """
        self._lexunits.append(unit)

    def is_root(self):
        """
        :return: True if this Synset is the root of the Graph (= has no hypernyms), otherwise false
        """
        return True if len(self._direct_hypernyms) == 0 else False

    def is_leaf(self):
        """
        :return: True if this Synset is a leaf of the Graph (= has no hyponyms), otherwise false
        """
        return True if len(self._direct_hyponyms) == 0 else False

    def num_lexunits(self):
        """
        :return: [int] The number of lexical units, contained in that synset
        """
        return len(self._lexunits)

    def hypernym_paths(self):
        """
        This method iterates recursively through the hypernyms of this synset to get all paths that connect this synset
        with the root node. a path is complete if it ends with the root node. all possible paths are returned. each
        path is a list of nodes.
        :return: A list of lists, each lists contains a node sequence connecting this synset with the root node
        """
        paths = []
        hypernyms = self._direct_hypernyms
        if self.is_root():
            paths = [[self]]
        for hypernym in hypernyms:
            for ancestor_list in hypernym.hypernym_paths():
                ancestor_list.append(self)
                paths.append(ancestor_list)
        return paths

    def all_hypernyms(self):
        """
        This method extracts all hypernyms for this synset (the transitive closure for this synset)
        :return: a set, containing all possible hypernym nodes. it is empty if the current synset is the root node
        """
        hypernyms = []
        for path in self.hypernym_paths():
            for synset in path:
                if synset is not self:
                    hypernyms.append(synset)
        return set(hypernyms)

    def hyponym_paths(self):
        """
        This method iterates recursively through the hyponyms of this synset to get all paths that connect
        this synset with a leaf node. A path is complete if it ends with a leaf node. All possible paths are
        returned. Each path is a list of nodes.
        :return: A list of lists, each lists contains a node sequence connecting this synset with a leaf node
                """
        paths = []
        hyponyms = self._direct_hyponyms
        if self.is_leaf():
            paths = [[self]]
        for hyponym in hyponyms:
            for ancestor_list in hyponym.hyponym_paths():
                ancestor_list.append(self)
                paths.append(ancestor_list)
        return paths

    def all_hyponyms(self):
        """
        This method returns all possible hyponyms of this synset.
        :return: [set(Synset)] A set of synset nodes, each constitutes a hyponym of the current synset.
        """
        hyponyms = []
        for path in self.hyponym_paths():
            for synset in path:
                if synset is not self:
                    hyponyms.append(synset)
        return set(hyponyms)

    def shortest_path_to_root(self):
        """
        This method returns the shortest path to the root node.
        :return: [list(Synset)] shortest path to the root node.
        """
        paths = self.hypernym_paths()
        shortest = paths.index(min([len(path) for path in paths]))
        return paths[shortest]

    def common_hypernyms(self, other):
        """
        Given another synset, this method computes shared hypernyms
        :param other: another synset object
        :return: [set(Synset)] a set of synset nodes, that denotes the shared hypernyms between this synset and the
        given one.
        """
        return set(self.all_hypernyms()).intersection(set(other.all_hypernyms()))

    def min_depth(self):
        """
        :return: [int] The length of the shortest hypernym path from this
        synset to the root.
        """

        hypernyms = self._relations[ConRel.has_hypernym]
        if not hypernyms:
            min_depth = 0
        else:
            min_depth = 1 + min(h.min_depth() for h in hypernyms)
        return min_depth

    def shortest_path_distance(self, other):
        """
        Returns the distance of the shortest path linking the two synsets (if
        one exists). If a node is compared with itself 0 is returned. The distance is denoted by the number of edges
        that exist in the shortest path.

        :type other: Synset
        :param other: The Synset to which the shortest path will be found.
        :return: [int] The number of edges in the shortest path connecting the two
            nodes, or None if no path exists.
        """
        if self == other:
            return 0

        paths = self.shortest_path(other)
        return None if paths == [] else len(paths[0]) - 1

    def shortest_path(self, other):
        """
        Returns the shortest possible sequence of synset nodes that are traversed from this synset to a given other
        synset. If there are several shortest sequences, all of then are returned.
        :param other: A synset the path should be computed to
        :return: [list(list(Synset))] A list of lists, each list containing the sequence of nodes traversed from this
        synset to the given
        other synset.
        """
        shortest_paths = []
        lcs = self.lowest_common_subsumer(other)
        for subsumer in lcs:
            paths_to_lcs1 = self.shortest_path_to_hypernym(subsumer)
            paths_to_lcs2 = other.shortest_path_to_hypernym(subsumer)
            for path_to_lcs1 in paths_to_lcs1:
                for path_to_lcs2 in paths_to_lcs2:
                    current_path = path_to_lcs1
                    path_to_lcs2 = path_to_lcs2[::-1]
                    for el in path_to_lcs2[1:]:
                        current_path.append(el)
                    shortest_paths.append(current_path)
        return shortest_paths

    def shortest_path_to_hypernym(self, hypernym):
        """
        The shortest path between this synset and the given hypernym. Asserts that the given other synset is a real
        hypernym of the current synset.
        :param hypernym: a synset, denoting the hypernym the shortest path should be computed to
        :return: [list(Synset)] a list of lists, each list storing the shortest sequence of synset nodes traversed
        from self to the given hypernym
        """
        if self == hypernym:
            return [[self]]
        assert hypernym in self.all_hypernyms(), "given hypernym is not a hypernym of this synset"
        shortest_path = []
        shortest = math.inf
        for path in self.hypernym_paths():
            if hypernym in path:
                index = path.index(hypernym)
                current_path = path[index:]
                path_len = len(current_path)
                if path_len <= shortest:
                    shortest = path_len
                    current_path.reverse()
                    shortest_path.append(current_path)
        shortest_dist = min([len(p) for p in shortest_path])
        shortest_path = [p for p in shortest_path if len(p) == shortest_dist]
        return shortest_path

    def lowest_common_subsumer(self, other):
        """
        Extract the lowes common subsumer(s) / lowest common ancestor(s) of the current synset and a given one.
        :param other: Another synset object the LCS should be computed to.
        :return: [set(Synset)] a set, containing one or several synset objects, being the LCS between the current
        synset and the
        given one.
        """
        lcs = set()
        if other == self:
            lcs.add(self)
            return lcs
        if other in self._direct_hypernyms or other.is_root():
            lcs.add(other)
            return lcs
        if self in other._direct_hypernyms or self.is_root():
            lcs.add(self)
            return lcs
        common_hypernyms = self.common_hypernyms(other)
        dist_dict1 = self.get_distances_hypernym_dic()
        dist_dict2 = other.get_distances_hypernym_dic()
        dist = math.inf
        for hypernym in common_hypernyms:
            dist1 = dist_dict1[hypernym]
            dist2 = dist_dict2[hypernym]
            if dist1 + dist2 < dist:
                lcs.clear()
                lcs.add(hypernym)
                dist = dist1 + dist2
            if dist1 + dist2 == dist:
                lcs.add(hypernym)
        return lcs

    def get_distances_hypernym_dic(self):
        """
        For each hypernym, store the shortest distance between the current synset and its hypernym.
        :return: [dic(Synset, int)] A dictionary containing all hypernyms of this synset as keys and the
        corresponding distances as values.
        """
        hypernym_paths = self.hypernym_paths()
        distances_dic = {}
        for p in hypernym_paths:
            for i in range(len(p)):
                hypernym = p[i]
                dist = len(p) - 1 - i
                if hypernym in distances_dic.keys():
                    current_dist = distances_dic[hypernym]
                    if dist < current_dist:
                        distances_dic[hypernym] = dist
                else:
                    distances_dic[hypernym] = dist
        return distances_dic

    @property
    def id(self):
        return self._id

    @property
    def word_category(self):
        return self._word_category

    @property
    def word_class(self):
        return self._word_class

    @property
    def paraphrase(self):
        return self._paraphrase

    @property
    def lexunits(self):
        return self._lexunits

    @property
    def relations(self):
        return self._relations

    @property
    def incoming_relations(self):
        return self._incoming_relations

    @property
    def direct_hypernyms(self):
        return self._direct_hypernyms

    @property
    def direct_hyponyms(self):
        return self._direct_hyponyms
