$(document).ready(function() {
    function callback(result) {
        if (result == 'exist') {
            Log();
            BindButtonClicks()
        }
        else {
            InitializePage()
        }
    }
    Get('/VisualScript/checkLog', callback)
})

function InitializePage() {
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
}

function Log() {
    Get('/VisualScript/log', function (result) {
        if (result == 'Success') {
            WorkSpace();
        }
        else {
            InitializePage()
        }
    });
}

function BindButtonClicks(){
    $("#runAllBtn").on("click", function(){
        var data = $("#FileStructure").jstree("get_checked",null,true)
        console.log(data);
    })
    $("#saveBtn").on("click", function(){
        var xml = Blockly.Xml.workspaceToDom(workspace);
        var xml_text = Blockly.Xml.domToText(xml);
        console.log(xml_text);
    })
}
