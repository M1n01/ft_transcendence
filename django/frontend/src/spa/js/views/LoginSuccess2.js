import AbstractView from './AbstractView.js';
import { executeScriptTab } from '../utility/script.js';
import { fetchJsonData } from '../utility/fetch.js';

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle('Posts');
  }

  checkRedirect = async () => {
    const json = fetchJsonData('/spa/is-login');
    return json;
  };
  getHtml = async () => {
    return `
            <h1>Posts2</h1>
            <p>You are viewing the posts!!!1234A</p>
            <a href="/settings" class="nav__link" data-link>Settings</a>
        `;
  };
  executeScript = () => {
    executeScriptTab('');
  };
  getState = () => {
    return null;
  };
}
