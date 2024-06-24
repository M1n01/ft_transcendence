//const i18n = require("i18n");
//import { getUserLanguage } from "../utility/lang.js";

function getUserLanguage() {
  console.log('lang No.1 naviagtor=' + window.navigator.languages);
  console.log('lang No.2 session =' + sessionStorage.getItem('userLanguage'));
  //console.log("lang No.3 session =" + i18n.getUILanguage());
  console.log('lang No.4  error=');
  //const browserLang =
  //(window.navigator.languages && window.navigator.languages[0]) ||
  //window.navigator.language;
  //document.getElementById("browser-language").textContent =
  //browserLang === "ja" ? "ja" : "En";
  return window.navigator.languages && window.navigator.languages[0]
    ? window.navigator.language
    : sessionStorage.getItem('userLanguage');
}

export function getUrl(path) {
  console.log('getUrl No.1');

  const http = window.location.protocol;
  const domain = window.location.host;
  //const lang = Headers.get("Content-Language");
  return http + '//' + domain + '/' + path;
}

export function getUrlWithLang(path) {
  console.log('getUrlWithLang No.1');
  //const myHeaders = new Headers();

  const http = window.location.protocol;
  const domain = window.location.host;
  //let lang = myHeaders.get("Content-Language");
  let lang = getUserLanguage();
  console.log('getUrlWithLang No.2 lang=' + lang);
  if (!lang) {
    lang = '';
  }
  console.log('No.2 lang=' + lang);
  return http + '//' + domain + '/' + path;
  return http + '//' + domain + '/' + lang + '/' + path;
}
