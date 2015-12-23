/*
 * test.js
 * Copyright (C) 2015 hzsunshx <hzsunshx@onlinegame-14-51>
 *
 * Distributed under terms of the MIT license.
 */


var Proxy = require('node-proxy');
var rpc = require('json-rpc2');
var sync = require('synchronize')


var client = rpc.Client.$create(28642, 'localhost')

var ret = sync.await(client.call('pyobjcall', ['PING'], sync.defer()))
console.log(ret)
    //var ret = client.call('ping', ['PING'], function(err, result) {
     //   console.log('ping = ' + result);
