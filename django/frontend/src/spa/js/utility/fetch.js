function makeRequest(method, url) {
  try {
    return fetch(url, {
      method: method,
      headers: { SPA: 'spa' },
      redirect: 'follow',
    }).then((response) => {
      if (!response.ok) {
        throw new Error('Fetch() Error');
      }
      if (response.status >= 400) {
        throw new Error(' Status Error:' + response.status);
      }
      return response;
    });
  } catch (error) {
    throw new Error('Fetch() Error:' + error);
  }
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
    const res = { error: true, status: 500 };
    return res;
  }
}
export async function fetchAsFormByGet(form, FormData, query_word) {
  //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const query = query_word == '' ? '' : '?' + query_word;
  const uri = form.action + query;
  try {
    const res = await fetch(uri, {
      method: 'GET',
      mode: 'same-origin',
    });
    return res;
  } catch (error) {
    console.error('Fetch Error:' + error.message);
    const res = { error: true, status: 500 };
    return res;
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
