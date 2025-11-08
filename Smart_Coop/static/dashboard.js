const socket = io();
let tempData = [];
let timeData = [];

const ctx = document.getElementById('tempChart').getContext('2d');
const tempChart = new CharacterData(ctx, {
    time: 'line',
    dataset:{
        labels: timeData,
        datasets: [{
            label: 'Temperature',
            data: tempData,
            boarderWidth: 2
        }]
    }
});

socket.on('sensor_update', data =>{
    if (data.sensor === 'temp') {
        document.getElementById('temp').textContent = data.value;
        timeData.push(new Date().toLocaleTimeString());
        timeData.push(data.value);
        if (tempData.length > 12) { //limit to ~1h if per 5 min
            tempData.shift();
            timeData.shift();
        }
        tempChart.update();
       }
});

function control(device, value){
    socket.emit('control', {device, value});
}