# Newsdata Project

**newsdata.py** is a database reporting tool written in python that connects to the **newsdata.sql** database, executes a series of postgresql queries, and prints the resulting data in list format. These queries return useful information regarding most popular articles, authors, and days with an unusually high percentage of error logs.

---

## Package Contents

### 1. newsdata.py
Python file containing all code to execute the queries and print results

### 2. newsdata_output.txt
 Plain text file containing printed results from `newsdata.py` 

### 3. README.md
Note: as requested, newsdata.sql database is not included in the submission of this project

---

## Functions

### 1. get_pop_articles()
Executes an SQL query that returns the top three articles of all time, ranked by view count.

### 1. get_pop_authors()
Executes an SQL query that returns all authors in the database, rank ordered by combined popularity of articles written.

### 1. get_error_logs()
Executes an SQL query that returns days where the database logs contained > 1% error status codes.

---

## Custom Views
The above functions utilize the following custom views. Each view is listed along with the code used to generate it.

### 1. tlogs:  View that displays total logs per day
The code used to create the custom 

`CREATE VIEW tlogs as
    SELECT date_trunc('day', time) as day, 
    count(*) as total 
    FROM log 
    GROUP BY day;`
    

### 2. elogs: View that displays total logs per day with an error status code

`CREATE VIEW elogs as
    SELECT date_trunc('day', time) as day, 
    count(*) as errors 
    FROM log 
    WHERE status like '4%' 
    GROUP BY day;`


