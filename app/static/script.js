// script.js
document.getElementById("flower-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const sepalLength = parseFloat(document.getElementById("sepal_length").value);
    const sepalWidth = parseFloat(document.getElementById("sepal_width").value);
    const petalLength = parseFloat(document.getElementById("petal_length").value);
    const petalWidth = parseFloat(document.getElementById("petal_width").value);

    const flowerData = {
        sepal_length: sepalLength,
        sepal_width: sepalWidth,
        petal_length: petalLength,
        petal_width: petalWidth
    };

    try {
        const response = await fetch("/predict_flower", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(flowerData)
        });

        const data = await response.json();

        // Display the result
        document.getElementById("prediction-result").innerHTML = `Prediction: ${data.data}`;
    } catch (error) {
        document.getElementById("prediction-result").innerHTML = "Error: Unable to get prediction.";
    }
});
