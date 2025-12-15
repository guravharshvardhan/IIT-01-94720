import pandas as pd
import pandasql as ps


filepath = r"emp_hdr(1).csv"
df = pd.read_csv(filepath)
print("Dataframe Column Types:")
print(df.dtypes)
print("\nEmp Data:")
print(df)
# query = "SELECT * FROM data WHERE sal BETWEEN 1000 AND 2000 ORDER BY sal"
query = """
SELECT job, SUM(sal) AS total
FROM data
GROUP BY job
"""
result = ps.sqldf(query, {"data": df})
print("\nQuery Result:")
print(result)
