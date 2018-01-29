function WorkSpace() {
    Get("/VisualScript/WorkSpace", function(response) {
        $("#FileStructure").jstree({
            'types': {
                'itsfile': {
                    'icon': 'jstree-file',
                },
            },
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
            'contextmenu': {
                show_at_node: true,
                items: Menu,
            },
            'plugins':["contextmenu", "checkbox", "types"]
        });

        Get('/VisualScript/saveLog', function(result) {
            if (result == 'Fail')
                alert("Saving Log File Failed");
        });
    });
};

function Menu(node) {
    var items = {
        CreateItem: {
            label: "Create",
            action: function(data) {
                var inst = $.jstree.reference(data.reference);
                var obj = inst.get_node(data.reference);
                if (obj["parents"].length == 1) {
                    createSuite(inst, obj);
                }
                else if (obj["parents"].length == 3) {
                    console.log(obj)
                }
                else {
                    createCase(inst, obj);
                }
            },
        },
    };

    // if (node["parents"].length >= 3) {
    //     delete items.CreateItem;
    // }
    return items;
}

function createSuite(inst, obj) {
    inst.create_node(obj, {}, "last", function (new_node) {
        try {
            inst.edit(new_node, null, function (node) {
                var data = {
                    Project: obj["text"],
                    Suite: node["text"],
                };
                Post("/VisualScript/WorkSpace/addSuite", data, function() {});
            });
        } catch (ex) {
            console.log(ex);
            setTimeout(function () { inst.edit(new_node); }, 0);
        }
    });
}

function createCase(inst, obj) {
    inst.create_node(obj, {}, "last", function (new_node) {
        try {
            inst.edit(new_node, null, function (node) {
                inst.set_type("itsfile", node)
                var data = {
                    Project: inst.get_node(obj["parent"])["text"],
                    Suite: obj["text"],
                    Case: node["text"],
                };
                Post("/VisualScript/WorkSpace/addCase", data, function() {});
            });
        } catch (ex) {
            console.log(ex);
            setTimeout(function () { inst.edit(new_node); }, 0);
        }
    });
}
