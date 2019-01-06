from fractions import Fraction
from random import choice, randint, randrange, shuffle
from os.path import dirname, abspath, join
try:
    from latex import build_pdf
except Exception:
    pass
import re

TRIG_BASE = (r"\sin", r"\cos", r"\tan")
TRIG_RECI = (r"\csc", r"\sec", r"\cot")
TRIG_INV_BASE = (r"\arcsin", r"\arccos", r"\arctan")
TRIG_INV_RECI = (r"\arccsc", r"\arcsec", r"\arccot")

#\frac{1}{\sqrt{3}}
ARCTAN = (r"\frac{\sqrt{3}}{3}", "1", r"\sqrt{3}", r"\infty",
             r"-\sqrt{3}", "-1", r"-\frac{\sqrt{3}}{3}", "0")
ARCCOT = (r"\sqrt{3}", "1", r"\frac{\sqrt{3}}{3}", r"\infty",
          r"-\sqrt{3}", "-1", r"-\frac{\sqrt{3}}{3}", "0")

#\frac{1}{\sqrt{2}}
ARCSIN_COS = ("-1", r"-\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{2}}{2}", r"-\frac{1}{2}", "0",
             r"\frac{1}{2}", r"\frac{\sqrt{2}}{2}", r"\frac{\sqrt{3}}{2}", "1")
ARCCSC_SEC = ("-1", r"-\frac{2\sqrt{3}}{3}", r"-\sqrt{2}", "-2", "\infty",
              "2", r"\sqrt{2}", r"\frac{2\sqrt{3}}{3}", "1")

DENOM = (1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6)
NORM_NUMER = {1:(0, 1), 2:(1, 3), 3:(1, 2, 4, 5), 4:(1, 3, 5, 7), 6:(1, 3, 5, 7, 9, 11)}

LATEX_SPC_CHAR = {"\\":r"\textbackslash{}", r"&":r"\&", r"%":r"\%", r"$":r"\$", r"#":r"\#", r"_":r"\_",
                  r"{":r"\{", r"}":r"\}", r"~":r"\textasciitilde{}", r"^":r"\textasciicircum{}"}

#### Creates the PDF based on the output of the get_problems function.
# [ALL INPUTS] Equivalent to that of method `get_problems`.
def create_tex(title, enabled, outRange, rangeNum, timesNewRoman, chOrAmt=True):
    problems = get_problems(enabled, outRange, rangeNum, chOrAmt)
    if problems == ('', 204):
        return ('', 204)
    with open(join(dirname(abspath(__file__)), "templates/template_quiz.tex"), 'rb') as file:
        quiz = file.read().decode()
    for count in range(12):
        quiz = quiz.replace("(((prob" + str(count+1) + ")))", problems.pop())
    title = esc_title(title)
    quiz = quiz.replace("Speed Trig Quiz", title)
    quiz = quiz.replace("%TIMES NEW ROMAN", r"\usepackage{mathptmx}") if timesNewRoman else quiz
    return build_pdf(quiz)

    # folder = join(dirname(abspath(__file__)), "tmp/", tmpfile)
    # filename = join(folder, tmpfile + ".pdf")
    # mkdir(folder)
    # call("pdflatex -output-directory=" + folder + join(dirname(abspath(__file__)), "tmp/", tmp.name), shell=True)
    # return (filename, folder)

###### Generates the functions to be used ######
# [INPUT 1: enabled (bool[])] List of booleans to choose functions to use
# [INPUT 2: outRange (bool)] True if inputs out of normal range are enabled, else False
# [INPUT 3: rangeNum (int)] Number determining % chance of inputs or exact amount out of normal range (i.e., [0, 2π))
# [INPUT 4: chrOrAmt (bool)] Indicates whether rangeNum refers to the % chance (True) or the exact amount (False)
def get_problems(enabled, outRange, rangeNum, chOrAmt):
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

###### Parses options given from index.html, generates random list of functions ######
# Uses set to ensure that no duplicate problems are generated
# [INPUT 1: funcs (set(string[]))] Set of functions to be generated within quiz
# [INPUT 2: outRange (bool)] True if inputs out of normal range are enabled, else False
# [INPUT 3: rangeInfo (tuple(int, bool))] Whether % chance or set # should be used, and the value to be used with said calculations
def get_func_inputs(funcs, outRange, rangeInfo=(0, False)):
    normFuncs = 12
    res = []
    rng = []
    output = set()
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
        while len(output) != index + 1:
            if any(item in x for x in (TRIG_BASE, TRIG_RECI)):
                output.add(item + get_rand_rad(rng[index]))
            if item in TRIG_INV_BASE:
                if item == r"\arctan": output.add(item + "{(" +get_rand_frac(False, True) + ")}")
                else: output.add(item + "{(" +get_rand_frac() + ")}")
            if item in TRIG_INV_RECI:
                if item == r"\arccot": output.add(item + "{(" +  get_rand_frac(True, True) + ")}")
                else: output.add(item + "{(" + get_rand_frac(True, False) + ")}")
    return output

###### Generates a random fraction (multiple of π/4 or π/6) given whether the output should be within [0, 2π) ######
# [INPUT 1: norm (bool)] True if output should be within [0, 2π), else False
def get_rand_rad(norm=True):
    curDenom = choice(DENOM)
    if norm:
        return get_frac(choice(NORM_NUMER[curDenom]), curDenom)
    else:
        return get_frac(choice(NORM_NUMER[curDenom]) + (-1 if randint(0, 1) == 0 else 1) * 2 * curDenom, curDenom)

###### Generates
def get_rand_frac(inv=False, tan=False):
    if tan:
        if inv: return choice(ARCCOT)
        else: return choice(ARCTAN)
    else:
        if inv: return choice(ARCCSC_SEC)
        else: return choice(ARCSIN_COS)


###### Formats latex fraction based on inputs. ######
# [INPUT 1: numerator (int)] Numerator
# [INPUT 2: denominator (int)] Denominator
# Automatically simplified via the fraction class.
def get_frac(numer, denom):
    frac = Fraction(numer, denom)
    if frac.numerator == 0:
        return "(0)"
    if frac.denominator == 1:
        return "(" + (str(frac.numerator) if frac.numerator not in (1, -1) else "") + r"\pi)"
    return (r"{(\frac{" + (str(frac.numerator) if frac.numerator not in (1, -1) else "") if frac.numerator > 0 else (r"{(-\frac{" + (str(abs(frac.numerator)) if frac.numerator not in (1, -1) else ""))) + r"\pi}{" + str(frac.denominator) + "})}"

###### Replaces/escapes latex special characters for title. ######
# [INPUT 1: title (String)] Title
def esc_title(title):
    return re.sub('|'.join(re.escape(key) for key in LATEX_SPC_CHAR.keys()),
                  lambda k: LATEX_SPC_CHAR[k.group(0)], title)

def test_tex(enabled, outRange, rangeNum, chOrAmt):
    problems = get_problems(enabled, outRange, rangeNum, chOrAmt)
    if problems == ('', 204):
        return ('', 204)
    with open(join(dirname(abspath(__file__)), "templates/template_quiz.tex"), 'rb') as file:
        quiz = file.read().decode()
    for count in range(12):
        quiz = quiz.replace("(((prob" + str(count+1) + ")))", problems.pop())
    return quiz.encode()