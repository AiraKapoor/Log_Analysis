# ! /usr/bin/env python

import psycopg2
DB_Project = "news"


def execute(query_command):
    # Existing Database is being connected in the command below
    data_base = psycopg2.connect(database=DB_Project)
    # Cursor is opened to perform operations on database
    a = data_base.cursor()
    a.execute(query_command)
    res = a.fetchall()
    # Communication is closed
    data_base.close()
    return res


# Ques3-On which days did more than 1% of requests lead to errors?
def error_calculated():
    query_command = """SELECT day, error_percent
                      FROM request_stats
                      WHERE error_percent > 1
                      ORDER BY error_percent DESC;"""
    result_q3 = execute(query_command)
    print("\nOn which days did more than 1% of requests lead to errors?\n")
    for g in result_q3:
        dte = g[0].strftime('%B %d, %Y')
        errs = str(g[1]) + "%" + " errors"
        print("\t" + dte + " --> " + errs)


# Ques2-Who are the most popular authors of all time?
def author():
    query_command = "SELECT author.name, count(*) AS views FROM authors author inner JOIN \
          articles a ON author.id = a.author inner JOIN log l ON  \
          a.slug = substr(l.path,10)\
          GROUP BY author.name \
          ORDER BY views DESC LIMIT 3;"
    result_q2 = execute(query_command)
    counter = 1
    print("\nWho are the most popular authors of all time?\n")
    for f in result_q2:
        print("\t" + f[0] + " --> " + str(f[1]) + " views")
        counter = counter+1


# Ques1-What are the most popular three articles of all time?
def popular_articles():
    query_command = """SELECT title, count(path) AS num FROM articles, \
                 log WHERE articles.slug = substring(path from 10 for 100)\
                 GROUP BY title ORDER BY num DESC LIMIT 3;"""

    result_q1 = execute(query_command)
    counter = 1
    print("\nThe most popular three articles of all time are:\n")
    for e in result_q1:
        head = e[0]
        viw = " --> " + str(e[1]) + " views"
        print("\t" + head + viw)
        counter = counter+1


# Functions are called
popular_articles()
author()
error_calculated()
