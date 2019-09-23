class WictionaryParaphrase:

    def __init__(self, lexunit_id, wiktionary_id, wiktionary_sense_id, wiktionary_sense, edited):
        self._lexunit_id = lexunit_id
        self._wiktionary_id = wiktionary_id
        self._wiktionary_sense_id = wiktionary_sense_id
        self._wiktionary_sense = wiktionary_sense
        self._edited = edited

    def get_lexunit_id(self):
        return self._lexunit_id

    def get_wiktionary_id(self):
        return self.get_wiktionary_id()

    def get_wiktionary_sense_id(self):
        return self._wiktionary_sense_id

    def get_wiktionary_sense(self):
        return self._wiktionary_sense

    def get_edited(self):
        return self._edited
