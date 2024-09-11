import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { TournmentEvent } from '../../../pong/js/tournament.js';
//import { RebuildTournmentEvent } from '../../../pong/js/rebuild_tournament.js';
//import { LoginEvent } from '../../../accounts/js/login.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign up');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async () => {
    const uri = getUrlWithLang('pong/tournament');
    const data = fetchData(uri);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(TournmentEvent);
    //document.dispatchEvent(RebuildTournmentEvent);
  };
  getState = () => {
    return null;
  };
}
