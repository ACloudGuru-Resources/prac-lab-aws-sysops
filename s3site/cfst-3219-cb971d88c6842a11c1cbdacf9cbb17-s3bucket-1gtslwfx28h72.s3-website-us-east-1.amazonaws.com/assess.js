// Replace the YOUR_API_ENDPOINT_URL with yours
// It should look something like this:
// https://example1a2s3d.execute-api.us-east-1.amazonaws.com/prod/reminders

var API_ENDPOINT = 'https://i9rojv5xsk.execute-api.us-east-1.amazonaws.com/prod';

// Setup divs that will be used to display interactive messages
var errorDiv = document.getElementById('error-message')
var successDiv = document.getElementById('success-message')
var resultsDiv = document.getElementById('results-message')

// Setup easy way to reference values of the input boxes
function waitSecondsValue() { return document.getElementById('waitSeconds').value }

function clearNotifications() {
    // Clear any exisiting notifications in the browser notifications divs
    errorDiv.textContent = '';
    resultsDiv.textContent = '';
    successDiv.textContent = '';
}

// Add listeners for each button that make the API request
document.getElementById('bothButton').addEventListener('click', function(e) {
    sendData(e, 'both');
});


function sendData (e, pref) {
    // Prevent the page reloading and clear exisiting notifications
    e.preventDefault()
    clearNotifications()
    // Prepare the appropriate HTTP request to the API with fetch
    // create uses the root /prometheon endpoint and requires a JSON payload

    post_url = API_ENDPOINT + '/?arn=' + waitSecondsValue()
    fetch(post_url, {
        method: "POST",
        body: "",
        headers: {'Content-type': 'application/x-www-form-urlencoded'}
    })
    .then(response => response.json())
    .then(json => console.log(json))
    //.then({
    //    resultsDiv.textContent = 'Check your result below!'
    //    resultsDiv.textContent = JSON.stringify(data)
   //  })
  //   .then(resultsDiv.textContent = JSON.stringify(data))
    .catch(err => console.log(err));
};