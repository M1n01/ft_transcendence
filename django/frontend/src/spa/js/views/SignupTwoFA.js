import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';
import { SignupTwoFAEvent } from '../../../accounts/js/signup_two_fa.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign up');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('accounts/signup-two-fa');
    const data = fetchData(uri);
    return data;
  };

  executeScript = () => {
    document.dispatchEvent(SignupTwoFAEvent);
  };
  getState = () => {
    return null;
  };
}
