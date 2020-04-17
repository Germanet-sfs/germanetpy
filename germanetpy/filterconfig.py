import re
import itertools
from Levenshtein import distance
from germanetpy.synset import WordCategory, WordClass
from germanetpy.lexunit import OrthFormVariant


class Filterconfig:
    """
    This class is a configuration object, that helps to filter GermaNets lexical units and Synsets to extract the
    ones with certain interesting properties.
    """

    def __init__(self, search_string: str, ignore_case: bool = False, regex: bool = False,
                 levenshtein_distance: int = 0):
        """
        The Filterconfiguration consists of a list of word categories (as a default all existing word categories are
        selected),
        a list of word classes (as a default all existing word classes are selected), a list of orthform variants (as
        a default all existing orthform variants are selected)
        :param search_string: a String, either a query word the user is looking for or a regular expression
        :param ignore_case: a boolean, specifying whether the case of the query should be ignored or not
        :param regex: a boolean, specifying whether a regular expression is used. If a regular expression is
        specified, a given levenshtein distance will not be taken into consideration.
        :param levenshtein_distance : specify a levenshtein distance to retrieve all words that have a certain
        levenshtein distance to a given query words. Cannot be used together with a regular expression.
        """
        self._search_string = search_string
        self._word_categories = [c for c in WordCategory]
        self._word_classes = [c for c in WordClass]
        self._orth_variants = [o for o in OrthFormVariant]
        self._ignore_case = ignore_case
        self._regex = regex
        self._levenshtein_distance = levenshtein_distance

    def filter_lexunits(self, germanet) -> set:
        """
        Applys the filter to the GermaNet data
        :type germanet: Germanet
        :param germanet: the GermaNet object, loaded from the data
        :return: a set of lexical units that are left after retrieval is filtered with the given
        constraints
        """
        result = set()
        if self.regex:
            lexunits = self._get_lexunits_by_regex(germanet)
        elif not self.regex and self.levenshtein_distance > 0:
            lexunits = self._filter_lexunits_levenshtein(germanet)
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

    def _filter_lexunits_orthform(self, lexunits, orthvariants, searchstring: str, ignore_case: bool) -> set:
        """
        The method filters the retrieved lexical units to match the user-specified orth variants
        :type orthvariants: list(OrthVariant)
        :type lexunits: set(Lexunit)
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

    def filter_synsets(self, germanet) -> set:
        """
        Applys the filter to the GermaNet data
        :type germanet: Germanet
        :param germanet: the GermaNet object, loaded from the data
        :return: a set of synsets that are left after retrieval is filtered with the given constraints
        """
        result = set()
        if self.regex:
            lexunits = self._get_lexunits_by_regex(germanet)
        elif self.levenshtein_distance > 0 and not self.regex:
            lexunits = self._filter_lexunits_levenshtein(germanet)
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

    def _get_lexunits_by_regex(self, germanet) -> set:
        """
        Filters lexical units with a regular expression. All lexical units that match the regular expression are
        returned.
        :type germanet: Germanet
        :param germanet: the GermaNet object, loaded from the data
        :return:  The set of lexical units that match the given regular expression
        """
        result = set()
        if self.ignore_case:
            pattern = re.compile(self.search_string.lower())
            l_ids = [germanet.lowercasedform2lexid[orthform] for orthform in germanet.lowercasedform2lexid.keys() if
                     pattern.fullmatch(orthform)]
        else:
            pattern = re.compile(self.search_string)
            l_ids = [germanet.orthform2lexid[orthform] for orthform in germanet.orthform2lexid.keys() if
                     pattern.fullmatch(orthform)]
        for id in list(itertools.chain.from_iterable(l_ids)):
            result.add(germanet.lexunits[id])
        return result

    def _filter_lexunits_levenshtein(self, germanet) -> set:
        """
        Filters lexical units with levenshtein distance. All lexical units that have a maximum of the given
        levenshtein distance or lower are returned.
        :type germanet: Germanet
        :param germanet: the GermaNet object, loaded from the data
        :return: The set of lexical units that match the given levenshtein distance
        """
        filtered_lexunits = set()
        for cat in self.word_categories:
            units = germanet.get_lexunits_by_wordcategory(category=cat)
            for unit in units:
                if unit.synset.word_class in self.word_classes:
                    for orthvar in self.orth_variants:
                        form = unit.get_orthform_variant(orthvar)
                        if form:
                            if self.ignore_case:
                                form = form.lower()
                                self._search_string = self.search_string.lower()
                            d = distance(form, self.search_string)
                            if d <= self.levenshtein_distance:
                                filtered_lexunits.add(unit)
        return filtered_lexunits

    @property
    def search_string(self):
        return self._search_string

    @property
    def word_categories(self):
        return self._word_categories

    @property
    def word_classes(self):
        return self._word_classes

    @property
    def orth_variants(self):
        return self._orth_variants

    @property
    def ignore_case(self):
        return self._ignore_case

    @property
    def regex(self):
        return self._regex

    @property
    def levenshtein_distance(self):
        return self._levenshtein_distance

    @word_classes.setter
    def word_classes(self, word_classes):
        self._word_classes = word_classes

    @word_categories.setter
    def word_categories(self, word_categories):
        self._word_categories = word_categories

    @orth_variants.setter
    def orth_variants(self, orth_variants):
        self._orth_variants = orth_variants
