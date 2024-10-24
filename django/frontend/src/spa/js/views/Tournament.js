import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { TournamentEvent } from '../../../tournament/js/tournament.js';
import { RebuildTournamentEvent } from '../../../tournament/js/rebuild_tournament.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Tournament');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
    const detail_values = rest.match(/^\/detail\/([-\w]*)$/);
    let detail_value = 0;
    if (detail_values) {
      detail_value = detail_values[1];
    }

    if (rest === '/organized') {
      const uri = getUrlWithLang('tournament/organized/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/participant') {
      const uri = getUrlWithLang('tournament/participant/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/recruiting') {
      let uri = getUrlWithLang('tournament/recruiting/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/all') {
      const uri = getUrlWithLang('tournament/all/');
      const data = fetchData(uri + params);
      return data;
    } else if (detail_value != 0) {
      const uri = getUrlWithLang('tournament/details/' + detail_value);
      const data = fetchData(uri);
      return data;
    } else if (rest === '') {
      const uri = getUrlWithLang('tournament/');
      const data = fetchData(uri);
      return data;
    } else {
      throw new Error(' Fetch() Error');
    }
  };
  executeScript = () => {
    document.dispatchEvent(TournamentEvent);
    document.dispatchEvent(RebuildTournamentEvent);
  };
  getState = () => {
    return null;
  };
}
