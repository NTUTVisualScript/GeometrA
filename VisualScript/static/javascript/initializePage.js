$(document).ready(function() {
    swal({
        title: 'Welcome to VisualScript',
        text: "Please load a project or create a new one",
        type: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Load',
        cancelButtonText: 'Create',
        buttonsStyling: true,
        allowEscapeKey: false,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.value) {
            swal({
                width: '200%',
                title: 'Load your test!',
                html: '<div>Select the json file of the project on your device</div>' +
                      '<button type="button" id="SelectFile">Select File</button>' +
                      '<div id="Create"></div>',
                    // '<input id="projectPath" type="file"  placeholder="" value="" class="swal2-input" \
                    // accept="text/json, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"/>',
                focusConfirm: false,
                showCancelButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
                preConfirm: () => {
                    var data = {
                        projectPath: ($('#projectPath').val())
                    }
                    $.ajax({
                        type: "POST",
                        url: "127.0.0.1:5000/VisualScript/WorkSpace/load",
                        data: data,
                        success: function(msg) {
                            if (msg)
                                swal("Project load successfully! ")
                            else
                                swal("It's not a project file! ")
                        },
                    });
                }
            });
            document.getElementById("SelectFile").onclick = function() {
                Get('/VisualScript/WorkSpace/getFilePath', function(path) {
                    $("#Create").html('<div id="projectPath">' + path + "</div>")
                })
            }
            // result.dismiss can be 'cancel', 'overlay',
            // 'close', and 'timer'
        } else if (result.dismiss === 'cancel') {
            var {
                value: formValues
            } = swal({
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
                    console.log(JSON.stringify(data));
                    $.ajax({
                        type: "POST",
                        url: "http://127.0.0.1:5000/VisualScript/WorkSpace/create",
                        data: data,
                        success: function(msg) {
                            if (msg)
                                swal("Project load successfully! ")
                            else
                                swal("It's not a project file! ")
                        },
                    });
                }
            });
            document.getElementById("SelectFolder").onclick = function() {
                Get('/VisualScript/WorkSpace/getProjectPath', function(path) {
                    $("#Create").html('<input id="projectPath" disabled="disabled" value="' + path + '" class="swal2-input">')
                })
            }
        }

    })
});
