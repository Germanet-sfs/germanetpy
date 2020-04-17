from germanetpy.compoundInfo import CompoundInfo, CompoundCategory, CompoundProperty
from germanetpy.lexunit import Lexunit, LexRel
from germanetpy.synset import Synset, WordCategory, WordClass
from germanetpy.utils import convert_to_boolean

# Lexunit xml attribute values
LEXID = 'id'
SENSE = 'sense'
SOURCE = 'source'
NAMEDENTITY = 'namedEntity'
STYLE = 'styleMarking'
ARTIFICIAL = 'artificial'
ORTHFORM = 'orthForm'
ORTHVAR = 'orthVar'
OLDORTHFORM = 'oldOrthForm'
OLDORTHVAR = 'oldOrthVar'
COMPOUND = 'compound'
FRAME = 'frame'
EXAMPLE = 'example'
LEXUNIT = "lexUnit"

# Synset xml attribute values
SYNID = 'id'
WORDCLASS = 'class'
WORDCATEGORY = 'category'


def get_attribute_element(attributes, element: str, enum):
    """
    Constructs an Emum object of a given attribute
    :rtype: FastEnum
    :type enum: FastEnum
    :type attributes: XML attributes
    :param attributes: XML attributes of a certain XML node
    :param elment: A String
    :param enum: The Enum object that should be initialized
    :return: The corresponding Enum object or None
    """
    if element in attributes:
        return enum[attributes[element]]
    return None


def create_compound_info(child) -> CompoundInfo:
    """
    Creates a compound info object. This has a modifier (String) and a head (String). Each modifier and the head can
    have a property (CompoundProperty) and a category (CompoundCategory).
    :param child: the XML element
    :return: A CompoundInfo object
    """
    assert len(child) > 0, "wrong data format"
    modifier1 = child[0]
    modifier1prop = get_attribute_element(modifier1.attrib, CompoundInfo.PROPERTY, CompoundProperty)
    modifier1cat = get_attribute_element(modifier1.attrib, CompoundInfo.CATEGORY, CompoundCategory)
    modifier2 = modifier2prop = modifier2cat = None
    if len(child) == 3:
        modifier2 = child[1]
        head = child[2]

        modifier2cat = get_attribute_element(modifier2.attrib, CompoundInfo.CATEGORY, CompoundCategory)
        modifier2prop = get_attribute_element(modifier2.attrib, CompoundInfo.PROPERTY, CompoundProperty)
    else:
        head = child[1]
    headprop = get_attribute_element(head.attrib, CompoundInfo.PROPERTY, CompoundProperty)
    compound = CompoundInfo(modifier1.text, head.text, modifier1prop, modifier1cat, modifier2, modifier2prop,
                            modifier2cat, headprop)
    return compound


def load_lexunits(germanet, tree):
    """
    Takes the XML tree and walks trough it to create the Lexunit objects.
    :type tree: Element Tree
    :type germanet: Germanet
    :param germanet: the germanet object
    :param tree: XML tree
    """
    root = tree.getroot()
    for child in root:
        attribute = child.attrib
        syn_id = attribute[SYNID]
        category = get_attribute_element(attribute, WORDCATEGORY, WordCategory)
        word_class = get_attribute_element(attribute, WORDCLASS, WordClass)
        synset = Synset(syn_id, category, word_class)
        germanet.synsets[synset.id] = synset

        for sub_child in child:
            if sub_child.tag == LEXUNIT:
                lexunit = create_lexunit(germanet, sub_child.attrib, sub_child, synset)
                germanet.lexunits[lexunit.id] = lexunit
                germanet.wordcat2lexid[category.name].add(lexunit.id)
                germanet.wordclass2lexid[word_class.name].add(lexunit.id)
                synset.add_lexunit(lexunit)
        for unit in synset.lexunits:
            for lexunit in synset.lexunits:
                if lexunit is not unit:
                    unit.relations[LexRel.has_synonym].add(lexunit)


def create_lexunit(germanet, attributes, lex_root, synset) -> Lexunit:
    """
    Given the XML data, creates a Lexunit object.
    :type attributes: XML attributes
    :type germanet: Germanet
    :param germanet: The germanet object.
    :param attributes: The XML attributes.
    :param lex_root: The XML root
    :param synset: the corresponding synset object
    :return: a lexical unit object
    """
    lex_id = attributes[LEXID]
    lex_sense = int(attributes[SENSE])
    lex_source = attributes[SOURCE]
    lex_named_entity = convert_to_boolean(attributes[NAMEDENTITY])
    lex_artificial = convert_to_boolean(attributes[ARTIFICIAL])
    lex_style = convert_to_boolean(attributes[STYLE])
    lexunit = Lexunit(id=lex_id, sense=lex_sense, source=lex_source, named_entity=lex_named_entity, synset=synset,
                      artificial=lex_artificial, style_marking=lex_style)
    for child in lex_root:
        tag = child.tag
        child_value = child.text
        if tag == COMPOUND:
            compound = create_compound_info(child)
            lexunit._compound_info = compound
            germanet.compounds.add(lexunit)
        elif "rth" in tag:
            add_orth_forms(germanet, lexunit, child_value, tag)
        elif tag == FRAME:
            lexunit.frames.append(child_value)
            for f in lexunit.frames:
                germanet.frames2lexunits[f].add(lexunit)
        elif tag == EXAMPLE:
            example = child[0].text
            lexunit.examples.append(example)
            if len(child) == 2:
                exframe = child[1].text
                lexunit.frames2examples[exframe].add(example)
    return lexunit


def add_orth_forms(germanet, lexunit: Lexunit, child_value: str, tag: str):
    """
    Checks which orthform the tag contains, and adds it to the lexunit object. Adds the lexunit id to the
    corresponding dictionary.
    :type germanet: Germanet
    :param germanet: The germanet object containing the Orthform variant dictionaries.
    :param lexunit: the Lexunit object the Orthform variant needs to be added to
    :param child_value:  the value of the XML element that contains this Orthform variant
    :param tag: the value of the XML tag specifying the type of Orthform variant
    """
    germanet.orthform2lexid[child_value].add(lexunit.id)
    germanet.lowercasedform2lexid[child_value.lower()].add(lexunit.id)

    if tag == ORTHFORM:
        lexunit._orthform = child_value
        germanet.mainOrtform2lexid[child_value].add(lexunit.id)
    elif tag == ORTHVAR:
        lexunit._orthvar = child_value
    elif tag == OLDORTHFORM:
        lexunit._old_orthform = child_value
    elif tag == OLDORTHVAR:
        lexunit._old_orthvar = child_value
