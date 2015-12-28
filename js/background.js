chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var domain = stripDomain(details.url);
    if (isGoogle(domain)) {
      return;
    }
    //console.log(domain);
    if (!callout(domain)) {
      return {redirectUrl: chrome.extension.getURL("html/redirectInfo.html")};
    }
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

function callout(domain) {
  var url = "http://localhost:8080/validate/" + domain;
  var client = new XMLHttpRequest();
  client.open("GET", url, false);
  client.setRequestHeader("Content-Type", "text/plain");
  client.send();
  console.log(client.status);
  console.log(client);
  return client.status === 200;
}

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
