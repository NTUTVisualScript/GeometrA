function Load() {
    swal({
        width: '200%',
        title: 'Load your test!',
        html: '<div>Select the json file of the project on your device</div>' +
              '<button type="button" id="SelectFile">Select File</button>' +
              '<div id="Create"></div>',
        focusConfirm: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowOutsideClick: false,
        preConfirm: () => {
            var data = {
                projectPath: ($('#projectPath').val())
            }

            function callback(msg) {
                if (msg == 'Success') {
                    swal("Project load successfully! ");
                    WorkSpace();
                }
                else {
                    swal("Not a project file!").then(function(){
                        Load();
                    });
                }
            }
            console.log("HIHIHI")
            Post("/VisualScript/WorkSpace/load", data, callback);
        }
    });
    document.getElementById("SelectFile").onclick = function() {
        Get('/VisualScript/WorkSpace/getFilePath', function(path) {
            $("#Create").html('<input id="projectPath" disabled="disabled" \
                                value="' + path + '" class="swal2-input">')
        })
    }
}
