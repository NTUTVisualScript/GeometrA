$(document).ready(function(){
    //tabs events
    $("#tabs").tabs();

    $("#tabs").on("tabsactivate", function(){
        var active = $('#tabs ul .ui-tabs-active').attr("id");
        // var target = active.attr("id");
        // console.log(active);
        var data = JSON.parse(active);
        Post('/GeometrA/WorkSpace/open', data, function(xml){
            openTestCase(xml);
        });
    });
    $("#tabs").on( "click", "span.ui-icon-close", function() {
        var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
        $( "#" + panelId ).remove();
        $("#tabs").tabs( "refresh" );
    });
});
