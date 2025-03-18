"use strict";
const orderDiv = document.getElementById("order");
const noisesDiv = document.getElementById("noises");
if (orderDiv && noisesDiv) {
    // Connect to the FastAPI stream
    const eventSource = new EventSource("http://127.0.0.1:8000/transcribe");
    // let transcriptSegments: string = ""; // Stores spoken text
    // let noiseSegments: string = ""; // Stores non-verbal sounds
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
    // let transcriptSegments: string[] = []; // Stores all transcriptions
    // eventSource.onmessage = (event: MessageEvent) => {
    //     const data = JSON.parse(event.data);
    //     const newSegment = data.text;
    //     // Only add to the transcript if it hasn't been added already
    //     if (!transcriptSegments.includes(newSegment)) {
    //         transcriptSegments.push(newSegment);
    //     }
    //     // Display all past messages + the new one
    //     orderDiv.innerText = transcriptSegments.join("\n");
    // };
    eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        orderDiv.innerText = "Error: Unable to connect to transcription service.";
    };
}
