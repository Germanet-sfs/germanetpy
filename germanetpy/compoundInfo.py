# -*- coding: iso-8859-1 -*-
import fastenum


class CompoundCategory(fastenum.Enum):
    """This Enum represents the syntactic wordcategory a modifier of a compound can belong to."""
    Adjektiv = 'Adjektiv'
    Nomen = 'Nomen'
    Verb = 'Verb'
    Adverb = 'Adverb'
    Präposition = 'Präposition'
    Partikel = 'Partikel'
    Pronomen = 'Pronomen'


class CompoundProperty(fastenum.Enum):
    """This Enum represents the properties a compound constituent can have."""
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
    nominalisiertesVerb = 'nominalisiertesVerb'

class CompoundInfo:
    PROPERTY = 'property'
    CATEGORY = 'category'
    XML_LEX_UNIT_ID = 'lexUnitId'
    XML_LEX_UNIT_ID2 = 'lexUnitId2'
    XML_LEX_UNIT_ID3 = 'lexUnitId3'

    def __init__(self, modifier1, head, modifier2=None, modifier1property=None, modifier1category=None,
                 mod1LexUnitId1=None, mod1LexUnitId2=None, mod1LexUnitId3=None, modifier2property=None, 
                 modifier2category=None, mod2LexUnitId1=None, mod2LexUnitId2=None, mod2LexUnitId3=None, 
                 headproperty=None, headLexUnitId=None):
        """
        This class stores information about a special linguistic entity in German - a compound. A compound
        consists
        of two constituents, a modifier and a head. The head will always be a noun, the modifier can stem from
        a noun,
        a verb or an adjective. Sometimes the modifier can be derived from different words, for example:
        Laufband - modifier: laufen or Lauf. This class stores both possibilities as modifier1 and modifier2.

        :type headproperty: String
        :type modifier2category: WordCategory
        :type modifier2property: String
        :type modifier2: String
        :type modifier1category: WordCategory
        :type modifier1property: String
        :type head: String
        :type modifier1: String
        :param modifier1: A String that represents the modifier (or one possibility). Example: 'Laufband' -
        modifier1:
        'laufen'
        :param head: A String that represents the head. Example: 'Laufband' - head: 'Band'
        :param modifier1property: A String that represents the property of the first modifier variant,
        e.g. if it is
        an Affixoid
        :param modifier1category: The category of the modifier, example: 'laufen' = Verb
        :param modifier2:  A String that represents the modifier (or second possibility). Example: 'Laufband' -
        modifier2:
        'Lauf'
        :param modifier2property: A String that represents the property of the second modifier variant
        :param modifier2category: The category of the second modifier variant, example: 'Lauf' = Nomen
        :param headproperty: A String that represents the property of the head
        """
        self._modifier1 = modifier1
        self._modifier1_property = modifier1property
        self._modifier1_category = modifier1category
        if mod1LexUnitId1 is not None:
            self._mod1_LexUnitId1 = mod1LexUnitId1
        if mod1LexUnitId1 is not None:
            self._mod1_LexUnitId2 = mod1LexUnitId2
        if mod1LexUnitId1 is not None:
            self._mod1_LexUnitId3 = mod1LexUnitId3
        self._modifier2 = modifier2
        if modifier2 is not None:
            self._modifier2 = modifier2.text
        self._modifier2_property = modifier2property
        self._modifier2_category = modifier2category
        if mod2LexUnitId1 is not None:
            self._mod2_LexUnitId1 = mod2LexUnitId1
        if mod2LexUnitId1 is not None:
            self._mod2_LexUnitId2 = mod2LexUnitId2
        if mod2LexUnitId1 is not None:
            self._mod2_LexUnitId3 = mod2LexUnitId3
        self._head = head
        self._head_property = headproperty
        if headLexUnitId is not None:
            self._head_LexUnitId = headLexUnitId

    def __repr__(self):
        return f'CompoundInfo( modifier = {self.modifier1}, head = {self.head})'

    @property
    def modifier1(self):
        return self._modifier1

    @property
    def modifier1_property(self):
        return self._modifier1_property

    @property
    def modifier1_category(self):
        return self._modifier1_category
        
    @property
    def mod1_LexUnitId1(self):
        return self._mod1_LexUnitId1
        
    @property
    def mod1_LexUnitId2(self):
        return self._mod1_LexUnitId2
        
    @property
    def mod1_LexUnitId3(self):
        return self._mod1_LexUnitId3

    @property
    def modifier2(self):
        return self._modifier2

    @property
    def modifier2_property(self):
        return self._modifier2_property

    @property
    def modifier2_category(self):
        return self._modifier2_category
        
    @property
    def mod2_LexUnitId1(self):
        return self._mod2_LexUnitId1
        
    @property
    def mod2_LexUnitId2(self):
        return self._mod2_LexUnitId2
        
    @property
    def mod2_LexUnitId3(self):
        return self._mod2_LexUnitId3

    @property
    def head(self):
        return self._head

    @property
    def head_property(self):
        return self._head_property

    @property
    def head_LexUnitId(self):
        return self._head_LexUnitId