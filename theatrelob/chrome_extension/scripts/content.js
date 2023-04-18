// attempt to get the current time of the video repeatedly
// until it is available

let video;
let apiKey, url;

var interval = setInterval(function() {
    video = document.querySelector('video');
    if (video) {
        clearInterval(interval);
        trackProgress();
    }
}, 100);

// declare a function to start tracking the progress of the video
function trackProgress() {
    video.addEventListener('timeupdate', function() {
        console.log("video.currentTime: " + video.currentTime);
        if (video.currentTime >= video.duration * 0.85) {
            console.log("Finished Movie");  
            // send a message to the background script to send a rest call
            // to the server
            var title = document.querySelector('[data-uia="video-title"]').innerText;
            console.log("title: " + title);
            chrome.runtime.sendMessage({message: "finished,"+title}, function(response) {
                console.log(response);  
            });
            // get the movie title from the page, the data-uia is video-title
           
            // do a simple post request to the server
            
    
            // remove the event listener
            video.removeEventListener('timeupdate', arguments.callee);

        }
    });
}





