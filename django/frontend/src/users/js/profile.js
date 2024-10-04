// カスタムイベントの作成
export const ProfileEvent = new Event('ProfileEvent');

// カスタムイベントリスナーの登録
document.addEventListener('ProfileEvent', function () {
  try {
    const input_element = document.getElementById('edit-profile');

    // ナビゲーションリンクのクリックイベントリスナーを追加
    const links = input_element.querySelectorAll('a[data-link]');
    links.forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault(); // デフォルトのリンクの動作をキャンセル
        // const targetPath = link.href; // クリックされたリンクのURLを取得
        // ここでページ遷移のカスタム処理を追加
        // console.log(`Navigating to: ${targetPath}`);
        // 例: navigateTo(targetPath); // カスタムナビゲーション関数の呼び出し
      });
    });

    // let tmp_path = window.location.pathname;

    // document.body.addEventListener('click', (e) => {
    //   // ページ切替
    //   if (e.target.matches('[data-link]')) {
    //     savePage(window.location.href);

    //     e.preventDefault();
    //     tmp_path = e.target.href;
    //     const uri = getDisplayedURI(tmp_path);
    //     navigateTo(uri.path, uri.rest, uri.params);
    //   }
  } catch (error) {
    console.error('Error: ' + error.message);
  }
});
