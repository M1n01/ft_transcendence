import { fetchAsFormByGet, fetchAsForm } from '../../spa/js/utility/fetch.js';
import { updatePage } from '../../spa/js/routing/routing.js';
export const FriendEvent = new Event('FriendEvent');
document.addEventListener('FriendEvent', () => {
  //const params = new URLSearchParams(window.location.search);
  //console.log('query=' + params);
  document.getElementById('search-friend').addEventListener('submit', async function (event) {
    const search_word = document.getElementById('id_query').value;
    const query = search_word == '' ? '' : 'username=' + search_word;
    console.log('username=' + query);
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    console.log('formData=' + formData);
    console.table(formData);
    const response = await fetchAsFormByGet(form, formData, query);
    if (response.status != 200) {
      console.log('Error');
      return;
    }

    await updatePage(response);
    console.log('reload?');
    document.dispatchEvent(FriendEvent);

    /*
    const container = document.querySelector('.searched-user');
    console.log('container=' + container);

    if (container != null) {
      console.log('test No.1');
      container.addEventListener('click', (event) => {
        console.log('test No.2');
        if (event.target.classList.contains('friend-request')) {
          // クリックされた要素がボタンの場合
          console.log('ボタンがクリックされました');
        }
      });
    }
    */

    const requests = document.getElementsByClassName('friend-request');

    // 各ボタンにクリックイベントを追加
    for (let i = 0; i < requests.length; i++) {
      requests[i].addEventListener('submit', async (event) => {
        const parent = event.target.parentNode;
        const user_div = parent.querySelector('div');
        const username = user_div.textContent;

        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        formData.append('username', username);
        //const data = { "username": username };
        const response = await fetchAsForm(form, formData);
        if (response.status != 200) {
          console.log('Error');
          return;
        }

        console.log('parent:' + username);
        //fetchAsForm();
      });
    }

    //this.dispatchEvent(FriendEvent);
    //reload();
    //fetchData();
    //document.dispatchEvent(TournmentChartEvent);
  });

  /*
  const buttons = document.getElementsByClassName('friend-request');

  // 各ボタンにクリックイベントを追加
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function (event) {
      // クリックされたときの処理
      console.log('ボタンがクリックされました');
    });
  }
  */
});
