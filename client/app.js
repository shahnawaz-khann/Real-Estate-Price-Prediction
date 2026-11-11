function getBathValue() {
  const uiBathrooms = document.getElementsByName("uiBathrooms");
  for (const radio of uiBathrooms) {
    if (radio.checked) {
      return Number(radio.value);
    }
  }
  return -1;
}

function getBHKValue() {
  const uiBHK = document.getElementsByName("uiBHK");
  for (const radio of uiBHK) {
    if (radio.checked) {
      return Number(radio.value);
    }
  }
  return -1;
}

function setPriceResult(message, isSuccess = false) {
  const priceBox = document.getElementById("uiEstimatedPrice");
  const resultValue = priceBox.querySelector(".result-value");
  resultValue.textContent = message;
  priceBox.classList.toggle("is-error", !isSuccess);
  priceBox.classList.toggle("is-success", isSuccess);
}

async function onClickedEstimatePrice() {
  const sqft = Number(document.getElementById("uiSqft").value);
  const bhk = getBHKValue();
  const bathrooms = getBathValue();
  const location = document.getElementById("uiLocations").value;
  const button = document.getElementById("estimateButton");
  const buttonLabel = button.querySelector("span");

  if (!location || Number.isNaN(sqft) || sqft <= 0 || bhk <= 0 || bathrooms <= 0) {
    setPriceResult("Please enter valid values.");
    return;
  }

  const url = "/api/predict_home_price";
  const payload = {
    total_sqft: sqft,
    bhk: bhk,
    bath: bathrooms,
    location: location,
  };

  button.disabled = true;
  buttonLabel.textContent = "Calculating estimate...";
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction failed.");
    }

    setPriceResult(`${data.estimated_price.toFixed(2)} Lakh`, true);
  } catch (error) {
    setPriceResult(error.message || "Unable to estimate price.");
  } finally {
    button.disabled = false;
    buttonLabel.textContent = "Estimate property value";
  }
}

async function onPageLoad() {
  const url = "/api/get_location_names";
  const uiLocations = document.getElementById("uiLocations");

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Unable to load neighborhoods.");
    }
    const data = await response.json();
    const locations = data.locations || [];

    uiLocations.innerHTML = '<option value="" selected disabled>Choose a neighborhood</option>';
    locations.forEach((location) => {
      const option = new Option(location, location);
      uiLocations.appendChild(option);
    });
    uiLocations.disabled = false;
  } catch (error) {
    console.error("Unable to load locations", error);
    uiLocations.innerHTML = '<option value="" selected disabled>Neighborhoods unavailable</option>';
    setPriceResult("Could not load neighborhoods. Please refresh the page.");
  }
}

window.onload = onPageLoad;
