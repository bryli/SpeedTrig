from flask import Flask, request, render_template, send_file
from io import BytesIO
import TrigGen
from datetime import datetime

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/generated-quiz', methods=['GET', 'POST'])
def generated():

    ### Title is a string used to create worksheet title text.
    if "title" in request.form:
        title = request.form["title"]
    else:
        title = "Speed Trig Quiz"
    print(title)

    ### norm is a Boolean for whether the Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    norm = "norm" in request.form
    print(norm)
    ### reci is a Boolean for whether the Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    reci = "reci" in request.form
    print(reci)

    ### invnorm is a Boolean for whether the Inverse Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invnorm = "invnorm" in request.form
    print(invnorm)

    ### invreci is a Boolean for whether the Inverse Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invreci = "invreci" in request.form
    print(invreci)

    ### inc is a Boolean for whether the user wants values above 2π or below 0.
    # True if selected
    # False if not selected
    if "inc" in request.form:
        inc = True if request.form["inc"] == "yes" else False
    else:
        inc = False
    print(inc)

    timesNewRoman = "timesnewroman" in request.form

    ### override is a Boolean for whether the user wants exact number or percent chance.
    # True if % chance
    # False if exact number wanted
    if "override" in request.form:
        override = True if request.form["override"] == "yes" else False
    else:
        override = False
    print(override)

    if "num" in request.form and "chance" in request.form:
        num = int(request.form["chance"]) if override else int(request.form["num"])
    elif "num" in request.form:
        num = int(request.form["num"])
        override = False
    elif "chance" in request.form:
        num = int(request.form["chance"])
        override = True
    else:
        num = 0
    print(num)

    dl = "dl" in request.form
    if app.config['TESTING']:
        quiz = TrigGen.test_tex([norm, reci, invnorm, invreci], inc, num, timesNewRoman, override)
        if quiz == ('', 204):
            return ('', 204)
        return send_file(BytesIO(quiz), as_attachment=dl, mimetype="text/x-tex",
                                 download_name="Speed Trig Quiz"+datetime.now().strftime(" %Y-%m-%d at %H.%M.%S.pdf"))
    quiz = TrigGen.create_tex(title, [norm, reci, invnorm, invreci], inc, num, timesNewRoman, override)
    if quiz == ('', 204):
        return ('', 204)

    return send_file(BytesIO(bytes(quiz)),
                     mimetype="application/pdf", as_attachment=dl,
                     download_name="Speed Trig Quiz"+datetime.now().strftime(" %Y-%m-%d at %H.%M.%S.pdf"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)