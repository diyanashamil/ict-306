function submitData() {
    const data = {
        datetime: document.getElementById("datetime").value,
        p: parseFloat(document.getElementById("p").value),
        T: parseFloat(document.getElementById("T").value),
        Tpot: parseFloat(document.getElementById("Tpot").value),
        Tdew: parseFloat(document.getElementById("Tdew").value),
        rh: parseFloat(document.getElementById("rh").value),
        VPmax: parseFloat(document.getElementById("VPmax").value),
        VPact: parseFloat(document.getElementById("VPact").value),
        VPdef: parseFloat(document.getElementById("VPdef").value),
        sh: parseFloat(document.getElementById("sh").value),
        H2OC: parseFloat(document.getElementById("H2OC").value),
        rho: parseFloat(document.getElementById("rho").value),
        wv: parseFloat(document.getElementById("wv").value),
        max_wv: parseFloat(document.getElementById("max_wv").value),
        wd: parseFloat(document.getElementById("wd").value),
        rain: parseFloat(document.getElementById("rain").value),
        raining: parseInt(document.getElementById("raining").value),
        SWDR: parseFloat(document.getElementById("SWDR").value),
        PAR: parseFloat(document.getElementById("PAR").value),
        max_PAR: parseFloat(document.getElementById("max_PAR").value),
        Tlog: parseFloat(document.getElementById("Tlog").value)
    };

    fetch("/save", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
.then(response => {
    console.log(response);  // Check if the response is successful
    return response.json();
})
.then(data => {
    alert("Data saved successfully!");
})
.catch(error => console.error("Error:", error));
}




function makePrediction() {
    const data = {
        p: parseFloat(document.getElementById("p").value),
        T: parseFloat(document.getElementById("T").value),
        Tpot: parseFloat(document.getElementById("Tpot").value),
        Tdew: parseFloat(document.getElementById("Tdew").value),
        rh: parseFloat(document.getElementById("rh").value),
        VPmax: parseFloat(document.getElementById("VPmax").value),
        VPact: parseFloat(document.getElementById("VPact").value),
        VPdef: parseFloat(document.getElementById("VPdef").value),
        sh: parseFloat(document.getElementById("sh").value),
        H2OC: parseFloat(document.getElementById("H2OC").value),
        rho: parseFloat(document.getElementById("rho").value),
        wv: parseFloat(document.getElementById("wv").value),
        max_wv: parseFloat(document.getElementById("max_wv").value),
        wd: parseFloat(document.getElementById("wd").value),
        SWDR: parseFloat(document.getElementById("SWDR").value),
        PAR: parseFloat(document.getElementById("PAR").value),
        max_PAR: parseFloat(document.getElementById("max_PAR").value),
        Tlog: parseFloat(document.getElementById("Tlog").value)
    };

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const result = data.rainfall_prediction;
        document.getElementById("predictionResult").innerText = `Predicted Rainfall: ${result} mm`;

        // Show warning if rainfall exceeds threshold
        if (result > 50) {
            alert("Warning: High risk of flood or landslide!");
        }
    })
    .catch(error => console.error("Error:", error));
}
