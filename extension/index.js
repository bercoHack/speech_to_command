//View
var microphoneButton = document.getElementById("start");
var stopRecordingButton = document.getElementById("stop");

//Listeners

//Listen to start recording button
microphoneButton.onclick = startAudioRecording;

//Listen to stop recording button
stopRecordingButton.onclick = stopAudioRecording;


/** Starts the audio recording*/
function startAudioRecording() {

    console.log("Recording Audio...");

    //start recording using the audio recording API
    audioRecorder.start()
        .then(() => { //on success
        })
        .catch(error => { //on error
            //No Browser Support Error
            if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {
                console.log("To record audio, use browsers like Chrome and Firefox.");
                displayBrowserNotSupportedOverlay();
            }
        });
}
/** Stop the currently started audio recording & sends it
 */
function stopAudioRecording() {

    console.log("Stopping Audio Recording...");

    //stop the recording using the audio recording API
    audioRecorder.stop()
        .then(audioAsblob => {
            //Play recorder audio
            alert(audioAsblob);
            
        })
        .catch(error => {
            //Error handling structure
            switch (error.name) {
                case 'InvalidStateError': //error from the MediaRecorder.stop
                    console.log("An InvalidStateError has occured.");
                    break;
                default:
                    console.log("An error occured with the error name " + error.name);
            };
        });
}
