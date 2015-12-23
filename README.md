# node-python-rpc
Node modules which helps call python code in node

Use JSONRPC to communicate nodejs and python.

Can work now. 

But libs hasn't published to npm and pypi.

This is still a alpha version. I will use it in my work, and it should get better in the future.

## Install
```
npm i --save node-python-rpc

pip install node-python-rpc
```

## Usage
Start the python rpc server

```
python -mnodepythonrpc --port 8000
```

Nodejs code

```
// python
var python = require('node-python-rpc')({host: 'localhost', port: 28642});
var os = python.import('os')

// nodejs
var path = require('path')

assert(os.path.basename(os.getcwd()) == path.basename(process.cwd()))
```

## Reference
* <https://github.com/JeanSebTr/node-python>
* <http://stackoverflow.com/questions/16586640/node-js-async-to-sync>

## LICENSE
[MIT](LICENSE)
