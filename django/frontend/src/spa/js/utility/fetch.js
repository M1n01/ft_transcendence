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
export async function fetchAsFormByGet(form, FormData, query_word) {
  //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const query = query_word == '' ? '' : '?' + query_word;
  console.log('fetch query=' + query);
  //console.log('url=' + form.action + query);
  //console.log('url=' + form.action[form.action.length - 1]);
  //const len = form.action.length - 1;
  const uri = form.action + query;
  console.log('fetch uri=' + uri);
  //console.log('url=' + form.action[length(form.action)]);
  try {
    const res = await fetch(uri, {
      method: 'GET',
      //headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      //body: FormData,
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
  const response = await makeRequest('GET', url);
  return response.json();
}
