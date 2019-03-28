/*
  ===============LICENSE_START==================================================
  Aimee Ukasick Apache-2.0
  ==============================================================================
  Copyright (C) 2018 Aimee Ukasick. All rights reserved.
  ==============================================================================
  This software file is distributed by Aimee Ukasick
  under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  This file is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  ===============LICENSE_END====================================================
*/

var appController;

// array of places in Chicago used to populate the map
var places = [
    {
        title: "Shedd Aquarium",
        location: {
            lat: 41.867901,
            lng: -87.614182
        }
    },
    {
        title: "Navy Pier",
        location: {
            lat: 41.891708,
            lng: -87.609657
        }
    },
    {
        title: "The Field Museum",
        location: {
            lat: 41.866161,
            lng: -87.616997
        }
    },
    {
        title: "Goodman Theatre",
        location: {
            lat: 41.884800,
            lng: -87.629620
        }
    },
    {
        title: "The Chicago Theatre",
        location: {
            lat: 41.885441,
            lng: -87.627258
        }
    },
    {
        title: "The Art Institute of Chicago",
        location: {
            lat: 41.879539,
            lng: -87.624039
        }
    },
    {
        title: "The Purple Pig",
        location: {
            lat: 41.890942,
            lng: -87.624352
        }
    },
    {
        title: "The Gage",
        location: {
            lat: 41.881809,
            lng: -87.624603
        }
    },
    {
        title: "Three Dots and a Dash",
        location: {
            lat: 41.890141,
            lng: -87.630928
        }
    },
    {
        title: "Beatrix",
        location: {
            lat: 41.891479,
            lng: -87.630821
        }
    },

];


// ***** MODEL DEFINITION
/**
* @description Represents a Place
* @constructor
* @param data - title, location
**/
var Place = function (data) {
    var self = this;
    this.title = data.title;
    this.location = data.location;
    this.show = ko.observable(true);
};


// ***** END MODEL DEFINITION

// ***** BEGIN MAP
//Project 5 rubric states "Knockout should not be used to handle the Google Map API."
var map;
var markers = [];


/**
* @description  this is the callback method for google maps; must match
* callback method pass in API call to Google Maps in index.html
**/
function initMap() {
    // intial map view when loaded is Chicago
    var myLatLng = {
        lat: 41.875970,
        lng: -87.623335
    };
    // create a map object and get map from DOM for display
    map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 13.5
    });

    // create a new InfoWindow to attach to each place pin
    var infoWindow = new google.maps.InfoWindow();

    // iterates through all places and drop pins on every single place
    for (j = 0; j < places.length; j++) {
        (function () {
            // store title and location iteration in variables
            var title = places[j].title;
            var location = places[j].location;

            // drop marker after looping
            var marker = new google.maps.Marker({
                position: location,
                map: map,
                title: title,
                animation: google.maps.Animation.DROP,
                address: address
            });
            // add marker to markers array
            markers.push(marker);

            appController.favPlaces()[j].marker = marker;

            // Add an onclick event to open an infoWindow at each marker
            marker.addListener("click", function () {
                populateInfoWindow(this, infoWindow);
                // set content to Foursquare results
                infoWindow.setContent(contentString);
            });

            /*
            Populate infoWindow for selected place marker here for better performance when place is clicked
            Make sure only one infoWindow is open at a time
            Sets animation to bounce when marker/place is clicked
            Adds listener to infoWindow to clear when closed
            */
            function populateInfoWindow(marker, infoWindow) {
                if (infoWindow.marker != marker) {
                    infoWindow.marker = marker;
                    infoWindow.setContent(
                        '<div class="title">' +
                        marker.title +
                        "</div>" +
                        marker.contentString
                    );
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                    setTimeout(function () {
                        marker.setAnimation(null);
                    }, 2130);
                    infoWindow.open(map, marker);
                    infoWindow.addListener("closeclick", function () {
                        infoWindow.setMarker = null;
                    });
                }
            }

            // foursquare client-id and client-secret
            var client_id = "CXOQWNVYWEUP4ZF25A5R1PYYBZISBQAOHD30K353VXV4ZECC";
            var client_secret = "A5VFXFRPJGV1JQ3Q2MYOAAHEC2CBJUDC4JEZ5DFQ11GX1ZDV";

            //https://developer.foursquare.com/docs/api/venues/search
            var foursquareUrl = "https://api.foursquare.com/v2/venues/search";

            // create variables outside of the ajax request for faster loading
            var venue, address, category, foursquareId, contentString;

            $.ajax({
                method: 'GET',
                url: foursquareUrl,
                dataType: "json",
                data: {
                    client_id: client_id,
                    client_secret: client_secret,
                    query: marker.title,
                    near: "Chicago, IL",
                    v: 20181122 // a date that represents the “version” of the API for which you expect from Foursquare. https://developer.foursquare.com/docs/api/configuration/versioning
                },
                success: function (data) {
                    // console.log(data);
                    venue = data.response.venues[0];
                    address = venue.location.formattedAddress[0];
                    category = venue.categories[0].name;
                    foursquareId = "https://foursquare.com/v/" + venue.id;
                    contentString =
                        "<div class='name'>" +
                        "Name: " +
                        "<span class='info'>" +
                        title +
                        "</span></div>" +
                        "<div class='category'>" +
                        "Catergory: " +
                        "<span class='info'>" +
                        category +
                        "</span></div>" +
                        "<div class='address'>" +
                        "Location: " +
                        "<span class='info'>" +
                        address +
                        "</span></div>" +
                        "<div class='information'>" +
                        "More Foursquare Info: " +
                        "<a href='" +
                        foursquareId +
                        "' target='_blank'>" +
                        "Click here" +
                        "</a></div>";

                    marker.contentString;
                },
                error: function () {
                    contentString =
                        "<div class='name'>Foursquare data is currently not available. Please try again.</div>";
                }
            });
        })(j);
    } // end of for loop through markers [j]
}
// ***** END MAP


function mapError() {
    console.log(mapError);
    alert("The map cannot be displayed at this time due to unforeseen issues. Please try refreshing the page.");
}


// VIEW MODEL in Knockout JS//
var Controller = function () {
    var self = this;

    this.favPlaces = ko.observableArray();
    this.filteredInput = ko.observable("");
    this.errorMsg = ko.observable();

    for (i = 0; i < places.length; i++) {
        var place = new Place(places[i]);
        self.favPlaces.push(place);
    }

    // http://www.knockmeout.net/2011/04/utility-functions-in-knockoutjs.html
    // takes user input and filters the array of Places as the user types;
    // display Places from filtered list
    // hide map markers that do not match input and show those that do
    this.searchFilter = ko.computed(function () {
        var filter = self.filteredInput().toLowerCase();
        for (j = 0; j < self.favPlaces().length; j++) {
            if (self.favPlaces()[j].title.toLowerCase().indexOf(filter) > -1
            )               {
                self.favPlaces()[j].show(true);
                if (self.favPlaces()[j].marker) {
                    self.favPlaces()[j].marker.setVisible(true);
                }
            } else {
                self.favPlaces()[j].show(false);
                if (self.favPlaces()[j].marker) {
                    self.favPlaces()[j].marker.setVisible(false);
                }
            }
        }
    });

    /*
    Map marker bounces when Place is clicked in the list
    https://developers.google.com/maps/documentation/javascript/events
    */
    this.showPlace = function (locations) {
        google.maps.event.trigger(locations.marker, "click");
    };
};

// instantiate the app
appController = new Controller();
ko.applyBindings(appController);
