import { getCookie } from './cookie.js';

const csrftoken = getCookie('csrftoken');

//If you activate CSRF_USE_SESSIONS or CSRF_COOKIE_HTTPONLY
//const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

function makeRequest(method, url) {
  return fetch(url, {
    method: method,
    headers: { SPA: 'spa' },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(' Fetch() Error');
    }
    return response.text();
  });
}

function sendRequestAsForm(method, url) {
  return fetch(url, {
    method: method,
    headers: { 'X-CSRFToken': csrftoken, SPA: 'spa' },
    mode: 'same-origin',
    body: {
      spa: 'enable',
    },
  }).then((response) => {
    console.error('Fetch error status:' + response.status);
    if (300 <= response.status && response.status < 400) {
      console.log(response.headers);
    }

    if (!response.ok) {
      throw new Error(' Fetch() Error');
    }

    return response.text();
  });
}

export default async function fetchData(url) {
  try {
    console.log('No.2 fetch url:' + url);
    //url = "http://localhost:8000/ja/pong/script";
    const response = await makeRequest('GET', url);
    //const response = await sendRequestAsForm("POST", url);
    return response;
  } catch (error) {
    console.error(error);
  }
  return '';
}
