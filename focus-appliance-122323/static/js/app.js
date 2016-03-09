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
});

