


// handle the click event of the button
document.getElementById("send").addEventListener("click", function() {
    // send a message to the active tab
    // get the text from the input field
    var text = document.getElementById("url").value;
    var apiKey = document.getElementById("apiKey").value;
    
    console.log("apiKey: " + apiKey);

    chrome.storage.sync.set({'apiKey': apiKey}, function() {
        console.log('Value is set to ' + apiKey);
    }
    );
    
    chrome.storage.sync.set({'url': text}, function() {
        console.log('Value is set to ' + text);
    }
    );
});


chrome.storage.sync.get(['apiKey'], function(result) {
    console.log('Value currently is ' + result.apiKey);
    if(result.apiKey != undefined)
        document.getElementById("apiKey").value = result.apiKey;
    
}
);

chrome.storage.sync.get(['url'], function(result) {
    console.log('Value currently is ' + result.url);
    if(result.url != undefined)
        document.getElementById("url").value = result.url;
}
);
