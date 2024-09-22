export default class {
  constructor(params) {
    this.params = params;
  }

  setTitle(title) {
    document.title = title;
  }

  checkRedirect = async () => {
    return { is_redirect: false };
  };
  getHtml = async () => {
    return '';
  };
  executeScript = () => {
    return '';
  };
  getState = () => {
    return '';
  };
}
