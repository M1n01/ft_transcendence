import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { fetchJsonData } from '../utility/fetch.js';
import { UserEvent } from '../../../users/js/users.js';
//import
import '../../../users/scss/users.scss';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign Up');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };

  getHtml = async (rest = '', params = '') => {
    if (rest === '') {
      const uri = getUrlWithLang('users/');
      const data = fetchData(uri + rest + params);
      return data;
    } else if (rest === '/profile') {
      const uri = getUrlWithLang('users/profile/');
      const data = fetchData(uri + params);
      return data;
    } else if (rest === '/edit') {
      const uri = getUrlWithLang('users/edit-profile/');
      const data = fetchData(uri + params);
      return data;
      // privacy-policyはログインしなくても入れるのでここにあると入れない
      //} else if (rest === '/privacy-policy') {
      //const uri = getUrlWithLang('users/privacy-policy/');
      //const data = fetchData(uri + params);
      //return data;
    } else if (rest === '/cookie-banner') {
      const uri = getUrlWithLang('users/cookie-banner/');
      const data = fetchData(uri + params);
      return data;
    } else {
      throw new Error(' Fetch() Error');
    }
  };
  executeScript = () => {
    document.dispatchEvent(UserEvent);
  };
  getState = () => {
    return null;
  };
}
