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
            max: 10,
            range: "min",
            value: 4    ,
            slide : function( event, ui ) {
                var year_text = ui.value > 1 ? ui.value+" years" : ui.value+" year";
                $( "span#years-value" ).html(year_text);
                loadCandidateHcc(ui.value, includeRejectedHcc());
                loadAnalysis(ui.value, includeSelectedHcc());
            }
        });
    }

    function setUpAnalysis(){
        if($("#analysis").length > 0){
            loadAnalysis($("#yearSlider").slider("value"), includeSelectedHcc());
        }
    }

    function loadAnalysis(years, include_selected){
        $.get("/analysis_table",{ pt_id : $("#pt_id").val(), include_selected : include_selected, years: years }, function(response){
                $("#analysis").find("div.content").html(response);
                var table = $('#analysis_table');
                setUpPieChart(table.find('div.piechart'), pie_chart_data);
                setUpBarChart(table.find('div.barchart'), bar_chart_data);
            });
    }

    function setUpCheckBoxes() {
        $("#include_rejected_hccs").change(function(){
            loadCandidateHcc($("#yearSlider").slider("value"), includeRejectedHcc());
        });
        $("#include_selected_hccs").change(function(){
             loadAnalysis($("#yearSlider").slider("value"), includeSelectedHcc());
        });
    }

    function includeRejectedHcc(){
       return $("#include_rejected_hccs").prop("checked");
    }

    function includeSelectedHcc(){
        return $("#include_selected_hccs").prop("checked");
    }

    function loadCandidateHcc(years, include_rejected){
        $.get("/candidate_hcc_table",{
            pt_id : $("#pt_id").val(),
            years: years,
            include_rejected : include_rejected
        }, function(response){
                $("#candidate_hcc").find("div.content").html(response);
                $('#candidate_hcc_table').DataTable({ "sDom": '<"top">rt<"bottom"lp><"clear">'});
                setUpCandidateHccEvents();
        });
    }

    function setUpCandidateHcc(){
        var candidate_hcc = $("#candidate_hcc");
        if(candidate_hcc.length > 0){
            loadCandidateHcc($("#yearSlider").slider("value"), includeRejectedHcc())
        }
    }

    function setUpCurrentHcc(){
        var current_hcc = $("#current_year_hcc");
        var pt_id = $("#pt_id");
        if(current_hcc.length > 0){
            $.get("/current_hcc_table",{ pt_id : pt_id.val() }, function(response){
                current_hcc.find("div.content").html(response);
            });
        }
    }

    function setUpCandidateHccEvents(){
        $("#candidate_hcc_table").find("td a").click(function(e){
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
        var pt_lookupType = $("input[name='pt_lookupType']:checked");
        
        var dashboard = $("#dashboard");
        var container = dashboard.find("#patient_list_container");
        var loading = dashboard.find("#loading");
        loading.show("fast");

        $.post("/patient_lookup", { pt_id: pt_id.val(), pt_lookupType: pt_lookupType.val() }, function (response) {
            loading.hide("fast");
            container.html(response);
            $('#patient_list').DataTable({ "sDom": '<"top">rt<"bottom"lp><"clear">'});
        });
    });

    $(document).foundation();
    setUpYearSlider();
    setUpCandidateHcc();
    setUpCurrentHcc();
    setUpAnalysis();
    setUpCheckBoxes();
    setUpRiskMeter("#risk_meter");
});



function setUpPieChart(container, data){
    container.highcharts({
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
            data: data
        }]
    });
}

function setUpBarChart(container, data){
     container .highcharts({
        exporting: { enabled: false },
        chart: {
            type: 'column'
        },
         title: {
            text: ''
        },
        xAxis: {
            categories: data.categories,
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
            data: data.values
        }]
    });

}

function setUpRiskMeter(selector){
     var value = parseFloat($(selector).attr("rel"));
     $(selector).highcharts({

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
            data: [value],
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    },

    function (chart) {});
}