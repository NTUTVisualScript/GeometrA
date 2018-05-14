function ToolBar() {
    $("#runButton").on("click", function(){
        var nodes = $("#FileStructure").jstree("get_checked",true);
        var data = [];
        for (i = 0; i < nodes.length; ++i) {
            if(nodes[i].parents.length != 3){
                continue;
            }
            var path = $("#FileStructure").jstree().get_path(nodes[i]).join('/');
            data.push(path);
        }
        data = {
            cases: data.join(','),
        };
        Post('/GeometrA/TestScript/run', data, function(msg){
            if(msg=='success'){
                swal("Success!");
            }
        });
    });

    $("#dumpButton").on("click", function() {
        Get('/GeometrA/Screen', function(html) {
            document.getElementById("CurrentScreen").src = "../static/screenshot_pic/tmp.png?time=" + new Date().getTime();
        });
        Get('/GeometrA/Node', function(data) {
            $("#Nodes").jstree({
                grid: {
                    columns: [
                        {width:'30%', header: "Index"},
                        {width:'30%', header: "Class", value: "class"},
                        {width:'40%', header: "Bounds", value: 'bounds'}
                    ],
                    width: document.getElementById('Nodes').width
                },
                'core': {
                    'check_callback': true,
                    'data': data,
                },
                'plugins':["core", "ui", "grid"]
            });
        })
    });
}
