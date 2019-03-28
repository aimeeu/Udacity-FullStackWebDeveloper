
<!---
.. ===============LICENSE_START=======================================================
.. Aimee Ukasick CC-BY-4.0
.. ===================================================================================
.. Copyright (C) Aimee Ukasick. All rights reserved.
.. ===================================================================================
.. This documentation file is distributed by Aimee Ukasick
.. under the Creative Commons Attribution 4.0 International License (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://creativecommons.org/licenses/by/4.0
..
.. This file is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
.. ===============LICENSE_END=========================================================
-->

# Movie Trailer Website Project
Source code for the Movie Trailer website project, which is part of Udacity's 
Full Stack Web Developer nanodegree.

# Environment Prerequisites
- Python 3.6
- Pandas 0.23.1

If you have Anaconda installed, you can use it to create a virtual 
environment:
```bash
$ conda create --name fullstack python=3.6
$ source activate fullstack
$ conda install pandas
```

# Installation
```bash
$ git clone https://github.com/aimeeu/udacity_fsnd_movie_trailer_project.git
```

# Files
## fresh_tomatoes.py
This file was provided by Udacity and contains code to render the web page.
## movies.csv
UTF-8, tab-delimited file with four string columns: 
1. TITLE - the title of the movie
2. STORY - brief plot synopsis
3. POSTER_URL - URL of the poster art
4. TRAILER_URL = URL of the movie trailer

Note: the file *must* be in this format with the specified column order
## media.py
This file contains a single class called Movie.
## entertainment_center.py
This file is the script that parses the movies.csv file, creates Movie 
objects, and then calls the fresh_tomatoes code to render the web page.

# Usage
To run the script with the default, included movies.csv file:
```bash
$ python entertainment_center.py
```
To run with a different file of movies:
```bash
$ python entertainment_center.py --movie_file='movies2.csv'
```
Please remember that any "movies" file used *must* be in the same format as 
the included movies.csv file.

To access the help:
```bash
$ python entertainment_center.py --help
usage: entertainment_center.py [-h] [--movie_file MOVIE_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --movie_file MOVIE_FILE
                        UTF-8, tab-delimited CSV file of movies; column order:
                        TITLE, STORY, POSTER_URL, TRAILER_URL; assumption is
                        that file is in the same directory as the code;
                        default is the included movies.csv file
```
