from flask import Flask, render_template, request, url_for, flash, redirect
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'er32gE1df3R2gs1T23sd1Pg23fW3dgh32N13h13klD31j3sd'

data = pd.DataFrame( pd.read_csv('results.csv') )


@app.route('/')
def index():
    return render_template('template/index.html', data=data)