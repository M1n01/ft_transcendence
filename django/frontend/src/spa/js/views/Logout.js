import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Log out');
  }
  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };

  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/logout');
    const data = fetchData(uri + rest + params);
    document.querySelector('#nav').innerHTML = '<div></div>';
    return data;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
