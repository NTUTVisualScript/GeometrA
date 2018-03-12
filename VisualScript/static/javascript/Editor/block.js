Blockly.Blocks['main'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Main");
    this.setInputsInline(true);
    this.setNextStatement(true, null);
    this.setColour(197);
 this.setTooltip("This is the start of workspace. ");
 this.setHelpUrl("");
  }
};

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
