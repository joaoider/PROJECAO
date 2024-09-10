# imports.py

import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame
from pandas import concat
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pylab import rcParams
from matplotlib import colors
import matplotlib as mpl
#%matplotlib inline

from datetime import datetime, timedelta

#from sklearn.metrics import mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from scipy.stats import boxcox

#from sklearn.model_selection import train_test_split 
#from sklearn.linear_model import LinearRegression
#from sklearn import metrics
#from sklearn.preprocessing import MinMaxScaler

import seaborn as sns
sns.set_style('white')

import warnings
warnings.filterwarnings('ignore')

from IPython.display import display, Markdown

from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATSx, NHITS, LSTM, BiTCN, GRU
from neuralforecast.utils import AirPassengersDF

from neuralforecast.losses.pytorch import DistributionLoss
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MAE
from neuralforecast.auto import AutoLSTM
from ray import tune