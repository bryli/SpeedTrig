from fractions import Fraction
from random import choice, randint, randrange, shuffle
from os.path import dirname, abspath, join

TRIG_BASE = ("\\sin", "\\cos", "\\tan")
TRIG_RECI = ("\\csc", "\\sec", "\\cot")
TRIG_INV_BASE = ("\\arcsin", "\\arccos", "\\arctan")
TRIG_INV_RECI = ("\\arccsc", "\\arcsec", "\\arccot")

#\\frac{1}{\\sqrt{3}}
ARCTAN_IN = ("\\frac{1}{\\sqrt{3}}", "1", "\\sqrt{3}", "\\infinity",
             "-\\sqrt{3}", "-1", "-\\frac{1}{\\sqrt{3}}", "0")
#\\frac{1}{\\sqrt{2}}
ARCSIN_COS = ("-1", "-\\frac{\\sqrt{3}}{2}", "-\\frac{\\sqrt{2}}{2}", "-\\frac{1}{2}", "0",
             "\\frac{1}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{sqrt{3}}{2}", "1")
OUT_DOM = () # NOT IMPLEMENTED


DENOM = (1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6)
NORM_NUMER = {1:(0, 1), 2:(1, 3), 3:(1, 2, 4, 5), 4:(1, 3, 5, 7), 6:(1, 3, 5, 7, 9, 11)}

def main(enabled, rangeNum, chOrAmt=True):
    problems = getProblems(enabled, rangeNum, chOrAmt)
    with open(join(dirname(abspath(__file__)), "template_quiz.tex"), 'r') as file:
        quiz = file.read()
    for count in range(12):
        quiz.replace("(((prob" + str(count+1) + ")))", problems[count])
    return quiz

def getProblems(enabled, rangeNum, chOrAmt=True):
    funcs = []
    if enabled[0]:
        funcs.extend(TRIG_BASE)
    if enabled[1]:
        funcs.extend(TRIG_RECI)
    if enabled[2]:
        funcs.extend(TRIG_INV_BASE)
    if enabled[3]:
        funcs.extend(TRIG_INV_RECI)
    return getFuncInputs(funcs, [rangeNum, chOrAmt])

def getFuncInputs(funcs, rangeInfo=(0, False)):
    normFuncs = 12
    res = []
    rng = []
    output = set()
    curProb = {}
    for count in range(12):
        funcChoice = choice(funcs)
        res.append(funcChoice)
        if any(funcChoice in x for x in (TRIG_BASE, TRIG_RECI)):
            if rangeInfo[1]:
                rng.append((False if randint(0, 100) < rangeInfo[0] else True))
        else:
            normFuncs-=1
    if not rangeInfo[1]:
        rng = [False]*rangeInfo[0] + [True]*max(normFuncs - rangeInfo[0], 0)
        shuffle(rng)
    for index, item in enumerate(res):
        if any(item in x for x in (TRIG_BASE, TRIG_RECI)):
            output.append(item + getRandRad(rng.pop(0)))
            while len(output) != index + 1:
                output.append(item + getRandRad(rng.pop(0)))
    return output




def getRandFrac():
    return

def getRandRad(norm=True):
    curDenom = choice(DENOM)
    if norm:
        return getFrac(choice(NORM_NUMER[curDenom]), curDenom)
    else:
        return getFrac(choice(NORM_NUMER[curDenom]) + (-1 if randint(0, 1) == 0 else 1) * randrange(2, 5, 2) * curDenom, curDenom)

def getFrac(numer, denom):
    frac = Fraction(numer, denom)
    if frac.denominator == 1:
        return (str(frac.numerator) if frac.numerator != 1 else "") + "\\pi"
    return "{\\frac{" + str(frac.numerator) + "\\pi}{" + str(frac.denominator) + "}}"
