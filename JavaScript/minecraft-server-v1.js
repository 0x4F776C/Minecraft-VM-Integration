const WebSocket = require('ws')
const uuid = require('uuid')
const child = require('child_process')

console.log('[!] Connect to server by typing /connect 192.168.1.97:8080')

// create server
const wss = new WebSocket.Server({
    port: 8080,
    host: '192.168.1.97',
    tls: true
})

// start server
wss.on('connection', function connection(socket) {
    console.log('Connected')

    // message format
    socket.send(JSON.stringify({
        "header": {
            "version": 1,
            "requestId": uuid.v4(),
            "messageType": "commandRequest",
            "messagePurpose": "subscribe"
        },
        "body": {
            "eventName": "PlayerMessage"
        }
    }))

    // prevent message spam
    const sendQueue = []
    // prevent error code spam
    const awaitedQueue = {}

    // receive message
    socket.on('message', packet => {
        const msg = JSON.parse(packet)
        //console.log(msg)

        if (msg.body.eventName == 'PlayerMessage') {
            //const match = msg.body.properties.Message.match(/^pyramid (\d+)/i)
            const match = msg.body.properties.Message.match(/^!exec/i)
            if (match) {
                //console.log('Drawing pyramid of size', match[1])
                //draw_pyramid(+match[1])
                //thunderstorm()

                cmd = msg.body.properties.Message
                filteredCmd = cmd.substr(6)

                child.exec(`${filteredCmd}`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`exec error: ${error}`)
                        return
                    }
                    console.log(`stdout: ${stdout}`)
                    console.error(`stderr: ${stderr}`)
                })
            }
        }
        if (msg.header.messagePurpose == 'commandResponse') {
            if (msg.header.requestId in awaitedQueue) {
                if (msg.body.statusCode < 0) {
                    console.log(awaitedQueue[msg.header.requestId].body.commandLine, msg.body.statusMessage)
                    delete awaitedQueue[msg.header.requestId]
                }
            }
        }

        let count = Math.min(sendQueue.length, 100 - Object.keys(awaitedQueue).length)
        
        for (let i = 0; i < count; i++) {
            let command = sendQueue.shift()
            socket.send(JSON.stringify(command))
            awaitedQueue[command.header.requestId] = command
        }
        
        if (msg.body.eventName == 'PlayerMessage') {
            const match = msg.body.properties.Message.match(/!exec/i)

            if (match) {
                cmd = msg.body.properties.Message
                console.log(cmd.substr(6))
            }
        }
    })

    // send function
    function send(cmd) {
        const msg = {
            "header": {
                "version": 1,
                "requestId": uuid.v4(),
                "messagePurpose": "commandRequest",
                "messageType": "commandRequest"
            },
            "body": {
                "commandLine": cmd,
                "origin": {
                    "type": "player"
                }
            }
        }

        //console.log(cmd)
        //socket.send(JSON.stringify(msg))
        sendQueue.push(msg)
    }

    // pyramid function
    function draw_pyramid(size) {
        for (let y = 0; y <= size; y++) {
            let side = size - y;
            for (let x = -side; x <= side; x++) {
                send(`setblock ~${x} ~${y} ~${-side} glowstone`)
                send(`setblock ~${x} ~${y} ~${+side} glowstone`)
                send(`setblock ~${-side} ~${y} ~${x} glowstone`)
                send(`setblock ~${+side} ~${y} ~${x} glowstone`)
            }
        }
    }

    // thunder function
    function thunderstorm() {
        send(`weather thunder`)
    }
    
})
