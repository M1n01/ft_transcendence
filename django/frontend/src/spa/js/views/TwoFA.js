import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { TwoFaEvent } from '../../../accounts/js/two_fa.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Two-Factor Authentication');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/two-fa/');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(TwoFaEvent);
  };
  getState = () => {
    return null;
  };
}
