.. ===============LICENSE_START====================================================
.. Aimee Ukasick CC-BY-4.0
.. ================================================================================
.. Copyright (C) 2018 Aimee Ukasick. All rights reserved.
.. ================================================================================
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
.. ===============LICENSE_END======================================================

Udacity Project 5 - Neighborhood MAP
====================================

This is a small Javascript app that displays a fixed set of places on a Google map. The user is able to click on a place to display an Info Window populated with data from Foursquare.

I wanted to use the Yelp Fusion API, which unfortunately does not support calls from front-end Javascript. I used a workaround (`cors-anywhere <https://github.com/Rob--W/cors-anywhere/#documentation>`_) but was dissatisfied with the performance, so I decided to use Foursquare instead.

This was surprisingly difficult for me. I really prefer back-end Python or Java development. So in addition to the course material provided by Udacity, I consulted the following resources while coding this project:

* Bootstrap sidebar `tutorials <https://bootstrapious.com/p/bootstrap-sidebar>`_
* Google Maps Platform `JavaScript API v3 Reference <https://developers.google.com/maps/documentation/javascript/reference/>`_
* Google Maps Platform `Guides <https://developers.google.com/maps/documentation/javascript/tutorial>`_ and `Samples <https://developers.google.com/maps/documentation/javascript/examples/>`_
* Foursquare Places API `docs <https://developer.foursquare.com/docs/api/endpoints>`_
* JQuery.ajax() `docs <https://api.jquery.com/jQuery.ajax/>`_
* KnockoutJS `docs <https://knockoutjs.com/documentation>`_ and `tutorials <http://learn.knockoutjs.com>`_
* `Chrome Web Developer console <https://developers.google.com/web/tools/chrome-devtools/console/>`_
* StackOverflow and lots of googling

Code was developed using the `Atom IDE <https://atom.io/>`_ and tested using the Chromium browser on Ubuntu 18.04 LTS.

Required Components
===================
As specified in the project requirements:

* `Knockout JS <https://knockoutjs.com>`_ v3.4.2
* `Google Maps API <https://developers.google.com/maps/>`_
* An API other than Google: `Foursquare API <https://developer.foursquare.com>`_

Additional Frameworks
=====================
* `Bootstrap <https://getbootstrap.com/>`_ 3.3.7 for HTML structure


Files
=====
* index.html - the HTML page
* assets/css - style sheets
* assets/js/main.js - the javascript file with the application code

How to Run the App
==================
1. Clone this repo ``git clone https://github.com/aimeeu/udacity_fsnd_proj5_neighborhood_map.git``
2. Open index.html in your browser

Screenshots
===========
Browser
-------

    .. image:: docs/browser.png


iPad - Horizontal
-----------------

    .. image:: docs/ipad.png


iPhoneX
-------

    .. image:: docs/iphonex.png
