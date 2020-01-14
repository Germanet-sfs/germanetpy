import re
import itertools
from germanetpy.synset import WordCategory, WordClass
from germanetpy.lexunit import OrthFormVariant


class Filterconfig:
    """
    This class is a configuration object, that helps to filter germanets lexical units and synsets to extract the
    ones with certain interesting properties.
    """

    def __init__(self, search_string, ignore_case=False, regex=False):
        """
        The Filterconfiguration consists of a list of word categories (as a default all existing word categories are
        selected),
        a list of word classes (as a default all existing word classes are selected), a list of orthform variants (as
        a default all existing orthform variants are selected)
        :param search_string: a String, either a word the user is looking for or a regular expression
        :param ignore_case: a boolean, specifying whether the case of the query should be ignored or not
        :param regex: a boolean, specifying whether a regular expression is used
        """
        self.search_string = search_string
        self.word_categories = [c for c in WordCategory]
        self.word_classes = [c for c in WordClass]
        self.orth_variants = [o for o in OrthFormVariant]
        self.ignore_case = ignore_case
        self.regex = regex

    def filter_lexunits(self, germanet):
        """
        Applys the filter to the germanet data
        :param germanet: the germanet object, loaded from the data
        :return: a set of lexical units that are left after retrieval is filtered with the given constraints
        """
        result = set()
        if self.regex:
            lexunits = self._get_lexunits_by_regex(germanet)
        else:
            lexunits = germanet.get_lexunits_by_orthform(self.search_string, self.ignore_case)
            lexunits = self._filter_lexunits_orthform(lexunits, self.orth_variants, self.search_string,
                                                      self.ignore_case)

        for unit in lexunits:
            if (unit.synset.word_class in self.word_classes) and (unit.synset.word_category in
                                                                      self.word_categories) and \
                    self.search_string:
                result.add(unit)
        return result

    def _filter_lexunits_orthform(self, lexunits, orthvariants, searchstring, ignore_case):
        """
        The method filters the retrieved lexical units to match the user-specified orth variants
        :param lexunits: the set if lexical units to be filtered by orth variant
        :param orthvariants: a list of oth variants that should be considered during filtering
        :param searchstring: the search query
        :param ignore_case: boolean, if case should be ignored or not
        :return: a set if lexical units, all lexical units match the given orth variants
        """
        filtered_units = set()
        for unit in lexunits:
            for orthvar in orthvariants:
                form = unit.get_orthform_variant(orthvar)
                if form == searchstring:
                    filtered_units.add(unit)
                if ignore_case and form is not None:
                    if form.lower() == searchstring.lower():
                        filtered_units.add(unit)
        return filtered_units

    def filter_synsets(self, germanet):
        """
        Applys the filter to the germanet data
        :param germanet: the germanet object, loaded from the data
        :return: a set of synsets that are left after retrieval is filtered with the given constraints
        """
        result = set()
        if self.regex:
            lexunits = self._get_lexunits_by_regex(germanet)
        else:
            lexunits = germanet.get_lexunits_by_orthform(self.search_string, self.ignore_case)
            lexunits = self._filter_lexunits_orthform(lexunits, self.orth_variants, self.search_string,
                                                      self.ignore_case)
        synsets = [lexunit.synset for lexunit in lexunits]
        for synset in synsets:
            if (synset.word_class in self.word_classes) and (synset.word_category in
                                                               self.word_categories):
                result.add(synset)
        return result

    def _get_lexunits_by_regex(self, germanet):
        """
        Filters lexical units with a regular expression. All lexical units that match the regular expression are
        returned.
        :param germanet: the germanet object, loaded from the data
        :return: The set of lexical units that match the given regular expression
        """
        result = set()
        if self.ignore_case:
            pattern = re.compile(self.search_string.lower())
            l_ids = [germanet.lowercasedform2lexid[orthform] for orthform in germanet.lowercasedform2lexid.keys() if
                     pattern.search(orthform)]
        else:
            pattern = re.compile(self.search_string)
            l_ids = [germanet.orthform2lexid[orthform] for orthform in germanet.orthform2lexid.keys() if
                     pattern.search(orthform)]
        for id in list(itertools.chain.from_iterable(l_ids)):
            result.add(germanet.lexunits[id])
        return result
