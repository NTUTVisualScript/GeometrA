Blockly.Blocks['main'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Main");
    this.setInputsInline(true);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("This is the start of workspace. ");
 this.setHelpUrl("");
  }
};

Blockly.Python['main'] = function(block) {
    var code = "Main\\";
    return code;
}

Blockly.Blocks['sleep'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Sleep(s)")
        .appendField(new Blockly.FieldNumber(0, 0, 60), "Time");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(225);
 this.setTooltip("This is an action for you to wait for few seconds. (Domain is between 0 and 60.)");
 this.setHelpUrl("");
  }
};

Blockly.Python['sleep'] = function(block) {
    var code = "Sleep(s)|" + block.getFieldValue("Time") + '\\';
    return code;
}

Blockly.Blocks['swipe'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Swipe")
        .appendField("start: ")
        .appendField("x")
        .appendField(new Blockly.FieldTextInput("0"), "startX")
        .appendField("y")
        .appendField(new Blockly.FieldTextInput("0"), "startY")
        .appendField(", end: ")
        .appendField("x")
        .appendField(new Blockly.FieldTextInput("0"), "EndX")
        .appendField("y")
        .appendField(new Blockly.FieldTextInput("0"), "EndY");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("This is an action for you to swipe on the device!");
    this.setHelpUrl("");
  },
  update: function(data){
    console.log(data)
    this.getField("startX").setValue(Math.round(data.startX));
    this.getField("startY").setValue(Math.round(data.startY));
    this.getField("EndX").setValue(Math.round(data.endX));
    this.getField("EndY").setValue(Math.round(data.endY));
  }
};

Blockly.Python['swipe'] = function(block) {
  var text_startx = block.getFieldValue('startX');
  var text_starty = block.getFieldValue('startY');
  var text_endx = block.getFieldValue('EndX');
  var text_endy = block.getFieldValue('EndY');
  var code = "Swipe|start x=" + text_startx + ", y=" + text_starty + ", end x=" + text_endx + ", y=" + text_endy + "\\";
  return code;
};

Blockly.Blocks['set_text'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set Text ")
        .appendField(new Blockly.FieldTextInput(""), "content");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This is an action for you to input the text on device!");
 this.setHelpUrl("");
  }
};

Blockly.Python['set_text'] = function(block) {
  var text_content = block.getFieldValue('content');
  var code = 'Set Text|' + text_content + '\\';
  return code;
};

Blockly.Blocks['android_keycode'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Android Keycode ")
        .appendField(new Blockly.FieldTextInput(""), "keycode");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This is an action for you to use the key codes provided by Android; you can use it with either key code name or key code index. ");
 this.setHelpUrl("https://github.com/NTUTVisualScript/GeometrA/blob/master/docs/KeycodeList.md");
  }
};

Blockly.Python['android_keycode'] = function(block) {
  var text_keycode = block.getFieldValue('keycode');
  var code = 'Android Keycode|' + text_keycode + "\\";
  return code;
};

Blockly.Blocks['loop'] = {
  init: function() {
    this.appendStatementInput("Loop")
        .setCheck(null)
        .appendField("Loop")
        .appendField(new Blockly.FieldNumber(1, 1), "times");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
 this.setTooltip("This is an action for you to execute your code iteratively.");
 this.setHelpUrl("");
  }
};

Blockly.Python['loop'] = function(block) {
  var number_times = block.getFieldValue('times');
  var statements_loop = Blockly.Python.statementToCode(block, 'Loop');
  var code = 'Loop Begin|' + number_times + '\\' + statements_loop.replace('  ', '') + 'Loop End| \\'
  return code;
};


Blockly.Blocks['click'] = {
  init: function() {
    this.appendDummyInput("clickInput")
        .appendField("Click")
        .appendField(new Blockly.FieldImage("", 100, 100, "*"), "image");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(220);
    this.getField('image').EDITABLE = true;
    this.setTooltip("This is an action for you to click on your device.");
    this.setHelpUrl("");
  },
  update: function(data){
     this.getField("image").setValue(data);
  }
};

Blockly.Python['click'] = function(block) {
    var image = block.getFieldValue('image');
    var code = 'Click|' + image + '\\';
    return code;
};

Blockly.Blocks['assert_exist'] = {
  init: function() {
    this.appendDummyInput("assertInput")
        .appendField("Assert Exist")
        .appendField(new Blockly.FieldImage("", 100, 100, "*"), "image");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(285);
    this.getField('image').EDITABLE = true;
    this.setTooltip("This is an action for you to assert if image exist, return true if exist");
    this.setHelpUrl("");
  },
  update: function(data){
        this.getField("image").setValue(data);
  }
};

Blockly.Python['assert_exist'] = function(block) {
    var image = block.getFieldValue('image');
    var code = 'Assert Exist|' + image + '\\';
    return code;
};

Blockly.Blocks['assert_not_exist'] = {
  init: function() {
    this.appendDummyInput("assertInput")
        .appendField("Assert Not Exist")
        .appendField(new Blockly.FieldImage("", 100, 100, "*"), "image");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(285);
    this.getField('image').EDITABLE = true;
    this.setTooltip("This is an action for you to assert if image exist, return true if not exist.");
    this.setHelpUrl("");
  },
  update: function(data){
        this.getField("image").setValue(data);
  }
};

Blockly.Python['assert_not_exist'] = function(block) {
    var image = block.getFieldValue('image');
    var code = 'Assert Not Exist|' + image + '\\';
    return code;
};

Blockly.Blocks['common_action'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Common Action")
        .appendField(new Blockly.FieldDropdown([["home","3"], ["back","4"], ["power","26"], ["enter","66"], ["delete","67"], ["search","84"]]), "keycode");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
 this.setTooltip("These are common actions for you to use.");
 this.setHelpUrl("");
  }
};

Blockly.Python['common_action'] = function(block) {
  var dropdown_keycode = block.getFieldValue('keycode');
  var code = 'Android Keycode|' + dropdown_keycode + "\\";
  return code;
};

Blockly.Blocks['open_app'] = {
  init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("Open App")
        .appendField("")
        .appendField(new Blockly.FieldTextInput("Apps Name"), "AppName");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("Input the name of the app you want to open");
 this.setHelpUrl("");
  }
};

Blockly.Python['open_app'] = function(block) {
  var appName = block.getFieldValue('AppName')
  var code = "Open App|" + appName + "\\";
  return code; 
}
