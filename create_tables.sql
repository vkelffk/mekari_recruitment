-- Create the 'employees' table
CREATE TABLE IF NOT EXISTS employees (
    employe_id INTEGER,
    branch_id INTEGER,
    salary NUMERIC,
    join_date DATE,
    resign_date DATE
);

-- Create the 'timesheets' table
CREATE TABLE IF NOT EXISTS timesheets (
    timesheet_id INTEGER,
    employee_id INTEGER,
    date DATE,
    checkin VARCHAR,
    checkout VARCHAR
);

-- Create the destination table 'branch_salary_per_hour'
CREATE TABLE IF NOT EXISTS branch_salary_per_hour (
    year INTEGER,
    month INTEGER,
    branch_id INTEGER,
    salary_per_hour NUMERIC,
    updated_at TIMESTAMP
);