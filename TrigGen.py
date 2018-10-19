from fractions import Fraction

trigBase = ["\\sin", "\\cos", "\\tan"]
trigReci = ["\\csc", "\\sec", "\\cot"]
trigInvBase = ["\\arcsin", "\\arccos", "\\arctan"]
trigInvReci = ["\\arccsc", "\\arcsec", "\\arccot"]


denom =[1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6]
normNumer = {1:[0, 1, 2], 2:[1, 3], 3:[1, 2, 4, 5], 4:[1, 3, 5, 7], 6:[1, 3, 5, 7, 9, 11]}



def getProblems(enabled, weight):
    funcs = []
    if enabled[0]:
        funcs.extend(trigBase)
    if enabled[1]:
        funcs.extend(trigReci)
    if enabled[2]:
        funcs.extend(trigInvBase)
    if enabled[3]:
        funcs.extend(trigInvReci)


def getFrac(numer, denom):
    frac = Fraction(numer, denom)
    return "\\frac{" + str(frac.numerator) + "\\pi}{" + str(frac.denominator) + "}"