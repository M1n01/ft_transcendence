import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { TwoFaEvent } from '../../../accounts/js/two_fa.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Two-Factor Authentication');
  }

  async getHtml() {
    console.log('2FA');
    const uri = getUrlWithLang('accounts/two-fa/');
    const data = fetchData(uri);
    return data;
  }
  async executeScript() {
    document.dispatchEvent(TwoFaEvent);
  }
}
