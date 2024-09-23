import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Top Page');
  }
  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };

  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('spa/top');
    const data = fetchData(uri + rest + params);
    return data;
  };

  executeScript = () => {};

  getState = () => {
    return null;
  };
}
