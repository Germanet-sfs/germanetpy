from functools import reduce


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

    def __init__(self, frames2lexunits: dict):
        """
        This class holds functionality to extract verbs with specific frame types. These subcategorisation patterns
        can help to disambiguate verbs in specific contexts and how many arguments a verb can take.
        :param frames2lexunits: A dictionary that stores the frames as keys and the corresponding lexunits as values.
        """

        self._frames2verbs = frames2lexunits

    def extract_expletives(self) -> set:
        """
        This method extracts all verbs that can take expletives as an argument. Example: "[Es] regnet."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.EXPLETIVE)

    def extract_accusative_complemtent(self) -> set:
        """
        This method returns all verbs that can take an accusative complement. Example: "Sie sieht [ihn]"
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.ACCOBJ)

    def extract_dative_complement(self) -> set:
        """
        This method returns all verbs that can take an dative complement. Example: "Sie schenkt [ihm] einen Hund."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.DATOBJ)

    def extract_gentive_complement(self) -> set:
        """
        This method returns all verbs that can take an genetive complement. Example: "Ihre Eltern berauben sie [ihrer
        Freiheit]."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.GENOBJ)

    def extract_prepositional_complement(self) -> set:
        """
        This method returns all verbs that can take an prepositional complement. Example: "Die Kugel klackte [an die
        Fensterscheibe]."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.PREPOBJ)

    def extract_reflexives(self) -> set:
        """
        This method returns all verbs that can take an reflexive complement. Example: "Sie wird [sich] rächen."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.reflexives[0]).union(
            self.extract_specific_complements(self.reflexives[1]))

    def extract_adverbials(self) -> set:
        """
        This method returns all verbs that can take an adverbial complement. Example: "Sie wohnt [in einem Haus]."
        :return: A set of lexical units that stores all verbs as Lexunits that have the specified frame.
        """
        return self.extract_specific_complements(self.LOC) \
            .union(self.extract_specific_complements(self.DIR)
                   .union(self.extract_specific_complements(self.TEMP)
                          .union(self.extract_specific_complements(self.MAN)
                                 .union(self.extract_specific_complements(self.INST)
                                        .union(self.extract_specific_complements(self.CAUSE)
                                               .union(self.extract_specific_complements(self.ROLE)
                                                      .union(self.extract_specific_complements(self.COM))))))))

    def extract_transitives(self) -> set:
        """
        This method returns all transitive verbs. A transitive verb is any verb that can have objects.
        :return: A set of lexical units that stores all transitive verbs as Lexunits.
        """
        return self.extract_specific_complements(self.ACCOBJ) \
            .union(self.extract_specific_complements(self.DATOBJ)
                   .union(self.extract_specific_complements(self.GENOBJ)
                          .union(self.extract_specific_complements(self.PREPOBJ))))

    def extract_intransitives(self) -> set:
        """
        This method returns all intransitive verbs. An intransitive verb is any verb that does not have objects.
        :return: A set of lexical units that stores all intransitive verbs as Lexunits.
        """
        transitives = self.extract_transitives()
        all_verbs = reduce(set.union, self.frames2verbs.values())
        return all_verbs.difference(transitives)

    def extract_specific_complements(self, complement: str) -> set:
        """
        This method returns all verbs that can take a given complement. This is specified in the frames of a verb.
        :param: complement : a syntactic complement (e.g NN for subject), the complements are specified as class
        variables of this class
        :return: A set of lexical units that stores all verbs as Lexunits that can take the specified complement.
        """
        complements = set()
        for (key, val) in self._frames2verbs.items():
            if complement in key:
                for unit in val:
                    complements.add(unit)
        return complements

    @property
    def frames2verbs(self):
        return self._frames2verbs
