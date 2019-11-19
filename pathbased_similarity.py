# -*- coding: iso-8859-1 -*-
import numpy as np
from synset import WordCategory, ConRel
from lexunit import LexRel
from germanet import Germanet
import re
from collections import deque


class PathBasedSimilarity:
    MAXSHORTESTPATH_NOUNS = 35
    MAXSHORTESTPATH_VERBS = 28
    MAXSHORTESTPATH_ADJ = 20

    MAXDEPTH_NOUNS = 20
    MAXDEPTH_VERBS = 15
    MAXDEPTH_ADJ = 10

    MAXLEN_HSO = 5
    HSO_REGEX = re.compile("^d*u*h*$|^d*h*u*$|^u*d*h*$|u*h*d*$|h*d*u*$|h*u*d*$")

    HORIZONTAL_RELATIONS = (
        ConRel.is_related_to, LexRel.has_antonym, LexRel.has_synonym, LexRel.has_participle, LexRel.has_pertainym
    )

    UPWARDS_RELATIONS = (
        ConRel.has_hypernym, ConRel.is_entailed_by, ConRel.has_component_holonym, ConRel.has_member_holonym,
        ConRel.has_portion_holonym, ConRel.has_substance_holonym
    )

    DOWNWARDS_RELATIONS = (
        ConRel.has_hyponym, ConRel.has_component_meronym, ConRel.has_member_meronym, ConRel.has_portion_meronym,
        ConRel.has_substance_meronym, ConRel.entails, ConRel.causes
    )

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

    def hirst_onge(self, synset1, synset2):
        lexunits_1 = synset1.lexunits()
        lexunits_2 = synset2.lexunits()
        lemmas_2 = set([lexunit.orthform().lower() for lexunit in lexunits_2])

        # conditions for a strong relationship
        strong = False
        # condition 1: if the synsets are identical, relation is strong
        if synset1 == synset2:
            return True
        # condition2 : if there is a horizontal link between the two synsets, relation is strong
        for lexunit in lexunits_1:
            related_lexunits = lexunit.relations()
            form = lexunit.orthform().lower()
            # condition 3: one word lemma is in the lemmas of the other synset
            for wordform in lemmas_2:
                if form in wordform or wordform in form:
                    return True
            for relation, units in related_lexunits.items():
                if relation in self.HORIZONTAL_RELATIONS:
                    for unit in units:
                        if unit in lexunits_2:
                            return True

        # conditions for a medium strong relationship

        return strong

    def walk(self, synset, end_synset, relations, visited):
        for relation, units in synset.relations().items():
            if relation in relations:
                for unit in units:
                    visited.add(unit)
                    if unit == end_synset:
                        return (True, visited)
        return (False, visited)

    def walk_lexrel(self, synset, end_synset, visited):
        lexunits = synset.lexunits()
        for lex in lexunits:
            for relation, units in lex.relations().items():
                if relation in self.HORIZONTAL_RELATIONS:
                    for unit in units:
                        visited.add(unit.synset())
                        if unit.synset() == end_synset:
                            return (True, visited)
        return (False, visited)

    def get_neighbours(self, synset, relations):
        related = synset.relations()
        neighbours = set()
        for rel in relations:
            if rel in related.keys():
                adjecent = related[rel]
                neighbours = neighbours.union(adjecent)
        return neighbours

    def get_neighbours_lexrel(self, synset):
        lexunits = synset.lexunits()
        neighbours = set()
        for lex in lexunits:
            for relation, units in lex.relations().items():
                if relation in self.HORIZONTAL_RELATIONS:
                    synsets = [lexunit.synset() for lexunit in units]
                    neighbours = neighbours.union(synsets)
        return neighbours

    # for one node:
    # I know all my directions
    # check directions that are still allowed and return lists of possibilities

    def get_adjacent(self, node, endnode, counter, all_paths, visited):
        """
        recursively iterate trough all neighbours of a node that are connected to a start node.
        Add a node and its path to the queue if the path is still legal. A path consists of all steps traversed from start
        to the current node with the direction, e.g uud means from the start node go two upward relations and one downward relation to reach the current node.
        A path is illegal if a direction steps needs to be taken again after the direction has already changed. For example
        udu is illegal but uud or duu is legal.
        pop the elements from the queue and call the method until the endnode is reached or the maximum distance is exceeded
        :param node:
        :param endnode:
        :param counter:
        :param all_paths:
        :return:
        """
        upwards = node[0] + "u"
        downwards = node[0] + "d"
        horizontal = node[0] + "h"
        end = False
        print("method call starts")
        print("current node")
        print(node)
        print("current queue")
        print(all_paths)
        if re.fullmatch(self.HSO_REGEX, upwards) != None:
            upwards_neighbours = self.get_neighbours(node[1], self.UPWARDS_RELATIONS)
            for neighbour in upwards_neighbours:
                if neighbour == endnode:
                    end = True
                if neighbour not in visited:
                    all_paths.append((upwards, neighbour))
                    visited.add(neighbour)
        if re.fullmatch(self.HSO_REGEX, downwards) != None:
            downward_neighbours = self.get_neighbours(node[1], self.DOWNWARDS_RELATIONS)
            for neighbour in downward_neighbours:
                if neighbour == endnode:
                    end = True
                all_paths.append((downwards, neighbour))
        if re.fullmatch(self.HSO_REGEX, horizontal) != None:
            horizontal_neighbours = self.get_neighbours(node[1], self.HORIZONTAL_RELATIONS)
            horizontal_neighbours = horizontal_neighbours.union(self.get_neighbours_lexrel(node[1]))
            for neighbour in horizontal_neighbours:
                if neighbour == endnode:
                    end = True
                if neighbour != node[1]:
                    all_paths.append((horizontal, neighbour))
        print("queue now")
        print(all_paths)

        newnode = all_paths.pop()
        counter = len(newnode[0])
        if not end and counter is not 5:
            print("new node")
            print(newnode)


            return self.get_adjacent(newnode, endnode, counter, all_paths)
        else:
            return end, all_paths, counter
    # start with an empty que and start node
    # get adjecent if match and add to que
    #

    def get_hso(self, synset1, synset2):
        counter = 0
        paths = deque()
        visited = set()
        startnode = ("", synset1)
        end, all_paths, counter = self.get_adjacent(startnode, synset2, counter, paths, visited)
        #print(counter)
        #print(all_paths)




if __name__ == '__main__':
    #p = re.compile(PathBasedSimilarity.HSO_REGEX)

    g = Germanet("./data")
    s = PathBasedSimilarity(g)


    apfelbaum = g.get_synset_by_id("s34197")
    apfel = g.get_synset_by_id("s74966")
    s.get_hso(apfelbaum, apfel)
# print(s.HORIZONTAL_RELATIONS)
# print(s.walk_lexrel(apfelbaum, apfelbaum))
