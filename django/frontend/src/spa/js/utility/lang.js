import { navigateTo, router } from '../routing/routing.js';

export async function changingLanguage(url, form, current_uri) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: form,
    });

    const result = await response.text();
    if (result) {
      navigateTo(current_uri);
      router();
    } else {
      console.error('Failure');
    }

    return response;
  } catch (error) {
    console.error(error);
  }

  return '';
}
