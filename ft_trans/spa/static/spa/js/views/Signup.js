import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { fetchAsForm } from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Sign up');
  }

  async getHtml() {
    console.log('account/signup');
    const uri = getUrlWithLang('account/signup');
    const data = fetchData(uri);
    return data;
  }
  async executeScript() {
    const url = '/account/signup/';
    const form = document.getElementById('signup-form');
    let formData = new FormData(form);

    console.log('execute signup()');
    await fetchAsForm(url, formData, 'signup');
    console.log('execute signup() end');
  }
}
