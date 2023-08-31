        
        var upArrow = L.Icon.extend({
            options: {
                iconUrl: 'custom_markers/Blue_Arrow_Up_Darker.png',
                iconSize: [30,30]
            }
        })

        var leftArrow = L.Icon.extend({
            options: {
                iconUrl: 'custom_markers/Blue_Arrow_Left_Darker.png',
                iconSize: [30,30]
            }
        })

        var downArrow = L.Icon.extend({
            options: {
                iconUrl: 'custom_markers/Blue_Arrow_Down_Darker.png',
                iconSize: [30,30]
            }
        })

        var rightArrow = L.Icon.extend({
            options: {
                iconUrl: 'custom_markers/Blue_Arrow_Right_Darker.png',
                iconSize: [30,30]
            }
        })

        var noArrow = L.Icon.extend({
            options: {
                iconUrl: 'custom_markers/blue-dot.png',
                iconSize: [20,20]
            }
        })

        var upArrow = new upArrow();           
        var leftArrow = new leftArrow();   
        var downArrow = new downArrow();   
        var rightArrow = new rightArrow();   
        var noArrow = new noArrow();


        var customOptions = {
            'maxWidth':'2000',
            'maxHeight':'3000'       
        }

        var currentPolyLine;

        function plotFlow(year, N, S, E, W) {

                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/traffic_flow_average_daily/year='+year 
                    + '&N=' + N + '&S=' + S + '&E=' + E + '&W=' + W,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            //var flowColor = flowIntensity(entry.AllMotorVehicles);
                            //var circle = L.circle([entry.Latitude, entry.Longitude], 20, {color: '', fillColor: flowColor, fillOpacity: 0.2})
                            var icon = getFlowIcon(entry.Direction);
                            var arrow = L.marker([entry.Latitude, entry.Longitude], {icon: icon});
                            flowMarkers.push(arrow);
                            // THE FOLLOWING WILL NOT WORKING IN THIS ITERATIVE WAY: This may solve this issue... http://stackoverflow.com/questions/15860683/onclick-event-in-a-for-loop
                            arrow.on("click", function() {
                                clearLine();
                                var latlngs =  getLinkEnds(entry.Latitude, entry.Longitude, entry.Direction, entry.LinkLength_miles);
                                var polyline = L.polyline(latlngs, {color: 'purple'}).addTo(map).bindPopup("<br>Start Junction: " + entry.StartJunction + "<br> End Junction: " + entry.EndJunction);;
                                currentPolyLine = polyline;
                                $("#wrapper").toggleClass("toggled");
                                $('#sidebarLongLat').text("LATITUDE: " + entry.Latitude.toString()+ "  LONGITUDE: " + entry.Longitude.toString());
                                $('#sidebarLocalAuthority').text("LOCAL AUTHORITY: " + entry.LocalAuthority);
                                $('#sidebarRoad').text("ROAD: " + entry.Road);
                                var chartCanvas1 = document.createElement('canvas');
                                chartCanvas1.id = 'myChart1';
                                $("#graph1").html("");  
                                $( "#graph1" ).append(chartCanvas1);

                                $.ajax({
                                    type: 'GET',
                                    dataType: 'json',
                                    url: 'http://localhost:5000/charts/accidents/data/chartJS/Lat=' + entry.Latitude.toString() + '&Lng=' + entry.Longitude.toString() + "&Dir=" + entry.Direction + "&Linklength=" + entry.LinkLength_miles,
                                    success: function(data) {
                                        console.log(data.toString());
                                        var ctx = document.getElementById("myChart1").getContext("2d");
                                        var myLineChart = new Chart(ctx).Line(data, lineChartOptions);
                                    }      
                                })

                                var chartCanvas2 = document.createElement('canvas');
                                chartCanvas2.id = 'myChart2';
                                $('#graph2').html(""); 
                                $( "#graph2" ).append(chartCanvas2);

                                $.ajax({
                                    type: 'GET',
                                    dataType: 'json',
                                    url: 'http://localhost:5000/charts/flow/data/chartJS/Lat=' + entry.Latitude.toString() + '&Lng=' + entry.Longitude.toString(),
                                    success: function(data) {
                                        console.log(entry.Direction);
                                        var ctx = document.getElementById("myChart2").getContext("2d");
                                        var myLineChart = new Chart(ctx).Line(data, lineChartOptions);
                                    }      
                                })
                            
                                var chartCanvas3 = document.createElement('canvas');
                                chartCanvas3.id = 'myChart3';
                                $('#graph3').html("");  
                                $( "#graph3" ).append(chartCanvas3);

                                $.ajax({
                                    type: 'GET',
                                    dataType: 'json',
                                    url: 'http://localhost:5000/charts/accidentsAndFlow/data/chartJS/Lat=' + entry.Latitude.toString() + '&Lng=' + entry.Longitude.toString() + "&Dir=" + entry.Direction + "&Linklength=" + entry.LinkLength_miles,
                                    success: function(data) {
                                        console.log(data.toString() + " LOL");
                                        var ctx = document.getElementById("myChart3").getContext("2d");
                                        var myLineChart = new Chart(ctx).Line(data, lineChartOptions);
                                    }      
                                })


                                var chartCanvas4 = document.createElement('canvas');
                                chartCanvas4.id = 'myChart4';
                                $('#graph4').html(""); // Not working???? 
                                $( "#graph4" ).append(chartCanvas4);

                                $.ajax({
                                    type: 'GET',
                                    dataType: 'json',
                                    url: 'http://localhost:5000/charts/accidentsAgainstFlow/data/chartJS/Lat=' + entry.Latitude.toString() + '&Lng=' + entry.Longitude.toString() + "&Dir=" + entry.Direction + "&Linklength=" + entry.LinkLength_miles,
                                    success: function(data) {

                                        var ctx = document.getElementById("myChart4").getContext("2d");
                                        var myLineChart = new Chart(ctx).Scatter(data, lineChartOptions);
                                    }      
                                }) 
                                
                            })
                            arrow.addTo(map);                                         
                        }) 
                    }      
                })
        }

        function clearLine() {

            if(currentPolyLine!=null) {
                map.removeLayer(currentPolyLine);
            }

        }

        function getFlowIcon(direction) {

            console.log(direction);

            var icon;

            switch(true) {
                case(direction=="N"): icon = upArrow; break;
                case(direction=="W"): icon = leftArrow; break;
                case(direction=="S"): icon = downArrow; break;
                case(direction=="E"): icon = rightArrow; break;
                default: icon = noArrow;
            }

            return icon;

        }


        function flowIntensity(n) {

            var color = '#D699FF';
            switch(true) {
                case(100000<n): color = '#25003D'; break; 
                case(50000<n): color = '#3D0066'; break;
                case(30000<n): color = '#590094'; break;
                case(10000<n): color = '#6E00B8'; break;
                case(5000<n): color = '#8700E0'; break;
                case(2000<n): color = '#9D0AFF'; break;
                case(1000<n): color = '#AD33FF'; break;
                case(500<n): color = '#BE5CFF'; break;
            }
            return color;
        }
        function getVehicleCallString() {
            var toReturn = "";

            if($('#allvehiclesCheck').is(':checked')) {
                toReturn += "allVehicles";
            }

            else  {
                switch(true) { 
                    case($('#cyclesCheck').is(':checked')): toReturn += "cycles&";
                    case($('#2wheeledCheck').is(':checked')): toReturn += "2wheeled&";
                    case($('#carsCheck').is(':checked')): toReturn += "cars&";
                    case($('#BusesCheck').is(':checked')): toReturn += "buses&";
                    case($('#lgvsCheck').is(':checked')): toReturn += "lgvs&";
                    case($('#hgvsCheck').is(':checked')): toReturn += "hgvs&";
                }
            }
            return toReturn;
        }

        function getLinkEnds(lat, lng, dir, length) {
            var toReturn = [];
            var radius = length/120;

            if(dir=="W" || dir=="E") {
                toReturn.push([lat, lng-radius],[lat, lng+radius]);
            } 

            else if(dir=="S" || dir=="N") {
                toReturn.push([lat-radius, lng],[lat+radius, lng]);
            }

            else {
                toReturn.push([lat,lng]);
            }

            return toReturn;
        }
        

                var lineChartOptions = {

                ///Boolean - Whether grid lines are shown across the chart
                scaleShowGridLines : true,

                //String - Colour of the grid lines
                scaleGridLineColor : "rgba(0,0,0,.05)",

                //Number - Width of the grid lines
                scaleGridLineWidth : 1,

                //Boolean - Whether to show horizontal lines (except X axis)
                scaleShowHorizontalLines: true,

                //Boolean - Whether to show vertical lines (except Y axis)
                scaleShowVerticalLines: true,

                //Boolean - Whether the line is curved between points
                bezierCurve : true,

                //Number - Tension of the bezier curve between points
                bezierCurveTension : 0.4,

                //Boolean - Whether to show a dot for each point
                pointDot : true,

                //Number - Radius of each point dot in pixels
                pointDotRadius : 4,

                //Number - Pixel width of point dot stroke
                pointDotStrokeWidth : 1,

                //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
                pointHitDetectionRadius : 20,

                //Boolean - Whether to show a stroke for datasets
                datasetStroke : true,

                //Number - Pixel width of dataset stroke
                datasetStrokeWidth : 2,

                //Boolean - Whether to fill the dataset with a colour
                datasetFill : true,

                //String - A legend template
                legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

            };




