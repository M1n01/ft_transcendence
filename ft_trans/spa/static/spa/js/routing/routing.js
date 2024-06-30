import { Routes } from './routes.js';
import { getUrl } from '../utility/url.js';
import { isLogined } from '../utility/user.js';

console.log('No.0 routing.js');
const pathToRegex = (path) =>
  new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

const getParams = (match) => {
  const values = match.result.slice(1);
  const keys = Array.from(match.route.path.matchAll(/:([\w]+)/g)).map((result) => result[1]);
  if (values.length > 0) {
    alert(values);
  }
  const url = match.result.toString();
  return Object.fromEntries(
    keys.map((key, i) => {
      return [key, values[i]];
    })
  );
};

export const navigateTo = (url) => {
  console.log('history pushState:' + url);
  console.log('router() No.1');
  history.pushState(null, null, url);
  console.log('router() start');
  router();
  console.log('router() end');
};

export const router = async () => {
  //console.log('router() No.12 path=' + route.path);
  //console.log('router() No.2 regpath=' + pathToRegex(route.path));
  //console.log('router() No.22 regpath=' + route.path);

  const potentialMatches = Routes.map((route) => {
    return {
      route: route,
      result: location.pathname.match(pathToRegex(route.path)),
    };
  });
  //console.log('router() No.3 length:' + potentialMatches.length);
  //if (potentialMatches.length > 0) {
  //console.log('router() No.3 potentilMathces[0]:' + potentialMatches[0]);
  //}

  let match = potentialMatches.find((potentialMatch) => potentialMatch.result !== null);
  //console.log('router() No.4:' + match.result);

  //console.log('No.1 match=' + match.route.path);
  //console.log('No.1 result=' + match.result);
  if (!match) {
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }
  console.log('No.2 match=' + match.route.path);
  console.log('No.2 result=' + match.result);

  if (isLogined() == false) {
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }
  //const view = new match.route.view(getParams(match));
  const view = new match.route.view();

  const html = await view.getHtml();
  document.querySelector('#app').innerHTML = html;

  try {
    view.executeScript();
  } catch (error) {
    //console.error(error);
  }
};
