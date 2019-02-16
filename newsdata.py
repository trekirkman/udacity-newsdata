#!/usr/bin/env python
# newsdata.py: an internal db reporting tool
# Written & submitted by Tremaine Kirkman

import datetime
import psycopg2
import bleach

DBNAME = "news"
OUTPUT_FILE_NAME = "newsdata_output.txt"

# MARK: - Declare Query Functions


def create_log_file(file_name=OUTPUT_FILE_NAME):
    file = open(file_name, 'w+')

    def write(text):
        file.write(text + '\n')
    
    def close():
        file.close()

    return write, close

log_write, log_close = create_log_file()

def execute_query(query):
    """
    returns the results of an SQL query.

    execute_query takes an SQL query as a parameter,
    executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """

    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def print_output(header, str, result):
    """prints a header and formatted result from an SQL query

    print_output takes a header string, a formatted string with three values
    to subsittute, and a list of tuples from an SQL query. It iterates
    over each row of tuples, inserting values into str object
    and prints the result.

    args:
    header - a string describing the output
    str - a formatted string to insert tuple values into
    result - SQL output as list of tuples, to be inserted into str
    """
    log_write(header)
    print header
    for index, row in enumerate(result, 1):
        output = str.format(index, row[0], row[1])
        log_write(output)
        print output


def get_pop_articles():
    """
    Print the top three articles by views.

    Prints a list of article titles, along with the number of views each title
    has, ordered by the number of views. Only the top three are printed. The
    list is printed to the console.
    """

    query = """
        SELECT articles.title, log.views
        FROM articles, log_path AS log
        WHERE log.path = '/article/' || articles.slug
        GROUP BY articles.title, log.views
        ORDER BY views desc limit 3;"""

    result = execute_query(query)
    header = "Top 3 Articles of All Time:"
    str = "{}. \"{}\" - {} views"
    print_output(header, str, result)


def get_pop_authors():
    """
    Print list of authors, ranked by article views.

    Prints a list of author names along with the number of views each author's
    articles has, ordered by the number of views. The list is printed to the
    console.
    """

    query = """
        SELECT name, views
        FROM articles
        INNER JOIN authors ON articles.author = authors.id
        INNER JOIN log_path AS log ON log.path = '/article/' || articles.slug
        ORDER BY views desc;
        """

    result = execute_query(query)
    header = "Author popularity:"
    str = "{}. {} - {} views"
    print_output(header, str, result)


def get_error_logs():
    """
    Print days where > 1% of requests result in errors.

    Prints a list of days along with percentage of requests that resulted in
    errors, ordered by percentage. Only days exceeding 1% are printed.
    The list is printed to the console.
    """

    query = """
        SELECT TO_CHAR(t.day, 'FMMonth DD, YYYY'),
        ROUND((100 * CAST(e.errors as DECIMAL)
        / CAST(t.total as DECIMAL)), 1) as pct
        FROM t_logs as t, e_logs as e
        WHERE t.day = e.day
        GROUP BY t.day, e.errors, t.total
        HAVING ROUND((100 * CAST(e.errors as DECIMAL)
        / CAST(t.total as DECIMAL)), 1) > 1
        ORDER BY pct desc;
    """
    result = execute_query(query)
    header = "Days with error rate over 1%"
    str = "{}. {} - {}% errors"
    print_output(header, str, result)


def main():
    """
    Generate data report.
    """
    get_pop_articles()
    get_pop_authors()
    get_error_logs()
    log_close()

# MARK: - Call Query Functions
if __name__ == "__main__":
    main()
