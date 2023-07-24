var socket = io();

var up = document.getElementById('up')
var down = document.getElementById('down')
var left = document.getElementById('left')
var right = document.getElementById('right')
var center = document.getElementById('center')
var right_click = document.getElementById('rightClicks')
var left_click = document.getElementById('leftClicks')

var stats = []

stats[0] = 0 // 'up'
stats[1] = 0 // 'down'
stats[2] = 0 // 'left'
stats[3] = 0 // 'right'
stats[4] = 0 // 'center'
stats[5] = 0  // 'right_click'
stats[6] = 0 // 'left_click'

var stats_string = ""

socket.on('connect', function() {
    //console.log('Connected')
})

socket.on('coordinates', function(data) {

    json_data = JSON.parse(data)
    //console.log(json_data.state)

    if(stats_string != ""){
        stats = JSON.parse(sessionStorage.getItem('stats_string'))
        console.log(stats)
    }

    if (json_data.state == 'Left'){
        stats[2] ++
        left.innerHTML = stats[2]
    }
    else if (json_data.state == 'Right'){
        stats[3] ++
        right.innerHTML =stats[3]
    }
    else if (json_data.state == 'Up'){
        stats[0] ++
        up.innerHTML = stats[0]
    }
    else if (json_data.state == 'Down'){
        stats[1] ++
        down.innerHTML = stats[1]
    }
    else if (json_data.state == 'Center'){
        stats[4] ++
        center.innerHTML = stats[4]
    }
    else if (json_data.state == 'Right click'){
        stats[5] ++
        right_click.innerHTML = stats[5]
    }
    else if (json_data.state == 'Left click'){
        stats[6] ++
        left_click.innerHTML = stats[6]
    }

    stats_string = sessionStorage.setItem('stats_string', JSON.stringify(stats))
})



    
  var time;
  window.onload = function() {
  time = setTimeout(function() {
  if (document.readyState === 'complete') {
      clearTimeout(time);
  } else {
      document.location.reload();}}, 5000);};