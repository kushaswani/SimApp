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

var sim_data;
var sim_tstep = 4;
var sim_framestep = 25;

var sim_hm_passStart;
var sim_hm_passEnd;
var sim_hm_parcStart;
var sim_hm_parcEnd;
var sim_passDropoffs = new Maps.MVCArray([]);
var sim_passPickups = new Maps.MVCArray([]);
var sim_parcDropoffs = new Maps.MVCArray([]);
var sim_parcPickups = new Maps.MVCArray([]);

//var sim_graphics = [];

var allLines = {};
var mode = {};

var emissions = [0, 0, 0];
var tot_distances = [0, 0, 0];
var emissions_coeffs = [2, 10, 5];
var person_wait_times = [
    { key: 0, value: 0 },
    { key: 5, value: 0 },
    { key: 10, value: 0 },
    { key: 15, value: 0 },
    { key: 20, value: 0 },
    { key: 25, value: 0 },
    { key: 30, value: 0 },
    { key: 35, value: 0 }];
var package_wait_times = [
    { key: 0, value: 0 },
    { key: 5, value: 0 },
    { key: 10, value: 0 },
    { key: 15, value: 0 },
    { key: 20, value: 0 },
    { key: 25, value: 0 },
    { key: 30, value: 0 },
    { key: 35, value: 0 }];


var c_taxi_time=0;
var t_taxi_time=0;

var charging_stations = [
    [114.007401,22.5355],
    [114.0090009,22.53423323],
    [113.987547,22.560519],
    [114.088303,22.562599],
    [114.361504,22.678499],
    [114.074406,22.559],
    [113.922977,22.546375],
    [114.123241,22.562538],
    [114.101748,22.582541],
    [114.068837,22.573326],
    [114.023404,22.54265],
    [114.023902,22.619512],
    [113.81775,22.650682],
    [113.944128,22.506854],
    [113.941642,22.527053],
    [113.962844,22.528519],
    [113.8149322,22.6513225],
    [114.304419,22.600844],
    [114.032902,22.524276],
    [113.85839,22.579457],
    [113.995054,22.547247],
    [114.003978,22.636233],
    [114.045125,22.55141],
    [113.838486,22.609576],
    [114.043404,22.601],
    [113.985199,22.547701],
    [113.8134,22.624201],
    [114.135002,22.544001],
    [114.353401,22.679399],
    [113.8564,22.616899],
    [114.031502,22.5252],
    [114.1798,22.5585]
];

var image = "http://maps.google.com/mapfiles/ms/icons/gas.png";
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

// function setMapNewbury() {
//     map.center = new Maps.LatLng(42.3519319, -71.0827417);
//     map.setZoom(15);
// }
//
// function setMapBoston() {
//     map.center = new Maps.LatLng(42.359456, -71.076336);
//     map.setZoom(14)
// }
function setMapNewbury() {
    map.center = new Maps.LatLng(22.7004312,113.9264277);
    map.setZoom(11);
}

function setMapShenzhen() {
  map.center = new Maps.LatLng(22.7004312,113.9264277);
  map.setZoom(11);
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
    alert('b2');
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

function fleet_sim() {
    var fleet_size = $('#fleetSize').val();
    var maxDist = $('#maxTripDist').val();
    var parcelFreq = $('#parcelAmount').val();
    var sim_params = {
        size: fleet_size,
        maxDist: maxDist,
        parcels: parcelFreq,
    };
    console.log(sim_params);
    $.post( '/fleetsim', JSON.stringify(sim_params), function( data ) {
        console.log(data);
        sim_data = data;
        animateCars();
    }, 'json');
}

function test_fleet_sim() {
    var fleet_size = $('#fleetSize').val();
    var maxDist = $('#maxTripDist').val();
    var parcelFreq = $('#parcelAmount').val();
    var sim_params = {
        size: fleet_size,
        maxDist: maxDist,
        parcels: parcelFreq,
    };
    console.log(sim_params);
    $.post( '/server/sim2.json', JSON.stringify(sim_params), function( data ) {
        console.log(data);
        sim_data = data;
        animateCars();
    }, 'json');
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

function initHeatmaps() {
    sim_hm_passEnd = new Maps.visualization.HeatmapLayer({
        data: sim_passDropoffs,
        map: map,
        radius: 40,
        opacity: .2,
        gradient: [
            'rgba(60, 170, 255, 0)',
            'rgba(60, 170, 255, 1)',
        ]
    });


    sim_hm_passStart = new Maps.visualization.HeatmapLayer({
        data: sim_passPickups,
        map: map,
        radius: 40,
        opacity: .2,
        gradient: [
            'rgba(255, 200, 0, 0)',
            'rgba(255, 200, 64, 1)',
        ]
    });

    sim_hm_parcStart = new Maps.visualization.HeatmapLayer({
        data: sim_parcPickups,
        map: map,
        radius: 40,
        opacity: .2,
        gradient: [
            'rgba(255, 200, 0, 0)',
            'rgba(255, 200, 64, 1)',
        ]
    });

    sim_hm_parcEnd = new Maps.visualization.HeatmapLayer({
        data: sim_parcDropoffs,
        map: map,
        radius: 40,
        opacity: .2,
        gradient: [
            'rgba(60, 170, 255, 0)',
            'rgba(60, 170, 255, 1)',
        ],
    });
}

// ACTIVATION/DEACTIVATION OF HEATMAP TYPES
function togglePassHeatmap() {
    sim_hm_passStart.setMap(sim_hm_passStart.getMap() ? null : map);
    sim_hm_passEnd.setMap(sim_hm_passEnd.getMap() ? null : map);
};

function toggleParcHeatmap() {
    sim_hm_parcStart.setMap(sim_hm_parcStart.getMap() ? null : map);
    sim_hm_parcEnd.setMap(sim_hm_parcEnd.getMap() ? null : map)
};


function drawUtilization() {
    var layers = zipUtilization();
    drawUtil(layers);
}

function zipUtilization() {
    // zip layers into len-24 arrays of format
    // [(index, y-value, y-min), ... ]
    var util_human = [];
    var util_parc = [];
    for (var i = 0; i < 24; i++) {
        if (i < sim_data.util.length) {
            util_human.push({
                x: i,
                y: sim_data.util[i][0],
                y0: 0,
            });
            util_parc.push({
                x: i,
                y: sim_data.util[i][0] + sim_data.util[i][1],
                y0: sim_data.util[i][0],
            });
        } else {
            util_human.push({
                x: i,
                y: 0,
                y0: 0,
            });
            util_parc.push({
                x: i,
                y: 0,
                y0: 0,
            });
        }
    }
    return [util_human, util_parc];
}

function calculateTripWaitTime(data) {
    // TODO: don't count actual trips as wait time
    // rounding to nearest multiple of 5
    var wait_time = Math.round(data.route.duration/60/5);
    if (wait_time > 7) wait_time = 7;
    if (data.is_human) {
        person_wait_times[wait_time].value += 1;
    } else {
        package_wait_times[wait_time].value += 1;
    }
    drawPersonWaitTime(person_wait_times);
    drawPackageWaitTime(package_wait_times);
}


function animateCars() {
    // like animateLines but for cars with a schedule of many things to do

    // first clear the intervals
    for (var i = 0; i < intervals.length; i++) {
        window.clearInterval(intervals[n]);
    }

    //drawUtilization();

    sim_data['tstep'] = 0;

    // Set up global time
    interval = window.setInterval(function() {
        if (!interval) {
            return;
        }
        sim_data.tstep += sim_tstep;
    }, sim_framestep);
    intervals.push(interval);

    initHeatmaps();

    //drawUtilization();

    var interval;

    var sim_factor = 10;

    sim_data['curTask'] = 0;
    sim_data['shown'] = [];
    sim_data['curHour'] = 0;

    interval = window.setInterval(function() {
        if (!interval) {
            return;
        }

        // TODO fuck it we'll just redraw the whole thing for now
        if (sim_data.curHour < sim_data.tstep / 3600) {
            // New hour
            sim_data.curHour++;
            if (sim_data.curHour < sim_data.emissions.length) {
            // emissions[0] = sim_data.emissions[sim_data.curHour];
            // drawEmissionChart(emissions);
            }
        }

        if (sim_data.curTask < sim_data.trips.length) {

            while (sim_data.tstep >= sim_data.trips[sim_data.curTask].time_ordered) {
                // draw the caller
                // xxx
                // console.log(sim_data.trips[sim_data.curTask])
                // drawUtilization();
                calculateTripEmission(sim_data.trips[sim_data.curTask], true);
                //drawEmissionChart(emissions);
                calculateTripWaitTime(sim_data.trips[sim_data.curTask]);
                var origin = {lat: sim_data.trips[sim_data.curTask].start_loc[0], lng: sim_data.trips[sim_data.curTask].start_loc[1]};
                var marker;
                if (sim_data.trips[sim_data.curTask].is_human) {
                    marker = new Maps.Marker({
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
                } else {
                    marker = new Maps.Marker({
                        position: origin,
                        map: map,
                        icon: {
                            path: fontawesome.markers.CUBE,
                            scale: 0.5,
                            strokeWeight: 0.1,
                            strokeColor: '#06c906',
                            strokeOpacity: 1,
                            fillColor: '#06c906',
                            fillOpacity: 1
                        },
                        clickable: false,
                    });
                }
                marker.info = {};
                sim_data.trips[sim_data.curTask]['marker'] = marker;

                sim_data.shown.push(sim_data.curTask);

                sim_data.curTask++;
                if (sim_data.curTask >= sim_data.trips.length) {
                    break;
                }
            }
        }

        if (sim_data.shown.length > 0) {
            // disappear old tasks that have completed
            // TODO use a heap implementation for speed ?
            for (var i = 0; i < sim_data.shown.length; i++) {
                var tripIdx = sim_data.shown[i];
                if (sim_data.trips[tripIdx].pickup <= sim_data.tstep) {
                    // remove element
                    sim_data.trips[tripIdx].marker.setMap(null);
                    if (sim_data.trips[tripIdx].is_human) {
                        sim_passPickups.push(sim_data.trips[tripIdx].marker.position);
                    } else {
                        sim_parcPickups.push(sim_data.trips[tripIdx].marker.position);
                    }
                    sim_data.trips[tripIdx].marker = null;

                    // remove element at [i]
                    sim_data.shown.splice(i, 1);
                    i--; // I hate doing this
                }

            }
        }

    }, sim_framestep * sim_factor);
    intervals.push(interval);

    // TODO how do I extract and render statistics at the frame level?
    // Should I just check and update every time a car finishes a trip or
    // something (and have a callback)
    sim_data.fleet.vehicles.forEach(drawCarStuff);
}

function drawCarStuff(car) {
    car.current = 0;
    var latLngLoc = {lat: car.spawn[0], lng: car.spawn[1]};
    var carMarker = new Maps.Marker({
        position: latLngLoc,
        icon: {
            path: Maps.SymbolPath.CIRCLE,
            scale: 8,
            strokeColor: 'white', // TODO color
        },
        map: map,
      });
    car['curTaskRender'] = carMarker;

    var interval; // I guess I declare this to have a static reference?

    interval = window.setInterval(function() {
       if (!interval) {
           return;
       }

        var newTask = false;

        if (car.current >= car.history.length) {
            return;
        }

        // update the car to the tstep
        var ctask = car.history[car.current]
        while (sim_data.tstep >= ctask.end) {
            if (ctask.kind == "PASSENGER") {
                // TODO Find good gaussian icon
                var dest = new Maps.LatLng(ctask.dest[0], ctask.dest[1]);
                sim_passDropoffs.push(dest);
            }
            else if (ctask.kind == "CHARGING") {
                var dest = new Maps.LatLng(ctask.dest[0], ctask.dest[1]);
                sim_parcDropoffs.push(dest);
            }
            car.current++;
            newTask = true;
            if (car.current >= car.history.length) {
                // What do we do when we're at the end of the sim?
                // TODO
                var loc = {lat: ctask.dest[0], lng: ctask.dest[1]};
                var carMarker = new Maps.Marker({
                    position: loc,
                    icon: {
                        path: Maps.SymbolPath.CIRCLE,
                        scale: 8,
                        strokeColor: 'white', // TODO color
                    },
                  });
                car.curTaskRender.setMap(null);
                car.curTaskRender = carMarker;
                car.curTaskRender.setMap(map);
                return;
            }
            ctask = car.history[car.current];
        }

        //  various tasks - based on car.history[car.current]
        switch(car.history[car.current].kind) {
            case 'IDLE':
                if (newTask) {
                    var loc = {lat: ctask.dest[0], lng: ctask.dest[1]};
                    var carMarker = new Maps.Marker({
                        position: loc,
                        icon: {
                            path: Maps.SymbolPath.CIRCLE,
                            scale: 8,
                            strokeColor: 'white', // TODO color
                            strokeOpacity: 0.5,
                        },
                      });
                    car.curTaskRender.setMap(null);
                    car.curTaskRender = carMarker;
                    car.curTaskRender.setMap(map);
                }
                break;
            case 'NAV':
                if (newTask) {
                    ctask['color'] = 'white';
                    // Draw a line from the car's polyline
                    var polyline = polylineFromTask(ctask);

                    car.curTaskRender.setMap(null);
                    car.curTaskRender = polyline;
                } else {
                    var icons = car.curTaskRender.get('icons');
                    icons[0].offset = ( ((sim_data.tstep - ctask.start) / (ctask.route.duration)) * 100 ) + '%'; // google maps api stuff here
                    car.curTaskRender.set('icons', icons);
                }
                car.curTaskRender.setMap(map);
                break;
            case 'PASSENGER':
                if (newTask) {
                    ctask['color'] = '#F0F000';

                    // Draw a line from the car's polyline
                    var polyline = polylineFromTask(ctask);

                    car.curTaskRender.setMap(null);
                    car.curTaskRender = polyline;

                } else {
                    var icons = car.curTaskRender.get('icons');
                    icons[0].offset = ( ((sim_data.tstep - ctask.start) / (ctask.route.duration)) * 100 ) + '%'; // google maps api stuff here
                    car.curTaskRender.set('icons', icons);
                }
                car.curTaskRender.setMap(map);
                break;
            case 'CHARGING':
                if (newTask) {
                    ctask['color'] = '#06c906'
                    // Draw a line from the car's polyline
                    var polyline = polylineFromTask(ctask);

                    car.curTaskRender.setMap(null);
                    car.curTaskRender = polyline;

                } else {
                    var icons = car.curTaskRender.get('icons');
                    icons[0].offset = ( ((sim_data.tstep - ctask.start) / (ctask.route.duration)) * 100 ) + '%'; // google maps api stuff here
                    car.curTaskRender.set('icons', icons);
                }
                car.curTaskRender.setMap(map);
                break;
            default:
                alert('error');
        }
        //    Car is going somewhere
        //      draw current line and car position on it
        //      color := package (dark green)/ passenger (light green)/navigation (de-sat green)
        //    Car is loitering
        //      draw car at position
        //      color := loiter color (de-sat green)?


    }, sim_framestep * 2);
    intervals.push(interval);
}

function polylineFromTask(ctask) {
    var polyline = new Maps.Polyline({
        path: [],
        icons: [],
        strokeColor: ctask.color,
        strokeOpacity: 0.5,
        strokeWeight: 7,
    });

    // Credits to http://www.geocodezip.com/V3_Polyline_from_directions.html
    // var path = ctask.route.rte.overview_polyline.points;
    var legs = ctask.route.rte.legs;
    for (var i = 0; i < legs.length; i++) {
        var steps = legs[i].steps;
        for (var j = 0; j < steps.length; j++) {
            var nextSegment = google.maps.geometry.encoding.decodePath(steps[j].polyline.points);
            for (var k = 0; k < nextSegment.length; k++) {
                polyline.getPath().push(nextSegment[k]);
            }
        }
    }

    var lineSymbol = {
        path: Maps.SymbolPath.CIRCLE,
        scale: 8,
        strokeColor: ctask.color,
    };

    // add the circular symbol to the line
    polyline.icons.push({
        icon: lineSymbol,
        offset: "0%", // at the starting position
    });

    return polyline;
}

function animateLines() {
    for (var n = 0; n < intervals.length; n++) {
        window.clearInterval(intervals[n]);
    }
    var finished = 0;

    lines.forEach(function(line) {
        // Prepare the circular symbol for the bike or taxi
        var lineSymbol = {
            path: Maps.SymbolPath.CIRCLE,
            scale: 8,
            strokeColor: line.strokeColor,
        };

        // add the circular symbol to the line
        line.icons.push({
            icon: lineSymbol,
            offset: "0%", // at the starting position
        });


        var count = 0; // Time step
        var interval; // basically a frame of rendering

        interval = window.setInterval(function() {
        	if (!interval) {
        		return;
        	}

            // increment the time step (seconds of real time)
            count += 5;
            if (count > line.travelTime.value) { // check if the trip finished
                // and clear the icon; the vehicle can disappear
                window.clearInterval(interval);
                finished += 1;
                interval = undefined;

                if (finished === lines.length) { // if all the lines at this step are done
                    // proceed to rendering the next trip
                 tripChanged(trips[++t]);
                 $("ol#trip-list li:nth-child(" + (t + 1) + ")").css("opacity", "1"); // some jquery I don't understand
                 lines.forEach(function(polyline) {
                  accumulator(polyline); // I think this is just unused statistics stuff
              });
                 lines.forEach(function(polyline) {
                    polyline.setMap(null); // stop drawing it I think?
                });
                 lines = []; // and... ? probably clear it since it's a global variable (yay?)
                 return;
             }
         }
         // whether the trip is finished or not...
            // update lines.icons[0] (which I think is the only icon [?]) to have advanced a percentage of the trip
         var icons = line.get('icons');
         icons[0].offset = ( (count / line.travelTime.value) * 100 ) + '%'; // google maps api stuff here
         line.set('icons', icons);
     }, 20); // ms per interval
        intervals.push(interval); // ...and push intervals? maybe this is necessary to render?
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
        if (paths[p].request.travelMode === Maps.TravelMode.DRIVING) {
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
        console.log(paths[p].routes[0]);
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

function getRouteDistance(route) {
    var sum = 0;
    for (var i = 0; i < route.legs.length; i++) {
        sum += route.legs[i].distance.value;
    }
    return sum;
}

function calculateEmissions(paths) {
    console.log(paths);
    for (var i = 0; i < paths.length; i++) {
    if (paths[i].request.travelMode === Maps.TravelMode.BICYCLING) {
        tot_distances[0] = getRouteDistance(paths[i].routes[0]);
    } else if (paths[i].request.travelMode === Maps.TravelMode.DRIVING) {
        tot_distances[1] = getRouteDistance(paths[i].routes[0]);
        tot_distances[2] = getRouteDistance(paths[i].routes[0]);
    }
    }

    for (var i = 0; i < emissions.length; i++) {
        emissions[i] = tot_distances[i] * emissions_coeffs[i] / 10000
    }
  //normalize_emissions()
}

function normalize_emissions() {
    var denom = d3.max(emissions) / 10;
    if (denom > 0) {
        for (var i = 0; i < emissions.length; i++) {
            emissions[i] = emissions[i] / denom;
        }
    }
}

function calculateTripEmission(trip, isCar) {
    if (isCar) {
        tot_distances[1] = trip.route.distance;
        tot_distances[2] = trip.route.distance;
    // } else {
        tot_distances[0] = trip.route.distance;
    }

    for (var i = 0; i < emissions.length; i++) {
        emissions[i] += tot_distances[i] * emissions_coeffs[i] / 10000;
    }
  //normalize_emissions()
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
                // TODO total trip distances and calculate emissions
                calculateEmissions(res)
                drawPaths(res, origin, trip.id);
                alert('breakpt');
                animateLines();
                //drawEmissionChart(emissions);
                //drawUtilization();
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
      //zoom: 14,
      zoom: 11,
      //center: new Maps.LatLng(42.359456, -71.076336),
      center: new Maps.LatLng(22.6004312,113.9264277),
      mapTypeId: Maps.MapTypeId.ROADMAP,
      mapTypeControl: false,
      streetViewControl: false,
      zoomControl: false
  });

    for (var i = 0; i < 32; i++){
        var marker = new google.maps.Marker({
            position: { lat:charging_stations[i][1], lng: charging_stations[i][0] },
            icon: image,
            map:map
        });
    }
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
