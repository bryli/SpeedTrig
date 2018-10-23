from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, request, url_for, redirect, render_template, session, send_file
from io import BytesIO
import TrigGen
from datetime import datetime
from secrets import token_hex

app = Flask(__name__)
app.secret_key = token_hex(32)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/generated', methods=['GET', 'POST'])
def generated():
    print(request.form)
    ### norm is a Boolean for whether the Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    norm = False
    if("norm" in request.form):
        norm = True
    print(norm)

    ### reci is a Boolean for whether the Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    reci = False
    if("reci" in request.form):
        reci = True
    print(reci)

    ### invnorm is a Boolean for whether the Inverse Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invnorm = False
    if("invnorm" in request.form):
        invnorm = True
    print(invnorm)

    ### invreci is a Boolean for whether the Inverse Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invreci = False
    if("invreci" in request.form):
        invreci = True
    print(invreci)

    ### inc is a Boolean for whether the user wants values above 2π or below 0.
    # True if selected
    # False if not selected
    inc = False
    if (request.form["inc"] == "yes"):
        inc = True
    print(inc)

    ### override is a Boolean for whether the user wants exact number or percent.
    # True if selected
    # False if not selected
    override = False
    if(request.form["override"] == "yes"):
        override = True
    print(override)

    if override:
        num = int(request.form["num"])
    else:
        num = int(request.form["chance"])
    print(num)

    quiz = TrigGen.createTex([norm, reci, invnorm, invreci], inc, num, override)
    if quiz == ('', 204):
        return ('', 204)

    return send_file(BytesIO(bytes(quiz)),
                     mimetype="application/pdf", as_attachment=True,
                     attachment_filename="Speed Trig Quiz"+datetime.now().strftime(" %Y-%m-%d at %H.%M.%S.pdf"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)