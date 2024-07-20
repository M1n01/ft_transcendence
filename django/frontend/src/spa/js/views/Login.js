import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';
import { LoginEvent } from '../../../accounts/js/login.js';

const myCustomEvent = new Event('myCustomEvent');
function myFunction() {
  console.log('Function executed');
  document.dispatchEvent(myCustomEvent);
}

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Log in');
  }

  async getHtml() {
    const uri = getUrlWithLang('accounts/login');
    const data = fetchData(uri);
    return data;
  }
  async executeScript() {
    document.dispatchEvent(LoginEvent);
  }
}
