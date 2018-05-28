// function mainDisabled(event) {
//     if ( workspace.getBlockById(event.blockId) != null &&
//         workspace.getBlockById(event.blockId).type == 'main') {
//         if (event.type == 'create') {
//             workspace.updateToolbox("<xml id='toolbox' style='display:none'> \
//                 <block type='main' disabled = 'true'></block> \
//                 <block type='sleep'></block> \
//             </xml>")
//         }
//         else if (event.type == 'delete') {
//             workspace.updateToolbox("<xml id='toolbox' style='display:none'> \
//                 <block type='main' disabled = 'false'></block> \
//                 <block type='sleep'></block> \
//             </xml>")
//         }
//     }
// };

function saveOnChange(event) {
    if(event.type != 'ui' && event.type != 'delete'){
        var xml = Blockly.Xml.workspaceToDom(workspace);
        var xml_text = Blockly.Xml.domToText(xml);
        var code = Blockly.Python.workspaceToCode(workspace);
        var data = {
            xml: xml_text,
            code: code,
        }
        Post('/GeometrA/WorkSpace/save', data, function (msg) {
        })
    }
}

function openTestCase(xml){
    var dom = Blockly.Xml.textToDom(xml);
    Blockly.mainWorkspace.clear();
    Blockly.Xml.domToWorkspace(dom, workspace);
}

// workspace.addChangeListener(mainDisabled);
workspace.addChangeListener(saveOnChange);
// Disabled the blocks don't attached to main.
workspace.addChangeListener(Blockly.Events.disableOrphans);
