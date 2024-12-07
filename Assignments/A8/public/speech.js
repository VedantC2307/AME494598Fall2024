(async function() {
    var r = document.getElementById("result");
    if ("webkitSpeechRecognition" in window) {
        var recognizer = new webkitSpeechRecognition();
        recognizer.continuous = true;
        recognizer.interimResults = false;
        recognizer.lang = "en-US";
        recognizer.start();
        
        var keyword = "robot";
        var finalTranscripts = "";
        var myTimer = undefined;

        let websocket = new WebSocket('wss://192.168.0.133:4000/transcription');

        recognizer.onresult = function(event){
            for(var i = event.resultIndex; i < event.results.length; i++){
                var transcript = event.results[i][0].transcript;
                transcript.replace("\n", "<br>");
                if(event.results[i].isFinal && (transcript.toLowerCase().includes(keyword) || finalTranscripts.toLowerCase().includes(keyword))){
                    finalTranscripts += transcript;
                    if (myTimer) {
                        clearTimeout(myTimer)
                    }
                    myTimer = setTimeout(() => {
                        split_arr = finalTranscripts.split(" ");
                        prompt_arr = null;
                        key_idx = split_arr.findIndex((word) => word.toLowerCase() == keyword);
                        prompt_arr = split_arr.splice(key_idx + 1);

                        let prompt = prompt_arr.join(" ");
                        if (websocket.readyState === WebSocket.OPEN) {
                            websocket.send(JSON.stringify({prompt}));
                            console.log('Sent a transcribed prompt to the server.');
                        }
                        finalTranscripts = "";
                        r.innerHTML = finalTranscripts;
                    }, 2500);

                }
                r.innerHTML = finalTranscripts;
            }

        };

        websocket.onopen = () => console.log('WebSocket connection established.');
        websocket.onerror = (err) => console.error('WebSocket error: ', err);
        websocket.onclose = () => console.log('WebSocket connection closed.');
            
        recognizer.onerror = function(event){
        
        };

        recognizer.onend = () => {
            setTimeout(() => {
                recognizer.start();
            }, 10);
        }
    }
    else {
        r.innerHTML = "Your browser does not support that.";
    }


}) ()
