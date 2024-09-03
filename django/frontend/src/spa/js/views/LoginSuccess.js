import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Log in Success');
  }

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
