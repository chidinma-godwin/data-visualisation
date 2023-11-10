#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 8 00:40:06 2023

@author: Chidex
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_line_graph(data, title, xlabel, ylabel):
    """
    Makes a line plot of the numeric columns in the given data

    Parameters
    ----------
    data : DataFrame
        The pandas dataframe to plot
    title: str
        The title of the plot
    xlabel: str
        The label of the X axis
    ylabel: str
        The label of the Y axis

    Returns
    -------
    None.

    """
    plt.figure(figsize=(10, 10))

    # This will plot all the numeric columns in the
    # dataframe using the index as the x-axis
    data.plot()

    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.xlim(data.index.min(), data.index.max())
    plt.legend()

    plt.savefig("line_plot.png", bbox_inches="tight")

    plt.show()


def plot_pie_chart(data, title):
    """
    Plot a pie chart of the given data

    Parameters
    ----------
    data : numpy array or pandas Series
        The sequence to plot
    title: str
        The title of the plot

    Returns
    -------
    None.

    """
    plt.figure()

    # Plot the chart as a percentage
    patches, texts, pcts = plt.pie(data, labels=data.index, autopct='%.1f%%',
                                   wedgeprops={'linewidth': 3.0,
                                               'edgecolor': 'white'},
                                   textprops={'fontweight': 600})

    # Set the colour of the label of each wedge to the wedge colour
    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())

    # Set the color of the percent values inside the pie to white
    plt.setp(pcts, color='white')

    plt.title(title, fontweight="bold")
    plt.tight_layout()

    plt.savefig("piechart.png")

    plt.show()


def plot_bar_chart(data, title, xlabel, ylabel):
    """
    Plot a bar chart of the given data

    Parameters
    ----------
    data : DataFrame
        The data frame to plot
    title: str
        The title of the plot
    xlabel: str
        The label of the X axis
    ylabel: str
        The label of the Y axis

    Returns
    -------
    None.

    """
    plt.figure(figsize=(10, 10))

    data.plot(kind="bar")

    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.25, 0.6), loc='center right')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("barchart.png")

    plt.show()


def plot_bubble_plot(x, y, col, title, xlabel, ylabel, legend_handles):
    """
    Plots a bubble plot with the given data

    Parameters
    ----------
    x : Series
        The x coordinates of the data points.
    y : Series
        The y coordinates of the data points.
    col : Series
        The sequence of colors for setting the colour of each points.
    title : str
        The title of the plot.
    xlabel: str
        The label of the X axis
    ylabel: str
        The label of the Y axis
    legend_handles : sequence
        Color box for creating the legend.

    Returns
    -------
    None.

    """
    plt.figure(figsize=(10, 10))

    plt.scatter(x, y, c=col, s=200, alpha=0.5)

    plt.title(title, fontweight="bold")
    plt.xlim(x.min(), x.max())
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    # Create a custom legend
    plt.legend(handles=legend_handles,
               loc="upper center", framealpha=0.2)

    # Save the plot
    plt.savefig("bubble-plot.png")

    plt.show()


def clean_outliers(column_data):
    '''
    Checks the column for outliers and sets them to a suitable value

    Parameters
    ----------
    column_data : Series
        The series to check for outliers .

    Returns
    -------
    The series with the outliers set to either the upper or lower limit.

    '''
    q3, q1 = np.quantile(column_data, [0.75, 0.25])
    iqr = q3 - q1
    lower_limit = q1 - 1.5*iqr
    upper_limit = q3 + 1.5*iqr

    # Set outliers above the upper limit to the upper limit
    column_data[column_data >= upper_limit] = upper_limit

    # Set outliers below the lower limit to the lower limit
    column_data[column_data <= lower_limit] = lower_limit

    return column_data


""" 
    import and visualise data on museum visitors
"""

museum_visitors = pd.read_csv('https://data.lacity.org/resource/trxm-jn3c.csv')

# Select the columns we want to work with
museum_visitors = museum_visitors.loc[:, [
    "month", "avila_adobe", "firehouse_museum", "america_tropical_interpretive_center", "chinese_american_museum"]]
museum_visitors.fillna(method="ffill", inplace=True)

# Rename the columns
museum_visitors.rename(columns={"month": "Date", "avila_adobe": "Avila Adobe", "firehouse_museum": "Firehouse Museum",
                                "america_tropical_interpretive_center": "America Tropical center",
                                "chinese_american_museum": "Chinese American Museum"}, inplace=True)

# Convert the Date column to a datetime tipe
museum_visitors['Date'] = museum_visitors['Date'].str.split('T').str[0]
museum_visitors['Date'] = pd.to_datetime(
    museum_visitors['Date'], format='%Y-%m-%d')

# Set the date column as the index of the data
museum_visitors.set_index('Date', inplace=True)

""" Draw a line plot of the data """
plot_line_graph(museum_visitors,
                title="Visitors to Different El Pueblo Museums",
                xlabel="Year",
                ylabel="Number of visitors")


# Get the sum of visitors in 2017 for each museum
museum_visitors_2017 = museum_visitors.loc["2017-01-01": "2017-12-01"].sum(
    axis=0)

""" Plot a pie chart of the percange of visitors that visited each museum """
plot_pie_chart(museum_visitors_2017,
               'El Pueblo Museums Monthly Visitors in 2017')

# Plot a bar chart of the visitors that visited each museum yearly
yearly_museum_visitors = museum_visitors.resample('Y').sum()
yearly_museum_visitors.index = yearly_museum_visitors.index.year

""" Plot a bar chart of the yearly museum visitors """
plot_bar_chart(yearly_museum_visitors,
               title="Yearly Number of El Pueblo Museum Visitors",
               xlabel="Years", ylabel="Number of Visitors")


"""
    Import and visualise data on pdp of countries
"""

gdp_data = pd.read_csv(
    'https://vincentarelbundock.github.io/Rdatasets/csv/AER/GrowthDJ.csv')

# Select the columns to use
gdp_data = gdp_data.loc[:, ["oecd", "gdp60", "gdp85"]]

# Drop countries with missing data
gdp_data.dropna(inplace=True)

# Set outliers to appropraite values
cleaned_gdp85_gdp60 = gdp_data[["gdp85", "gdp60"]].apply(clean_outliers)
gdp_data["gdp85"] = cleaned_gdp85_gdp60["gdp85"]
gdp_data["gdp60"] = cleaned_gdp85_gdp60["gdp60"]

# Create color box to use for custom legend
color = {"yes": "green", "no": "red"}
oecd_patch = mpatches.Patch(color="green", label="OECD Country")
non_oecd_patch = mpatches.Patch(color="red", label="NON OECD Country")

""" Make the bubble plot """
plot_bubble_plot(gdp_data["gdp60"], gdp_data["gdp85"],
                 col=gdp_data["oecd"].map(color),
                 title="Cross Country GDP",
                 xlabel="Per capita GDP in 1960",
                 ylabel="Per capita GDP in 1960",
                 legend_handles=[oecd_patch, non_oecd_patch])
