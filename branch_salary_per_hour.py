import pandas as pd
from datetime import date, datetime

def extract(employees_df, timesheets_df):
    '''
    Extracts data for better usability. 
    Starts by merging both the 'employees' and 'timesheets' tables, filtered yesterday data,
    processes the time string values to make them suitable for calculations,
    and calculates the hours worked by subtracting the checkout and check-in times.
    '''

    df = pd.merge(timesheets_df, employees_df, on='employee_id')
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    max_date = df['date'].max() # Getting new data
    filtered_df = df[df['date'].dt.month == max_date.month] # Get all data from the same month as the new data

    # Uncomment line code below to use all data for further process
    # filtered_df = df

    filtered_df['checkin'] = pd.to_datetime(filtered_df['date'].astype(str) + ' ' + filtered_df['checkin'])
    filtered_df['checkout'] = pd.to_datetime(filtered_df['date'].astype(str) + ' ' + filtered_df['checkout'])

    filtered_df['hours_worked'] = (filtered_df['checkout'] - filtered_df['checkin']).dt.total_seconds() / 3600
    filtered_df['hours_worked'] = filtered_df['hours_worked'].abs()

    return filtered_df

def calculate_salary_perhour(df):
    '''
    Calculates salary perhour.
    'hours_worked' missing data will be replaced by 8 (assuming an 8-hour workday company's policy)
    '''

    df['hours_worked'].fillna(8, inplace=True)

    # DataFrame for total salary per month
    total_salary_permonth = df.drop_duplicates(subset=['branch_id', 'year', 'month', 'employee_id']).groupby(['branch_id', 'year', 'month']).agg(
        total_salary=('salary', 'sum'),
        employee_counts=('employee_id', 'nunique')
    ).reset_index()
    # DataFrame for sum of hours worked per month
    sum_hours_worked = df.groupby(['branch_id', 'year', 'month']).agg(
        total_hours_worked=('hours_worked', 'sum'),
        employee_counts=('employee_id', 'nunique')
    ).reset_index()

    result_df = total_salary_permonth.merge(sum_hours_worked, on=['branch_id', 'year', 'month', 'employee_counts'])
    result_df['salary_per_hour'] = result_df['total_salary'] / result_df['total_hours_worked']
    result_df['updated_at'] = datetime.now()

    return result_df

def load_to_destination(csv_path, result_df):
    '''
    Loads final result to destination csv.
    Will only update existing branch_id, year, month with new entry in result_df
    or create new row for brand new entry in destination csv
    '''
    try:
        existing_data = pd.read_csv(csv_path)
        existing_data = pd.concat([existing_data, result_df], ignore_index=True)
        existing_data.to_csv(csv_path, index=False)
    except FileNotFoundError:
        # If the CSV file does not exist, create a new DataFrame from result_df
        existing_data = result_df
        existing_data.to_csv(csv_path, index=False)

if __name__ == "__main__":
    employees_df = pd.read_csv("employees.csv")
    employees_df = employees_df.rename(columns={'employe_id': 'employee_id'})
    timesheets_df = pd.read_csv("timesheets.csv")

    filtered_df = extract(employees_df, timesheets_df)
    result_df = calculate_salary_perhour(filtered_df)

    load_to_destination('salary_per_hour.csv', result_df)
