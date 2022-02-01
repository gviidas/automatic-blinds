
def web_page(stepperPos, batteryVol, current_date, current_time, srs, sns):
    html = """

<html><head>
  <style>
      h1 {width: 100%; text-align: center; color:rgb(255, 255, 255);}
  </style>
  <h1>ZALIUZIU VALDYMAS</h1></head>
<body style="background-color: rgb(61, 60, 60);">

<div style="text-align:center;">
<a name= closebutton href="/?blindsClose" class="button-30"> UZDARYTI</a>
<a name= openbutton href="/?blindsOpen" class="button-30"> ATIDARYTI</a>
</div>

<div class="slidecontainer">        
  <h1>PASIRINKTI POZICIJA</h1>  
  <input type="range" href="#" min="1" max="4000" value=""" + str(stepperPos) + """ onchange='changeLink()' step="1" class="slider" id="myRange"></input>      
</div>
<div>
  <h1>AUTOMATINIS ATIDARYMAS IR UZDARYMAS</h1>
  <div class="row">
      <div class= "column">
        <form action="/?"style="text-align: left">

          <label for="autoOpen" style="font-size: 180%;color: blanchedalmond;">SAULE KYLA: """ + str(srs) + """AM</label><br>
          <label for="autoClose"style="font-size: 180%;color: blanchedalmond;">SAULELYDIS: """ + str(sns) + """PM</label><br>

          <a name=autoBlindsAPI href='/?blindsAutoAPI' onclick="href" class="button-40"> NUSTATYTI</a>
        </form>

      </div>
      <div class= "column">
        <form action="/?"style="text-align: center;">
          <a name=autoBlindsOFF href='/?blindsAutoOFF' onclick="href" class="button-40"> ISJUNGTI</a>
        </form>

      </div>
      <div class= "column">
        <form action="/?"style="text-align: right">

          <label for="autoOpen" style="font-size: 180%;color: blanchedalmond;">ATIDARYTI: </label>
          <input type="time" style="height: 30%;width: 30%;" id="autoOpen" name="autoOpen" value=""><br>

          <label for="autoClose"style="font-size: 180%;color: blanchedalmond;">UZDARYTI: </label>
          <input type="time"style="height: 30%;width: 30%;" id="autoClose" name="autoClose" value=""><br>

          <a name=autoBlinds onclick='autoBlinds()' class="button-40"> NUSTATYTI</a>
        </form>

      </div>
  </div>
</div>
  <h1>Data: """ + str(current_date)+"  " + str(current_time) + """ </h1>
  <h1>Baterija """ + str(batteryVol) + """V </h1>
</body>
</html>

<script>
function autoBlinds() {
  var autoOpenValue = document.getElementById("autoOpen").value;
      autoCloseValue = document.getElementById("autoClose").value;
      window.location.href = "/?blindsAutoINPUT" + autoOpenValue +"|"+ autoCloseValue;
}

function changeLink() {
  var sliderValue = document.getElementById("myRange").value;
      window.location.href = "/?blindsValue" + sliderValue;
  
}
</script>
<style>

.button-30 {
align-items: center;
appearance: none;
background-color: #FCFCFD;
border-radius: 4px;
border-width: 0;
box-shadow: rgba(45, 35, 66, 0.4) 0 2px 4px,rgba(45, 35, 66, 0.3) 0 7px 13px -3px,#D6D6E7 0 -3px 0 inset;
box-sizing: border-box;
color: #36395A;
cursor: pointer;
display: inline-flex;
font-family: "JetBrains Mono",monospace;
height: 20%;
justify-content: center;
line-height: 1;
list-style: none;
overflow: hidden;
padding-left: 10%;
padding-right: 10%;
position: relative;
text-align: left;
text-decoration: none;
transition: box-shadow .15s,transform .15s;
user-select: none;
-webkit-user-select: none;
touch-action: manipulation;
white-space: nowrap;
will-change: box-shadow,transform;
font-size: xx-large;
}

.button-40 {
align-items: center;
appearance: none;
background-color: #FCFCFD;
border-radius: 4px;
border-width: 0;
box-shadow: rgba(45, 35, 66, 0.4) 0 2px 4px,rgba(45, 35, 66, 0.3) 0 7px 13px -3px,#D6D6E7 0 -3px 0 inset;
box-sizing: border-box;
color: #36395A;
cursor: pointer;
display: inline-flex;
font-family: "JetBrains Mono",monospace;
height: 30%;
justify-content: center;
line-height: 1;
list-style: none;
overflow: hidden;
padding-left: 20%;
padding-right: 20%;
position: relative;
text-align: left;
text-decoration: none;
transition: box-shadow .15s,transform .15s;
user-select: none;
-webkit-user-select: none;
touch-action: manipulation;
white-space: nowrap;
will-change: box-shadow,transform;
font-size: xx-large;
}

.button-30:focus {
box-shadow: #D6D6E7 0 0 0 1.5px inset, rgba(45, 35, 66, 0.4) 0 2px 4px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
}

.button-30:hover {
box-shadow: rgba(45, 35, 66, 0.4) 0 4px 8px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
transform: translateY(-2px);
}

.button-30:active {
box-shadow: #D6D6E7 0 3px 7px inset;
transform: translateY(2px);
}
.slidecontainer {
width: 100%;
}

.slider {
-webkit-appearance: none;
width: 100%;
height: 10%;
background: #d3d3d3;
outline: none;
opacity: 0.7;
-webkit-transition: .2s;
transition: opacity .2s;
}

.slider:hover {
opacity: 1;
}

.slider::-webkit-slider-thumb {
-webkit-appearance: none;
appearance: none;
width: 25px;
height: 120%;
background: #04AA6D;
cursor: pointer;
}

.slider::-moz-range-thumb {
width: 25px;
height: 25px;
background: #04AA6D;
cursor: pointer;
}
/* Create two equal columns that floats next to each other */
.row {
  display: flex;
}

.column {
  flex: 50%;
}

</style>

"""
    return html