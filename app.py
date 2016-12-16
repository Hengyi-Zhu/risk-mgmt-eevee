################## Imports ##################
# Remember to properly add the packages to requirements.txt or conda-requirements.txt. 
from __future__ import division

from flask import Flask, render_template, request, redirect
import requests
import dill, os
import sys

from bokeh.plotting import figure
from bokeh.embed import components

import pandas_datareader.data as web
import scipy.stats as stat
import pandas as pd
import numpy as np
import datetime
import dateutil.relativedelta


##################  Function definitions ##################

# Function definitions
def create_df_from_tickers(tickers_string, position_date, end_date):
    tickers_list = tickers_string.split(",")
    start_date = position_date - dateutil.relativedelta.relativedelta(years = 10)
    d={}
    for ticker in tickers_list:
        d["{0}".format(ticker)] = web.DataReader(ticker, 'yahoo', start_date, end_date)['Adj Close'].rename(ticker)
    df = pd.DataFrame(d).sort_index(ascending = False)
    plot_length = len(df[df.index >= position_date])
    return df, plot_length

# Price plot
def plot_price(price, length):
    data = price[:length]   
    plot = figure(width=550, height=400, title = "%s Historical Prices" % data.columns.values[0], 
                  x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime")
    plot.line(data.index, data)
    plot.title.text_font_size = '12pt'
    return plot

# Calculate estimated parameters for GBM based on x year (in days) rolling windows
def gbm_est(prices, window_days):
    rtn = -np.diff(np.log(prices))
    rtnsq = rtn * rtn
    mubar = list(reversed(np.convolve(rtn, np.ones((window_days,))/window_days, mode='valid')))
    x2bar = list(reversed(np.convolve(rtnsq, np.ones((window_days,))/window_days, mode='valid')))
    var = x2bar - np.square(mubar)
    sigmabar = np.sqrt(np.maximum(var, np.zeros(len(var))))
    sigma = sigmabar / np.sqrt(1/252)
    mu = np.array(mubar)*252 + np.square(sigma)/2
    return rtn, mu, sigma, np.array(mubar), sigmabar

def plot_parameters(price, choice):
    rtn_2, mu_2, sigma_2, mubar_2, sigmabar_2 = gbm_est(price, 2*252)
    rtn_5, mu_5, sigma_5, mubar_5, sigmabar_5 = gbm_est(price, 5*252)
    rtn_10, mu_10, sigma_10, mubar_10, sigmabar_10 = gbm_est(price, 10*252)
    length = min(len(mu_2), len(mu_5), len(mu_10), len(sigma_2), len(sigma_5), len(sigma_10))
    if choice == "mu":
        mu = pd.DataFrame({'Mu_2': mu_2[:length], 'Mu_5': mu_5[:length], 'Mu_10': mu_10[:length]}, 
                          index = price.index[:length])
        plot = figure(width=550, height=400, title = "Mu", 
                      x_axis_label='Date', y_axis_label='Mu', x_axis_type="datetime")
        plot.line(mu.index, mu['Mu_2'], legend = '2-year roling window')
        plot.line(mu.index, mu['Mu_5'], color = 'green', legend = '5-year roling window')
        plot.line(mu.index, mu['Mu_10'], color = 'orange', legend = '10-year roling window')
        plot.legend.location = 'top_right'
        plot.title.text_font_size = '12pt'
        return plot
    elif choice == "sigma":
        sigma = pd.DataFrame({'Sigma_2': sigma_2[:length], 'Sigma_5': sigma_5[:length], 'Sigma_10': sigma_10[:length]}, 
                             index = price.index[:length])
        plot = figure(width=550, height=400, title = "Sigma", 
                      x_axis_label='Date', y_axis_label='Sigma', x_axis_type="datetime")
        plot.line(sigma.index, sigma['Sigma_2'], legend = '2-year roling window')
        plot.line(sigma.index, sigma['Sigma_5'], color = 'green', legend = '5-year roling window')
        plot.line(sigma.index, sigma['Sigma_10'], color = 'orange', legend = '10-year roling window')
        plot.legend.location = 'top_right'
        plot.title.text_font_size = '12pt'
        return plot
    else:
        print "Please choose between 'mu' and 'sigma' for the second argument."



################## Flask & html interaction ##################

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # Feature 1 - Individual stock
        tickers_string_1 = request.form["tickers_string_1"]
        position_date_1 = datetime.datetime.strptime(request.form["position_date_1"], '%Y-%m-%d')
        end_date_1 = datetime.datetime.strptime(request.form["end_date_1"], '%Y-%m-%d')
        df_1, plot_length_1 = create_df_from_tickers(tickers_string_1, position_date_1, end_date_1)
        plot_1 = plot_price(df_1, plot_length_1)
        plot_2 = plot_parameters(df_1.iloc[:,0], 'mu')
        plot_3 = plot_parameters(df_1.iloc[:,0], 'sigma')
        plot_4 = plot_price(df_1, plot_length_1)
        plots = {'div_1_1': plot_1, 'div_1_2': plot_2, 'div_1_3': plot_3, 'div_1_4': plot_4}
        script, div = components(plots)
        return render_template('index.html', scroll='feature1', 
                               script = script, div_1_1 = div['div_1_1'], div_1_2 = div['div_1_2'], 
                               div_1_3 = div['div_1_3'], div_1_4 = div['div_1_4'])
        # Feature 2 - Portfolio

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)