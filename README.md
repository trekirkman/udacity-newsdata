# Newsdata Logs Project

## Overview

**newsdata.py** is a database reporting tool written in Python (2.7) for the Udacity Full Stack Nanodegree program. It connects to the **newsdata.sql** database, which features information relating to a hypothetical web-based news platform. The program executes PostgreSQL queries and prints the resulting data in a formatted list.

This tool seeks to answer the following questions:
1. Who are the top 3 most popular authors on this site, ranked by article views?
2. Who are the most popular authors, ranked by article views?
3. Are there any days where the percentage of HTTP logs with error codes exceeds 1%?

---

## Package Contents

### 1. newsdata.py
Python file containing all code to execute the queries and print results

### 2. newsdata_output.txt
 Plain text file containing printed results from `newsdata.py` 

---

## Instructions

### Install Python 2.7
Download can be found [here](https://www.python.org/downloads/)

### Install Virtual Box
VirtualBox is software that runs the Virtual Machine (VM) that will be used to run this program. Download [here](https://www.virtualbox.org/wiki/Downloads), and install the platform package. Note: you do not need the extension pack, SDK or to launch the program

### Install Vagrant
Vagrant configures the VM and establishes a shared directory between the VM and your local filesystem. Download [here](https://www.vagrantup.com/downloads.html) and download `vagrantfile` from this repo. Navigate to the directory containing `vagrantfile` and run

```vagrant up```

to set up the VM. Note: this process should take a while. 

When finished run

```vagrant ssh``` 

to log in to the virtual machine. For more information, see the Vagrant documentation [here](https://www.vagrantup.com/docs/).

### Download Database
Download `newsdata.sql`, found [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and place in your vagrant directory. To connect to the database run:

```psql -d news -f newsdata.sql```

### Create Custom SQL Views
`newsdata.py` makes use of three custom SQL Views for convenience. Download `create_views.sql` and then import the views:

```psql -d news -f create_views.sql```


### Download Program & Run
Download `newsdata.py` file to the same directory in the VM as newsdata.sql, and run:

```python newsdata.py```

---

## Custom Views
`newsdata.py` makes use of three custom SQL Views for convenience. The code used to create these views is listed below:

### 1. t_logs:  View that displays total logs per day
The code used to create the custom 

```sql
CREATE VIEW t_logs as
SELECT date_trunc('day', time) as day, 
count(*) as total 
FROM log 
GROUP BY day;
```


### 2. e_logs: View that displays total logs per day with an error status code

```sql
CREATE VIEW e_logs as
SELECT date_trunc('day', time) as day, 
count(*) as errors 
FROM log 
WHERE status like '4%' 
GROUP BY day;
```

---

## Functions

### 1. get_pop_articles()
Executes an SQL query that returns the top three articles of all time, ranked by view count.

### 1. get_pop_authors()
Executes an SQL query that returns all authors in the database, rank ordered by combined popularity of articles written.

### 1. get_error_logs()
Executes an SQL query that returns days where the database logs contained > 1% error status codes.

---

## License
[MIT](https://choosealicense.com/licenses/mit/)





