import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Script');
  }

  async getHtml() {
    console.log('script getHtml()');
    const uri = getUrlWithLang('pong/script');
    console.log('script:' + uri);
    const data = await fetchData(uri);
    console.log('data:' + data);
    return data;
  }
  async executeScript() {
    executeScriptTab('/static/spa/js/script/pong/test.js');
  }
}
