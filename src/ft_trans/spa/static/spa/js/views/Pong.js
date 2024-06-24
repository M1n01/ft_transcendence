import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Pong');
  }

  async getHtml() {
    const uri = getUrlWithLang('/pong/');
    const data = await fetchData(uri);
    //console.log("Pong:" + data);
    return data;
  }
  async executeScript() {
    //executeScriptTab("");
  }
}
