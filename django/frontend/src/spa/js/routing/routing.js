import { Routes } from './routes.js';
import { getUrl } from '../utility/url.js';
import { isLogined } from '../utility/user.js';
import { executeScriptTab } from '../utility/script.js';
import { reload } from '..//utility/user.js';
import { getDisplayedURI } from '../../../../src/index.js';

let view = undefined;
window.addEventListener('popstate', async (event) => {
  try {
    const stateJson = await event.state;
    if (stateJson) {
      for (let key in stateJson) {
        document.getElementById(key).value = stateJson[key];
      }
    } else {
      const uri = getDisplayedURI(window.location.pathname);
      router(uri.rest, uri.params);
    }
  } catch (error) {
    console.error(error);
  }
});

const pathToRegex = (path) =>
  new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

export const moveTo = async (url) => {
  console.log('navigateTo No.2 MoveTo');
  navigateTo(url);
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
  console.log('history_url=' + history_url);
  if (view !== undefined && view !== null) {
    const state = await view.getState();
    history.replaceState(state, null, history_url);
  } else {
    history.replaceState(null, null, history_url);
  }

  const tmp_view = await router(rest, params);
  if (tmp_view !== null) {
    view = tmp_view;
  }
  /*
  const history_url = url + rest + params;
  try {
    const setState = async () => {
      if (view !== undefined && view !== null) {
        const state = await view.getState();
        history.pushState(state, null, history_url);
      } else {
        history.pushState(null, null, history_url);
      }
      //view = await router(rest, params);
      //return view;
    };
    view = await setState();
    return view;
  } catch (error) {
    console.error('ignore:' + error);
  }
  return null;
  */
};

export const router = async (rest = '', params = '') => {
  let url;
  console.log('router No.1 location.pathname=' + location.pathname);
  if (rest !== '') {
    url = location.pathname.substring(0, location.pathname.indexOf(rest));
  } else {
    url = location.pathname;
  }
  console.log('router No.2');
  const potentialMatches = Routes.map((route) => {
    console.log('url=' + url);
    console.log('path=' + route.path);
    console.log('path=' + pathToRegex(route.path));
    return {
      route: route,
      result: url.match(pathToRegex(route.path)),
    };
  });

  console.log('router No.3');
  let match = potentialMatches.find((potentialMatch) => potentialMatch.result !== null);
  if (!match) {
    console.log('router No.4');
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }

  if (isLogined() == false) {
    console.log('router No.5');
    match = {
      route: Routes[0],
      result: [getUrl(Routes[0].path)],
    };
  }
  console.log('router No.6');
  const view = new match.route.view();
  try {
    console.log('router No.7');
    console.log('router No.7 view:' + view.setTitle);
    const json = await view.checkRedirect();
    if (json['is_redirect']) {
      console.log('router No.8');
      console.log('navigateTo No.3 router()');
      navigateTo(json['uri']);
      return;
    }
    let html;
    console.log('router No.9');
    try {
      html = await view.getHtml(rest, params);
      console.log('router No.10');
    } catch (e) {
      console.warn('404 Error. move to Top page:' + e);
      moveTo('/');
      console.log('router No.11');
      return;
    }
    document.querySelector('#app').innerHTML = html;
    view.executeScript();
    console.log('router No.12');
  } catch (error) {
    console.error('executeScript Error:' + error);
    console.log('router No.13');
  }
  console.log('router No.14');
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
        console.log('navigateTo No.1');
        console.log('navigateTo No.4 router() updatePage');
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
