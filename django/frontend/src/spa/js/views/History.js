import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
//import { TournmentEvent } from '../../../tournament/js/tournament.js';
//import { RebuildTournmentEvent } from '../../../tournament/js/rebuild_tournament.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign up');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    if (rest === '') {
      const uri = getUrlWithLang('history/');
      const data = fetchData(uri + rest + params);
      return data;
    } else if (rest === '/ovo') {
      const uri = getUrlWithLang('history/ovo/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/tournament') {
      const uri = getUrlWithLang('history/tournament/');
      const data = fetchData(uri + params);
      return data;
    }
  };
  executeScript = () => {
    //document.dispatchEvent(RebuildTournmentEvent);
  };
  getState = () => {
    return null;
  };
}
