$(document).ready(function(){
    $("#loginButton").click(function(){
        $("#login").find("form").submit();
    });


    $("#lookUp").click(function(){
        var pt_id = $("#pt_id");
        var dashboard = $("#dashboard");

        var container = dashboard.find("#patient_history_out");
        var loading = dashboard.find("#loading");
        loading.show("fast");

        $.post("/patient_history",{ pt_id : pt_id.val() }, function(response){
            loading.hide("fast");
            container.html(response);
        });
    });

    $(document).foundation();
});

