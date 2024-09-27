// カスタムイベントの作成
export const CookieBannerEvent = new Event('CookieBannerEvent');

// カスタムイベントリスナーの登録
document.addEventListener('CookieBannerEvent', function () {
  try {
    const banner = document.getElementById('cookie-banner');
    
    // 同意ボタンのクリックイベント
    document.getElementById('accept-cookies').addEventListener('click', () => {
      banner.style.display = 'none'; // バナーを非表示
    });
  } catch (error) {
    console.error('Error: ' + error.message);
  }
});
