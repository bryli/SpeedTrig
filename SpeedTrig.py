from flask import Flask, request, url_for, redirect, render_template, session

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/generated', methods=['GET', 'POST'])
def generated():
    ### norm is a Boolean for whether the Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    norm = False
    if(request.form.get("norm") == "on"):
        norm = True
    print(norm)

    ### reci is a Boolean for whether the Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    reci = False
    if(request.form.get("reci") == "on"):
        reci = True
    print(reci)

    ### invnorm is a Boolean for whether the Inverse Normal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invnorm = False
    if(request.form.get("invnorm") == "on"):
        invnorm = True
    print(invnorm)

    ### invreci is a Boolean for whether the Inverse Reciprocal Trig Functions option was selected.
    # True if selected
    # False if not selected
    invreci = False
    if(request.form.get("invreci") == "on"):
        invreci = True
    print(invreci)

    ### override is a Boolean for whether the user wants exact number or perecnt.
    # True if selected
    # False if not selected
    override = False
    if(request.form.get("override") == "on"):
        override = True
    print(override)

    chance = int(request.form.get("chance"))
    print(chance)
    return render_template('generated.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)