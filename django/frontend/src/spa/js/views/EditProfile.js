import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Edit Profile');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('users/edit-profile');
    const data = await fetchData(uri);
    return data;
  };

  executeScript = () => {
  };

  getState = () => {
    return null;
  };
}
