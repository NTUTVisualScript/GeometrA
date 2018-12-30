function Load() {
    swal({
        width: '200%',
        title: 'Load your test!',
        html: '<div>Select the json file of the project on your device</div>' +
              '<button type="button" id="SelectFile">Select File</button>' +
              '<div id="Create"></div>',
        focusConfirm: false,
        showCancelButton: true,
        allowEscapeKey: false,
        allowOutsideClick: false,
        preConfirm: () => {
            var data = {
                projectPath: ($('#projectPath').val())
            }

            function callback(msg) {
                if (msg == 'Success') {
                    swal("Project load successfully! ");
                    //update workspace jstree and record.log after load new project
                    if ($('#FileStructure').jstree(true) != false){
                        Get("/GeometrA/WorkSpace", function(response) {
                            $('#FileStructure').jstree(true).settings.core.data = response;
                            $("#FileStructure").jstree(true).refresh();
                            Get('/GeometrA/saveLog', function(result) {
                                if (result == 'Fail')
                                    alert("Saving Log File Failed");
                            });
                        });
                    }else {
                        WorkSpace();
                    }
                }
                else {
                    swal("Not a project file!").then(function(){
                        Load();
                    });
                }
            }
            Post("/GeometrA/WorkSpace/load", data, callback);
        }
    });
    document.getElementById("SelectFile").onclick = function() {
        const electron = require('electron');
        const remote = electron.remote;
        const mainProcess = remote.require('./main');
        mainProcess.selectProject( function(path) {
          let pathString = path[0].split('\\').join('/');
          $("#Create").html('<input id="projectPath" disabled="disabled" value="' + pathString + '" class="swal2-input">');
        });
    }
}

if (exports) {
    exports.Load = Load
}