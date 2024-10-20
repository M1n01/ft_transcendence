import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { GameEvent } from '../../../pong/js/pong.js';
import { PongMainEvent } from '../../..//pong/js/pong/main.js';

// Pong.jsと同じ内容
// 設計をミスったのでできれば修正したいが時間がないのでそのままにする

//import { PongMainEvent } from '../../pong/js/pong.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Pong');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async (rest = '', params = '') => {
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

    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(GameEvent);
    document.dispatchEvent(PongMainEvent);
  };
  getState = () => {
    return null;
  };
}
