import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Admin');
  }

  async getHtml() {
    const uri = getUrlWithLang('/admin/login/?next=/');
    const data = await fetchData(uri);
    return data;
  }
  async executeScript() {
    //executeScriptTab("");
  }
}
