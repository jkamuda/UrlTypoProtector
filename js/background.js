chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    console.log(details);
    var domain = stripDomain(details.url);
    /*if (details.url.match(re)) {
      return {redirectUrl: chrome.extension.getURL("html/redirectInfo.html")};
    }*/
  },
  {
    urls: ["<all_urls>"],
    types: ['main_frame']
  },
  ["blocking"]
);

function stripDomain(fullUrl) {
  //console.log(fullUrl);
  return fullUrl
    .replace('http://', '')
    .replace('https://', '')
    .replace('www.', '')
    .split(/[/?#]/)[0];
};
