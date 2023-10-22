## General Info
- `branch_salary_per_hour.sql`: The answer to task (a). An SQL ETL script.
- `create_tables.sql`: Contains DDL for tables used in `branch_salary_per_hour.sql`.
- `branch_salary_per_hour.ipynb`: Performs data analysis and processing to gain insights.
- `branch_salary_per_hour.py`: The answer to task (b). A Python ETL script.
- Both `branch_salary_per_hour.py` and `branch_salary_per_hour.ipynb` contain the same code. However, in the `.ipynb` file, you can find a line-by-line data processing with more explanations, as well as the reasons behind assumptions and conclusions about data treatment.
- `salary_per_hour.csv` is the output from the Python script.
- I'm using the same data cleaning process in both `.py` and `.sql` scripts.

## Assumptions
- An employee with 0 working hours (i.e., `checkout - checkin = 0`) is considered to be on paid leave, so I will retain the 0 values.
- The company's policy is 8 working hours a day.
- The Python script pipeline will run after we receive complete data for a day's timesheets with no missing dates. Therefore, it's safe to only process data with the `max(date)` in the `.py` script. This filtered data is considered as "new" data.

## How to Use the Notebook & Python Script
#### - `branch_salary_per_hour.ipynb`
You can simply view it on the Github website or open the file in your local environment.
1. Create and activate a virtual environment:


```
python -m venv env
source env/bin/activate
```
2. Install & run jupyter notebook
```
pip install jupyter
jupyter notebook
```
3. Open the `branch_salary_per_hour.ipynb` file



#### - `branch_salary_per_hour.py`
1. Run the following command within the folder path:
```
python branch_salary_per_hour.py
```
The output is a csv file named: `salary_per_hour.csv`
