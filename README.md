# node-python-rpc
Node modules which helps call python code in node

Use JSONRPC to communicate nodejs and python.

Still developing.

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
var python = require('node-python-rpc')('localhost:8000');
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
