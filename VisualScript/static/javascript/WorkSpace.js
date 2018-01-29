function WorkSpace() {
    Get("/VisualScript/WorkSpace", function(response) {
        console.log($.jstree.version);
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
            },
        },
    };

    if (node["parents"].length == 3) {
        delete items.CreateItem;
    }
    return items;
}

function createSuite(inst, obj) {
    var addSuite = function (msg) {
        inst.create_node(obj, {}, "last", function (new_node) {
            try {
                inst.edit(new_node, null, function (msg) {
                    console.log(msg);
                });
            } catch (ex) {
                setTimeout(function () { inst.edit(new_node); }, 0);
            }
        });
    };
    var data = {
        "Project" = obj["text"],
    };
    Post("/VisualScript/WorkSpace/AddSuite", data, addSuite);
}
