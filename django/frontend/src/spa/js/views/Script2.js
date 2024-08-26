import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Script2');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('pong/script2');
    const data = await fetchData(uri);
    return data;
  };

  executeScript = () => {
    //return '';
    executeScriptTab('');
  };
  getState = () => {
    return null;
  };
}
