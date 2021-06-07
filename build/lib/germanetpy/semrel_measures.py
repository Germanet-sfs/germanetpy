import fastenum


class SemRelMeasure(fastenum.Enum):
    """This Enum represents the semantic relatedness measures"""
    SimplePath = "SimplePath"
    LeacockAndChodorow = "LeacockAndChodorow"
    WuAndPalmer = "WuAndPalmer"
    Resnik = "Resnik"
    Lin = "Lin"
    JiangAndConrath = "JiangAndConrath"