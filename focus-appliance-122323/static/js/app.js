String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

$(document).ready(function(){
    $("#loginButton").click(function(){
        $("#login").find("form").submit();
    });

    function setUpYearSlider(){
        $("#yearSlider").slider({
          min: 1,
          max: 5,
          range: "min",
          value: 1
         });
    }

    function setUpAnalysis(){
        var analysis = $("#analysis");
        var pt_id = $("#pt_id");
        if(analysis.length > 0){
            $.get("/analysis_table",{ pt_id : pt_id.val() }, function(response){
                analysis.find("div.content").html(response);
                setUpCharts();
            });
        }
    }

    function setUpCandidateHcc(){
        var candidate_hcc = $("#candidate_hcc");
        var pt_id = $("#pt_id");
        if(candidate_hcc.length > 0){
            $.get("/candidate_hcc_table",{ pt_id : pt_id.val() }, function(response){
                candidate_hcc.find("div.content").html(response);
                $('#candidate_hcc_table').DataTable({ "sDom": '<"top">rt<"bottom"lp><"clear">'});
                setUpCandidateHccEvents();
            });
        }
    }

    function setUpCandidateHccEvents(){
        $("#candidate_hcc_table td a").click(function(e){
            e.preventDefault();
            var anchor = $(this);
            var action = anchor.attr("rel");
            var id = anchor.attr("data-id");
            loadHccFor(action, id);
        });
    }

    function loadHccFor(action, id){
        var pt_id = $("#pt_id");
        var action_title = action.capitalize();
        $.post("/"+action+"_candidate_hcc",{ pt_id : pt_id.val(), hcc: id}, function(response){
            $("#candidate_hcc_dashboard").append(response);
            var buttons = {};
            buttons[action_title] =  function() {
                            alert("Added");
                            $( this ).dialog( "close" );
            };
            buttons["Cancel"] = function() {
                          $( this ).dialog( "close" );
            };

            $( "#"+action+"_dialog" ).dialog({
                  modal: true,
                  width: 1000,
                  height: 550,
                  buttons: buttons
            });
            $( "#verification_status" ).selectmenu();
        });

    }

    $("#lookUp").click(function(){
        var pt_id = $("#pt_id");
        var dashboard = $("#dashboard");
        var container = dashboard.find("#patient_list_container");
        var loading = dashboard.find("#loading");
        loading.show("fast");

        $.post("/patient_lookup",{ pt_id : pt_id.val() }, function(response){
            loading.hide("fast");
            container.html(response);
            $('#patient_list').DataTable({ "sDom": '<"top">rt<"bottom"lp><"clear">'});

        });
    });

    $(document).foundation();
    setUpYearSlider();
    setUpCandidateHcc();
    setUpAnalysis();
    setUpRiskMeter();
});



function setUpCharts(){
    $('#analysis_table').find('div.piechart').highcharts({
        exporting: { enabled: false },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                        enabled: false
                    },
                showInLegend: true
            }
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'Value 1',
                y: 56.33
            }, {
                name: 'Value 2',
                y: 24.03,
                sliced: true,
                selected: true
            }, {
                name: 'Value 3',
                y: 10.38
            }, {
                name: 'Value 4',
                y: 4.77
            }]
        }]
    });

     $('#analysis_table').find('div.barchart').highcharts({
        exporting: { enabled: false },
        chart: {
            type: 'column'
        },
         title: {
            text: ''
        },
        xAxis: {
            categories: [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Risk',
            data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]

        }]
    });


}

function setUpRiskMeter(){
     $('#risk_meter').highcharts({

        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },

        title: {
            text: ''
        },
        exporting: { enabled: false },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },

        // the value axis
        yAxis: {
            min: 0,
            max: 100,

            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: '%'
            },
            plotBands: [{
                from: 0,
                to: 30,
                color: '#55BF3B' // green
            }, {
                from: 30,
                to: 60,
                color: '#DDDF0D' // yellow
            }, {
                from: 60,
                to: 100,
                color: '#DF5353' // red
            }]
        },

        series: [{
            name: 'Risk',
            data: [90],
            tooltip: {
                valueSuffix: ' %'
            }
        }]

    },
    // Add some life
    function (chart) {
        if (!chart.renderer.forExport) {
            setInterval(function () {
                var point = chart.series[0].points[0],
                    newVal,
                    inc = Math.round((Math.random() - 0.5) * 20);

                newVal = point.y + inc;
                if (newVal < 0 || newVal > 200) {
                    newVal = point.y - inc;
                }

                point.update(newVal);

            }, 3000);
        }
    });
}