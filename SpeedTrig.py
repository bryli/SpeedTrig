from flask import Flask, request, url_for, redirect, render_template, session

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/generated', methods=['GET', 'POST'])
def generated():
    print(request.form.get("chance"))
    return render_template('generated.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)