import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';
import { ScriptEvent } from '../../../pong/js/test.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Script');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('pong/script');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    executeScriptTab('/static/spa/js/script/pong/test.js');
    document.dispatchEvent(ScriptEvent);
  };
  getState = () => {
    const test_input = document.getElementById('test-input').value;
    const state = { 'test-input': test_input };
    return state;
  };
}
