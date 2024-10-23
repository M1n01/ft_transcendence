import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';
import { LoginEvent } from '../../../accounts/js/login.js';
import { SignupEvent } from '../../../accounts/js/signup.js';
import { executeScriptTab } from '../utility/script.js';
import { CookieBannerEvent } from '../../../users/js/banner.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Login/Signup');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async (rest = '', params = '') => {
    const uri = getUrlWithLang('accounts/login-signup/');
    const data = fetchData(uri + rest + params);
    return data;
  };
  executeScript = () => {
    executeScriptTab();
    document.dispatchEvent(LoginEvent);
    document.dispatchEvent(SignupEvent);
    document.dispatchEvent(CookieBannerEvent);
    /*

    document.getElementById('index-nav').hidden = true;
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
