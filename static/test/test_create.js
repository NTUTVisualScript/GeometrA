var create = require('../javascript/Create')
var sinon = require('sinon')
var assert = require('assert')
const {JSDOM} = require('jsdom')

const fakeCreateHTML = `<div>Project name</div><input id="projectName" type="text" placeholder="" value="" class="swal2-input"><div>Suite name</div><input id="suiteName" type="text" placeholder="" value="" class="swal2-input"><div>Case name</div><input id="caseName" type="text"  placeholder="" value="" class="swal2-input"><div>The path on your device</div><button type="button" id="SelectFolder">Select Path</button><div id="Create"></div>`

describe('Create', function() {
    before(function(){
        const jsdom = new JSDOM(fakeCreateHTML)
        global.window = jsdom.window
        global.document = jsdom.window.document    
    })
    
    beforeEach(function(){
        var swal = sinon.spy()
        global.swal = swal
    })

    it('Create swal function args test', function(){
        create.Create()
        assert.equal(swal.callCount, 1, 'swal should be called once')
        assert.equal(swal.args[0][0].width, '200%', 'swal width should be 200%')
        assert.equal(swal.args[0][0].title, 'Create your first test!', `swal title should be 'Create your first test!'`)
        assert.equal(swal.args[0][0].html, fakeCreateHTML, 'swal html should be fakeCreateHTML')
        assert.equal(swal.args[0][0].focusConfirm, false, 'swal focusConfirm should be false')
        assert.equal(swal.args[0][0].showCancelButton, true, 'swal showCancelButton should be true')
        assert.equal(swal.args[0][0].allowEscapeKey, false, 'swal allowEscapeKey should be false')
        assert.equal(swal.args[0][0].allowOutsideClick, false, 'swal allowOutsideClick should be false')
        assert.equal(typeof(swal.args[0][0].preConfirm), 'function', 'swal preConfirm should be a function')
    })

    
})