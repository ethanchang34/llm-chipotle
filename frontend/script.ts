const orderDiv = document.getElementById("order") as HTMLDivElement;

if (orderDiv) {
    // Connect to the FastAPI stream
    const eventSource = new EventSource("http://127.0.0.1:8000/transcribe");

    eventSource.onmessage = (event: MessageEvent) => {
        orderDiv.innerText = event.data;  // Update the displayed text dynamically
    };

    eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        orderDiv.innerText = "Error: Unable to connect to transcription service.";
    };
}
