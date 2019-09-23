from wictionaryparaphrase import WiktionaryParaphrase
from utils import convert_to_boolean

LEXID = 'lexUnitId'
ID = 'wiktionaryId'
SENSEID = 'wiktionarySenseId'
SENSE = 'wiktionarySense'
EDITED = 'edited'


def create_wictionary(attributes):
    """
    Creates a wiktionary object given the XML attributes that contain the required information
    :param attributes: XML attributes that contain information about the wiktionary paraphrase
    :return: a wiktionary object
    """
    lex_id = attributes[LEXID]
    wiktionary_id = attributes[ID]
    wiktionary_sense_id = int(attributes[SENSEID])
    wiktionary_sense = attributes[SENSE]
    edited = convert_to_boolean(attributes[EDITED])
    wiki = WiktionaryParaphrase(lexunit_id=lex_id, wiktionary_id=wiktionary_id, wiktionary_sense_id=wiktionary_sense_id,
                                wiktionary_sense=wiktionary_sense, edited=edited)
    return wiki


def load_wiktionary(germanet, tree):
    """
    Given a XML tree this method initialized the wiktionary objects and adds them to the germanet object and the
    corresponding lexunits
    :param germanet: The germane object
    :param tree: The XML tree of the wiktionary file
    """
    root = tree.getroot()
    for child in root:
        attributes = child.attrib
        wiktionary = create_wictionary(attributes)
        lexunit = germanet._lexunits[wiktionary._lexunit_id]
        lexunit._wiktionary_paraphrases.append(wiktionary)
        germanet._wiktionary_entries.append(wiktionary)
