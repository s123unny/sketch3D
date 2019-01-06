var line_coordinate = [];
var drawcanvas;
var context;
var paint = false;
function postdata(raw_data) {
    var data = JSON.stringify(raw_data);
    // console.log(data);
    $.ajax({
      type: "POST",
      url: "http://localhost:8000",
      data: data,
      success: function(data){
        console.log(data);
      },
      dataType: "text",
      contentType : "application/json"
    });
}
function setContext() {
    console.log("start");
    drawcanvas = document.getElementById("overlay");
    context = drawcanvas.getContext("2d");
};
function mousedownHandler(e) {
    var x = e.clientX;
    var y = e.clientY;
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = 'white';
    context.moveTo(x, y);
    paint = true;
}
function mousemoveHandler(e) {
    if (paint) {
    	// console.log(e.clientX, e.clientY);
        line_coordinate.push([e.clientX, e.clientY]);
        var x = e.clientX;
        var y = e.clientY;
        context.lineTo(x, y);
        context.stroke();
    }
}
function mouseupHandler(e) {
    paint = false;
    postdata(line_coordinate);
    line_coordinate = [];
}
function clearCanvas() {
    context.clearRect(0, 0, drawcanvas.width, drawcanvas.height);
}
