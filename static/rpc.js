var functions = 0
var ws = new WebSocket("ws://localhost:9000/rpc")
    ws.onopen = function() {
        ws.send("Connect!");
    };

    ws.onmessage = function (funcs) {
        functions = JSON.parse(funcs.data)
        for (i = 0; i < functions.length; i++){
            console.log("FUNCTION CREATE: " + functions[i])
            window[functions[i]] = make_stub(functions[i])
        }
    };
var func_receive = 0
var return_val = -1

var ws2 = new WebSocket("ws://localhost:9000/rpc_call")
    ws2.onopen = function() {
        ws.send("Connect!");
    };

    ws2.onmessage = function (ret) {
        return_val = JSON.parse(ret.data)
        func_receive = 1
        console.log(return_val)
    };

function make_stub(func_name){
    function stub(){
        var args = Array.prototype.slice.call(arguments, 0);
        fobj = {"name": func_name, "args":args}
        ws2.send(JSON.stringify(fobj))

        while (0 && !func_receive){
            //do nothing
        }
        func_receive = 0
        var ret = return_val
        return_val = -1
    }
    return stub
}
