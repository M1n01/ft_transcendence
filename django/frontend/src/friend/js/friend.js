import { fetchAsFormByGet, fetchAsForm } from '../../spa/js/utility/fetch.js';
import { updatePage } from '../../spa/js/routing/routing.js';
export const FriendEvent = new Event('FriendEvent');
document.addEventListener('FriendEvent', () => {
  document.getElementById('search-friend').addEventListener('submit', async function (event) {
    const search_word = document.getElementById('id_query').value;
    const query = search_word == '' ? '' : 'username=' + search_word;
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    console.table(formData);
    const response = await fetchAsFormByGet(form, formData, query);
    if (response.status != 200) {
      console.Error('Error');
      return;
    }

    await updatePage(response);
    document.dispatchEvent(FriendEvent);

    const requests = document.getElementsByClassName('friend-request');

    for (let i = 0; i < requests.length; i++) {
      requests[i].addEventListener('submit', async (event) => {
        const parent = event.target.parentNode;
        const user_div = parent.querySelector('div');
        const username = user_div.textContent;

        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        formData.append('username', username);
        const response = await fetchAsForm(form, formData);
        if (response.status != 200) {
          console.error('Error');
          return;
        }
      });
    }
  });
});
