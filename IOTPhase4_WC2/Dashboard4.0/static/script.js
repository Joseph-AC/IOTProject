var temperatureThreshold = 35;
var lightThreshold = 2000;
var currentProfile;

var animateValue = function animateValue (newPercent, elem) {
    //elem = elem || $('#fu-percent span');
    const val = parseInt(elem.text(), 10);

    if(val !== parseInt(newPercent, 10)) {
        let diff = newPercent < val ? -1 : 1;
        elem.text(val + diff);
        setTimeout(animateValue.bind(null, newPercent, elem), 5);
    }
}; 

function setHumidity(newHum)
{
const amount = Math.ceil(newHum || 25);
const currentPercent = $('#fu-percent span').text();
const waterAnimSpeed = (Math.abs(currentPercent - amount) / 50) * 10;
const waterPercent = 100 - amount;
animateValue(amount, $('#fu-percent span'));
$('#water').css({
  top : waterPercent + '%'
});
}
  
function setTemperature(temp) {

    if (temp < 0 || temp > 40) {
        return;
    }

    let value = temp/40

    $('#gauge__fill').css('transform', `rotate(${ value / 2 }turn)`);
    animateValue(temp, $('#gauge__cover'));

    if (value < 0.5) {
        document.querySelector("#gauge__fill").style.backgroundColor = 'blue';
    } else {
        document.querySelector("#gauge__fill").style.backgroundColor = 'red';
    }

}

var output = document.getElementById("LB-cover");
var output_value = document.getElementById("LEDValue");
var notif = document.getElementById("notif");
var sentEmail = false;

function clearNotification()
{
    notif.innerHTML = "";
}

async function updateHumTemp() {
    try {
        const response = await fetch('/temp-hum');
        
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const tempData = parseFloat(data.temperature);
        const humData = parseFloat(data.humidity);

        if (isNaN(tempData) && isNaN(humData)) {
            throw new Error('Invalid data received from the server.');
        }

        setHumidity(humData);
        setTemperature(tempData);

        $("#fanMode").text(data.fan);

    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

async function updateLED() {
    try {
        const response = await fetch('/LED');
        
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const LED_Intensity = parseFloat(data.intensity);
        
        if (isNaN(LED_Intensity)) {
            throw new Error('Invalid data received from the server.');
        }

        output.style.opacity = (LED_Intensity/4500);
        output_value.innerHTML = LED_Intensity;

        if (LED_Intensity < lightThreshold)
        {        
            notif.innerHTML = "Email has been sent."
            if (sentEmail == false)
            {
                sentEmail = true;
                setTimeout(clearNotification, 1000);
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

async function updateProfile()
{
    try {
        const response = await fetch('/profile');
        
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const profileData = await response.json();
        

        temperatureThreshold = (profileData.data["temperature_threshold"]);
        lightThreshold = (profileData.data["intensity_threshold"])
        
        if (isNaN(temperatureThreshold) && isNaN(lightThreshold)) {
            throw new Error('Invalid data received from the server.');
        }

        if (!currentProfile || (profileData.userID != currentProfile.userID))
        {
            console.log("PP: " + currentProfile)
            currentProfile = profileData;
            $("#profile_img").attr('src', currentProfile.data["profile_image"]);
            $("#profile_name").text("User: " + currentProfile.data["username"]);
            $("#TT").text(`Temperature Threshold: ${temperatureThreshold}`);
            $("#LT").text(`Light Threshold: ${lightThreshold}`);
        
        }
        

    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

const fanImg = document.getElementById('fanIcon');

// Set up the click event listener
fanImg.addEventListener('click', async () => {
    console.log("CLICKIN")
    try {
        const response = await fetch('/toggle-off');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('Fan toggled successfully:', data); // Handle response as needed
        
        // COde block for off

        /*if (data.fan) {
            // we use the HTML part to retrieve the images. (to find it.)
            fanImg.src = fanOnUrl; // Use the variable defined in HTML
        } else {
            fanImg.src = fanUrl; // Use the variable defined in HTML
        }*/

    } catch (error) {
        console.error('Error toggling fan:', error);
    }
});

function transmitData()
{
    updateProfile();
    updateLED();
    updateHumTemp();
}

transmitData();
setInterval(transmitData, 1000);