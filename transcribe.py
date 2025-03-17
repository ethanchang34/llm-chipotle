import subprocess

WHISPER_MODEL = "whisper.cpp-1.7.4/models/ggml-base.en.bin"
WHISPER_BINARY = "./whisper.cpp-1.7.4/build/bin/whisper-stream"

def transcribe_live():
    """Runs whisper-stream and captures live transcription output."""
    process = subprocess.Popen(
        [WHISPER_BINARY, "-m", WHISPER_MODEL, "--capture", "2", "-t", "8", "--step", "500", "--length", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("🎙️ Listening for Chipotle orders... (Press Ctrl+C to stop)")

    try:
        while True:
            output = process.stdout.readline()
            if output:
                print(f"{output.strip()}")  # Print live transcript
            # error = process.stderr.readline()
            # if error:
            #     print(f"Error: {error.strip()}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping transcription...")
        process.terminate()

if __name__ == "__main__":
    transcribe_live()
