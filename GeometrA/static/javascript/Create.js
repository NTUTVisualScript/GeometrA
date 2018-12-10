function Create() {
    swal({
        width: '200%',
        title: 'Create your first test!',
        html: '<div>Project name</div>' +
            '<input id="projectName" type="text" placeholder="" value="" class="swal2-input">' +
            '<div>Suite name</div>' +
            '<input id="suiteName" type="text" placeholder="" value="" class="swal2-input">' +
            '<div>Case name</div>' +
            '<input id="caseName" type="text"  placeholder="" value="" class="swal2-input">' +
            '<div>The path on your device</div>' +
            '<button type="button" id="SelectFolder">Select Path</button>' +
            '<div id="Create"></div>',
        focusConfirm: false,
        showCancelButton: true,
        allowEscapeKey: false,
        allowOutsideClick: false,
        preConfirm: () => {
            var data = {
                projectName: ($('#projectName').val()),
                suiteName: ($('#suiteName').val()),
                caseName: ($('#caseName').val()),
                projectPath: ($('#projectPath').val())
            }
            function callback(msg) {
                if (msg == 'Success') {
                    swal("Project load successfully! ");
                    //update workspace jstree and record.log after create new project
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
                    swal("Creation Failed ").then(function() {
                        Create();
                    });
                }
            }

            Post('/GeometrA/WorkSpace/create', data, callback);
        }
    });
    document.getElementById("SelectFolder").onclick = function() {
        const electron = require('electron');
        const remote = electron.remote;
        const mainProcess = remote.require('./main');
        mainProcess.selectDirectory( function(path) {
            $("#Create").html('<input id="projectPath" disabled="disabled" value="' + path[0] + '" class="swal2-input">');
        });
    };
}
