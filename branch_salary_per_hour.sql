-- Import csv data to tables
COPY employees FROM 'employees.csv' DELIMITER ',' CSV HEADER;
COPY timesheets FROM 'timesheets.csv' DELIMITER ',' CSV HEADER;

-- CTEs
-- employee_salary: retrieves the salary from the "employees" table 
-- for each unique employee within a branch, year, and month. 
WITH employee_salary AS (
    SELECT
        e.employee_id,
        e.branch_id,
        EXTRACT(YEAR FROM t.date) AS year,
        EXTRACT(MONTH FROM t.date) AS month,
        e.salary
    FROM employees e
    INNER JOIN timesheets t ON e.employee_id = t.employee_id
)
-- total_salary: sum of salary of a branch per month, per year
total_salary AS (
    SELECT
        branch_id,
        year,
        month,
        SUM(salary) AS sum_salary
    FROM employee_salary
    GROUP BY branch_id, year, month
),
-- hours_worked_perday: retrieves hours worked perday of an employee
hours_worked_perday AS (
    SELECT 
        e.branch_id,
        EXTRACT(YEAR FROM t.date) AS year,
        EXTRACT(MONTH FROM t.date) AS month,
        ABS(COALESCE(EXTRACT(EPOCH FROM (to_timestamp(t.date || ' ' || t.checkout, 'YYYY-MM-DD HH24:MI:SS') - 
            to_timestamp(t.date || ' ' || t.checkin, 'YYYY-MM-DD HH24:MI:SS'))) / 3600), 8.0) AS hours_worked
    FROM employees e
    LEFT JOIN timesheets t ON e.employe_id = t.employee_id
),
-- total_hours_worked: sum of hours worked of a branch per month, per year
total_hours_worked AS (
    SELECT 
        branch_id,
        year,
        month,
        SUM(hours_worked) AS sum_hours_worked
    FROM hours_worked_perday
    GROUP BY branch_id, year, month
)

-- Insert the result to destination table. 
-- Only overwrites data with changed salary_per_hour value
INSERT INTO branch_salary_per_hour (year, month, branch_id, salary_per_hour, updated_at)
SELECT
    branch_id,
    year,
    month,
    total_salary.sum_salary / total_hours_worked.sum_hours_worked AS salary_per_hour,
    NOW() AS updated_at
FROM total_salary
JOIN total_hours_worked USING (branch_id, year, month)
ON CONFLICT (year, month, branch_id) DO UPDATE
SET
    salary_per_hour = EXCLUDED.salary_per_hour,
    updated_at = NOW();