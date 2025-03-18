"use strict";
const orderDiv = document.getElementById("order");
const noisesDiv = document.getElementById("noises");
if (orderDiv && noisesDiv) {
    // Connect to the FastAPI stream
    const eventSource = new EventSource("http://127.0.0.1:8000/transcribe");
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const newSegment = data.text;
        if (data.noise) {
            noisesDiv.innerText = newSegment;
        }
        else {
            orderDiv.innerText = newSegment;
        }
    };
    eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        orderDiv.innerText = "Error: Unable to connect to transcription service.";
    };
}
