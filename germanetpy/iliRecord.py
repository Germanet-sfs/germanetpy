class IliRecord:

    def __init__(self, lexunit_id: str, ewnRelation: str, pwnWord: str, pwn20Id: str, pwn30Id: str, source: str,
                 pwn20synonyms: list, pwn20paraphrase: str = None):
        """
        This class holds an ili record object. These store a mapping between a lexical unit and the correponding
        English lexical unit (from WordNet)
        :param lexunit_id: The lexical unit id this ili record belongs to
        :param ewnRelation: WordNet relation
        :param pwnWord: word (orth form) in WordNet
        :param pwn20Id: WordNet ID (WordNet 2.0)
        :param pwn30Id: WordNet ID (WordNet 3.0)
        :param source: source of this ili record
        :param pwn20synonyms: English synonyms
        :param pwn20paraphrase: English sense definition
        """
        self._lexunit_id = lexunit_id
        self._relation = ewnRelation
        self._english_equivalent = pwnWord
        self._pwn20id = pwn20Id
        self._pwn30id = pwn30Id
        self._pwn20synonyms = pwn20synonyms
        self._pwn20paraphrase = pwn20paraphrase
        self._source = source

    def __repr__(self):
        return f'IliRecord(LexUnit ID={self.lexunit_id}, relation={self.relation}, english_equivalent={self.english_equivalent})'

    @property
    def lexunit_id(self):
        return self._lexunit_id

    @property
    def relation(self):
        return self._relation

    @property
    def english_equivalent(self):
        return self._english_equivalent

    @property
    def pwn20id(self):
        return self._pwn20id

    @property
    def pwn30id(self):
        return self._pwn30id

    @property
    def pwn20synonyms(self):
        return self._pwn20synonyms

    @property
    def pwn20paraphrase(self):
        return self._pwn20paraphrase

    @property
    def source(self):
        return self._source
