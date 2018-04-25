function Tab(data){
    //create a tab which <li> id is string of its data object.
    function createTab() {
        var _data = JSON.stringify(data);
        var num_tabs = $("div#tabs ul li").length + 1;

        $("div#tabs ul").append(
            "<li id='"+ _data + "'>" + "<a href='#tab" + num_tabs + "'>" + data['Case'] +
            "</a>"+"<span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span>"+"</li>"
        );

        $("div#tabs").append(
            "<div id='tab" + num_tabs + "'></div>"
        );

        $("div#tabs").tabs("refresh");
    };
    /*check if the tab has existed by comparing
    its <li> id with selected file data.*/
    function checkTab(){
        var check = false;
        $("ul#ul_tabs li").each(function(){
            var _data = $(this).attr("id");
            var dataString = JSON.stringify(data);
            if(_data == dataString){
                check =  true;
            }
        });
        return check;
    };
    //To focus on the tab when user double click a case
    function selectTab (li_id) {
        //find the tab that its <li> id equals to selected file data.
        var tab = $("ul#ul_tabs li").filter(function(){
            return $(this).attr("id") == li_id
        });
        var index = $("#tabs li").index(tab);
        $("#tabs").tabs({active: index});
        Post('/GeometrA/WorkSpace/Focus', data, function(msg) {});
    };
    
    Tab.createTab = createTab;
    Tab.checkTab = checkTab;
    Tab.selectTab = selectTab;
};
