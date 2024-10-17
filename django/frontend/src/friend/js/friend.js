import { submitForm } from '../../spa/js/utility/form.js';
import { moveTo } from '../../spa/js/routing/routing.js';
import { reload } from '../../spa/js/utility/user.js';
import { sendWebSocket } from '../../spa/js/ws/socket.js';
import '../scss/friend.scss';

export const FriendEvent = new Event('FriendEvent');

export const setUserActive = async (list) => {
  const user_id_list = document.querySelectorAll('.friend-user-id-hidden');

  if (list == '') {
    return;
  }
  const json = JSON.parse(list);

  user_id_list.forEach((element) => {
    const id = element.textContent;
    const card = element.parentElement.parentElement;
    const active_true = card.querySelector('.login-active-true');
    const active_false = card.querySelector('.login-active-false');
    if (active_true && active_false && id in json) {
      const active = json[id];
      if (active === 'True') {
        active_true.hidden = false;
        active_false.hidden = true;
      } else if (active === 'False') {
        active_true.hidden = true;
        active_false.hidden = false;
      }
    }
  });
};

function intervalFunc() {
  const user_id_list = document.querySelectorAll('.friend-user-id-hidden');
  let id_list = '';
  if (user_id_list.length == 0) {
    return;
  }
  user_id_list.forEach((element) => {
    const id = element.textContent;
    id_list += id + '@';
  });
  if (id_list !== '') {
    id_list = id_list.substring(0, id_list.length - 1);
    const message = {
      type: 'get',
      message: 'active_list',
      content: id_list,
    };
    sendWebSocket(message);
  }
}
export let CheckFriendInterval = setInterval(intervalFunc, 5000);

const accept_friend_request = () => {
  const accepts = document.querySelector('#app').querySelectorAll('.pre-accept-friend');
  if (accepts.length == 0) {
    return;
  }

  accepts.forEach((button) => {
    button.addEventListener('click', () => {
      const error = document.getElementById('request-accept-error');
      error.hidden = true;

      const name = button.getAttribute('data-name');
      const id = button.getAttribute('data-id');
      const img_url = button.getAttribute('data-img');

      const username = document.getElementById('request-accept-user-name');
      const input_id = document.getElementById('request-accept-input-user-id');
      const avatar = document.getElementById('request-accept-user-avatar');

      username.textContent = name;
      input_id.value = id;
      avatar.src = img_url;

      const form = document.getElementById('accept-friend-request-form');
      form.addEventListener('submit', async (event) => {
        const response = await submitForm(event);
        if (response.error) {
          error.hidden = false;
          return;
        }
        document.getElementById('close-accept-request-modal').click();
        reload();
      });
    });
  });
};

const block_friend_request = () => {
  const blocks = document.querySelector('#app').querySelectorAll('.pre-block-friend');
  if (blocks.length == 0) {
    return;
  }

  blocks.forEach((button) => {
    button.addEventListener('click', () => {
      const error = document.getElementById('request-block-error');
      error.hidden = true;

      //const id = button.value;
      //const name = button.name;
      const id = button.getAttribute('data-id');
      const name = button.getAttribute('data-name');
      const img_url = button.getAttribute('data-img');

      const username = document.getElementById('request-block-user-name');
      username.textContent = name;
      const input_id = document.getElementById('request-block-input-user-id');
      input_id.value = id;
      const avatar = document.getElementById('request-block-user-avatar');
      avatar.src = img_url;

      const form = document.getElementById('reject-friend-request-form');
      form.addEventListener('submit', async (event) => {
        const response = await submitForm(event);
        /*
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const response = await fetchAsForm(form, formData);
        */
        if (response.error) {
          error.hidden = false;
          return;
        }
        document.getElementById('close-block-request-modal').click();
        reload();
      });
    });
  });
};

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

      //const username = name_elements[0].textContent;
      const user_id = name_elements[0].getAttribute('data-id');
      const username = name_elements[0].getAttribute('data-name');
      const img_url = name_elements[0].getAttribute('data-url');
      //document.getElementById('modal-username').value = username;
      document.getElementById('modal-userid').value = user_id;
      document.getElementById('friend-user-name-head').textContent = username;
      //document.getElementById('friend-user-id-head').textContent = user_id;
      document.getElementById('friend-user-icon-head').src = img_url;
    });
  });
};

document.addEventListener('FriendEvent', () => {
  const friend_top = () => {
    const input_user = document.getElementById('search-friend');
    if (input_user == null) {
      return;
    }
    document.getElementById('search-friend').addEventListener('submit', async function (event) {
      const search_word = document.getElementById('id_query').value;
      const query = search_word == '' ? '' : '?username=' + search_word;
      event.preventDefault();
      //const form = event.target;
      moveTo('/friend', '/searched', query);
      return;
    });
  };

  const friend_request = () => {
    links();
    friend_request_click();

    const requests_form = document.getElementById('friend-request');
    if (requests_form == null) {
      return;
    }
    const error_message = document.getElementById('friend-request-send-error');

    requests_form.addEventListener('submit', async (event) => {
      error_message.hidden = true;
      const response = await submitForm(event);
      if (response.status != 200) {
        error_message.hidden = false;
        console.error('Error');
        return;
      }
      document.getElementById('close-register-modal').click();
      await reload();
    });
  };

  const display_friend_message = () => {
    const messages = document.querySelector('#app').querySelectorAll('.message-friend-card');
    if (messages.length == 0) {
      return;
    }

    messages.forEach((button) => {
      button.addEventListener('click', () => {
        const name = button.getAttribute('data-name');
        //const id = button.getAttribute('data-id');
        const img_url = button.getAttribute('data-img');
        const message = button.getAttribute('data-message');

        const username = document.getElementById('request-message-user-name');
        //const input_id = document.getElementById('request-accept-input-user-id');
        const avatar = document.getElementById('request-message-user-avatar');
        const message_div = document.getElementById('request-message-user-message');

        username.textContent = name;
        //input_id.value = id;
        avatar.src = img_url;
        message_div.textContent = message;
      });
    });
  };

  friend_request();
  friend_top();
  block_friend_request();
  accept_friend_request();
  display_friend_message();

  intervalFunc();
  CheckFriendInterval;
});
