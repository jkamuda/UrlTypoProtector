chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var domain = stripDomain(details.url);
    if (isGoogle(domain) || whitelist[domain]) {
      return;
    }
    var corrections = callout(domain);
    if (corrections) {
      whitelist[corrections] = true;
      return {redirectUrl: 'http://' + corrections + '.com'};
    } else {
      whitelist[domain] = true;
    }
  },
  {
    urls: ["<all_urls>"],
    types: ['main_frame']
  },
  ["blocking"]
);

var whitelist = {};

function callout(domain) {
  var url = "http://localhost:8080/v1/domain/" + domain;
  var client = new XMLHttpRequest();
  client.open("GET", url, false);
  client.setRequestHeader("Content-Type", "text/plain");
  client.send(null);
  if (client.response) {
    return JSON.parse(client.response).intended;
  } else {
    return '';
  }
}

function stripDomain(fullUrl) {
  return fullUrl
    .replace('http://', '')
    .replace('https://', '')
    .replace('www.', '')
    .split(/[/?#]/)[0]
    .replace('.com', '');
};

var googleRe = /google\./;
function isGoogle(domain) {
  return domain.match(googleRe) != null || domain === 'chrome-extension:';
};
