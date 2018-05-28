function ToolBar() {
    $("#runButton").on("click", function(){
        document.getElementById("loader").style.display = "block";
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
        if(data.cases){
            Post('/GeometrA/TestScript/run', data, function(msg){
                if(msg=='success'){
                    document.getElementById("loader").style.display = "none";
                }
                $("#MessageList").append("<p>Executed Success!</p>");
            });
        }
        else{
            swal("Please select some cases that you want to run!")
        }
    });

    $("#dumpButton").on("click", function() {
        document.getElementById("loader").style.display = "block";
        Get('/GeometrA/Screen', function(path) {
            // "../static/screenshot_pic/tmp.png?time=" + new Date().getTime()
            if(!path) {
                $("#MessageList").append("<p>Device is not connected.</p>");
                document.getElementById("loader").style.display = "none";
            }
            else{
                var _path = path.replace("./GeometrA", "..") +
                         "?time=" + new Date().getTime()
                document.getElementById("CurrentScreen").src = _path;
                $("#MessageList").append("<p>Get ScreenShot Success.</p>");
            }
        });
    });
}
