// Replace the YOUR_API_ENDPOINT_URL with yours
// It should look something like this:
// https://example1a2s3d.execute-api.us-east-1.amazonaws.com/prod/reminders

var api_endpoint = _config.api.invokeUrl

// Setup divs that will be used to display interactive messages
var resultsDiv = document.getElementById('results-message')

// Setup easy way to reference values of the input boxes
function waitSecondsValue() { return document.getElementById('waitSeconds').value }

function clearNotifications() {
    // Clear any exisiting notifications in the browser notifications divs
    resultsDiv.textContent = '';
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
    api_endpoint_with_query = api_endpoint + '/?arn=' + waitSecondsValue()
    fetch(api_endpoint_with_query, {
        headers: {'Content-type': 'application/x-www-form-urlencoded'},
        method: 'POST',
        body: JSON.stringify({
            arn: waitSecondsValue()
    }),
        mode: 'cors'
    })
    .then(
    function(response) {
        console.log(response)
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        console.log(data);
        resultsDiv.textContent = 'Check your result below!'
        resultsDiv.textContent = JSON.stringify(data)
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
};