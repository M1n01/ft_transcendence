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
    console.log('rest:' + rest);
    console.log('location:' + window.location.pathname);
    if (rest === '') {
      console.log('normal');
      const uri = getUrlWithLang('friend/');
      const data = fetchData(uri + rest + params);
      return data;
    } else if (rest === '/requests') {
      console.log('requests');
      const uri = getUrlWithLang('friend/requests/');
      console.log('searched uri:' + uri);
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/friends') {
      console.log('friends');
      console.log('params:' + params);
      const uri = getUrlWithLang('friend/friends/');
      console.log('uri:' + uri + params);
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/searched') {
      console.log('searched');
      console.log('params:' + params);
      const uri = getUrlWithLang('friend/search');
      console.log('uri:' + uri + params);
      const data = fetchData(uri + params);
      return data;
    }

    return '';
    //return data;
  };
  executeScript = () => {
    document.dispatchEvent(FriendEvent);
  };
  getState = () => {
    return null;
  };
}
