import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        "Which city you would like to explore [Chicago, New York City, Washington]:\n").lower()
    while city not in cities:
        city = input(
            "Please enter only [Chicago, New York City, Washington]:\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input(
        "\nIf you want to filter by month enter the month you want to filter by [January, February, March, April, May, June] or enter [all] for no filter:\n").lower()
    while month not in months and month != "all":
        month = input(
            "Please enter only [January, February, March, April, May, June] or [all] for no filter:\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        "If you want to filter by day enter the day you want to filter by [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] or enter [all] for no filter:\n").lower()
    while day not in days_of_week and day != "all":
        day = input(
            "Please enter only [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] or [all] for no filter:\n").lower()

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print('Most Popular Month:', df['month'].mode()[0])

    # display the most common day of week
    if day == 'all':
        print('Most Popular Day:', df['day_of_week'].mode()[0])

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    print('Most Popular Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Popular Start Station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Popular End Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    most_trip = df.groupby(['Start Station', 'End Station'])['Trip Duration'].agg(
        'count').sort_values(ascending=False).head(1).to_string()
    print("Most Popular trip: \n", most_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Average Travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types:\n",
          df['User Type'].value_counts().to_string())

    if city != 'washington':
        # Display counts of gender
        print("The counts of gender: ",
              df['Gender'].value_counts().to_string())

        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year: ", df['Birth Year'].min())
        print("The most recent year: ", df['Birth Year'].max())
        print("The most common year: ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_rows(df):
    """Display the first 5 rows of the DataFrame and print next 5 rows as the user wish"""
    print_rows = 'yes'
    first_row = 0
    second_row = 5
    while print_rows.lower() == 'yes':
        print(df[first_row:second_row])
        first_row += 5
        second_row += 5
        print_rows = input(
            '\nWould you like to print more rows? Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
