class IliRecord:

    def __init__(self, lexunit_id, ewnRelation, pwnWord, pwn20Id, pwn30Id, source, pwn20synonyms, pwn20paraphrase=None):
        self._lexunit_id = lexunit_id
        self._relation = ewnRelation
        self._english_equivalent = pwnWord
        self._pwn20id = pwn20Id
        self._pwn30id = pwn30Id
        self._pwn20synonyms = pwn20synonyms
        self._pwn20paraphrase = pwn20paraphrase
        self._source = source

    def lexunit_id(self):
        return self._lexunit_id

    def relation(self):
        return self._relation

    def english_equivalent(self):
        return self._english_equivalent

    def pwn20id(self):
        return self._pwn20id

    def pwn30id(self):
        return self._pwn30id

    def pwn20synonyms(self):
        return self._pwn20synonyms

    def pwn20paraphrase(self):
        return self._pwn20paraphrase

    def source(self):
        return self._source
