//import { updatePage } from './routing/routing.js';
function displayInstruction(id) {
  document.getElementById('instruction').hidden = true;
  document.getElementById('instruction-processing').hidden = true;
  document.getElementById('instruction-error').hidden = true;
  document.getElementById(id).hidden = false;
}

document.getElementById('openDialog').addEventListener('click', function () {
  document.getElementById('myDialog').showModal();
});

document.getElementById('closeDialog').addEventListener('click', async function () {
  const ft_oauth_url = document.getElementById('ft-oauth-url').href;
  displayInstruction('instruction-processing');

  try {
    const url = window.location.protocol + '//' + window.location.host + '/accounts/oauth-login/';
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: JSON.stringify({ url: ft_oauth_url }),
      credentials: 'include',
    });
    if (res.status >= 400) {
      displayInstruction('instruction-error');
      document.getElementById('instruction').style.color = 'red';
      return '';
    }
    document.getElementById('myDialog').close();
    document.getElementById('success-login').click();
  } catch (error) {
    displayInstruction('instruction-error');
    console.error('Fetch Error:' + error);
    return '';
  }
});
