import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
import { CookieBannerEvent } from '../../../users/js/banner.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Cookie Banner');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('users/cookie-banner');
    const data = await fetchData(uri);
    return data;
  };
  executeScript = () => {
    document.dispatchEvent(CookieBannerEvent);
  };
  getState = () => {
    return null;
  };
}
