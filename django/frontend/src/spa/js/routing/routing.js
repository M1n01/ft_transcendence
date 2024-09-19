import { Routes } from './routes.js';
import { getUrl } from '../utility/url.js';
import { isLogined } from '../utility/user.js';
import { executeScriptTab } from '../utility/script.js';
import { reload } from '..//utility/user.js';

let view = undefined;
window.addEventListener('popstate', async (event) => {
  try {
    const stateJson = await event.state;
    for (let key in stateJson) {
      document.getElementById(key).value = stateJson[key];
    }
  } catch (error) {
    console.error(error);
  }
});

const pathToRegex = (path) =>
  new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

export const moveTo = async (url) => {
  navigateTo(url);
  await reload();
};

export const navigateTo = async (url, rest = '', params = '') => {
  const history_url = url + rest + params;
  try {
    const setState = async () => {
      if (view !== undefined && view !== null) {
        const state = await view.getState();
        history.pushState(state, null, history_url);
      } else {
        history.pushState(null, null, history_url);
      }
      view = await router(rest, params);
      return view;
    };
    view = await setState();
    return view;
  } catch (error) {
    console.error('ignore:' + error);
  }
  return null;
};

export const router = async (rest = '', params = '') => {
  let url;
  if (rest !== '') {
    url = location.pathname.substring(0, location.pathname.indexOf(rest));
  } else {
    url = location.pathname;
  }
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

  if (isLogined() == false) {
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }
  const view = new match.route.view();
  try {
    const json = await view.checkRedirect();
    if (json['is_redirect']) {
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
    document.querySelector('#app').innerHTML = html;
    view.executeScript();
  } catch (error) {
    console.error('executeScript Error:' + error);
  }
  return view;
};

export async function updatePage(res) {
  try {
    const status = await res.status;
    if (status >= 400) {
      return;
    }
    const contentType = await res.headers.get('content-type');
    if (contentType && contentType.indexOf('application/json') !== -1) {
      // 他にどうしようもなかったので特別対応
      // Jsonで遷移するurlを取得する。
      const data = await res.json();
      if ('html' in data) {
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
