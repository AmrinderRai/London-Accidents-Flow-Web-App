
//CREATE CUSTOM ICON OBJECTS : 
            var yellowIcon = L.Icon.extend({
                options: {
                    iconUrl: 'custom_markers/yellow_circle.png',
                    iconSize: [10,10]
                }
            })

            var orangeIcon = L.Icon.extend({
                options: {
                    iconUrl: 'custom_markers/orange_circle.png',
                    iconSize: [10,10]
                }
            })

            var redIcon = L.Icon.extend({
                options: {
                    iconUrl: 'custom_markers/red_circle.png',
                    iconSize: [10,10]
                }
            })

            var yellowIcon = new yellowIcon();           
            var orangeIcon = new orangeIcon();
            var redIcon = new redIcon();


        function plot(year) {

            var Nconstraint = map.getBounds().getNorthWest().lat.toString(); 
            var Sconstraint = map.getBounds().getSouthWest().lat.toString(); 
            var Econstraint = map.getBounds().getSouthEast().lng.toString(); 
            var Wconstraint = map.getBounds().getSouthWest().lng.toString();   

            if($('#check1').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 1 
                    + '&N=' + Nconstraint + '&S=' + Sconstraint + '&E=' + Econstraint + '&W=' + Wconstraint,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            var marker = L.marker([entry.Latitude, entry.Longitude], {icon: yellowIcon});
                            markers.push(marker); 
                            marker.addTo(map).bindPopup(entry['Date'] + "<br> Severity: " + entry.Accident_Severity + "<br> Number of Vehicles: " + entry.Number_of_Vehicles + "<br> Number of Casualties: " + entry.Number_of_Vehicles);
                        }) 
                    }      
                })
            }

            if($('#check2').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 2
                    + '&N=' + Nconstraint + '&S=' + Sconstraint + '&E=' + Econstraint + '&W=' + Wconstraint,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            var marker = L.marker([entry.Latitude, entry.Longitude], {icon: orangeIcon});
                            markers.push(marker);
                            marker.addTo(map).bindPopup(entry['Date'] + "<br> Severity: " + entry.Accident_Severity + "<br> Number of Vehicles: " + entry.Number_of_Vehicles + "<br> Number of Casualties: " + entry.Number_of_Vehicles);
                        }) 
                    }      
                })
            }

            if($('#check3').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 3 
                    + '&N=' + Nconstraint + '&S=' + Sconstraint + '&E=' + Econstraint + '&W=' + Wconstraint,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            var marker = L.marker([entry.Latitude, entry.Longitude], {icon: redIcon});
                            markers.push(marker);
                            marker.addTo(map).bindPopup(entry['Date'] + "<br> Severity: " + entry.Accident_Severity + "<br> Number of Vehicles: " + entry.Number_of_Vehicles + "<br> Number of Casualties: " + entry.Number_of_Vehicles);
                        }) 
                    }      
                })
            }

            plotFlow(year, Nconstraint, Sconstraint, Econstraint, Wconstraint);

        }

        function getCurrentVehicleString() {

            var toReturn = "";

            if($('#allvehiclesCheck').is(':checked')) {
                toReturn = "allVehicles";
            }

            else  {
                switch(true) { 
                    case($('#cyclesCheck').is(':checked')): toReturn = "cycles"; break;
                    case($('#2wheeledCheck').is(':checked')): toReturn = "2wheeled"; break;
                    case($('#carsCheck').is(':checked')): toReturn = "cars"; break;
                    case($('#BusesCheck').is(':checked')): toReturn = "buses"; break;
                    case($('#lgvsCheck').is(':checked')): toReturn = "lgvs"; break;
                    case($('#hgvsCheck').is(':checked')): toReturn = "hgvs"; break;
                }
            }

            return toReturn;
        }
