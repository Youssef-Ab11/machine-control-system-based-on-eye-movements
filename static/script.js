var socket = io();

var up = document.getElementById('up')
var down = document.getElementById('down')
var left = document.getElementById('left')
var right = document.getElementById('right')
var center = document.getElementById('center')
var right_click = document.getElementById('rightClicks')
var left_click = document.getElementById('leftClicks')

var stats_string
var stats = []
var tmp = []

console.log(stats)

stats_string = ""

if (stats_string != "") {
    stats = JSON.parse(sessionStorage.getItem('stats_string'))

    tmp[0] = stats[0] // 'up'
    tmp[1] = stats[1] // 'down'
    tmp[2] = stats[2] // 'left'
    tmp[3] = stats[3] // 'right'
    tmp[4] = stats[4] // 'center'
    tmp[5] = stats[5] // 'right_click'
    tmp[6] = stats[6] // 'left_click
} else {
    tmp[0] = 0 // 'up'
    tmp[1] = 0 // 'down'
    tmp[2] = 0 // 'left'
    tmp[3] = 0 // 'right'
    tmp[4] = 0 // 'center'
    tmp[5] = 0 // 'right_click'
    tmp[6] = 0 // 'left_click'
}

socket.on('connect', function () {
    //console.log('Connected')
})

socket.on('coordinates', function (data) {

    json_data = JSON.parse(data)
    //console.log(json_data.state)

    if (json_data.state == 'Left') {
        tmp[2]++
    } else if (json_data.state == 'Right') {
        tmp[3]++
    } else if (json_data.state == 'Up') {
        tmp[0]++
    } else if (json_data.state == 'Down') {
        tmp[1]++
    } else if (json_data.state == 'Center') {
        tmp[4]++
    } else if (json_data.state == 'Right click') {
        tmp[5]++
    } else if (json_data.state == 'Left click') {
        tmp[6]++
    }

    stats = tmp.slice()

    left.innerHTML = stats[2]
    right.innerHTML = stats[3]
    up.innerHTML = stats[0]
    down.innerHTML = stats[1]
    center.innerHTML = stats[4]
    right_click.innerHTML = stats[5]
    left_click.innerHTML = stats[6]

    stats_string = sessionStorage.setItem('stats_string', JSON.stringify(stats))
    console.log(sessionStorage.setItem('stats_string', JSON.stringify(stats)))
})

var time;
window.onload = function () {
    time = setTimeout(function () {
        if (document.readyState === 'complete') {
            clearTimeout(time);
        } else {
            document.location.reload();
        }
    }, 5000);
};


