import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    #Load the data
    data = pd.read_csv('epa-sea-level.csv')

    #Create a scatter plot
    plt.figure(figsize=(10, 6))
    ax = plt.scatter(data['Year'], data['CSIRO Adjusted Sea Level'], label='Data Points', alpha=0.7)

    #Perform linear regression for all data
    slope, intercept, _, _, _ = linregress(data['Year'], data['CSIRO Adjusted Sea Level'])

    #Generate prediction values
    years_extended = pd.Series(range(1880, 2051))
    sea_levels_extended = intercept + slope * years_extended

    #Plot the first line of best fit
    plt.plot(years_extended, sea_levels_extended, 'r', label='Best Fit (All Data)')

    #Filter data from year 2000 onwards
    data_recent = data[data['Year'] >= 2000]

    #Perform linear regression for recent data
    slope_recent, intercept_recent, _, _, _ = linregress(data_recent['Year'], data_recent['CSIRO Adjusted Sea Level'])

    #Generate prediction values for recent data
    years_recent = pd.Series(range(2000, 2051))
    sea_levels_recent = intercept_recent + slope_recent * years_recent

    #Plot the second line of best fit
    plt.plot(years_recent, sea_levels_recent, 'g', label='Best Fit (2000 Onward)')

    #Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    plt.grid(True)

    #Return the Axes object
    ax = plt.gca()
    return ax
