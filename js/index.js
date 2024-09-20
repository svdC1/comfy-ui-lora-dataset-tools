// index.js

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
  name: "LoRaDatasetTools.extension",
  async setup() {
    console.log("LoRaDatasetTools extension loaded!");
    }})