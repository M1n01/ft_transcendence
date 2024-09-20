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
    console.log('tournament rest=' + rest);
    const split = rest.split('/');
    console.log('split[0]=' + split[0]);
    if (split[0] === '/organized' || rest === '/organized') {
      const uri = getUrlWithLang('tournament/organized/');
      console.log('in url=' + uri + rest + params);
      const new_url = uri + rest + params;
      console.log('new_url=' + new_url);
      //const data = fetchData(new_url.replace('//', '/') + '/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '') {
      const uri = getUrlWithLang('tournament/');
      console.log('url=' + uri);
      const data = fetchData(uri);
      return data;
    } else {
      console.log('tournament ERROR');
      console.log('tournament ERROR');
      console.log('tournament ERROR');
      console.log('tournament ERROR');
      throw new Error(' Fetch() Error');
    }
  };
  executeScript = () => {
    //const split = rest.split('/');
    console.log('TournmentEvent No.0');
    document.dispatchEvent(TournmentEvent);
    //document.dispatchEvent(RebuildTournmentEvent);
    //document.dispatchEvent(TournmentEvent);
    //document.dispatchEvent(RebuildTournmentEvent);
  };
  getState = () => {
    return null;
  };
}
