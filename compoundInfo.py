import fastenum


class CompoundCategory(fastenum.Enum):
    Adjektiv = 'Adjektiv'
    Nomen = 'Nomen'
    Verb = 'Verb'
    Adverb = 'Adverb'
    Präposition = 'Präposition'
    Partikel = 'Partikel'
    Pronomen = 'Pronomen'


class CompoundProperty(fastenum.Enum):
    Abkürzung = 'Abkürzung'
    Affixoid = 'Affixoid'
    Fremdwort = 'Fremdwort'
    Konfix = 'Konfix'
    Wortgruppe = 'Wortgruppe'
    Eigenname = 'Eigenname'
    opaquesMorphem = 'opaquesMorphem'
    virtuelleBildung = 'virtuelleBildung'
    gebundenesMorphem = 'gebundenesMorphem'
    freiesMorphem = 'freiesMorphem'


class CompoundInfo:
    PROPERTY = 'property'
    CATEGORY = 'category'

    def __init__(self, modifier1, head, modifier1property=None, modifier1category=None, modifier2=None,
                 modifier2property=None, modifier2category=None, headproperty=None):
        self._modifier1 = modifier1
        self._modifier1_property = modifier1property
        self._modifier1_category = modifier1category
        self._modifier2 = modifier2
        if modifier2 is not None:
            self._modifier2 = modifier2.text
        self._modifier2_property = modifier2property
        self._modifier2_category = modifier2category
        self._head = head
        self._head_property = headproperty

    def modifier1(self):
        return self._modifier1

    def modifier1_property(self):
        return self._modifier1_property

    def modifier1_category(self):
        return self._modifier1_category

    def modifier2(self):
        return self._modifier2

    def modifier2_property(self):
        return self._modifier2_property

    def modifier2_categroy(self):
        return self._modifier2_category

    def head(self):
        return self._head

    def head_property(self):
        return self._head_property
