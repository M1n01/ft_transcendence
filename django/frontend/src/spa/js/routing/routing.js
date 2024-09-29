import { Routes } from './routes.js';
import { getUrl } from '../utility/url.js';
import { isLogined } from '../utility/user.js';
import { executeScriptTab } from '../utility/script.js';
import { reload } from '..//utility/user.js';
import { getDisplayedURI } from '../../../../src/index.js';
import { WebsocketInit } from '../ws/socket.js';

let view = undefined;
window.addEventListener('popstate', async (event) => {
  try {
    const stateJson = await event.state;
    if (stateJson) {
      for (let key in stateJson) {
        document.getElementById(key).value = stateJson[key];
      }
    } else {
      const uri = getDisplayedURI(window.location.href);
      console.log('pre router() No.1');
      router(uri.rest, uri.params);
    }
  } catch (error) {
    console.error(error);
  }
});

const pathToRegex = (path) =>
  new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

export const moveTo = async (url, rest = '', params = '') => {
  savePage(url, rest, params);
  await navigateTo(url, rest, params);
  await reload();
};

export const savePage = async (url, rest = '', params = '') => {
  const history_url = url + rest + params;
  if (view !== undefined && view !== null) {
    const state = await view.getState();
    history.pushState(state, null, history_url);
  } else {
    history.pushState(null, null, history_url);
  }
};

export const navigateTo = async (url, rest = '', params = '') => {
  const history_url = url + rest + params;

  if (view !== undefined && view !== null) {
    const state = await view.getState();
    history.replaceState(state, null, history_url);
  } else {
    history.replaceState(null, null, history_url);
  }

  console.log('pre router() No.2 pathname:' + window.location.pathname);
  const tmp_view = await router(rest, params);
  if (tmp_view !== null) {
    view = tmp_view;
  }
};

export const router = async (rest = '', params = '') => {
  console.log('router No.0');
  WebsocketInit();
  console.log('router No.1');

  let url;
  if (rest !== '') {
    console.log('router No.2 pathname:' + location.pathname);
    url = location.pathname.substring(0, location.pathname.indexOf(rest));
    console.log('No.3 router:' + url);
  } else {
    console.log('router No.4');
    url = location.pathname;
    console.log('No.5 router:' + url);
  }
  console.log('router No.6 uri:' + url);
  const potentialMatches = Routes.map((route) => {
    return {
      route: route,
      result: url.match(pathToRegex(route.path)),
    };
  });

  let match = potentialMatches.find((potentialMatch) => potentialMatch.result !== null);
  if (!match) {
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }

  console.log('router No.7 uri:' + url);
  if (isLogined() == false) {
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }
  console.log('router No.8 uri:' + url);
  const view = new match.route.view();
  try {
    console.log('router No.9 uri:' + url);
    const json = await view.checkRedirect();
    if (json['is_redirect']) {
      console.log('router No.10 uri:' + url);
      navigateTo(json['uri']);
      return;
    }
    let html;
    try {
      html = await view.getHtml(rest, params);
    } catch (e) {
      console.warn('404 Error. move to Top page:' + e);
      moveTo('/');
      return;
    }
    console.log('router No.11 uri:' + url);
    document.querySelector('#app').innerHTML = html;
    console.log('router No.12 uri:' + url);
    view.executeScript();
    console.log('router No.13 uri:' + url);
  } catch (error) {
    console.error('executeScript Error:' + error);
  }
  console.log('router No.14 uri:' + url);
  return view;
};

export async function updatePage(res) {
  console.log('updatePage No.1');
  try {
    const status = await res.status;
    if (status >= 400) {
      return;
    }
    const contentType = await res.headers.get('content-type');
    if (contentType && contentType.indexOf('application/json') !== -1) {
      console.log('updatePage No.2');
      // 他にどうしようもなかったので特別対応
      // Jsonで遷移するurlを取得する。
      const data = await res.json();
      console.log('updatePage No.3');
      if ('html' in data) {
        console.log('updatePage No.4');
        navigateTo(data['html']);
      }
    } else if (contentType && contentType.indexOf('text/html') !== -1) {
      document.querySelector('#app').innerHTML = await res.text();
    } else {
      console.error('Error');
    }
    executeScriptTab('');
  } catch (error) {
    console.error(error);
  }
}
