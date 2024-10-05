// クッキーを設定する関数
function setCookie(name, value, days) {
  var date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  var expires = 'expires=' + date.toUTCString();
  document.cookie = name + '=' + value + ';' + expires + ';path=/';
}

// クッキーを取得する関数
function getCookie(name) {
  var nameEQ = name + '=';
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

// バナーの表示を制御する関数
function checkCookieBanner() {
  var cookieAccepted = getCookie('cookieAccepted');
  if (cookieAccepted === 'true') {
    const banner = document.getElementById('cookie-banner');
    banner.style.display = 'none';
  }
}

// ページロード時にバナーの表示をチェック
window.onload = function () {
  checkCookieBanner();
};

// カスタムイベントの作成
export const CookieBannerEvent = new Event('CookieBannerEvent');

// カスタムイベントリスナーの登録
document.addEventListener('CookieBannerEvent', function () {
  try {
    const banner = document.getElementById('cookie-banner');

    // クッキーをチェックしてバナーを表示するかどうかを決定
    checkCookieBanner();

    // 同意ボタンのクリックイベント
    document.getElementById('accept-cookies').addEventListener('click', () => {
      banner.style.display = 'none'; // バナーを非表示

      // 「はい」ボタンを押したらクッキーを設定
      setCookie('cookieAccepted', 'true', 1); // 1日（24時間）クッキーを保持
    });
  } catch (error) {
    console.error('Error: ' + error.message);
  }
});
