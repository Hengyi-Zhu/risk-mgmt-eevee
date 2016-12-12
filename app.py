from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import requests
import datetime
import dill, os

def create_df_from_tickers(tickers_string, start_date, end_date):
    tickers_list = tickers_string.split(",")
    d={}
    for ticker in tickers_list:
        d["{0}".format(ticker)] = web.DataReader(ticker, 'yahoo', start_date, end_date)['Adj Close'].rename(ticker)
    df = pd.DataFrame(d).sort_index(ascending = False)
    return df

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # Feature 1
        tickers_string_1 = request.form["tickers_string_1"]
        position_date_1 = datetime.datetime.strptime(request.form["position_date_1"], '%Y-%m-%d')
        end_date_1 = datetime.datetime.strptime(request.form["end_date_1"], '%Y-%m-%d')
        df_1 = create_df_from_tickers(tickers_string_1, position_date_1, end_date_1)
        p_1_1 = figure(width=600, height=400, title = "%s historical prices" % df_1.columns.values[0], 
                       x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime")
        p_1_1.line(df_1.iloc[:,0].index, df_1.iloc[:,0])
        script_1_1, div_1_1 = components(p_1_1)
        # Feature 2       
        return render_template('index.html', script_1_1 = script_1_1, div_1_1 = div_1_1)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)