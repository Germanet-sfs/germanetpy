from somajo import Tokenizer
from nltk.stem.cistem import Cistem
from germanet import Germanet


class Lesk:
    PUNCTUATION = {'.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']',
                   '{', '}', '?', '!', '-', '–', '+', '*', '--', '\'\'', '``'}

    def __init__(self):
        self._tokenizer = Tokenizer(split_camel_case=True, token_classes=False, extra_info=False)
        self._stemmer = Cistem()

    def gloss(self, synset, germanet=True, wictionary=True):
        gloss = ""
        if germanet:
            gloss += synset.paraphrase
        if wictionary:
            for lexunit in synset.lexunits:
                for wictionary_paraphrase in lexunit.wiktionary_paraphrases:
                    gloss += wictionary_paraphrase.wiktionary_sense
        tokenized_gloss = set(self.tokenizer.tokenize(gloss))
        filtered_tokens = tokenized_gloss - self.PUNCTUATION
        return filtered_tokens

    def get_lexical_field(self, synset):
        """
        This method computes the lexical field of a lexical unit. To a lexical field belong all wordforms that are part
        of this lexical unit and all words that can be gathered by taking all related (lexically and conceptually) words
        into account.
        :return: [set(String)] a set of words defining a lexical field.
        """
        field = set()
        related_synsets = synset.relations
        for rel, items in related_synsets.items():
            for s in items:
                lexunits = s.lexunits
                [field.add(l.orthform) for l in lexunits]
        for lexunit in synset.lexunits:
            related_lexunits = lexunit.relations
            for rel, units in related_lexunits.items():
                [field.add(unit.orthform) for unit in units]
            related_lexunits = lexunit.incoming_relations
            for rel, units in related_lexunits.items():
                [field.add(unit.orthform) for unit in units]
        field.add(synset.word_class.name)
        return field

    def compute_overlap(self, synset1, synset2, stemming=True):
        lexical_field_1 = self.get_lexical_field(synset1)
        lexical_field_2 = self.get_lexical_field(synset2)

        gloss_1 = self.gloss(synset1)
        gloss_2 = self.gloss(synset2)

        field_1 = set()
        field_2 = set()
        if stemming:
            field_1.add(self.stemmer.stem(word) for word in lexical_field_1)
            field_2.add(self.stemmer.stem(word) for word in lexical_field_2)
            field_1.add(self.stemmer.stem(word) for word in gloss_1)
            field_2.add(self.stemmer.stem(word) for word in gloss_2)
        else:
            field_1 = lexical_field_1.union(gloss_1)
            field_2 = lexical_field_2.union(gloss_2)
        return len(field_1.intersection(field_2))

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def stemmer(self):
        return self._stemmer


germanet = Germanet('data')

eisen = germanet.get_lexunit_by_id('l68372')
print(eisen.get_lexical_field())
print(eisen.wiktionary_paraphrases)
eisen_set = eisen.synset
lesk = Lesk()
print(lesk.gloss(eisen_set))
