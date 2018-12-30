var load = require('../javascript/Load')
var sinon = require('sinon')
var assert = require('assert')
const {JSDOM} = require('jsdom')

const fakeLoadHTML = `<div>Select the json file of the project on your device</div><button type="button" id="SelectFile">Select File</button><div id="Create"></div>`
describe('Create', function() {
    const jsdom = new JSDOM(fakeLoadHTML)
    global.window = jsdom.window
    global.document = jsdom.window.document

    beforeEach(function(){
        var swal = sinon.spy()
        global.swal = swal
    })

    it('Load swal function args test', function(){
        load.Load()
        assert.equal(swal.callCount, 1, 'swal should be called once')
        assert.equal(swal.args[0][0].width, '200%', 'swal width should be 200%')
        assert.equal(swal.args[0][0].title, 'Load your test!', `swal title should be 'Load your test!'`)
        assert.equal(swal.args[0][0].html, fakeLoadHTML, 'swal html should be fakeLoadHTML')
        assert.equal(swal.args[0][0].focusConfirm, false, 'swal focusConfirm should be false')
        assert.equal(swal.args[0][0].showCancelButton, true, 'swal showCancelButton should be true')
        assert.equal(swal.args[0][0].allowEscapeKey, false, 'swal allowEscapeKey should be false')
        assert.equal(swal.args[0][0].allowOutsideClick, false, 'swal allowOutsideClick should be false')
        assert.equal(typeof(swal.args[0][0].preConfirm), 'function', 'swal preConfirm should be a function')
    })

    
})