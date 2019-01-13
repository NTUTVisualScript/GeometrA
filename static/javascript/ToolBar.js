function screenCallback (path) {
  if(!path) {
      Message.deviceNotConnected();
  }
  else {
      console.log(path)
      var _path = path + "?time=" + new Date().getTime()
      document.getElementById("CurrentScreen").src = _path;
      Message.getScreenShotSuccess();
  }
  Message.done();
}

function getScreen() {
    Get('/GeometrA/Screen', screenCallback);
}

function ToolBar() {
    $("#runButton").on("click", function() {
        const electron = require('electron');
        const remote = electron.remote;
        const mainProcess = remote.require('./main');
        mainProcess.startLive();
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
                try {
                    var jsonResult = JSON.parse(result)
                    if(jsonResult["state"]=='success') {
                        Message.executedCaseSuccess();
                    }
                    else {
                        Message.executedCaseFail();
                    }
                    Message.reportPath(jsonResult["reportPath"]);
                } catch {
                    Message.executedCaseFail();
                }
                mainProcess.endLive();
                Message.done();
            });
        }
        else{
            swal("Please select cases that you want to run!")
        }
    });

    $("#dumpButton").on("click", function() {
        Message.running();
        getScreen();
    });

    $("#loadButton").on("click", function() {
        Load();
    });

    $("#createButton").on("click", function() {
        Create();
    });
}
