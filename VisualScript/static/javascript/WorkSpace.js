function WorkSpace() {
    $(document).ready( function() {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000" + "/VisualScript/getWorkSpace",
            data: {path:"D:/Project"},
            success: function(response) {
                $("#FileStructure").jstree({
                    'core' : {
                      'data' : response
                    }
                  });
            },
        });
    });

    $('#FileStructure').on("changed.jstree", function (e, data) {
        // console.log("The selected nodes are:");
        // console.log(data.selected);
      });
};

tree = WorkSpace();


// var tree = WorkSpace()

// [
//   { "text" : "Project1", "children" : [
//       { "text" : "Suite1" , "children":[
//           {"text":"case1"},
//           {"text":"case2"}
//       ]},
//       { "text" : "Suite2" , "children": [
//           {"text":"case2"}
//       ]}
//     ]}
// ]
