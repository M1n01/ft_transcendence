import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
//import { RebuildTournamentEvent } from '../../../tournament/js/rebuild_tournament.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Games');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    //document.dispatchEvent(RebuildTournamentEvent);
  };
  getState = () => {
    return null;
  };
}
