import asyncio
import websockets
import openai
import cv2
import numpy as np
import time

# OpenAI API Key
openai.api_key = "your-api-key"

# WebSocket URLs
VIDEO_URL = "ws://192.168.0.167:4000/video-stream"
AUDIO_URL = "ws://192.168.0.167:4000/audio-stream"

# Global variables
latest_transcription = None
image_path = "current_frame.jpg"

# Dummy function to calculate distance to the object (replace with actual sensor logic)
def get_distance_to_object():
    # Logic to get distance from ultrasonic sensor via ESP-NOW
    return 5.0  # Example distance in cm

def detect_object_with_gpt(image_path, transcription):
    """
    Uses GPT-4-turbo to analyze an image and determine if the object is in the scene.
    """
    try:
        with open(image_path, "rb") as img:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a computer vision assistant specialized in object detection and localization. "
                            "You are mounted on a 4-wheel mobile robot. Your primary purpose is to decode what the user "
                            "is trying to find and find the specific objects in its environment. "
                            "You can generate the commands 'ROTATE' and 'MOVE_FORWARD' to move the camera to find the object requested. "
                            "If the object is not found in scene 'ROTATE' by 30 degrees. If object is found in the scene move 'FORWARD' "
                            "till the distance to the object is 2.0 cm. Only provide the output in JSON format with the following information: "
                            "'command' : 'FORWARD' or 'ROTATE', 'rotate_degree': rotation angle if 'command' is 'ROTATE', "
                            "'object' : object to find, 'in_scene': if object is found in scene then True or else False."
                        ),
                    },
                    {"role": "user", "content": transcription}
                ]
            )
        response_content = response['choices'][0]['message']['content']
        return eval(response_content)  # Convert JSON response to Python dictionary
    except Exception as e:
        print(f"Error during GPT object detection: {e}")
        return None

async def handle_audio():
    """
    Handles the audio stream from the WebSocket and updates the global transcription variable.
    """
    global latest_transcription
    async with websockets.connect(AUDIO_URL) as websocket:
        print("Connected to audio WebSocket")
        while True:
            try:
                # Receive a text message (speech transcription)
                transcription = await websocket.recv()
                print(f"Received speech transcription: {transcription}")
                latest_transcription = transcription.strip()
            except Exception as e:
                print(f"Error in audio stream: {e}")
                break

async def agent_loop():
    """
    Main loop for the robot's behavior based on object detection and distance measurements.
    """
    global latest_transcription
    cap = cv2.VideoCapture(0)  # Initialize the camera
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        # Wait for a transcription command
        if not latest_transcription:
            print("Waiting for a command...")
            await asyncio.sleep(1)
            continue

        print(f"Command by user: {latest_transcription}")

        # Step 1: Capture an image
        ret, frame = cap.read()
        if not ret:
            print("Error capturing image. Skipping iteration.")
            continue

        # Save the frame to a file
        cv2.imwrite(image_path, frame)

        # Step 2: Use GPT for object detection
        print(f"Analyzing image based on transcription: {latest_transcription}")
        gpt_response = detect_object_with_gpt(image_path, latest_transcription)

        if not gpt_response:
            print("Error in object detection. Skipping iteration.")
            await asyncio.sleep(1)
            continue

        print(gpt_response)  # Print the JSON response for debugging

        # Step 3: Process response
        command = gpt_response["command"]
        in_scene = gpt_response["in_scene"]
        rotate_degree = gpt_response.get("rotate_degree", 0)

        if command == "MOVE_FORWARD" and in_scene:
            # Check distance to object
            distance = get_distance_to_object()
            if distance > 2.0:
                print(f"Moving forward. Distance to object: {distance} cm.")
                # Logic to send to ESP32 through ESP-NOW to move forward
                time.sleep(1)  # Simulate forward movement
            else:
                # Logic to send to ESP32 through ESP-NOW to stop
                print("Reached the object. Stopping.")
                break
        elif command == "ROTATE":
            print(f"Rotating by {rotate_degree} degrees to search for the object.")
            # Logic to send to ESP32 through ESP-NOW to rotate
            time.sleep(1)  # Simulate rotation

async def main():
    # Run audio handling and agent loop concurrently
    await asyncio.gather(handle_audio(), agent_loop())

if __name__ == "__main__":
    asyncio.run(main())
