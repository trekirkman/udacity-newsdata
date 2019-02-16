#!/usr/bin/env python3
# newsdata.py — an internal db reporting tool
# Written & submitted by Tremaine Kirkman

import datetime
import psycopg2
import bleach

DBNAME = "news"
text_file = open("newsdata_output.txt", "w")


# MARK: - Declare Query Functions


# What are the most popular three articles of all time?
def get_pop_articles():
    # 1. Establish db connection
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()

    # 2. Query db for top 3 articles, defining views as logs w/ method = 'GET'
    query = """
        SELECT articles.id, articles.title, count(*) as views
        FROM articles, log
        WHERE CONCAT ('/article/', articles.slug) = log.path
        and log.method = 'GET'
        GROUP BY articles.id
        ORDER BY views desc limit 3;"""
    cursor.execute(query)
    result = cursor.fetchall()

    # 3. Close db connection and print result
    db.close()
    header = "Top 3 Articles of All Time:\n"
    text_file.write(header)
    print header
    str = "{}. \"{}\" - {} views\n"
    for index, row in enumerate(result):
        rank = index + 1
        output = str.format(rank, row[1], row[2])
        text_file.write(output)
        print output


# Who are the most popular article authors of all time?
def get_pop_authors():
    # 1. Establish db connection
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()

    # 2. Query db for top 3 articles, defining views as logs w/ method = 'GET'
    query = """
        SELECT authors.name, count(*) as views
        FROM articles, authors, log
        WHERE CONCAT ('/article/', articles.slug) = log.path
        and articles.author = authors.id
        and log.method = 'GET'
        GROUP BY authors.id
        ORDER BY views desc;
        """
    cursor.execute(query)
    result = cursor.fetchall()

    # 3. Close db connection and print result
    db.close()
    header = "Author popularity:\n"
    text_file.write(header)
    print header
    str = "{}. {} - {} views\n"
    for index, row in enumerate(result):
        rank = index + 1
        output = str.format(rank, row[0], row[1])
        text_file.write(output)
        print output


# On which days did more than 1% of requests lead to errors?
def get_error_logs():
    # 1. Establish db connection
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()

    # 2. Query db for error percentage, using custom views t_logs & e_logs
    pct_query = """
        SELECT t.day, ROUND((100 * CAST(e.errors as DECIMAL)
        / CAST(t.total as DECIMAL)), 1) as pct
        FROM t_logs as t, e_logs as e
        WHERE t.day = e.day
        GROUP BY t.day, e.errors, t.total
        HAVING ROUND((100 * CAST(e.errors as DECIMAL)
        / CAST(t.total as DECIMAL)), 1) > 1
        ORDER BY pct desc;
    """
    cursor.execute(pct_query)
    result = cursor.fetchall()

    header = "Days with error rate over 1%\n"
    text_file.write(header)
    print header
    f = '%B %d, %Y'
    str = "{}. {} - {}% errors\n"
    for index, row in enumerate(result):
        rank = index + 1
        time = datetime.datetime.strftime(row[0], f)
        output = str.format(rank, time, row[1])
        text_file.write(output)
        print output


# MARK: - Call Query Functions

get_pop_articles()
get_pop_authors()
get_error_logs()
text_file.close()
