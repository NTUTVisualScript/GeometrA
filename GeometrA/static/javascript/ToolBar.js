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
                $("#MessageList").append("<p>Executed Success!</p>");
            }
        });
    });

    $("#dumpButton").on("click", function() {
        Get('/GeometrA/Screen', function(path) {
            // "../static/screenshot_pic/tmp.png?time=" + new Date().getTime()
            if(!path) {
                $("#MessageList").append("<p>Device is not connected.</p>");
            }
            else{
                var _path = path.replace("./GeometrA", "..") +
                         "?time=" + new Date().getTime()
                document.getElementById("CurrentScreen").src = _path;
                $("#MessageList").append("<p>Get ScreenShot Success.</p>");
            }
        });

        Get('/GeometrA/Node', function(data) {
            console.log(data);
            $("#Nodes").jstree({
                'types': {
                    'itsfile': {
                        'icon': 'jstree-file',
                    },
                },
                'core': {
                    'check_callback': true,
                    'data': data,
                },
                'plugins':["types"]
            });
            LoadElement(-1, data);
        })
    });

    function LoadElement(node, branch) {
        data = {
            data: branch.index,
            attr: branch.class,
            state: branch.name
        };
        var node = $.jstree.reference(document.getElementById("Nodes")).create_node(
            node, data, 'last', function(new_node) {}
        );
        if (typeof branch.children === 'undefined') return false;
        for (var i=0; i < branch.children.length; i++) {
            LoadElement(node, branch.children[i]);
        }
    }
}
