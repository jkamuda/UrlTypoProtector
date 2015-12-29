chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var domain = stripDomain(details.url);
    if (isGoogle(domain)) {
      return;
    }
    var corrections = callout(domain);
    if (corrections) {
      return {redirectUrl: 'http://' + corrections + '.com'};
    }
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
  client.send(null);
  if (client.response) {
    return JSON.parse(client.response).correction;
  } else {
    return '';
  }
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
  return domain.match(googleRe) != null || domain === 'chrome-extension:';
};
