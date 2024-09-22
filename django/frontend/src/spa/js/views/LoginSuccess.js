import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Log in Success');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async () => {
    const uri = getUrlWithLang('accounts/signup-two-fa/');
    const data = fetchData(uri);
    return data;
  };
  executeScript = () => {
    //executeScriptTab('');
  };
  getState = () => {
    return null;
  };
}
