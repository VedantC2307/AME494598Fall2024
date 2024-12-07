import cv2
import numpy as np
import websockets
import asyncio
import ssl

async def process_video_frame():
    uri = 'wss://192.168.0.55:4000/video-stream'  # Use the server IP address
    ssl_context = ssl._create_unverified_context()  # Disable SSL verification for testing

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        try:
            while True:
                # Attempt to receive frame data
                frame_data = await websocket.recv()
                print('Received a video frame in Python script')  # Debug log

                # Convert the binary data to a numpy array and decode it
                nparr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if frame is not None:
                    print('Decoded the video frame successfully')  # Debug log

                    # Perform computer vision processing (e.g., edge detection)
                    # edges = cv2.Canny(frame, 100, 200)

                    # Display the result
                    cv2.imshow('Edge Detection', frame)

                    # Exit on 'q' key press
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print('Failed to decode the video frame')  # Debug log
        except asyncio.TimeoutError:
            print('No frame data received within the timeout period.')
            
    cv2.destroyAllWindows()

# Run the async function
asyncio.run(process_video_frame())
