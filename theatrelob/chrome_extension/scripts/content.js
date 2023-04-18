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
            // make an API call to the server
            // to send the video id and the current time


            // get the movie title from the page, the data-uia is video-title
            var title = document.querySelector('[data-uia="video-title"]').innerText;
            console.log("title: " + title);
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url + "/api/watch_movie", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({
                "apiKey": apiKey,
                "title": title,
            }));
            // remove the event listener
            video.removeEventListener('timeupdate', arguments.callee);

        }
    });
}

chrome.storage.sync.get(['apiKey'], function(result) {
    console.log('Value currently is ' + result.apiKey);
    if(result.apiKey != undefined)
        apiKey = result.apiKey;
    
}
);

chrome.storage.sync.get(['url'], function(result) {
    console.log('Value currently is ' + result.url);
    if(result.url != undefined)
        url = result.url;
}
);




