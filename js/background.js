chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var domain = stripDomain(details.url);
    if (isGoogle(domain)) {
      return;
    }
    console.log(domain);
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
  return fullUrl
    .replace('http://', '')
    .replace('https://', '')
    .replace('www.', '')
    .split(/[/?#]/)[0];
};

var googleRe = /google\./;
function isGoogle(domain) {
  return domain.match(googleRe) != null;
};
