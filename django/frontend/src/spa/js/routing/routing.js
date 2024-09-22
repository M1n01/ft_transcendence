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

export const navigateTo = async (url) => {
  try {
    const setState = async () => {
      if (view !== undefined && view !== null) {
        const state = await view.getState();
        history.pushState(state, null, url);
      } else {
        history.pushState(null, null, url);
      }
      view = await router();
      return view;
    };
    view = await setState();
    return view;
  } catch (error) {
    console.error('ignore:' + error);
  }
  return null;
};

export const router = async () => {
  const potentialMatches = Routes.map((route) => {
    return {
      route: route,
      result: location.pathname.match(pathToRegex(route.path)),
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
  //const view = new match.route.view(getParams(match));
  const view = new match.route.view();
  try {
    const json = await view.checkRedirect();
    if (json['is_redirect']) {
      navigateTo(json['uri']);
      router();
      return;
    }
    const html = await view.getHtml();
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
    } else {
      document.querySelector('#app').innerHTML = await res.text();
    }
    executeScriptTab('');
  } catch (error) {
    console.error(error);
  }
}
