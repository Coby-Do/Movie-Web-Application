

// listen to a message from the content script
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        // if the message is finished
        // break the message into the title and the api key
        // send a post request to the server
        var title = request.message.split(",")[1];
        console.log("title: " + title);

        fetch(url + "api/watch_movie", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "access_token": apiKey,
                "movie_title": title
            }),
        })


    }
);

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


