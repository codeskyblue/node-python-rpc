var PyObject = function(obj){
	this._obj = obj;
	// get or set method
}

var Connection = function(url){
	this._url = url;
	this.import = function(pkg){
		// need json-rpc call
		return new PyObject({
			name: pkg
		})
	}
}

module.exports = function(url){
	return new Connection(url);
}
