import { getCookie } from './cookie.js';

//const csrftoken = getCookie('csrftoken');

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

export async function fetchAsForm(url, form, current_uri) {
  console.log('fetchAsForm No.1');
  console.log('fetchAsForm No.1');
  console.log('fetchAsForm No.1');
  console.log('fetchAsForm No.2');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: form,
    });

    const result = await response.text();
    /*
    if (result) {
      navigateTo(current_uri);
      router();
    } else {
      console.error('Failure');
    }
      */

    return response;
  } catch (error) {
    console.error(error);
  }

  return '';
}

export default async function fetchData(url) {
  console.log('fetchData No.1');
  console.log('fetchData No.1');
  console.log('fetchData No.1');
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
