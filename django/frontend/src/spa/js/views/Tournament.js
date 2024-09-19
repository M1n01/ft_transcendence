import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { TournmentEvent } from '../../../tournament/js/tournament.js';
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
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('tournament/');
    console.log('tournament No.1 rest:' + rest);
    const split = rest.split('/');
    console.log('tournament No.2 rest:' + split);
    if (split[0] === 'register') {
      console.log('tournament No.2');
      const data = fetchData(uri + rest + params);
      return data;
    } else if (rest === '') {
      console.log('tournament No.3');
      const data = fetchData(uri + rest + params);
      return data;
    } else {
      console.log('tournament No.4');
      throw new Error(' Fetch() Error');
    }
  };
  executeScript = () => {
    document.dispatchEvent(TournmentEvent);
    //document.dispatchEvent(RebuildTournmentEvent);
    //document.dispatchEvent(TournmentEvent);
    //document.dispatchEvent(RebuildTournmentEvent);
  };
  getState = () => {
    return null;
  };
}
