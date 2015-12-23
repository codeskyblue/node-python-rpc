"use strict"
/*
 * test.js
 * Copyright (C) 2015 hzsunshx <hzsunshx@onlinegame-14-51>
 *
 * Distributed under terms of the MIT license.
 */


var python = require('.')();

var os = python.import('os');

console.log("GOOD: import os")


var getcwd = os.getcwd;
console.log(getcwd())
console.log(os.path.sep)
// console.log("GOOD: call getcwd")
