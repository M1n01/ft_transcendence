import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Error Page');
  }
  checkRedirect = async () => {
    return { is_redirect: false };
  };

  getHtml = async () => {
    const uri = getUrlWithLang('spa/top');
    const data = fetchData(uri);
    return data;
  };

  executeScript = () => {};

  getState = () => {
    return null;
  };
}
