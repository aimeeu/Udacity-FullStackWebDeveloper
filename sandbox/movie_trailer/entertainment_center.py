#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===============LICENSE_START================================================
# Apache-2.0
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
"""
Created on Wed Jun 27 12:19:00 2018

@author: aimeeu
"""

import argparse
import pandas as pd
import media
import fresh_tomatoes


def main():
    """
    Calls parse_input_args
    Calls parse_movies_list
    Calls fresh_tomatoes.open_movies_page
    """
    # retrieve command line argument
    input_args = parse_input_args()
    movies = parse_movies_list(input_args.movie_file)
    fresh_tomatoes.open_movies_page(movies)


def parse_input_args():
    """
    Parse command line argument
    There is only one argument, movie_file, which is a tab-delimited,
    UTF-8 file with 4 columns:  TITLE, STORY, POSTER_URL, TRAILER_URL
    All columns should contain string values
    :return: parsed argument
    """
    parser = argparse.ArgumentParser()

    # One command line argument - the .
    parser.add_argument('--movie_file', type=str, default='movies.csv',
                        help='UTF-8, tab-delimited CSV file of movies; '
                             'column order: TITLE, STORY, POSTER_URL, '
                             'TRAILER_URL; assumption is that file is in the '
                             'same directory as the code; default is the '
                             'included movies.csv file')

    # returns parsed argument collection
    return parser.parse_args()


def parse_movies_list(file_name):
    """
    Uses Pandas to read the tab-delimited file of movies
    Creates a Movie object for each row and adds to a list of movies
    :param file_name: the name of the movies file, which is a command line
    argument
    :return: a sorted list of Movie objects
    """
    movies = []
    movies_df = pd.read_table(file_name)
    for row in movies_df.itertuples():
        entry = media.Movie(row[1], row[2], row[3], row[4])
        movies.append(entry)

    # return sorted list
    return sorted(movies, key=lambda movie: movie.title)


# Call to main function to run the program
if __name__ == "__main__":
    main()
