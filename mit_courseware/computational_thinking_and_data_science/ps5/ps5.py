# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy
import statistics

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models_coeff = list()
    
    for deg in degs:
        models_coeff.append(pylab.polyfit(x, y, deg))
    
    return models_coeff     


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = ((estimated - y)**2).sum()
    mean_error = error/len(y)
    return 1 - (mean_error/numpy.var(y))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = pylab.poly1d(model)   # setting degree of polynomial
        r2 = r_squared(y, p(x))
        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(x, p(x), 'r-', label='Model')
        pylab.legend(loc='best')
        if len(model) == 2:
            pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r2} \n Ratio of SE: {se_over_slope(x, y, p(x), model)}.')
        else:
            pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r2}')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')
        pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avg_temp_per_year = list()
    for year in years:
        # collect all the temp for cities in a given year
        given_year = list()
        for city in multi_cities:
            given_year.append(climate.get_yearly_temp(city, year))
        avg_temp_per_year.append(pylab.mean(pylab.array(given_year)))
    return pylab.array(avg_temp_per_year)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    i = 0
    moving_y = list()
    while i < len(y) - window_length + 1:
        moving_y.append(numpy.average(y[i:i+window_length]))
        
    return pylab.array(moving_y)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    error = ((estimated - y)**2).sum()
    meanError = error/len(y)
    return 1 - (meanError/numpy.var(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # std_dev_cities = list()
    # for year in years:
    #     # go through each city and then add the temp at given date
    #     year_temp = list()
    #     for city in multi_cities:
    #         # get the 1 year temp for each city and append to the list year
    #         city_year_avg = climate.get_yearly_temp(city, year)
    #         year_temp.append(numpy.mean(city_year_avg))
    #     # find the std dev at the given year
    #     std_dev_cities.append(statistics.stdev(year_temp))

    # return pylab.array(std_dev_cities)

    std_devs = []

    #iterate thru years
    for year in years:
        #iterate thru cities
        for city in range(len(multi_cities)):
            #if its the first city create the array
            if city == 0:
                city_list = numpy.array(climate.get_yearly_temp(multi_cities[city],year))
            #otherwise add up the arrays
            else:
                city_list += climate.get_yearly_temp(multi_cities[city],year)
        #find the average temp at each date
        city_list = city_list / len(multi_cities)
        #compute the std and append to the back of the list
        std = numpy.std(city_list)

        std_devs.append(std)
        
    
    return pylab.array(std_devs)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = pylab.poly1d(model)
        rmse_value = rmse(y, p(x))
        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(x, p(x), 'r-', label='Model')
        pylab.legend(loc='best')
        pylab.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_value}')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')
        pylab.show()
        

if __name__ == '__main__':

    # Part A.4
    # provide x values
    years = list(TRAINING_INTERVAL)
    y_values = list()
    climate = Climate('data.csv')
    for year in years:
        y_values.append(climate.get_daily_temp('NEW YORK', 1, 10, year))
    # generate models
    models = generate_models(pylab.array(years), pylab.array(y_values), [1])
    # evalute the models on training
    evaluate_models_on_training(pylab.array(years), pylab.array(y_values), models)
    
    # Part B
    years = list(TRAINING_INTERVAL)
    climate = Climate('data.csv')
    y_values = gen_cities_avg(climate, CITIES, list(TRAINING_INTERVAL))

    # generate the models
    models = generate_models(pylab.array(years), y_values, [1])
    # evalute the models
    evaluate_models_on_training(pylab.array(years), y_values, models)
    
    # Part C
    # TODO: replace this line with your code

    # Part D.2
    # TODO: replace this line with your code

    # Part E
    # calculate the std_dev of all the cities
    climate = Climate('data.csv')
    std_dev = gen_std_devs(climate, CITIES, list(TRAINING_INTERVAL))
    # compute the 5 year moving average
    window_length = 5
    moving_avg = moving_average(std_dev, window_length)
    
    # generate the model
    model = generate_models(list(TRAINING_INTERVAL), moving_avg, [1])
    # evalute models
    evaluate_models_on_training(pylab.array(list(TRAINING_INTERVAL)), moving_avg, model)
