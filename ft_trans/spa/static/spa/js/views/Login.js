import AbstractView from "./AbstractView.js";
import fetchData from "../utility/fetch.js";
import { getUrlWithLang } from "../utility/url.js";
import { executeScriptTab } from "../utility/script.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Test2");
  }

  async getHtml() {
    const uri = getUrlWithLang("/pong/bootstrap_sign-in/");
    const data = fetchData(uri);
    return data;
  }
  async executeScript() {
    //executeScriptTab("");
  }
}
