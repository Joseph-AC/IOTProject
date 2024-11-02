// fan.js
async function updateFanStatus() {
    try {
        const response = await fetch('/sensor-data');
        if (response.ok) {
            const data = await response.json();
            const fanStatus = data.fan_on; // Get the fan status from the response

            // Select the fan image
            const fan = document.getElementById('fan');

            // Toggle spin class based on fan status
            if (fanStatus) {
                fan.classList.add('spin'); // Add spin class to start spinning
            } else {
                fan.classList.remove('spin'); // Remove spin class to stop spinning
            }
        } else {
            console.error('Failed to fetch sensor data:', await response.text());
        }
    } catch (error) {
        console.error('Error fetching fan status:', error);
    }
}

// Fetch fan status every 5 seconds
setInterval(updateFanStatus, 5000);
updateFanStatus(); // Initial call to set fan status on load
