import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Lang');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('pong/lang');
    const data = await fetchData(uri);
    return data;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
