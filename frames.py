class Frames:
    EXPLETIVE = 'NE'
    SUBJECT = 'NN'
    ACCOBJ = 'AN'
    DATOBJ = 'DN'
    GENOBJ = 'GN'
    PREPOBJ = 'PP'
    LOC = 'BL'
    DIR = 'BD'
    TEMP = 'BT'
    MAN = 'BM'
    INST = 'BS'
    CAUSE = 'BC'
    ROLE = 'BR'
    COM = 'BO'
    reflexives = ['DR', 'AR']

    def __init__(self, frames2lexunits):

        self._frames2verbs = frames2lexunits

    def extract_expletives(self):
        return self.extract_specific_complements(self.EXPLETIVE)

    def extract_accusative_complemtent(self):
        return self.extract_specific_complements(self.ACCOBJ)

    def extract_dative_complement(self):
        return self.extract_specific_complements(self.DATOBJ)

    def extract_gentive_complement(self):
        return self.extract_specific_complements(self.GENOBJ)

    def extract_prepositional_complement(self):
        return self.extract_specific_complements(self.PREPOBJ)

    def extract_reflexives(self):
        return self.extract_specific_complements(self.reflexives[0]).union(
            self.extract_specific_complements(self.reflexives[1]))

    def extract_adverbials(self):
        return self.extract_specific_complements(self.LOC) \
            .union(self.extract_specific_complements(self.DIR)
                 .union(self.extract_specific_complements(self.TEMP)
                      .union(self.extract_specific_complements(self.MAN)
                           .union(self.extract_specific_complements(self.INST)
                                .union(self.extract_specific_complements(self.CAUSE)
                                     .union(self.extract_specific_complements(self.ROLE)
                                          .union(self.extract_specific_complements(self.COM))))))))

    def extract_specific_complements(self, complement):
        complements = set()
        for (key, val) in self._frames2verbs.items():
            if complement in key:
                for unit in val:
                    complements.add(unit)
        return complements

    def frames2verbs(self):
        return self._frames2verbs
