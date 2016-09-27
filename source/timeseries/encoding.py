'''
script that loads commits from express.git and encodes it into an image
TODO: now it loads the data from bare repo, however we have data prepared in postgresql that can be loaded in
'''
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import collections

date_format = '%Y-%m-%d'

def _rescale(serie):
    '''
    Rescale data into [0,1]
    '''
    maxval = max(serie)
    minval = min(serie)
    gap = float(maxval - minval)
    return [(each - minval) / gap for each in serie]


def _rescaleminus(serie):
    '''
    Rescale data into [-1,1]
    '''
    maxval = np.max(serie)
    minval = np.min(serie)
    gap = float(maxval - minval)
    return [(each - minval) / gap * 2 - 1 for each in serie]


def _paa(series, now, opw):
    '''
    PAA smoothing function
    '''
    if now is None:
        now = len(series) / opw
    if opw is None:
        opw = len(series) / now

    opw = int(opw)
    return [sum(series[i * opw: (i + 1) * opw]) / opw for i in range(now)]


def _add_missing_days(commits, labels):
    '''
    labels -> date strings in format '%Y-%m-%d'
    commits -> an array of number of commits
    there might be days where commit number is 0 and therefore they do not appear
    in the data, but for our analysis we need these 0 there.
    '''
    assert len(commits) > 0 and len(labels) > 0 and len(labels) == len(commits)

    commits_copy = [commits[0]]
    labels_copy = [labels[0]]

    previous = datetime.datetime.strptime(labels[0], date_format)
    for (l, c) in zip(labels[1:], commits[1:]):
        counter = 1
        while counter < 5000:
            added = previous + datetime.timedelta(days=counter)

            if added.strftime(date_format) == l:
                commits_copy.append(c)
                labels_copy.append(l)
                break
            else:
                commits_copy.append(0)
                labels_copy.append(added.strftime(date_format))

            counter += 1

        previous = datetime.datetime.strptime(l, date_format)

    return commits_copy, labels_copy


def display_encoded_time_series(time_series, date_labels):
    '''
    displays 2 plots for encoded time series
    '''
    time_series, labels = _add_missing_days(time_series, date_labels)
    time_series = np.array(time_series)
    time_series = np.add.accumulate(time_series)  # make it accumulate (for nicer plots, data doesn't gain or lose any value)
    std_data = _rescale(time_series)
    paalistcos = _paa(std_data, 64, None)

    datacos = np.array(std_data)
    datasin = np.sqrt(1 - np.array(std_data) ** 2)

    paalistcos = np.array(paalistcos)
    paalistsin = np.sqrt(1 - paalistcos ** 2)

    datacos = np.matrix(datacos)
    datasin = np.matrix(datasin)

    image = np.array(datasin.T * datacos - datacos.T * datasin)

    paalistcos = np.matrix(paalistcos)
    paalistsin = np.matrix(paalistsin)

    paaimage = np.array(paalistsin.T * paalistcos - paalistcos.T * paalistsin)

    length = len(time_series)
    r = np.array(range(1, length + 1))
    r = r / 100.0
    theta = np.array(_rescale(time_series)) * 2 * np.pi
    plt.figure()
    ax = plt.subplot(111, polar=True)
    ax.plot(theta, r, color='r', linewidth=3)
    plt.show()

    # draw large image and paa image

    plt.figure()
    ax1 = plt.subplot(121)
    plt.title('without PAA')
    plt.imshow(image)
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    plt.colorbar(cax=cax)
    ax2 = plt.subplot(122)
    plt.title('with PAA')
    plt.imshow(paaimage)
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    plt.colorbar(cax=cax)
    plt.show()




