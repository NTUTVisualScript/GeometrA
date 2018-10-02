function ToolBar() {
    $("#runButton").on("click", function(){
        Message.running();
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
            Post('/GeometrA/TestScript/run', data, function(result){
                var jsonResult = JSON.parse(result)
                if(jsonResult["state"]=='success'){
                    Message.executedCaseSuccess();    
                }
                Message.reportPath(jsonResult["reportPath"]);
                Message.done();
            });
        }
        else{
            swal("Please select cases that you want to run!")
        }
    });

    $("#dumpButton").on("click", function() {
        Message.running();
        Get('/GeometrA/Screen', function(path) {
            // "../static/screenshot_pic/tmp.png?time=" + new Date().getTime()
            if(!path) {
                Message.deviceNotConnected();
            }
            else{
                var _path = path.replace("./GeometrA", "..") +
                         "?time=" + new Date().getTime()
                document.getElementById("CurrentScreen").src = _path;
                Message.getScreenShotSuccess();
            }
            Message.done();
        });
    });

    $("#loadButton").on("click", function() {
        Load();
    });

    $("#createButton").on("click", function() {
        Create();
    });
}
