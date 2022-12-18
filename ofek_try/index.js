const express = require('express'); //Import the express dependency
const path = require('path');
const app = express();
const server = require('http').createServer(app);//Instantiate an express app, the main work horse of this server
const io = require('socket.io')(server)
const port = 5000;                  //Save the port number where your server will be listening

//Idiomatic expression in express to route and respond to a client request
// app.post('/', (req, res) => {
//     const recording = req.body; ///ההקלטה
//     console.log(req.body);
//     ////
//     // resend json data
//     const me = 'hey'
//     res.status(200).json(me)
// });

io.on("connection",(socket)=>{
    console.log('new connection');
    socket.on("disconnect",()=>{
        console.log('disconnected');
    });

    socket.on("new message",msg =>{
        console.log(msg);
        io.emit("incoming",msg);
    });
});

server.listen(port, () => {            //server starts listening for any attempts from a client to connect at port: {port}
    console.log(`Now listening on port ${port}`); 
});