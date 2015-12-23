var Proxy = require('node-proxy');
var rpc = require('json-rpc2');
var deasync = require('deasync');
var _ = require('underscore');


var rpcCallSync = function(client, funcName, args){
    var res = null;
    var done = false;
    client.call(funcName, args, function(err, result) {
        res = result;
        done = true;
    });
    deasync.loopWhile(function(){ return !done;})
    return res;
}

var unwrap = function(client, res){
    if (res.type === 'function'){
        return makePyFunction(client, res)
    }
    if (res.type === 'object'){
        return makePyObject(client, res);
    }
    if (res.type === 'error'){
        throw res.value;
    }
    return res.value;
}

var makePyFunction = function(client, obj){
    return function(){
        var res = rpcCallSync(client, 'pyobjrun', [obj.value, _.values(arguments)])
        return unwrap(client, res);
    }
}

var makePyObject = function(client, obj){
    var handler = {
        get: function(receiver, name){
            var res = rpcCallSync(client, 'pyobjget', [obj.value, name]);
            return unwrap(client, res);
        },
		// need json-rpc call
        set: function(receiver, name, value){
            console.log(name, value)
            return true;
        }
    }
    return Proxy.create(handler);
}


var Connection = function(config){
    var config = config || {};
    this._host = config.host || 'localhost';
    this._port = config.port || 28642;
    this._client = rpc.Client.$create(this._port, this._host);

    var self = this;
	this.import = function(pkg){
        var res = rpcCallSync(this._client, 'pyimport', [pkg])
		return makePyObject(this._client, res);
	}
}

module.exports = function(url){
	return new Connection(url);
}
