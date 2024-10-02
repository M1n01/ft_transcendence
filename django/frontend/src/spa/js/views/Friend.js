import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { FriendEvent } from '../../../friend/js/friend.js';
//import { LoginEvent } from '../../../accounts/js/login.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Friend');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    if (rest === '') {
      const uri = getUrlWithLang('friend/');
      const data = fetchData(uri + rest + params);
      return data;
    } else if (rest === '/requests') {
      const uri = getUrlWithLang('friend/requests/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/friends') {
      const uri = getUrlWithLang('friend/friends/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/blocks') {
      const uri = getUrlWithLang('friend/blocks/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/searched') {
      const uri = getUrlWithLang('friend/search');
      const data = fetchData(uri + params);
      return data;
    }

    return '';
  };
  executeScript = () => {
    document.dispatchEvent(FriendEvent);
  };
  getState = () => {
    return null;
  };
}
