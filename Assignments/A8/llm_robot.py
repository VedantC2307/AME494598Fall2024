import asyncio
import ssl
import time
import websockets
import json
from openai import OpenAI
import base64
import cv2
import numpy as np


last_saved_frame = None      
WS_URL = 'wss://192.168.0.133:4000'

client = OpenAI(api_key = "YOUR_API_KEY")

def get_distance_to_object():
    return 5.0

def detect_object_with_gpt(b64_img, prompt):
    """
    Uses GPT-4-turbo to analyze an image and determine if the object is in the scene.
    """
    # print(f"Firing API with prompt: {prompt} and img: {b64_img}")
    # return None
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a computer vision assistant specialized in object detection and localization. "
                        "You are mounted on a 4-wheel mobile robot. Your primary purpose is to decode what the user "
                        "is trying to find and find the specific objects in its environment. "
                        "You can generate the commands 'ROTATE' and 'MOVE_FORWARD' to move the camera to find the object requested. "
                        "If the object is not found in scene 'ROTATE' by 30 degrees. If object is found in the scene move 'FORWARD' "
                        "till the distance to the object is 2.0 cm. Only provide the output in a JSON object with the following information: "
                        "'command' : 'FORWARD' or 'ROTATE', 'rotate_degree': rotation angle if 'command' is 'ROTATE', "
                        "'object' : object to find, 'in_scene': if object is found in scene then True or else False."
                    ),
                },
                {"role": "user", "content": [
                    {"type": "text", "text": prompt + "?"},
                    {"type": "image_url", "image_url": {
                        "url": b64_img
                    }}
                ]}
            ],
            response_format={"type": "json_object"}
        )

        response_content = response.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        print(f"Error during GPT object detection: {e}")
        return None

found_obj = False
latest_prompt = None
# rotating = False
count = -1
async def processWS():
    global last_saved_frame
    global latest_prompt
    # global rotating
    global count
    ssl_context = ssl._create_unverified_context()
    async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
        while True:
            try:
                data = await websocket.recv()
                event = json.loads(data)
                # print("received data from websocket", event["path"])
                if (event["path"] == "video-stream"):
                    if count >= 0:
                        count -= 1
                    print(f"received video frame, count = {count}")
                    last_saved_frame = event["message"]["dataUrl"]
                
                if (event["path"] == "transcription"):
                    latest_prompt = event["message"]["prompt"]
                    print(f"\n\nPrompt Recieved: {latest_prompt}.\nFiring OpenAI API for inference on latest saved frame.\n\n")
                    decode_img(last_saved_frame)
                    gpt_response = detect_object_with_gpt(last_saved_frame, latest_prompt)
                    print(gpt_response)

                # if (event["path"] == "robot-data"):
                #     print(event["message"])
                    # rotating = False
                
                if not latest_prompt:
                    print("Waiting for a command...")
                    continue
                
                if latest_prompt and count < 0:
                    decode_img(last_saved_frame)
                    gpt_response = detect_object_with_gpt(last_saved_frame, latest_prompt)
                    print(gpt_response)
                    command = gpt_response["command"]
                    in_scene = gpt_response["in_scene"]
                    rotate_degree = gpt_response.get("rotate_degree", 0)

                    print(f'Prompt: {latest_prompt}')
                    if command == "FORWARD" and in_scene:
                        # Logic to send to ESP32 through ESP-NOW to stop
                        print(f"Found object. Stopping.")
                        count = -1
                        # rotating = False
                        latest_prompt = None
                    
                    elif command == "ROTATE":
                        print(f"Rotating by {rotate_degree} degrees to search for the object.")
                        # rotating = True
                        count = 2 # wait for 3 frames before checking to allow for rotation delay
                        # Logic to send to ESP32 through ESP-NOW to rotate       
            
            except Exception as e:
                print(e)
                break

def decode_img(img_url):
    img_url = img_url.split(',')[-1]
    img_buf = base64.b64decode(img_url)
    nparr = np.frombuffer(img_buf, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("frame.png", frame)

# Run the async function
asyncio.run(processWS())
