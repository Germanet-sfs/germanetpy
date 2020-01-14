class WiktionaryParaphrase:

    def __init__(self, lexunit_id, wiktionary_id, wiktionary_sense_id, wiktionary_sense, edited):
        """
        This class holds the Wictionary paraphrase object. A wictionary paraphrase can be part of lexical units. The
        contain a definition of the lexical unit which helps to differentiate between different sense of a word.
        :param lexunit_id: [String] The lexical unit id, this wictionary entry belongs to
        :param wiktionary_id: [String] The corresponding wictionary identifier
        :param wiktionary_sense_id: [int] The sense identifier
        :param wiktionary_sense: [String] The sense definition
        :param edited: [boolean] If this paraphrase was edited.
        """
        self._lexunit_id = lexunit_id
        self._wiktionary_id = wiktionary_id
        self._wiktionary_sense_id = wiktionary_sense_id
        self._wiktionary_sense = wiktionary_sense
        self._edited = edited

    def __repr__(self):
        return f'Wictionary(LexUnit ID={self.lexunit_id}, definition={self.wiktionary_sense})'

    @property
    def lexunit_id(self):
        return self._lexunit_id

    @property
    def wiktionary_id(self):
        return self._wiktionary_id

    @property
    def wiktionary_sense_id(self):
        return self._wiktionary_sense_id

    @property
    def wiktionary_sense(self):
        return self._wiktionary_sense

    @property
    def edited(self):
        return self._edited
