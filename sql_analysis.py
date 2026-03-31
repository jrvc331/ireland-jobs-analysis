import pandas as pd
import sqlite3

# Load the clean CSV into a SQLite database
df = pd.read_csv("output/ireland_employment_clean.csv")

conn = sqlite3.connect("output/ireland_jobs.db")
df.to_sql("employment", conn, if_exists="replace", index=False)

# SQL Query 1: Total employment by sector in 2024
q1 = pd.read_sql_query("""
    SELECT Sector, ROUND(Employed_Thousands, 2) as Employed_Thousands
    FROM employment
    WHERE Year = 2024
    ORDER BY Employed_Thousands DESC
""", conn)

# SQL Query 2: Year with highest employment for each sector
q2 = pd.read_sql_query("""
    SELECT Sector, Year, ROUND(MAX(Employed_Thousands), 2) as Peak_Employment
    FROM employment
    GROUP BY Sector
    ORDER BY Peak_Employment DESC
""", conn)

# SQL Query 3: Average employment per sector across all years
q3 = pd.read_sql_query("""
    SELECT Sector, ROUND(AVG(Employed_Thousands), 2) as Avg_Employment
    FROM employment
    GROUP BY Sector
    ORDER BY Avg_Employment DESC
""", conn)

# SQL Query 4: Sectors that grew every single year
q4 = pd.read_sql_query("""
    SELECT a.Sector, a.Year, ROUND(a.Employed_Thousands, 2) as Current,
           ROUND(b.Employed_Thousands, 2) as Previous,
           ROUND(a.Employed_Thousands - b.Employed_Thousands, 2) as Growth
    FROM employment a
    JOIN employment b ON a.Sector = b.Sector AND a.Year = b.Year + 1
    WHERE a.Employed_Thousands > b.Employed_Thousands
    ORDER BY a.Sector, a.Year
""", conn)

# SQL Query 5: Employment recovery post-COVID (2020 vs 2022)
q5 = pd.read_sql_query("""
    SELECT a.Sector,
           ROUND(a.Employed_Thousands, 2) as Employment_2020,
           ROUND(b.Employed_Thousands, 2) as Employment_2022,
           ROUND(b.Employed_Thousands - a.Employed_Thousands, 2) as Recovery
    FROM employment a
    JOIN employment b ON a.Sector = b.Sector
    WHERE a.Year = 2020 AND b.Year = 2022
    ORDER BY Recovery DESC
""", conn)

conn.close()

# Save results
q1.to_csv("output/sql_q1_2024_employment.csv", index=False)
q2.to_csv("output/sql_q2_peak_employment.csv", index=False)
q3.to_csv("output/sql_q3_avg_employment.csv", index=False)
q4.to_csv("output/sql_q4_consistent_growth.csv", index=False)
q5.to_csv("output/sql_q5_covid_recovery.csv", index=False)

print("=== Q1: Employment by Sector in 2024 ===")
print(q1.to_string(index=False))
print("\n=== Q2: Peak Employment Year per Sector ===")
print(q2.to_string(index=False))
print("\n=== Q3: Average Employment per Sector ===")
print(q3.to_string(index=False))
print("\n=== Q5: COVID Recovery 2020 vs 2022 ===")
print(q5.to_string(index=False))

print("\nDone. SQL queries saved in output/ folder.")
