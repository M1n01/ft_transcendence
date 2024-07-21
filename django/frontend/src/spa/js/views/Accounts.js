import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Accounts');
  }

  async getHtml() {
    const uri = getUrlWithLang('accounts/');
    const data = await fetchData(uri);
    return data;
  }
  async executeScript() {
    //executeScriptTab("");
  }
}
