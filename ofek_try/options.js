let button = document.getElementById('requestPermission');

button.onclick = ()=>{
    console.log('ya');
    navigator.getUserMedia = navigator.getUserMedia ||
                    navigator.webkitGetUserMedia ||
                    navigator.mozGetUserMedia;

    if (navigator.getUserMedia) {
    navigator.getUserMedia({ audio: true, video: false },
        (stream) => {
            sessionStorage.setItem('st',stream);///נסיון לשלוח את השידור לסקריפט השני
            console.log('success');
        },
        (err) => {
            console.error(`The following error occurred: ${err.name}`);
        }
    );
    } else {
        console.log("getUserMedia not supported");
    }   
};

