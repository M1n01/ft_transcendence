import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Home');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('/home');
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
