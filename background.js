chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var re = /yahoo\.com/;
    if (details.url.match(re)) {
      return {redirectUrl: chrome.extension.getURL("redirectInfo.html")};
    }
  },
  {
    urls: ["<all_urls>"],
    types: ['main_frame']
  },
  ["blocking"]
);
