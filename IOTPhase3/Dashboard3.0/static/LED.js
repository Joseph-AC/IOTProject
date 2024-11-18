var slider = document.getElementById("myRange");
var output = document.getElementById("LB-cover");
var output_value = document.getElementById("LEDValue");
var notif = document.getElementById("notif");
var sentEmail = false;

slider.oninput = function() {

  var intensity = this.value
  output.style.opacity = intensity/500;
  output_value.innerHTML = intensity;

}

function clearNotification()
{
    notif.innerHTML = "";
}

async function updateSensorData() {
    try {
        const response = await fetch('/sensor-data');
        
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const LED_Intensity = parseFloat(data.intensity);
        console.log(LED_Intensity);
        
        if (isNaN(LED_Intensity)) {
            throw new Error('Invalid data received from the server.');
        }

        output.style.opacity = (LED_Intensity/500);
        output_value.innerHTML = LED_Intensity;

        if (LED_Intensity < 2000)
        {        
            notif.innerHTML = "Email has been sent."
            if (sentEmail == false)
            {
                sentEmail = true;
                setTimeout(clearNotification, 5000);
            }
        }
        else
        {
            sentEmail = false;
        }

    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

setInterval(updateSensorData, 5000);
updateSensorData();