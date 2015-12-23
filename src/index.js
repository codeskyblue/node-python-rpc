var Proxy = require('node-proxy');
var rpc = require('json-rpc2');
var deasync = require('deasync');


var makePyObject = function(client, obj){
    return {
		// need json-rpc call
        get: function(receiver, name){
            console.log('hello, ' + name + obj.value);
            return function(){
                var res = null;
                var done = false;
                console.log(client.call)
                console.log('arguments', arguments, name, obj.value)
                client.call('pyobjcall', [obj.value, name, []], function(err, result) {
                    console.log("pyobj", err, result)
                    console.log('objcall = ' + result);
                    res = result;
                    done = true;
                });
                deasync.loopWhile(function(){ return !done;})
                if (res.type !== 'object'){
                    return res.value;
                }
                return makePyObject(client, res);
            };
        },
		// need json-rpc call
        set: function(receiver, name, value){
            console.log(name, value)
            return true;
        }
    }
}


var Connection = function(config){
    var config = config || {};
    this._host = config.host || 'localhost';
    this._port = config.port || 28642;
    this._client = rpc.Client.$create(this._port, this._host);

    var self = this;
	this.import = function(pkg){
        //console.log(deasync(this._client.call)('ping', [pkg]))
        var res = null;
        var done = false;
        this._client.call('pyimport', [pkg], function(err, result) {
            //console.log('ping = ' + result);
            res = result;
            done = true;
        });
        deasync.loopWhile(function(){ return !done;});
        var newClient = rpc.Client.$create(this._port, this._host);
		return Proxy.create(makePyObject(this._client, res));
	}
}

module.exports = function(url){
	return new Connection(url);
}
