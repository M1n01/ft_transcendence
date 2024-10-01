import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Lang');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('pong/lang');
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
