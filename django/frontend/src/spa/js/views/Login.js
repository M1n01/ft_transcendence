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

  async getHtml() {
    console.log('Login Test');
    const uri = getUrlWithLang('accounts/login');
    const data = fetchData(uri);
    return data;
  }
  async executeScript() {
    document.dispatchEvent(LoginEvent);
  }
}
