(async function() {
    const videoElement = document.getElementById('camera');
    let websocket;

    try {
        // Check if mediaDevices API is available
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('getUserMedia API is not supported in this browser. Please use a modern browser like Chrome, Firefox, or Edge.');
        }

        // Request access to the user's camera
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment" } 
        });

        // Set the video element's source to the camera stream
        videoElement.srcObject = stream;

        // Create a WebSocket connection to the server
        websocket = new WebSocket('wss://192.168.0.133:4000/video-stream');

        // Capture video frames and send them to the server
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = videoElement.width;
        canvas.height = videoElement.height;

        // Send video frames every 100ms
        setInterval(() => {
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            
            const dataUrl = canvas.toDataURL();
            // console.log(dataUrl);
            if (websocket.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify({dataUrl}));
                console.log('Sent a video frame to the server.');
            }
        }, 2000);

        websocket.onopen = () => console.log('WebSocket connection established.');
        websocket.onerror = (err) => console.error('WebSocket error: ', err);
        websocket.onclose = () => console.log('WebSocket connection closed.');

    } catch (err) {
        console.error('Error accessing camera: ', err);
        alert('Could not access the camera. ' + err.message + '\nPlease ensure your browser allows camera access and refresh the page.');
    }
})();