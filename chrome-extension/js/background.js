var fixedWhitelist = {};
var userWhitelist = {};

chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    var domain = stripDomain(details.url);
    if (fixedWhitelist[domain] || userWhitelist[domain]) {
      return;
    }
    var corrections = callout(domain);
    if (corrections) {
      // TODO consider persisting typo correction mapping
      return {redirectUrl: 'http://' + corrections + '.com'};
    } else {
      updateUserWhitelist(domain);
    }
  },
  {
    urls: ["<all_urls>"],
    types: ['main_frame']
  },
  ["blocking"]
);

function updateUserWhitelist(domain) {
	if (fixedWhitelist[domain] || userWhitelist[domain]) {
    return;
  }
  userWhitelist[domain] = true;
  saveUserWhitelist();
}

function saveUserWhitelist() {
  localStorage['user_whitelist'] = JSON.stringify(userWhitelist);
}

function loadFixedWhitelist() {
  fixedWhitelist['chrome-extension:'] = true;
  readTextFile(chrome.extension.getURL('resources/fixed_whitelist.txt'));
}

function loadUserWhitelist() {
  if (!localStorage['user_whitelist']) {
     userWhitelist = {};
  } else {
    userWhitelist = JSON.parse(localStorage['user_whitelist']);
    console.log(userWhitelist);
  }
}

function readTextFile(file) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", file, false);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var whitelist_domains = xhr.responseText.split(',');
      for (var idx in whitelist_domains) {
        fixedWhitelist[whitelist_domains[idx]] = true;
      }
    }
  }
  xhr.send(null);
}

loadFixedWhitelist();
loadUserWhitelist();

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
