from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, request, url_for, redirect, render_template, session, send_file
from io import BytesIO
import TrigGen
from datetime import datetime

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/generated-quiz', methods=['GET', 'POST'])
def generated():
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
    inc = True if request.form["inc"] == "yes" else False
    print(inc)

    ### override is a Boolean for whether the user wants exact number or percent.
    # True if selected
    # False if not selected
    override = True if request.form["override"] == "yes" else False
    print(override)


    num = int(request.form["num"]) if override else int(request.form["chance"])
    print(num)

    dl = "dl" in request.form

    quiz = TrigGen.create_tex([norm, reci, invnorm, invreci], inc, num, override)
    if quiz == ('', 204):
        return ('', 204)

    return send_file(BytesIO(bytes(quiz)),
                     mimetype="application/pdf", as_attachment=dl,
                     attachment_filename="Speed Trig Quiz"+datetime.now().strftime(" %Y-%m-%d at %H.%M.%S.pdf"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)