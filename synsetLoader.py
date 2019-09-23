from compoundInfo import CompoundInfo, CompoundCategory, CompoundProperty
from lexunit import Lexunit, LexRel
from synset import Synset, WordCategory, WordClass
from utils import convert_to_boolean

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

# Synset xml attribute values
SYNID = 'id'
WORDCLASS = 'class'
WORDCATEGORY = 'category'


def get_attribute_element(attributes, element, enum):
    """
    Constructs an Emum object of a given attribute
    :param attributes: XML attributes of a certain XML node
    :param elment: A String
    :param enum: The Enum object that should be initialized
    :return:
    """
    if element in attributes:
        return enum[attributes[element]]
    return None


def create_compound_info(child):
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
    root = tree.getroot()
    for child in root:
        attribute = child.attrib
        id = attribute[SYNID]
        category = get_attribute_element(attribute, WORDCATEGORY, WordCategory)
        word_class = get_attribute_element(attribute, WORDCLASS, WordClass)
        synset = Synset(id, category, word_class)
        germanet._synsets[synset._id] = synset

        for sub_child in child:
            if sub_child.tag == "lexUnit":
                lexunit = create_lexunit(germanet, sub_child.attrib, sub_child, synset)
                germanet._lexunits[lexunit._id] = lexunit
                germanet._wordcat2lexid[category.name].add(lexunit._id)
                germanet._wordclass2lexid[word_class.name].add(lexunit._id)
                synset.add_lexunit(lexunit)
        for unit in synset._lexunits:
            for lexunit in synset._lexunits:
                if lexunit is not unit:
                    unit._relations[LexRel.has_synonym].add(lexunit)


def create_lexunit(germanet, attributes, lex_root, s):
    lex_id = attributes[LEXID]
    lex_sense = int(attributes[SENSE])
    lex_source = attributes[SOURCE]
    lex_named_entity = convert_to_boolean(attributes[NAMEDENTITY])
    lex_artificial = convert_to_boolean(attributes[ARTIFICIAL])
    lex_style = convert_to_boolean(attributes[STYLE])
    lexunit = Lexunit(id=lex_id, sense=lex_sense, source=lex_source, named_entity=lex_named_entity, synset=s,
                      artificial=lex_artificial, style_marking=lex_style)
    for child in lex_root:
        tag = child.tag
        child_value = child.text
        if tag == COMPOUND:
            compound = create_compound_info(child)
            lexunit._compound_info = compound
            germanet._compounds.add(lexunit)
        elif "rth" in tag:
            add_orth_forms(germanet, lexunit, child_value, tag)
        elif tag == FRAME:
            lexunit._frames.append(child_value)
            for f in lexunit._frames:
                germanet._frames2id[f].add(lexunit)
        elif tag == EXAMPLE:
            example = child[0].text
            lexunit._examples.append(example)
            if len(child) == 2:
                exframe = child[1].text
                lexunit._frames2examples[exframe].add(example)
        else:
            print("undefined tag")
    return lexunit


def add_orth_forms(germanet, lexunit, child_value, tag):
    germanet._ortform2lexid[child_value].add(lexunit._id)
    germanet._lowercasedform2lexid[child_value.lower()].add(lexunit._id)

    if tag == ORTHFORM:
        lexunit._orthform = child_value
        germanet._mainOrtform2lexid[child_value].add(lexunit._id)
    elif tag == ORTHVAR:
        lexunit._orthvar = child_value
    elif tag == OLDORTHFORM:
        lexunit._old_orthform = child_value
    elif tag == OLDORTHVAR:
        lexunit._old_orthvar = child_value
