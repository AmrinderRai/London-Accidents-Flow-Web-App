     // heat layer 
     var heat;

        function heatPlot(year) {

                var plots = [];

            if($('#check1').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 1,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            plots.push([entry.Latitude, entry.Longitude, 0.2]);
                        }) 
                    }      
                })
            }

            if($('#check2').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 2,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            plots.push([entry.Latitude, entry.Longitude, 0.6]);
                        }) 
                    }      
                })
            }


            if($('#check3').is(':checked')) {
                $.ajax({
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://localhost:5000/accidents/year='+year+'&'+ 'accident_severity=' + 3,
                    success: function(data) {
                        $.each(data,function(i, entry) {
                            plots.push([entry.Latitude, entry.Longitude, 1]);
                        }) 
                    }      
                })
            }

            heat = L.heatLayer(plots, {radius: 25});
            console.log("Heated");
            heat.addTo(map); 
            cluster = true;

        }

        function removeHeat() {
            if(cluster) {
                map.removeLayer(heat);
            }
        }

        function reHeat() {
            removeHeat();
            heatPlot(parseInt($('#currentYear').text()));
        }