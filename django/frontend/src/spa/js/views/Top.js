import AbstractView from './AbstractView.js';
//import fetchData from '../utility/fetch.js';
import { fetchJsonData } from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { executeScriptTab } from '../utility/script.js';
import { LoginEvent } from '../../../accounts/js/login.js';
import { SignupEvent } from '../../../accounts/js/signup.js';

//let dispatchEvent = [];

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Top Page');
  }

  getHtml = async () => {
    console.log('spa top test');
    const uri = getUrlWithLang('spa/top');
    const data = await fetchJsonData(uri);
    //console.log('is_auth:' + data['is_auth']);
    //console.log('html:' + data['html']);
    if (data['is_auth']) {
      return data['html'];
    }
    //dispatchEvent.push();

    return data['html'];
  };

  executeScript = () => {
    executeScriptTab('');
    document.dispatchEvent(LoginEvent);
    document.dispatchEvent(SignupEvent);
    if (LoginEvent == undefined) console.log('spa top test No.2');
    //document.dispatchEvent(LoginEvent);
    //document.dispatchEvent(SignupEvent);

    /*
    const login_link = document.getElementById('tab-login');
    const signup_link = document.getElementById('tab-signup');
    const login_area = document.getElementById('login-area');
    const signup_area = document.getElementById('signup-area');
    login_link.addEventListener('click', () => {
      login_link.classList.add('active');
      signup_link.classList.remove('active');
      signup_area.hidden = true;
      login_area.hidden = false;
    });
    signup_link.addEventListener('click', () => {
      signup_link.classList.add('active');
      login_link.classList.remove('active');
      login_area.hidden = true;
      signup_area.hidden = false;
    });
    */
  };

  getState = () => {
    return null;
  };
}
