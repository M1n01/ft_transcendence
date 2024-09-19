import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';
import { SignupEvent } from '../../../accounts/js/signup.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign up');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/signup');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(SignupEvent);
  };
  getState = () => {
    return null;
  };
}
