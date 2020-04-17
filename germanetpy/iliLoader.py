from germanetpy.iliRecord import IliRecord

LEXID = "lexUnitId"
EWNREL = 'ewnRelation'
PWNWORD = 'pwnWord'
PWN20ID = 'pwn20Id'
PWN30ID = 'pwn30Id'
SOURCE = 'source'
PWN20PARAPHRASE = 'pwn20paraphrase'


def create_ili_record(attributes, synonyms) -> IliRecord:
    """
    Creates the ili record given the XML attributes.
    :type synonyms: list(String)
    :type attributes: xml attributes
    :param attributes: The XML attributes that contain the required information about the ili record.
    :param synonyms: A list of Strings, containing the synonyms of the ili record.
    :return: The ili record object
    """
    lex_id = attributes[LEXID]
    ewnrelation = attributes[EWNREL]
    pwnword = attributes[PWNWORD]
    pwn20Id = attributes[PWN20ID]
    pwn30Id = attributes[PWN30ID]
    source = attributes[SOURCE]
    pwn20paraphrase = attributes.get(PWN20PARAPHRASE)
    ili = IliRecord(lexunit_id=lex_id, ewnRelation=ewnrelation, pwnWord=pwnword, pwn20Id=pwn20Id,
                    pwn30Id=pwn30Id, source=source, pwn20synonyms=synonyms, pwn20paraphrase=pwn20paraphrase)

    return ili


def load_ili(germanet, tree):
    """
    This method creates the ili record objects given a datafile and adds them to the GermaNet object and the
    corresponding lexical unit.
    :type tree: Element Tree
    :type germanet: Germanet
    :param germanet: The GermaNet object
    :param tree: The XML tree containing the data about the ili records
    """
    root = tree.getroot()
    for child in root:
        attributes = child.attrib
        synonyms = []
        for subchild in child:
            for subsubchild in subchild:
                synonyms.append(subsubchild.text)
        ili = create_ili_record(attributes, synonyms)
        lexunit = germanet.lexunits[ili.lexunit_id]
        lexunit.ili_records.append(ili)
        germanet.ili_records.append(ili)
