import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';
import { LoginEvent } from '../../../accounts/js/login.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Log in');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/login');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(LoginEvent);
  };
  getState = () => {
    return null;
  };
}
