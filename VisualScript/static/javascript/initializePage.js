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
            Load()
        } else if (result.dismiss === 'cancel') {
            Create()
        }
    })
});
