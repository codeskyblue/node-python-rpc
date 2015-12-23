var Proxy = require('node-proxy');
var rpc = require('json-rpc2');
var Sync = require('sync');


var makePyObject = function(obj){
    return {
		// need json-rpc call
        get: function(receiver, name){
            return 'hello, ' + name;
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

	this.import = function(pkg){
        var result = this._client.call.sync(null, 'ping', [pkg]) //('ping', [pkg], function(err, result) {
            //console.log('ping = ' + result);
        //});
        return result;
		return Proxy.create(makePyObject(pkg));
	}
}

module.exports = function(url){
	return new Connection(url);
}
