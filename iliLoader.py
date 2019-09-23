from iliRecord import IliRecord

LEXID = "lexUnitId"
EWNREL = 'ewnRelation'
PWNWORD = 'pwnWord'
PWN20ID = 'pwn20Id'
PWN30ID = 'pwn30Id'
SOURCE = 'source'
PWN20PARAPHRASE = 'pwn20paraphrase'


def create_ili_record(attributes, synonyms):
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
    root = tree.getroot()
    for child in root:
        attributes = child.attrib
        synonyms = []
        for subchild in child:
            for subsubchild in subchild:
                synonyms.append(subsubchild.text)
        ili = create_ili_record(attributes, synonyms)
        lexunit = germanet._lexunits[ili._lexunit_id]
        lexunit._ili_records.append(ili)
        germanet._ili_records.append(ili)
