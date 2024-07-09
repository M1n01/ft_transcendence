document.getElementById('openDialog').addEventListener('click', function () {
  document.getElementById('myDialog').showModal();
});

document.getElementById('closeDialog').addEventListener('click', async function () {
  document.getElementById('myDialog').close();
  const ft_oauth_url = document.getElementById('ft-oauth-url').href;

  try {
    const url = window.location.protocol + '//' + window.location.host + '/accounts/oauth-login/';
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const res = fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: JSON.stringify({ url: ft_oauth_url }),
      credentials: 'include',
    })
      .then((response) => {
        if (!response.ok) {
          console.error('Fetch Error');
          return '';
        }
        return response.json();
      })
      .then((data) => {
        return data;
      })
      .catch((error) => {
        console.error(error);
        return '';
      });
    return res;
  } catch (error) {
    console.error('Fetch Error:' + error);
    return '';
  }
});
