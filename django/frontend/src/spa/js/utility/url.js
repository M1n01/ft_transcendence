import Cookies from 'js-cookie';

export function getUrl(path) {
  const http = window.location.protocol;
  const domain = window.location.host;
  return http + '//' + domain + '/' + path;
}

export function getUrlWithLang(path) {
  const http = window.location.protocol;
  const domain = window.location.host;
  let lang = Cookies.get('django_language');
  if (!(lang == 'ja' || lang == 'en' || lang == 'fr')) {
    lang = 'ja';
  }
  return http + '//' + domain + '/' + lang + '/' + path;
}
