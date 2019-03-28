#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===============LICENSE_START================================================
# Aimee Ukasick Apache-2.0
# ============================================================================
# Copyright (C) 2018 Aimee Ukasick. All rights reserved.
# ============================================================================
# This software file is distributed by Aimee Ukasick
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END==================================================
import psycopg2
from time import time


DBNAME = "news"

def main():
    """
    Calls report_three_most_popular_articles
    Calls report_most_popular_authors
    Calls report_high_error_days
    """
    # Measures total program runtime by collecting start time
    start_time = time()

    report_three_most_popular_articles()
    report_most_popular_authors()
    report_high_error_days()

    # Measure total program runtime by collecting end time
    end_time = time()

    # Computes overall runtime in seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("")
    print("** Total Elapsed Runtime:",
          str(int((tot_time / 3600))) + ":" + str(
              int((tot_time % 3600) / 60)) + ":"
          + str(int((tot_time % 3600) % 60)))


def report_three_most_popular_articles():
    '''
    Fetches data and prints the Top 3 Articles report
    '''
    try:
        query_str = (
            'select count(trim.trim_path) as num_of_views'
            ', a.title as article_title '
            'from view_log_path_trim as trim, articles as a '
            'where trim.trim_path = a.slug '
            'group by trim_path, a.title '
            'order by num_of_views desc '
            'limit 3'
            ';')
        rows = fetch_data(query_str)
        print("Top Three Articles:")
        for row in rows:
            views = row[0]
            title = row[1]
            print('\t * "{}" -- {:,} views'.format(title, views))
    except Exception as e:
        print(e)


def report_most_popular_authors():
    '''
    Fetches data and prints the Most Popular Authors report
    '''
    try:
        query_str = (
            'SELECT author'
            ', SUM (num_of_views) AS total_views '
            'FROM view_author_hits '
            'GROUP BY author '
            'ORDER BY total_views DESC'
            ';')
        rows = fetch_data(query_str)
        print("Most Popular Authors:")
        for row in rows:
            author = row[0]
            views = row[1]
            print('\t * {} -- {:,} views'.format(author, views))
    except Exception as e:
        print(e)


def report_high_error_days():
    '''
    Fetches data and prints the High Error Days report
    '''
    try:
        query_str = (
            'SELECT error_day'
            ', percent_error_hits '
            'FROM view_log_error_percent '
            'WHERE percent_error_hits > 1.0 '
            'ORDER BY error_day DESC'
            ';')
        rows = fetch_data(query_str)
        print("Dates With More Than 1.0% Request Errors:")
        for row in rows:
            # 2016-07-17 00:00:00+00:00
            date_str = (row[0]).strftime('%b %d, %Y')
            error_hits = row[1]
            print("\t * {} -- {}% errors".format(date_str, error_hits))
    except Exception as e:
        print(e)


def fetch_data(query_str):
    '''
    Fetches data
    :param query_str:
    :return: returns the database rows as a list of tuples; empty list if no
    records
    '''
    conn = None
    try:
        conn = psycopg2.connect(database=DBNAME)
        cursor = conn.cursor()
        cursor.execute(query_str)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        conn.close()

# Call to main function to run the program
if __name__ == "__main__":
    main()