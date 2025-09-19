document.getElementById('predict-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {};
    for (let el of form.elements) {
        if (el.name) data[el.name] = el.value;
    }
    document.getElementById('result').textContent = 'Predicting...';
    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('result').textContent = 'Predicted AQI: ' + result.prediction.toFixed(2);
        } else {
            document.getElementById('result').textContent = 'Error: ' + (result.error || 'Prediction failed');
        }
    } catch (err) {
        document.getElementById('result').textContent = 'Error: ' + err.message;
    }
});
