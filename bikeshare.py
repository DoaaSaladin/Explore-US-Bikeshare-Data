import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Cities = {'nyc':'new york city', 'chi':'chicago', 'wa':'washington'}

Months = {'jan':'january', 'feb':'february', 'mar':'march', 'apr':'april',
          'may':'may', 'jun':'june', 'non':'all'}

Days = {'sun':'sunday', 'mon':'monday', 'tues':'tuesday', 'wed':'wednesday',
        'thur':'thursday', 'fri':'friday', 'sat':'saturday', 'non':'all'}

def validity_checker(user_input , sequence_key):
    while True:
        input_check = input(user_input)
        try:
            if input_check in Cities.keys() and sequence_key == 0:
                print('\n\nnice.... let\'s see how do you want to display your data...\n\n')
                break
            elif input_check in Months.keys() and sequence_key == 1:
                print('\n\n.... you\'re getting closer\n\n')
                break
            elif input_check in Days.keys() and sequence_key ==2:
                print('\n\nHola! It\'s time to explore your data, stay connected\n\n')
                break
            else:
                if sequence_key == 0:
                    print('\n\nplease eneter a valid city abbreviation!!\n\n')
                if sequence_key == 1:
                    print('\n\nplease eneter a month from january to june, or type "non"\n\n')
                if sequence_key == 2:
                    print('\n\nplease eneter a valid day name from monday to sunday, or type "non"\n\n')
        except KeyboardInterrupt or KeyError:
                print('\nNo Input Taken!!\nPlease eneter one of the listed city abbreviation')
                
    return input_check


def get_filters():
    
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')   
    
    selected_city = validity_checker('Kindly type the abbreviation for the city you wish to explore:\n {}\n'.format(list(Cities.items())).lower() , 0)
    city = Cities[selected_city]
    
    selected_month = validity_checker('Enter a month from the availble range to display more specific data, or you can simply type "non" to access the whole scope\n \n {}\n'.format(list(Months.keys())).lower() , 1)
    month = Months[selected_month]

    selected_day = validity_checker('Please enter the name of the day you wish to inspect or enter "non" to access the whole week data\n {}\n'.format(list(Days.keys())).lower() , 2)
    day = Days[selected_day]

    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    cityfile = CITY_DATA[city]
    print('retriving your data from {} for {}, {}, and {}'.format(cityfile , city, month , day))
    df = pd.read_csv(cityfile)

    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filtering by month if applicable
    if month != 'all':
        months = list(Months.values())
        month = months.index(month)+1
        df = df.loc[df['month'] == month]

    # filtering by day of week if applicable
    if day != 'all':
        df = df.loc[df['weekday'] == day.title()]
       
     
    return df


def time_stats(df):
       
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month: ' , df['month'].mode()[0])

    # display the most common day of week
    print('The most common day of week: ' , df['weekday'].mode()[0])

     # find the most popular hour
    print('The most common hour: ' , df['hour'].mode()[0])
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used start station is: {}'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used End station is: {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['Complete Trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' to >>> ')
    common_combined_trip = df['Complete Trip'].mode()[0]
    print('Most commonly trip Combination starts from:{}'.format(common_combined_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
  
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_ttime = df['Trip Duration'].sum()
    print('Total travel time is: {}'.format(total_ttime))

    # display mean travel time
    average_ttime = df['Trip Duration'].mean()
    print('Average travel time is: {}'.format(average_ttime))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
   
    print('\nCalculating User Stats...\n')
    start_time = time.time()
   
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nuser types:\n{}\n'.format(user_types))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender =df['Gender'].value_counts()
        print('\ngenders:\n{}\n'.format(gender))
    else:
        print('\ngender type is not available for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        early_bd = int(df['Birth Year'].min())
        recent_bd = int(df['Birth Year'].max())
        common_bd = int(df['Birth Year'].mode()[0])

        print('\nthe earliest year of birth is... {}\n'.format(early_bd))
        print('\nthe most recent year of birth is... {}\n'.format(recent_bd))
        print('\nthe most common year of birth is... {}\n'.format(common_bd))
    else:
        print('\nyear of birth is not available for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    user_input = ['yes', 'no']
    display_raw = input('\nRaw data is available, do you want to display some?!\n Type {} or {}\n'.format(user_input[0], user_input[1]).lower())
    if display_raw not in user_input:
        print('Invalid input, the system will skip!')
    else:
        while display_raw.lower() == 'yes':
            try:
                def chunker(seq, size):
                    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
                for i in chunker(df, 5):
                    print(i)
                    display_raw = input('\nYou may want to have a look at more raw data?!\n Type yes or no\n')
                    
                    if display_raw == 'no':
                        print('Thank You..')
                        break
                    elif display_raw != 'yes' or 'no':
                        print('Invalid input, system will skip!')
                        break
            except KeyboardInterrupt:
                print('Invalid input, the system will skip!')

 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for using our Bikeshare statistics explorer')
            break


if __name__ == "__main__":
	main()
