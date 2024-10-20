import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { GameEvent } from '../../../pong/js/pong.js';
import { PongMainEvent } from '../../..//pong/js/pong/main.js';
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
    console.log('Games No.1');
    const pong_ids = rest.match(/^\/match\/([-\w]*)$/);
    let pong_id = 0;
    if (pong_ids) {
      pong_id = pong_ids[1];
    }
    if (pong_id != 0) {
      const uri = getUrlWithLang('pong/matches/' + pong_id);
      const data = fetchData(uri);
      return data;
    }
    console.log('Games No.2');

    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    console.log('Games No.3');
    document.dispatchEvent(GameEvent);
    console.log('Games No.4');
    document.dispatchEvent(PongMainEvent);
    console.log('Games No.5');
  };
  getState = () => {
    return null;
  };
}
