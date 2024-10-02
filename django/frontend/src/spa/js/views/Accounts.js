import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { fetchJsonData } from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Accounts');
  }
  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };

  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
