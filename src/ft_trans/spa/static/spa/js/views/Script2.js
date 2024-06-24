import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Script2');
  }

  async getHtml() {
    const uri = getUrlWithLang('pong/script2');
    const data = await fetchData(uri);
    console.log('script2:' + uri);
    console.log('data:' + data);
    return data;
  }

  async executeScript() {
    //return '';
    executeScriptTab('');
  }
}
