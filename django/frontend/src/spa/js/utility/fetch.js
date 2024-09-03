function makeRequest(method, url) {
  return fetch(url, {
    method: method,
    headers: { SPA: 'spa' },
    redirect: 'follow',
  }).then((response) => {
    if (!response.ok) {
      throw new Error(' Fetch() Error');
    }
    return response;
  });
}

export async function fetchAsForm(form, FormData) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const res = await fetch(form.action, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: FormData,
    });
    return res;
  } catch (error) {
    console.error('Fetch Error:' + error.message);
    return '';
  }
}

export default async function fetchData(url) {
  const response = await makeRequest('GET', url);
  return response.text();
}
export async function fetchJsonData(url) {
  console.log('fetchJsonData No.1');
  const response = await makeRequest('GET', url);
  return response.json();
  //return response.json();
}
