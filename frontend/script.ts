const orderDiv = document.getElementById("order") as HTMLDivElement;

if (orderDiv) {
    // Connect to the FastAPI stream
    const eventSource = new EventSource("http://127.0.0.1:8000/transcribe");

    // let fullTranscript: string = ""; // Stores full corrected transcript

    // eventSource.onmessage = (event: MessageEvent) => {
    //     const data = JSON.parse(event.data);
    //     const newTranscript = data.text;

    //     // Replace the entire transcript with the newest refined version
    //     fullTranscript = newTranscript;
    //     orderDiv.innerText = fullTranscript;
    // };

    let transcriptSegments: string[] = []; // Stores all transcriptions

    eventSource.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        const newSegment = data.text;

        // Only add to the transcript if it hasn't been added already
        if (!transcriptSegments.includes(newSegment)) {
            transcriptSegments.push(newSegment);
        }

        // Display all past messages + the new one
        orderDiv.innerText = transcriptSegments.join("\n");
    };

    eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        orderDiv.innerText = "Error: Unable to connect to transcription service.";
    };
}
