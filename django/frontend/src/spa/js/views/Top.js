import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
//import { GameEvent } from '../../../pong/js/pong.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Top Page');
  }
  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };

  getHtml = async (rest = '', params = '') => {
    //Topページは現状はgamesに遷移する
    const uri = getUrlWithLang('pong/games');
    const data = fetchData(uri + rest + params);
    return data;
  };

  executeScript = () => {
    //非常にわかりにくいが、Topページはpong(game)ページに遷移するので、
    //GameEventを読み出す必要がある
    //document.dispatchEvent(GameEvent);
  };

  getState = () => {
    return null;
  };
}
