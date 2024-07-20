import AbstractView from "./AbstractView.js";
import { executeScriptTab } from "../utility/script.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.postId = params.id;
    this.setTitle("Viewing Post");
  }

  async getHtml() {
    return `
            <h1>Post</h1>
            <p>You are viewing post #${this.postId}.</p>
        `;
  }
  async executeScript() {
    //executeScriptTab("");
  }
}
