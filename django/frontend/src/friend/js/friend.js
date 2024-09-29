import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import { moveTo } from '../../spa/js/routing/routing.js';
import { reload } from '../../spa/js/utility/user.js';
import '../scss/friend.scss';

export const FriendEvent = new Event('FriendEvent');

const links = () => {
  const links = document.querySelector('#app').querySelectorAll('a');
  links.forEach((event) => {
    event.dataset.link = '';
  });
};

const friend_request_click = () => {
  const searched_user = document.getElementById('searched-user');
  if (searched_user == null) {
    return;
  }
  const friend_requests = searched_user.querySelectorAll('button');
  if (friend_requests.length == 0) {
    return;
  }
  friend_requests.forEach((event) => {
    event.addEventListener('click', (e) => {
      const button = e.target;
      const name_elements = button.getElementsByClassName('request-button-name');
      if (name_elements.length == 0) {
        return;
      }

      const username = name_elements[0].textContent;
      document.getElementById('modal-username').value = username;
      console.log('click No.8');
      const test_modal = document.getElementById('modal-username');
      document.getElementById('friend-user-name-head').textContent = username;
      document.getElementById('friend-user-icon-head').src = '';
      //const
      console.log('click No.9 modal:' + test_modal);
    });
  });
};

document.addEventListener('FriendEvent', () => {
  console.log('friend top load');
  const friend_top = () => {
    const input_user = document.getElementById('search-friend');
    console.log('input_user:' + input_user);
    if (input_user == null) {
      return;
    }
    document.getElementById('search-friend').addEventListener('submit', async function (event) {
      console.log('search test No.1');
      const search_word = document.getElementById('id_query').value;
      const query = search_word == '' ? '' : '?username=' + search_word;
      event.preventDefault();
      const form = event.target;
      console.log('query:' + query);
      console.log('action:' + form.action);
      console.log('search test No.2');
      moveTo('/friend', '/searched', query);
      console.log('search test No.3');
      return;
    });
  };

  const friend_request = () => {
    links();
    friend_request_click();

    const requests_form = document.getElementById('friend-request');
    console.log('requests_form:' + requests_form);
    if (requests_form == null) {
      return;
    }
    requests_form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      if (response.status != 200) {
        console.error('Error');
        return;
      }
      document.getElementById('close-register-modal').click();
      await reload();
    });
  };

  friend_request();
  friend_top();
});
