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

export async function fetchAsForm(form, FormData) {
  console.log('fetchAsForm No.1');
  console.log('fetchAsForm No.2 + form:' + form.toString());
  console.log('fetchAsForm No.3 + form:' + form[0]);
  console.log('fetchAsForm No.1');

  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  try{
    const res = await fetch(form.action, {
      method: "POST",
      headers: { 'X-CSRFToken': csrftoken
      },
      mode: 'same-origin',
      body: FormData
    })
    .then(response => {
      console.log("then response");

      //const result = await response.text();
      if (!response.ok) {
        console.error("Fetch Error");
        return "";
      }
      return response;
    })
    .then((data) => {
      return data.text();
    })
    .catch((error) => {
          return "";
    })
      return (res);
    }catch(error){
      console.error("Fetch Error");
      return "";
      //console.log(error);
    }
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
