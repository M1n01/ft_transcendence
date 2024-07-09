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
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const res = await fetch(form.action, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: FormData,
    })
      .then((response) => {
        //const result = await response.text();
        if (!response.ok) {
          console.error('Fetch Error');
          return '';
        }
        return response;
      })
      .then((data) => {
        return data.text();
      })
      .catch((error) => {
        console.error('Fetch Error:' + error);
        return '';
      });
    return res;
  } catch (error) {
    console.error('Fetch Error:' + error);
    return '';
  }
}

export default async function fetchData(url) {
  try {
    const response = await makeRequest('GET', url);
    return response;
  } catch (error) {
    console.error(error);
  }
  return '';
}
