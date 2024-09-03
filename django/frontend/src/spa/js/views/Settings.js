import AbstractView from './AbstractView.js';
//import { executeScriptTab } from '../utility/script.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Settings');
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async () => {
    return `
            <h1>Settings</h1>
            <p>Manage your privacy and configuration.</p>
            <a href="/posts" class="nav__link" data-link>Posts</a>
        `;
  };
  executeScript = () => {
    //executeScriptTab("");
  };
  getState = () => {
    return null;
  };
}
