$(document).ready(function(){
    //tabs events
    $("#tabs").tabs();

    $("#tabs").on("tabsactivate", function(){
        var active = $('#tabs').tabs('option', 'active') + 1;
        var target = "#d_tab" + active;
        var data = JSON.parse($(target).text());
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
