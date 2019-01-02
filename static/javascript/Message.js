var exports

var Message = {

    running: function(){
        document.getElementById("loader").style.display = "block";
    },

    done: function(){
        document.getElementById("loader").style.display = "none";
    },

    executedCaseSuccess: function(){
        $("#MessageList").append("<p>Test Success!</p>");
    },

    executedCaseFail: function() {
        $("#MessageList").append("<p>Test Failed!</p>");
    },

    deviceNotConnected: function(){
        $("#MessageList").append("<p>Device is not connected.</p>");
    },

    getScreenShotSuccess: function(){
        $("#MessageList").append("<p>Get ScreenShot Success.</p>");
    },

    reportPath: function(path) {
        $("#MessageList").append("<p>Report: <a href='file://" + path + "' target=_blank>" + path + "</a></p>")
    }
}

if (exports) {
    exports.Message = Message
  }