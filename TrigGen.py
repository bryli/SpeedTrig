from __future__ import absolute_import, division, print_function, unicode_literals
from fractions import Fraction
from random import choice, randint, randrange, shuffle
from os.path import dirname, abspath, join
# from os import mkdir, remove
# from subprocess import call
# import tempfile
from latex import build_pdf
import re

TRIG_BASE = (r"\sin", r"\cos", r"\tan")
TRIG_RECI = (r"\csc", r"\sec", r"\cot")
TRIG_INV_BASE = (r"\arcsin", r"\arccos", r"\arctan")
TRIG_INV_RECI = (r"\arccsc", r"\arcsec", r"\arccot")

#\frac{1}{\sqrt{3}}
ARCTAN_IN = (r"\frac{1}{\sqrt{3}}", "1", r"\sqrt{3}", r"\infinity",
             r"-\sqrt{3}", "-1", r"-\frac{1}{\sqrt{3}}", "0")
#\frac{1}{\sqrt{2}}
ARCSIN_COS = ("-1", r"-\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{2}}{2}", r"-\frac{1}{2}", "0",
             r"\frac{1}{2}", r"\frac{\sqrt{2}}{2}", r"\frac{sqrt{3}}{2}", "1")
OUT_DOM = () # NOT IMPLEMENTED

FIND_FILE = re.compile(r"tmp/(.*).tex")

DENOM = (1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6)
NORM_NUMER = {1:(0, 1), 2:(1, 3), 3:(1, 2, 4, 5), 4:(1, 3, 5, 7), 6:(1, 3, 5, 7, 9, 11)}

def createTex(enabled, outRange, rangeNum, chOrAmt=True):
    problems = get_problems(enabled, outRange, rangeNum, chOrAmt)
    if problems == ('', 204):
        return ('', 204)
    with open(join(dirname(abspath(__file__)), "templates/template_quiz.tex"), 'rb') as file:
        quiz = file.read().decode()
    for count in range(12):
        quiz = quiz.replace("(((prob" + str(count+1) + ")))", problems.pop())
    return build_pdf(quiz)
    # tmp = tempfile.NamedTemporaryFile(suffix=".tex", dir=join(dirname(abspath(__file__)), "tmp/"), delete=False)
    # tmp.write(quiz.encode())
    # tmp.close()
    # tmpfile = FIND_FILE.search(tmp.name).group(1)
    # folder = join(dirname(abspath(__file__)), "tmp/", tmpfile)
    # filename = join(folder, tmpfile + ".pdf")
    # mkdir(folder)
    # call("pdflatex -output-directory=" + folder + join(dirname(abspath(__file__)), "tmp/", tmp.name), shell=True)
    # return (filename, folder)

def get_problems(enabled, outRange, rangeNum, chOrAmt=True):
    funcs = []
    if not any(enabled):
        return ('', 204)
    if enabled[0]:
        funcs.extend(TRIG_BASE)
    if enabled[1]:
        funcs.extend(TRIG_RECI)
    if enabled[2]:
        funcs.extend(TRIG_INV_BASE)
    if enabled[3]:
        funcs.extend(TRIG_INV_RECI)
    return get_func_inputs(funcs, outRange, [rangeNum, chOrAmt])

def get_func_inputs(funcs, outRange, rangeInfo=(0, False)):
    normFuncs = 12
    res = []
    rng = []
    output = set()
    curProb = {}
    for count in range(12):
        funcChoice = choice(funcs)
        res.append(funcChoice)
        if any(funcChoice in x for x in (TRIG_BASE, TRIG_RECI)):
            if outRange and rangeInfo[1]:
                rng.append((False if randint(0, 100) < rangeInfo[0] else True))
        else:
            normFuncs-=1
    if outRange and not rangeInfo[1]:
        rng = [False]*rangeInfo[0] + [True]*max(normFuncs - rangeInfo[0], 0)
        shuffle(rng)
    if not outRange:
        rng = [True]*12
    for index, item in enumerate(res):
        if any(item in x for x in (TRIG_BASE, TRIG_RECI)):
            output.add(item + get_rand_rad(rng[index]))
            while len(output) != index + 1:
                output.add(item + get_rand_rad(rng[index]))
    return output




def get_rand_frac():
    return

def get_rand_rad(norm=True):
    curDenom = choice(DENOM)
    if norm:
        return get_frac(choice(NORM_NUMER[curDenom]), curDenom)
    else:
        return get_frac(choice(NORM_NUMER[curDenom]) + (-1 if randint(0, 1) == 0 else 1) * randrange(2, 5, 2) * curDenom, curDenom)

def get_frac(numer, denom):
    frac = Fraction(numer, denom)
    if frac.nominator == 0:
        return "(0)"
    if frac.denominator == 1:
        return "(" + (str(frac.numerator) if frac.numerator not in (1, -1) else "") + r"\pi)"
    return (r"{(\frac{" + (str(frac.numerator) if frac.numerator not in (1, -1) else "") if frac.numerator > 0 else (r"{(-\frac{" + (str(abs(frac.numerator)) if frac.numerator not in (1, -1) else ""))) + r"\pi}{" + str(frac.denominator) + "})}"
