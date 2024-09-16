// index.js

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
  name: "LoRaDatasetTools.extension",
  async setup() {
    console.log("LoRaDatasetTools extension loaded!");

    // Listen for validation error messages from the server
    api.addEventListener("LoRaDatasetTools.validation_error", (event) => {
      const message = event.detail.message;
      displayError(message);
    });

    // Function to display error messages to the user
    function displayError(message) {
      // Create or select an error message container
      let errorContainer = document.getElementById('LoRaDatasetTools-error');
      if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.id = 'LoRaDatasetTools-error';
        // Style the error message container
        errorContainer.style.position = 'fixed';
        errorContainer.style.bottom = '20px';
        errorContainer.style.left = '20px';
        errorContainer.style.padding = '10px';
        errorContainer.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';
        errorContainer.style.color = '#fff';
        errorContainer.style.borderRadius = '5px';
        errorContainer.style.zIndex = '1000';
        document.body.appendChild(errorContainer);
      }
      errorContainer.textContent = message;

      // Automatically hide the error after a few seconds
      setTimeout(() => {
        if (errorContainer) {
          errorContainer.remove();
        }
      }, 5000);
    }
  }
});
