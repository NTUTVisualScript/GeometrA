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
                html: '<div>The path on your device</div>' +
                    '<input id="projectPath" type="file"  placeholder="" value="" class="swal2-input">',
                focusConfirm: false,
                showCancelButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
                preConfirm: () => {
                    var data = {
                        "projectPath": ($('#projectPath').val())
                    }
                    //console.log(JSON.stringify(data));
                    Post('/login', data, function(msg) {
                        swal(msg);
                    });
                }
            });
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
                    '<input id="projectPath" type="file"  placeholder="" value="" class="swal2-input">',
                focusConfirm: false,
                showCancelButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
                preConfirm: () => {
                    var data = {
                        "projectName": ($('#projectName').val()),
                        "suiteName": ($('#suiteName').val()),
                        "caseName": ($('#caseName').val()),
                        "projectPath": ($('#projectPath').val())
                    }
                    //console.log(JSON.stringify(data));
                    Post('/login', data, function(msg) {
                        swal(msg);
                    });
                }
            });

        }
    })
});