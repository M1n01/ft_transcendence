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
  getHtml = async () => {
    const uri = getUrlWithLang('friend/');
    const data = fetchData(uri);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(FriendEvent);
  };
  getState = () => {
    return null;
  };
}
