import AbstractView from './AbstractView.js';
import fetchData from '../utility/fetch.js';
import { getUrlWithLang } from '../utility/url.js';
//import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Edit Profile');
  }

  getHtml = async () => {
    const uri = getUrlWithLang('users/edit-profile');
    const data = await fetchData(uri);
    return data;
    // return `
    //         <h1>Profile</h1>
    //         <p>profile</p>
    //     `;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
