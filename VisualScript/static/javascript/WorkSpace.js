function WorkSpace() {
    Get("/VisualScript/WorkSpace", function(response) {

        $("#FileStructure").jstree({
            'core': {
                'check_callback': true,
                'data': response
            },
            'checkbox': {
              'three_state' : false, // to avoid that fact that checking a node also check others
              'whole_node' : false,  // to avoid checking the box just clicking the node
              'tie_selection' : false, // for checking without selecting and selecting without checking
              'cascade' : "down"
            },
            'plugins':["contextmenu", "checkbox", "state", "dnd", "unique"]
        });

        Get('/VisualScript/saveLog', function(result) {
            if (result == 'Fail')
                alert("Saving Log File Failed");
        });
    });


    // $(document).ready( function() {
    //     $.ajax({
    //         type: "POST",
    //         url: "http://127.0.0.1:5000" + "/VisualScript/getWorkSpace",
    //         data: {path:"D:/Project"},
    //         success: function(response) {
    //             $("#FileStructure").jstree({
    //                 'core' : {
    //                   'data' : response
    //                 }
    //               });
    //         },
    //     });
    // });
    // this.update = function() {
    //     $("#FileStructure").jstree({
    //         'core' : {
    //           'data' : [
    //             { "text" : "Project1", "children" : [
    //                 { "text" : "Suite1" , "children":[
    //                     {"text":"case1"},
    //                     {"text":"case2"}
    //                 ]},
    //                 { "text" : "Suite2" , "children": [
    //                     {"text":"case2"}
    //                 ]}
    //               ]}
    //           ]}
    //       });
    // };
    // this.right = function(e, d) {
    //     console.log("The selected nodes are:");
    //     console.log(data.selected);
    // };
    // $('#FileStructure').on("changed.jstree", function (e, data) {
    //     // console.log("The selected nodes are:");
    //     // console.log(data.selected);
    //     this.right(e, data.selected);
    //   });
};

// tree = WorkSpace();
