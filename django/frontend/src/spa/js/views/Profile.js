import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
// import { ProfileEvent } from '../../../users/js/profile.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Profile');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('users/profile');
    const data = await fetchData(uri);
    return data;
  };
  executeScript = () => {
    // document.dispatchEvent(ProfileEvent);
  };
  getState = () => {
    return null;
  };
}
