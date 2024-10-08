import AbstractView from './AbstractView.js';
//import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Posts');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async (rest = '', params = '') => {
    console.log(rest + params);
    return `
            <h1>Posts</h1>
            <p>You are viewing the posts!!!1234A</p>
            <a href="/settings" class="nav__link" data-link>Settings</a>
        `;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
