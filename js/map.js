"use strict";

var trips = [];
var Maps = google.maps;
var Directions = new Maps.DirectionsService();
var lines = [];
var intervals = [];
var tripID;
var map;
var mapOptions; 
var t;
var markers = [];
var bTime = 0;
var bDist = 0;
var dTime = 0;
var dDist = 0;
var taxiTime = 0;

var allLines = {};
var mode = {};


var c_taxi_time=0;
var t_taxi_time=0;


// window.localStorage.setItem(id, json string)


$(function() {
    $( "#sliderFleetSize" ).slider({
      value: 20,
      min: 0,
      max: 250,
      step: 10,
      slide: function( event, ui ) {
        $( "#fleetSize" ).val( ui.value );
      }
    });
    $( "#fleetSize" ).val(  $( "#sliderFleetSize" ).slider( "value" ) );
});


$(function() {
    $( "#sliderMaxTripDist" ).slider({
      value: 3,
      min: 1,
      max: 5,
      step: .5,
      slide: function( event, ui ) {
        $( "#maxTripDist" ).val( ui.value + " mi" );
      }
    });
    $( "#maxTripDist" ).val( $( "#sliderMaxTripDist" ).slider( "value" ) + " mi"  );
});


$(function() {
    $( "#sliderParcelAmount" ).slider({
      value: 10,
      min: 0,
      max: 250,
      step: 10,
      slide: function( event, ui ) {
        $( "#parcelAmount" ).val( ui.value + " /hr");
      }
    });
    $( "#parcelAmount" ).val(  $( "#sliderParcelAmount" ).slider( "value" ) + " /hr"  );
});

$(function() {
    $( "#sliderSimSpeed" ).slider({
      value: 10,
      min: 5,
      max: 20,
      step: 1,
      slide: function( event, ui ) {
        $( "#simSpeed" ).val( ui.value + "x" );
      }
    });
    $( "#simSpeed" ).val(  $( "#sliderSimSpeed" ).slider( "value" ) + "x"  );
});

function setMapNewbury() {
    map.center = new Maps.LatLng(42.3519319, -71.0827417);
    map.setZoom(16);
}

function setMapBoston() {
    map.center = new Maps.LatLng(42.367700, -71.089783);
    map.setZoom(13)
}

function day() {
    var time = 0;
    var timeLines = makeTimeLines();
    window.setInterval(function() {
        if (timeLines[time]) {
            timeLines[time].forEach(tripChanged);

        }
        time++;
        
    }, 1000);
}

function makeTimeLines() {
    var timeLines = {};
    function timeParse(trip) {
        var t = new Date(trip.start.time).getTime();
        t %= 86400000;
        t /= 60000;
        var key = Math.floor(t);
        key -= 240;
        if (timeLines[key]) {
            timeLines[key].push(trip);
        }
        else {
            timeLines[key] = [];
        }
    }
    console.log(timeParse);
    trips.forEach(timeParse);
    // console.log(timeLines);
    return timeLines;
}


function start() {
    for (var m = 0; m < markers.length; m++) {
        markers[m].setMap(null);
    }
    document.getElementById("bothBtn").disabled = true;
    document.getElementById("bikeBtn").disabled = true;
    document.getElementById("driveBtn").disabled = true;

    t = 0;
    tripChanged(trips[t]);
    $("ol#trip-list li:nth-child(" + (t + 1) + ")").css("opacity", "1");
}

function bike() {
    mode = {};
    mode[Maps.TravelMode.BICYCLING] = true;
    start();
}

function car() {
    mode = {};
    mode[Maps.TravelMode.DRIVING] = true;
    start();
}

function both() {
    mode = {};
    mode[Maps.TravelMode.BICYCLING] = true;
    mode[Maps.TravelMode.DRIVING] = true;
    start();
}

function taxi(trip) {
    var start   = new Date(trip.start.time);
    var end     = new Date(trip.end.time);
    var time = (end - start)/1000;
    taxiTime += time;
    $("p#c-taxi-time").html(expandTime(time));
    $("p#t-taxi-time").html(expandTime(taxiTime));
    c_taxi_time=expandTime(time);
    t_taxi_time=expandTime(taxiTime);

    if (typeof(Storage) !== "undefined") {
    // Store
    localStorage.setItem("c_taxi_time",c_taxi_time);
    // Retrieve
    // document.getElementById("result").innerHTML = localStorage.getItem("lastname");
    // console.log(localStorage.getItem("c_taxi_time"));
} else {
    console.log("Sorry, your browser does not support Web Storage..."); 
}
    

}

function expandTime(time) {
    var hours   = Math.floor(time/3600);
    time %= 3600;
    var minutes = Math.floor(time/60);
    var seconds = time%60;
    return hours + "hrs " + minutes + "min ";
    
    // + seconds + "sec"
    
}

function clear() {
    bTime = 0;
    bDist = 0;
    dTime = 0;
    dDist = 0;
    $("p#bike-time").html(expandTime(bTime));
    $("p#bike-dist").html(bDist + " meters");
    $("p#drive-time").html(expandTime(dTime));
    $("p#drive-dist").html(dDist + " meters");
}
//Why? sort by time

function sortByTime(trips) {
    trips.sort(function(a,b) {
        var c = new Date(a.start.time);
        var d = new Date(b.start.time);
        return c - d;
    })
}

function accumulator(mark) {
    if (mark.travelMode === Maps.TravelMode.BICYCLING) {
        bTime += mark.travelTime.value;
        bDist += mark.travelDistance.value;
    }
    else if (mark.travelMode === Maps.TravelMode.DRIVING) {
        dTime += mark.travelTime.value;
        dDist += mark.travelDistance.value;
    }
    $("p#bike-time").html(expandTime(bTime));
    $("p#bike-dist").html(bDist + " meters");
    $("p#drive-time").html(expandTime(dTime));
    $("p#drive-dist").html(dDist + " meters");
}

function animateLines() {
    for (var n = 0; n < intervals.length; n++) {
        window.clearInterval(intervals[n]);
    }

    var finished = 0;

    lines.forEach(function(line) {
        var lineSymbol = {
            path: Maps.SymbolPath.CIRCLE,
            scale: 8,
            strokeColor: line.strokeColor,
        };
        line.icons.push({
            icon: lineSymbol,
            offset: "0%",
        });
        var count = 0;
        var interval;

        interval = window.setInterval(function() {
        	if (!interval) {
        		return;
        	}
            count += 5;
            if (count > line.travelTime.value) {
                window.clearInterval(interval);
                finished += 1;
                interval = undefined;

                if (finished === lines.length) {
                 tripChanged(trips[++t]);
                 $("ol#trip-list li:nth-child(" + (t + 1) + ")").css("opacity", "1");
                 lines.forEach(function(polyline) {
                  accumulator(polyline);
              });
                 lines.forEach(function(polyline) {
                    polyline.setMap(null);
                });
                 lines = [];
                 return;
             }
         }
         var icons = line.get('icons');
         icons[0].offset = ( (count / line.travelTime.value) * 100 ) + '%';
         line.set('icons', icons);
     }, 20);
        intervals.push(interval);
    });
}

function drawPaths(paths, origin, id) {

    var marker = new Maps.Marker({
        position: origin,
        map: map,
        icon: {
            path: fontawesome.markers.CHILD,
            scale: 0.5,
            strokeWeight: 0.1,
            strokeColor: '#FFFF00',
            strokeOpacity: 1,
            fillColor: '#FFFF00',
            fillOpacity: 1
        },
        clickable: false,
    });
    marker.info = {};
    allLines[id] = [];
    //Maps.LatLngBounds(): Constructs a rectangle from the points at its south-west and north-east corners.
    var bounds = new Maps.LatLngBounds();
    for (var p = 0; p < paths.length; p++) {
        var color;
        if (paths[p].request.travelMode === Maps.TravelMode.BICYCLING) {
            color = "#00FF00";
        } else {
            color = "#FF0000";
        }

        var polyline = new Maps.Polyline({
            path: [],
            icons: [],
            strokeColor: color,
            strokeOpacity: 0.5,
            strokeWeight: 7,
        });

        // Credits to http://www.geocodezip.com/V3_Polyline_from_directions.html
        var path = paths[p].routes[0].overview_path;
        var legs = paths[p].routes[0].legs;
        for (var i = 0; i < legs.length; i++) {
            var steps = legs[i].steps;
            for (var j = 0; j < steps.length; j++) {
                var nextSegment = steps[j].path;
                for (var k = 0; k < nextSegment.length; k++) {
                    polyline.getPath().push(nextSegment[k]);
                    bounds.extend(nextSegment[k]);
                }
            }
        }

        polyline.travelMode     = paths[p].request.travelMode;
        polyline.travelDistance = paths[p].routes[0].legs[0].distance;
        polyline.travelTime     = paths[p].routes[0].legs[0].duration;
        polyline.setMap(map);
        lines.push(polyline);
        allLines[id].push(polyline);
        
        var popup = new Maps.InfoWindow({
            content: "Distance: " + polyline.travelDistance.value+ "\n"
            + "Duration: "+ polyline.travelTime.value
        });
        Maps.event.addListener(marker, 'click', function(){
            popup.open(map, marker);
        });
        marker.info[polyline.travelMode] = {
        	distance: polyline.travelDistance,
        	time:     polyline.travelTime,
        };
        marker.info.id = id;
    }
    map.fitBounds(bounds);
    map.setZoom(map.getZoom() - 1);
    if (marker.info[Maps.TravelMode.BICYCLING]) {
        $("p#c-bike-time").html(expandTime(marker.info[Maps.TravelMode.BICYCLING].time.value));
        $("p#c-bike-dist").html(marker.info[Maps.TravelMode.BICYCLING].distance.value + " meters");
    }
    if (marker.info[Maps.TravelMode.DRIVING]) {
        $("p#c-drive-time").html(expandTime(marker.info[Maps.TravelMode.DRIVING].time.value));
        $("p#c-drive-dist").html(marker.info[Maps.TravelMode.DRIVING].distance.value + " meters");
    }
    var stored = {
        "BICYCLING": marker.info[Maps.TravelMode.BICYCLING],
        "DRIVING": marker.info[Maps.TravelMode.DRIVING]
    }
    // console.log(stored);
    // window.localStorage(marker.info.id, JSON.stringify(stored));
    Maps.event.addListener(marker, 'click', function() {
    	marker_data(marker.info);
    });
}

function marker_data(info) {
    lines.forEach(function(line) {
    	line.setMap(null);
    });

    lines = [];

    if (tripID === info.id) {
		// accumulator({});
		tripID = undefined;
		return;
	}
	tripID = info.id;

    if (marker.info[Maps.TravelMode.BICYCLING]) {
        var bTimeSpecific = info[Maps.TravelMode.BICYCLING].time.value;
        var bDistSpecific = info[Maps.TravelMode.BICYCLING].distance.value;
        $("p#c-bike-time").html(expandTime(bTimeSpecific));
        $("p#c-bike-dist").html(bDistSpecific + " meters");
    }
    if (marker.info[Maps.TravelMode.DRIVING]) {
        var dTimeSpecific = info[Maps.TravelMode.DRIVING].time.value;
        var dDistSpecific = info[Maps.TravelMode.DRIVING].distance.value;
        $("p#c-drive-time").html(expandTime(dTimeSpecific));
        $("p#c-drive-dist").html(dDistSpecific + " meters");
    }

    allLines[info.id].forEach(function(line) {
    	lines.push(line);
    	line.setMap(map);
    });
}

function tripChanged(trip) {
    if (!trip) {
        return
    }
    
    taxi(trip);

    var res = [];
    var origin      = new Maps.LatLng(trip.start.lat, trip.start.long);
    var destination = new Maps.LatLng(trip.end.lat, trip.end.long);
    var dirfunc = function(response, status) {
        if (status == Maps.DirectionsStatus.OK) {
            res.push(response);
            //What is Object>.keys(mode)
            if (res.length === Object.keys(mode).length) {
                drawPaths(res, origin, trip.id);
                animateLines();
            }
        }
    };
    if (mode[Maps.TravelMode.DRIVING]) {
        Directions.route({
            origin:      origin,
            destination: destination,
            travelMode:  Maps.TravelMode.DRIVING,
        }, dirfunc);
    }
    if (mode[Maps.TravelMode.BICYCLING]) {
        Directions.route({
            origin:      origin,
            destination: destination,
            travelMode:  Maps.TravelMode.BICYCLING,
        }, dirfunc);
    }
}


function fileChanged(event) {
    var csv = event.target.files[0];
    Papa.parse(csv, {
        step: function(results, parser) {
            var row = results.data[0];
            if (row[2]) {
                var trip = {
                    id: parseInt(row[0]),
                    start: {
                        long: parseFloat(row[3]),
                        lat:  parseFloat(row[4]),
                        time: row[1],
                        address: row[2],
                    },
                    end: {
                        long: parseFloat(row[7]),
                        lat:  parseFloat(row[8]),
                        time: row[5],
                        address: row[6],
                    },
                };

                trips.push(trip);
            }
        },
        complete: function() {
            // sortByTime(trips);
            $('#prompt').empty();
            // for (var t = 0; t < trips.length; t++) {
            //     var index = t;
            //     $("ol#trip-list").append("<li data-index=\"" + index + "\">" + trips[t].start.address + "</li>");

            // }
            $("#trip-list").click(function(event) {
                var newID = $(event.toElement).attr("data-index");
                if (newID !== tripID) {
                    tripID = newID;
                    $("ol#trip-list li").css("opacity", "0.5");
                    $(event.toElement).css("opacity", "1");
                    tripChanged(trips[newID]);
                }
            });
        }
    });
document.getElementById("bothBtn").disabled = false;
document.getElementById("bikeBtn").disabled = false;
document.getElementById("driveBtn").disabled = false;

}

window.onload = function() {
    document.getElementById("trip-file").addEventListener("change", fileChanged, false);
    map = new Maps.Map(document.getElementById('map-canvas'), {
      zoom: 13,
      center: new Maps.LatLng(42.367700, -71.089783),
      mapTypeId: Maps.MapTypeId.ROADMAP,
      mapTypeControl: false,
      streetViewControl: false,
      zoomControl: false
  });
    map.setOptions({styles: darkMap});
    document.getElementById("trip-file").value = "";
    document.getElementById("bothBtn").disabled = true;
    document.getElementById("bikeBtn").disabled = true;
    document.getElementById("driveBtn").disabled = true;
};



var darkMap = [
    {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
        {
            "saturation": 36
        },
        {
            "color": "#ffffff"
        },
        {
            "lightness": 40
        }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
        {
            "visibility": "on"
        },
        {
            "color": "#000000"
        },
        {
            "lightness": 16
        }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 20
        }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 17
        },
        {
            "weight": 1.2
        }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "labels.text",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "labels.text.fill",
        "stylers": [
        {
            "visibility": "off"
        },
        {
            "hue": "#ff0000"
        }
        ]
    },
    {
        "featureType": "administrative.neighborhood",
        "elementType": "labels.text",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 20
        }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "labels.text",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "labels.text",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 21
        }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "labels.text",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
        {
            "visibility": "off"
        }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [
        {
            "visibility": "on"
        }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "color": "#882425"
        },
        {
            "visibility": "on"
        }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "color": "#5c5c5c"
        },
        {
            "lightness": 17
        }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 29
        },
        {
            "weight": "0.20"
        }
        ]
    },
    {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "visibility": "on"
        },
        {
            "color": "#6e6e6e"
        }
        ]
    },
    {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry.stroke",
        "stylers": [
        {
            "weight": "0.89"
        }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 18
        }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "color": "#646464"
        },
        {
            "visibility": "on"
        }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [
        {
            "weight": "0.68"
        }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 16
        }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry.fill",
        "stylers": [
        {
            "color": "#5c5c5c"
        },
        {
            "visibility": "on"
        }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry.stroke",
        "stylers": [
        {
            "weight": "0.68"
        }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 19
        }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
        {
            "color": "#000000"
        },
        {
            "lightness": 17
        }
        ]
    }
    ]