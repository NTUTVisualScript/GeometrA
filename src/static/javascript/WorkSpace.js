function WorkSpace() {
    // $("#FileStructure").jstree({
    //     'core' : {
    //       'data' : [
    //         { "text" : "Project1", "children" : [
    //             { "text" : "Suite1" , "children":[
    //                 {"text":"case1"},
    //                 {"text":"case2"}
    //             ]},
    //             { "text" : "Suite2" , "children": [
    //                 {"text":"case2"}
    //             ]}
    //           ]}
    //       ]}
    //   });
    this.update = function() {
        $("#FileStructure").jstree({
            'core' : {
              'data' : [
                { "text" : "Project1", "children" : [
                    { "text" : "Suite1" , "children":[
                        {"text":"case1"},
                        {"text":"case2"}
                    ]},
                    { "text" : "Suite2" , "children": [
                        {"text":"case2"}
                    ]}
                  ]}
              ]}
          });
    }
    this.right = function(e, d) {
        console.log("The selected nodes are:");
        console.log(data.selected);
    };
    $('#FileStructure').on("changed.jstree", function (e, data) {
        // console.log("The selected nodes are:");
        // console.log(data.selected);
        this.right(e, data.selected)
      });
}

tree = WorkSpace()

export FIleTree = tree
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
