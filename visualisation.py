#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 00:40:06 2023

@author: Chidex
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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


def plot_bubble_plot(x, y, col, title, legend_handles):
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
    legend_handles : sequence
        Color box for creating the legend.

    Returns
    -------
    None.

    """
    plt.figure(figsize=(10, 10))

    plt.scatter(x, y, c=col, s=200, alpha=0.5)

    plt.title(title)
    plt.xlim(x.min(), x.max())
    plt.xlabel("Per capita GDP in 1960")
    plt.ylabel("Per capita GDP in 1985")
    plt.grid()

    # Create a custom legend
    plt.legend(handles=legend_handles,
               loc="upper center", framealpha=0.2)

    # Save the plot
    plt.savefig("bubble-plot.png")

    plt.show()


def plot_line_graph(data):
    """
    Makes a line plot of the numeric columns in the given data

    Parameters
    ----------
    data : DataFrama
        The pandas dataframe to plot

    Returns
    -------
    None.

    """
    plt.figure(figsize=(10, 10))
    
    # This will plot all the numeric columns in the
    # dataframe using the index as the x-axis
    data.plot()

    plt.title("Monthly Visitors To Different Museums")
    plt.xlabel("Year")
    plt.ylabel("Number of visitors")
    plt.xticks(rotation=45)
    plt.legend()

    plt.savefig("line_plot.png", bbox_inches="tight")

    plt.show()


""" Import and visualise data on pdp of countries """

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

# Make the bubble plot
plot_bubble_plot(gdp_data["gdp60"], gdp_data["gdp85"],
                 gdp_data["oecd"].map(color), "Cross Country GDP",
                 [oecd_patch, non_oecd_patch])


""" Import and visualise data on museum visitors """

museum_visitors = pd.read_csv("museum_visitors.csv")

# Set the date column as the index of the data
museum_visitors.set_index('Date', inplace=True)

plot_line_graph(museum_visitors)
