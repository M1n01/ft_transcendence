function getUserLanguage() {
  return window.navigator.languages && window.navigator.languages[0]
    ? window.navigator.language
    : sessionStorage.getItem('userLanguage');
}

export function getUrl(path) {
  const http = window.location.protocol;
  const domain = window.location.host;
  return http + '//' + domain + '/' + path;
}

export function getUrlWithLang(path) {
  const http = window.location.protocol;
  const domain = window.location.host;
  let lang = getUserLanguage();
  if (!lang) {
    lang = '';
  }
  return http + '//' + domain + '/' + path;
}
