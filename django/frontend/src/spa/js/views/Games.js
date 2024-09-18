import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { RebuildTournmentEvent } from '../../../tournament/js/rebuild_tournament.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Games');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async () => {
    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(RebuildTournmentEvent);
  };
  getState = () => {
    return null;
  };
}
