import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';
//import { SignupEvent } from '../../../accounts/js/signup.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Games');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri);
    return data;
  };
  executeScript = () => {
    //document.dispatchEvent(SignupEvent);
  };
  getState = () => {
    return null;
  };
}
