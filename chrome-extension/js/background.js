var fixed_whitelist = {};
var whitelist = {};

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

function loadFixedWhitelist() {
  console.log('loading fixed whitelist...');
  var whitelist = chrome.extension.getURL('resources/fixed_whitelist.txt');
  readTextFile(whitelist);
}

function readTextFile(file) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", file, false);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var whitelist_domains = xhr.responseText.split(',');
      for (var idx in whitelist_domains) {
        fixed_whitelist[whitelist_domains[idx]] = true;
      }
    }
  }
  xhr.send(null);
}

loadFixedWhitelist();

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
