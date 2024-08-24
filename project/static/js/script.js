let detectionInterval;
let selectedPart = document.getElementById('part-select').value;

document.getElementById('part-select').addEventListener('change', () => {
    selectedPart = document.getElementById('part-select').value;
});

function startDetection() {
    fetch(`/set_part?part=${selectedPart}`)
        .then(response => {
            if (response.ok) {
                document.getElementById('result').innerText = `Part set to ${selectedPart}. Starting detection...`;
                detectionInterval = setInterval(fetchDetectionOutput, 1000);
            } else {
                throw new Error('Failed to set part.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = `Error: ${error.message}`;
        });
}

function stopDetection() {
    clearInterval(detectionInterval);
    document.getElementById('result').innerText = 'Detection stopped.';
}

function fetchDetectionOutput() {
    fetch(`/get_detection_output`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch detection output.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('detection-output').src = `data:image/jpeg;base64,${data.image}`;
            document.getElementById('result').innerText = `Result: ${data.result}`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = `Error: ${error.message}`;
        });
}
