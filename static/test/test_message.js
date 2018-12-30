var assert = require('assert')
var message = require('../javascript/Message')
const {JSDOM} = require('jsdom')

describe('Message', function() {  
    // Build a fake dom by JSDOM
    before(function(){
        const jsdom = new JSDOM(`
        <div id="Message">
            <h6>Message</h6>
            <div id="loader"></div>
            <div id="MessageList"></div>
        </div>`)
        global.window = jsdom.window
        global.document = jsdom.window.document
        global.$  = global.jQuery = require('jquery')
    })
    
    // Clear the <p> in MessageList if <p> exists after every case
    // to make MessageList clean
    afterEach(function(){
        var message = document.getElementById("MessageList")
        if (message.hasChildNodes()) {
            message.removeChild(message.childNodes[0])
        }
    })

    it('message running test', function() {
        message.Message.running();
        assert.equal(document.getElementById("loader").style.display, "block"
                        , "loader display should be block")
    });

    it('message done test', function(){
        message.Message.done()
        assert.equal(document.getElementById("loader").style.display, "none"
                        , "loader display should be none")
    })

    it('message executedCaseSuccess test', function() {
        message.Message.executedCaseSuccess()
        assert.equal(document.getElementById("MessageList").textContent, "Test Success!"
                        , "MessageList should append new text 'Test Success!'")
    })

    it('message executedCaseFail test', function(){
        message.Message.executedCaseFail()
        assert.equal(document.getElementById("MessageList").textContent, "Test Failed!"
                        , "MessageList should append new text 'Test Failed!'")
    })

    it('message deviceNotConnected test', function(){
        message.Message.deviceNotConnected()
        assert.equal(document.getElementById("MessageList").textContent, "Device is not connected."
                        ,"MessageList should append new text 'Device is not connected.'")
    })

    it('message getScreenShotSuccess test', function(){
        message.Message.getScreenShotSuccess()
        assert.equal(document.getElementById("MessageList").textContent, "Get ScreenShot Success."
                        ,"MessageList should append new text 'Get ScreenShot Success.'")
    })

    it('message reportPath test', function(){
        var path = "src/test/report"
        message.Message.reportPath(path)
        assert.equal(document.getElementById("MessageList").textContent, "Report: " + path
                        ,"MessageList should append new text " + path)
    })
})
