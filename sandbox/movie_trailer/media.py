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

import webbrowser


class Movie:
    """
    Class for storing related movie data
    """

    # constructor
    def __init__(self, movie_title, movie_storyline, poster_image_url,
                 trailer_youtube_url):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url

    def __str__(self):
        return "Title: {}; Story: {}; Poster URL: {}; Trailer: {}".format(
            self.title, self.storyline, self.poster_image_url,
            self.trailer_youtube_url)

    # instance method (all instance methods take self as the first arg)
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
