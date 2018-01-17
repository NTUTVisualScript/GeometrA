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
        showCancelButton: false,
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
                    WorkSpace();
                }
                else {
                    swal("Creation Failed ").then(function() {
                        Create();
                    });
                }
            }
            
            Post('/VisualScript/WorkSpace/create', data, callback);
        }
    });
    document.getElementById("SelectFolder").onclick = function() {
        Get('/VisualScript/WorkSpace/getProjectPath', function(path) {
            $("#Create").html('<input id="projectPath" disabled="disabled" value="' + path + '" class="swal2-input">')
        })
    };
}
