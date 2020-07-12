var socket = io();
socket.on('connect',()=>{
    document.querySelector('#annoucementForm').addEventListener('submit',(e)=>{
        socket.emit('annoucement','An annoucement has been made')
    })
    socket.on('message',(msg)=>{
        alert(msg)
    })
})
