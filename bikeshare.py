<<<<<<< HEAD
<<<<<<< HEAD
import time
import pandas as pd
import numpy as np

"""
I googled a number of python, numpy, and pandas concepts throughout this project.
I did not copy anything, but I did learn how to accomplish/implement tasked by
  reading through documentation and questions/solutions.

main sources: https://www.geeksforgeeks.org/
              https://www.python.org/
              https://www.stackoverflow.com/
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_inputs(question_str, comparison_list, wrong_str):
    """
    Asks user to specify a question and process the response.
    
    If 5 wrong inputs are given the program will be exited.

    Inputs:
        (str) question_str - a question asking for input from the user
        (list of str) comparison_list - what are "correct values" for the user input, assumes lower case
        (str) wrong_str - recommendation to help the user give a correct input, if the prior input was not in the list

    Returns:
        (str) value - the input value that was given by the user and in the comparison_list
    """
    count = 0
    match = False

    while count < 5:
        value = input(question_str).lower()

        for comparison_word in comparison_list:
            if comparison_word in value:
                match = True

        if match:
            break
        else:
            print("Sorry, your input wasn't recognized. " + wrong_str)
            count += 1

        if count == 5:
            print("That's 5 unrecognized inputs. This might not be the script for you. \n")
            print("Exiting program. Goodbye!")
            quit()
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_question_str = "Which city would you like to see data for; Chicago, New York City, or Washington? "
    cities_list = ("chicago", "new york city", "washington")
    city_wrong_str = "Please enter one of the three cities listed: Chicago, New York City, or Washington."
    city = check_inputs(city_question_str, cities_list, city_wrong_str)

    # Get user input for if they want to filter by month, day of the week (day), both, or none (Month, Day, Both, None = mdbn)
    filter_question_str = "Would you like to filter by month, day, both, or none? "
    filter_list = ("month", "day", "both", "none")
    filter_wrong_str = "Please enter one of the following: Month, Day, Both, None."
    mdbn = check_inputs(filter_question_str, filter_list, filter_wrong_str)

    if ("month" in mdbn) or ("both" in mdbn):
        # Get user input for month (all, january, february, ... , june)
        month_question_str = "Which month would you like to look at; (January - June, or all)? "
        month_list = ("all", "january", "february", "march", "april", "may", "june")
        month_wrong_str = "Please enter one of the months listed: All, January, February, March, April, May, or June."
        month = check_inputs(month_question_str, month_list, month_wrong_str)
    elif ("day" in mdbn) or ("none" in mdbn):
        month = "all"

    if ("day" in mdbn) or ("both" in mdbn):
        # Get user input for day of week (dow) (all, monday, tuesday, ... sunday)
        dow_question_str = "Which day of the week would you like to look at (Monday - Sunday, or all)? "
        dow_list = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        dow_wrong_str = "Please enter one of the days of the week listed: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
        day = check_inputs(dow_question_str, dow_list, dow_wrong_str)
    elif ("month" in mdbn) or ("none" in mdbn):
        day = "all"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("    Month: {}".format(months[df['month'].mode()[0] - 1].capitalize()))

    # Display the most common day of week
    print("    Day of the Week: {}".format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    print("    Hour to Start: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("    Starting Station: {}".format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print("    Ending Station: {}".format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    print("\nThe Most Popular Trip is: \n    {}".format(df["trip"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("    Total Travel Time: {}".format(df['Trip Duration'].sum()))

    # Display mean travel time
    print("    Average Travel Time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if ('Gender' in df):
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No Gender Data Available.')

    # Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df):
        print('Birth Year Data:\n')
        print('    Earliest Birth Year: {}'.format(df['Birth Year'].min()))
        print('    Latest Birth Year: {}'.format(df['Birth Year'].max()))
        print('    Most Common Birth Year: {}'.format(df['Birth Year'].mode()))
    else:
        print('No Birth Year Data Available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def produce_raw_data(df):
    """ Displays raw data 5 lines at a time. If user would like to see it. """

    count = 0    
    raw_question_str = "Would you like to see 5 lines of raw data? "
    
    while count + 5 < len(df):
        # Get user input on if they want to see raw data
        raw_list = ("yes", "no", "y", "n")
        raw_wrong_str = "Please enter one of the following: Yes or No."
        raw_yes_no = check_inputs(raw_question_str, raw_list, raw_wrong_str)
        raw_question_str = "Would you like to see 5 more lines of raw data? "

        # Display raw data, 5 lines at a time
        if raw_yes_no in 'yes':
            print(df[count:count + 5])
            count += 5
        elif raw_yes_no in 'no':
            break

    # Display final lines if there are any
    if count < len(df) and raw_yes_no in 'yes':
        print(df[count:len(df)])
        print('Those we the final lines of the file')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        produce_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    """ I truely enjoyed this project and it has been fun to apply what I learned. """
||||||| 06513a5
=======
import time
import pandas as pd
import numpy as np

"""
I googled a number of python, numpy, and pandas concepts throughout this project.
I did not copy anything, but I did learn how to accomplish/implement tasked by
  reading through documentation and questions/solutions .

main sources: https://www.geeksforgeeks.org/
              https://www.python.org/
              https://www.stackoverflow.com/
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_inputs(question_str, comparison_list, wrong_str):
    """
    Asks user to specify a question and process the response.
    
    If 5 wrong inputs are given the program will be exited.

    Inputs:
        (str) question_str - a question asking for input from the user
        (list of str) comparison_list - what are "correct values" for the user input, assumes lower case
        (str) wrong_str - recommendation to help the user give a correct input, if the prior input was not in the list

    Returns:
        (str) value - the input value that was given by the user and in the comparison_list
    """
    count = 0
    match = False

    while count < 5:
        value = input(question_str).lower()

        for comparison_word in comparison_list:
            if comparison_word in value:
                match = True

        if match:
            break
        else:
            print("Sorry, your input wasn't recognized. " + wrong_str)
            count += 1

        if count == 5:
            print("That's 5 unrecognized inputs. This might not be the script for you. \n")
            print("Exiting program. Goodbye!")
            quit()
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_question_str = "Which city would you like to see data for; Chicago, New York City, or Washington? "
    cities_list = ("chicago", "new york city", "washington")
    city_wrong_str = "Please enter one of the three cities listed: Chicago, New York City, or Washington."
    city = check_inputs(city_question_str, cities_list, city_wrong_str)

    # Get user input for if they want to filter by month, day of the week (day), both, or none (Month, Day, Both, None = mdbn)
    filter_question_str = "Would you like to filter by month, day, both, or none? "
    filter_list = ("month", "day", "both", "none")
    filter_wrong_str = "Please enter one of the following: Month, Day, Both, None."
    mdbn = check_inputs(filter_question_str, filter_list, filter_wrong_str)

    if ("month" in mdbn) or ("both" in mdbn):
        # Get user input for month (all, january, february, ... , june)
        month_question_str = "Which month would you like to look at; (January - June, or all)? "
        month_list = ("all", "january", "february", "march", "april", "may", "june")
        month_wrong_str = "Please enter one of the months listed: All, January, February, March, April, May, or June."
        month = check_inputs(month_question_str, month_list, month_wrong_str)
    elif ("day" in mdbn) or ("none" in mdbn):
        month = "all"

    if ("day" in mdbn) or ("both" in mdbn):
        # Get user input for day of week (dow) (all, monday, tuesday, ... sunday)
        dow_question_str = "Which day of the week would you like to look at (Monday - Sunday, or all)? "
        dow_list = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        dow_wrong_str = "Please enter one of the days of the week listed: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
        day = check_inputs(dow_question_str, dow_list, dow_wrong_str)
    elif ("month" in mdbn) or ("none" in mdbn):
        day = "all"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("    Month: {}".format(months[df['month'].mode()[0] - 1].capitalize()))

    # Display the most common day of week
    print("    Day of the Week: {}".format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    print("    Hour to Start: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("    Starting Station: {}".format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print("    Ending Station: {}".format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    print("\nThe Most Popular Trip is: \n    {}".format(df["trip"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("    Total Travel Time: {}".format(df['Trip Duration'].sum()))

    # Display mean travel time
    print("    Average Travel Time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if ('Gender' in df):
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No Gender Data Available.')

    # Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df):
        print('Birth Year Data:\n')
        print('    Earliest Birth Year: {}'.format(df['Birth Year'].min()))
        print('    Latest Birth Year: {}'.format(df['Birth Year'].max()))
        print('    Most Common Birth Year: {}'.format(df['Birth Year'].mode()))
    else:
        print('No Birth Year Data Available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def produce_raw_data(df):
    """ Displays raw data 5 lines at a time. If user would like to see it. """

    count = 0    
    raw_question_str = "Would you like to see 5 lines of raw data? "
    
    while count + 5 < len(df):
        # Get user input on if they want to see raw data
        raw_list = ("yes", "no", "y", "n")
        raw_wrong_str = "Please enter one of the following: Yes or No."
        raw_yes_no = check_inputs(raw_question_str, raw_list, raw_wrong_str)
        raw_question_str = "Would you like to see 5 more lines of raw data? "

        # Display raw data, 5 lines at a time
        if raw_yes_no in 'yes':
            print(df[count:count + 5])
            count += 5
        elif raw_yes_no in 'no':
            break

    # Display final lines if there are any
    if count < len(df) and raw_yes_no in 'yes':
        print(df[count:len(df)])
        print('Those we the final lines of the file')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        produce_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    """ I truely enjoyed this project and it has been fun to apply what I learned. """
>>>>>>> documentation
||||||| 06513a5
=======
import time
import pandas as pd
import numpy as np

"""
I googled a number of python, numpy, and pandas concepts throughout this project.
I did not copy anything, but I did learn how to accomplish/implement tasked by
  reading through documentation and questions/solutions.

main sources: https://www.geeksforgeeks.org/
              https://www.python.org/
              https://www.stackoverflow.com/
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_inputs(question_str, comparison_list, wrong_str):
    """
    Asks user to specify a question and process the response.
    
    If 5 wrong inputs are given the program will be exited.

    Inputs:
        (str) question_str - a question asking for input from the user
        (list of str) comparison_list - what are "correct values" for the user input, assumes lower case
        (str) wrong_str - recommendation to help the user give a correct input, if the prior input was not in the list

    Returns:
        (str) value - the input value that was given by the user and in the comparison_list
    """
    count = 0
    match = False

    while count < 5:
        value = input(question_str).lower()

        for comparison_word in comparison_list:
            if comparison_word in value:
                match = True

        if match:
            break
        else:
            print("Sorry, your input wasn't recognized. " + wrong_str)
            count += 1

        if count == 5:
            print("That's 5 unrecognized inputs. This might not be the script for you. \n")
            print("Exiting program. Goodbye!")
            quit()
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_question_str = "Which city would you like to see data for; Chicago, New York City, or Washington? "
    cities_list = ("chicago", "new york city", "washington")
    city_wrong_str = "Please enter one of the three cities listed: Chicago, New York City, or Washington."
    city = check_inputs(city_question_str, cities_list, city_wrong_str)

    # Get user input for if they want to filter by month, day of the week (day), both, or none (Month, Day, Both, None = mdbn)
    filter_question_str = "Would you like to filter by month, day, both, or none? "
    filter_list = ("month", "day", "both", "none")
    filter_wrong_str = "Please enter one of the following: Month, Day, Both, None."
    mdbn = check_inputs(filter_question_str, filter_list, filter_wrong_str)

    if ("month" in mdbn) or ("both" in mdbn):
        # Get user input for month (all, january, february, ... , june)
        month_question_str = "Which month would you like to look at; (January - June, or all)? "
        month_list = ("all", "january", "february", "march", "april", "may", "june")
        month_wrong_str = "Please enter one of the months listed: All, January, February, March, April, May, or June."
        month = check_inputs(month_question_str, month_list, month_wrong_str)
    elif ("day" in mdbn) or ("none" in mdbn):
        month = "all"

    if ("day" in mdbn) or ("both" in mdbn):
        # Get user input for day of week (dow) (all, monday, tuesday, ... sunday)
        dow_question_str = "Which day of the week would you like to look at (Monday - Sunday, or all)? "
        dow_list = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        dow_wrong_str = "Please enter one of the days of the week listed: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
        day = check_inputs(dow_question_str, dow_list, dow_wrong_str)
    elif ("month" in mdbn) or ("none" in mdbn):
        day = "all"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("    Month: {}".format(months[df['month'].mode()[0] - 1].capitalize()))

    # Display the most common day of week
    print("    Day of the Week: {}".format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    print("    Hour to Start: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("    Starting Station: {}".format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print("    Ending Station: {}".format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    print("\nThe Most Popular Trip is: \n    {}".format(df["trip"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("    Total Travel Time: {}".format(df['Trip Duration'].sum()))

    # Display mean travel time
    print("    Average Travel Time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if ('Gender' in df):
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No Gender Data Available.')

    # Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df):
        print('Birth Year Data:\n')
        print('    Earliest Birth Year: {}'.format(df['Birth Year'].min()))
        print('    Latest Birth Year: {}'.format(df['Birth Year'].max()))
        print('    Most Common Birth Year: {}'.format(df['Birth Year'].mode()))
    else:
        print('No Birth Year Data Available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def produce_raw_data(df):
    """ Displays raw data 5 lines at a time. If user would like to see it. """

    count = 0    
    raw_question_str = "Would you like to see 5 lines of raw data? "
    
    while count + 5 < len(df):
        # Get user input on if they want to see raw data
        raw_list = ("yes", "no", "y", "n")
        raw_wrong_str = "Please enter one of the following: Yes or No."
        raw_yes_no = check_inputs(raw_question_str, raw_list, raw_wrong_str)
        raw_question_str = "Would you like to see 5 more lines of raw data? "

        # Display raw data, 5 lines at a time
        if raw_yes_no in 'yes':
            print(df[count:count + 5])
            count += 5
        elif raw_yes_no in 'no':
            break

    # Display final lines if there are any
    if count < len(df) and raw_yes_no in 'yes':
        print(df[count:len(df)])
        print('Those we the final lines of the file')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        produce_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
>>>>>>> refactoring
