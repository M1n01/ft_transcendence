import '../scss/users.scss';
import { submitForm } from '../../spa/js/utility/form.js';
import { moveTo } from '../../spa/js/routing/routing.js';
import { reload } from '../../spa/js//utility/user.js';

export const UserEvent = new Event('UserEvent');

document.addEventListener('UserEvent', function () {
  // ユーザ情報の編集内容を保存
  const edit_profile_form = document.getElementById('edit-profile-form');
  if (edit_profile_form != null) {
    edit_profile_form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) {
        // console.log('Error: edit-profile-form');
        return;
      }
      if (response.status != 200) {
        console.log('Error: edit-profile-form');
        return;
      }
      moveTo('/users/profile');
    });
  }
  // パスワードの変更
  const change_password_form = document.getElementById('change-password-form');
  if (change_password_form != null) {
    change_password_form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) {
        return;
      }
      if (response.status != 200) {
        const html = await response.text();
        // TODO: debug用。あとで消す。
        // console.error(html);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const oldPwdErrors = tempDiv.querySelector('#old-password-errors ul.errorlist');
        if (oldPwdErrors != null) {
          document.getElementById('old-password-errors').innerHTML = oldPwdErrors.outerHTML;
        }
        const newPwd1Errors = tempDiv.querySelector('#new-password1-errors ul.errorlist');
        if (newPwd1Errors != null) {
          document.getElementById('new-password1-errors').innerHTML = newPwd1Errors.outerHTML;
        }
        const newPwd2Errors = tempDiv.querySelector('#new-password2-errors ul.errorlist');
        if (newPwd2Errors != null) {
          document.getElementById('new-password2-errors').innerHTML = newPwd2Errors.outerHTML;
        }
      } else {
        // console.log('Success: change-password-form');
        moveTo('/users/changed-password');
        return;
      }
    });
    // フォームの各入力フィールドにイベントリスナーを追加
    const oldPasswordField = change_password_form.querySelector('input[name="old_password"]');
    const newPassword1Field = change_password_form.querySelector('input[name="new_password1"]');
    const newPassword2Field = change_password_form.querySelector('input[name="new_password2"]');

    const clearErrorMessages = (errorElementId) => {
      document.getElementById(errorElementId).innerHTML = ''; // エラーメッセージをクリア
    };
    const clearNewPwdErrorMessages = () => {
      clearErrorMessages('new-password1-errors');
      clearErrorMessages('new-password2-errors');
    };

    if (oldPasswordField) {
      oldPasswordField.addEventListener('input', () => clearErrorMessages('old-password-errors'));
    }
    if (newPassword1Field || newPassword2Field) {
      newPassword1Field.addEventListener('input', () => clearNewPwdErrorMessages());
      newPassword2Field.addEventListener('input', () => clearNewPwdErrorMessages());
    }
  }

  const export_profile = document.getElementById('export-profile');
  if (export_profile != null) {
    export_profile.addEventListener('click', async (event) => {
      event.preventDefault();
      // CSVエクスポートのリクエストを行う
      try {
        const response = await fetch('/users/export-profile/'); // エクスポートURLにリクエストを送信
        if (response.ok) {
          const blob = await response.blob(); // レスポンスをBlobとして取得
          const url = window.URL.createObjectURL(blob); // BlobをURLに変換

          const a = document.createElement('a'); // 新しいaタグを作成
          a.style.display = 'none'; // 非表示にする
          a.href = url; // BlobのURLを設定
          a.download = 'user_data.csv'; // ダウンロードファイル名を設定
          document.body.appendChild(a); // DOMに追加
          a.click(); // クリックイベントを発火させてダウンロード
          window.URL.revokeObjectURL(url); // メモリを解放
          moveTo('/users/exported-profile');
        } else {
          console.error('エクスポートに失敗しました。');
          moveTo('/users/profile');
        }
      } catch (error) {
        console.error('エラー:', error);
        moveTo('/users/profile');
      }
    });
  }

  // アカウント削除
  const delete_user_form = document.getElementById('delete-user');
  if (delete_user_form !== null) {
    const delete_user_error = document.getElementById('delete-user-error');
    const open_delete_modal = document.getElementById('open-delete-modal-button');
    const close_modal = document.getElementById('delete-user-cancel');

    delete_user_form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) {
        delete_user_error.hidden = false;
        return;
      }
      close_modal.click();
      moveTo('/');
    });
    open_delete_modal.addEventListener('click', () => {
      delete_user_error.hidden = true;
    });
  }

  // アバター変更
  const update_avatar_form = document.getElementById('update-avatar-form');
  if (update_avatar_form !== null) {
    const update_avatar_error = document.getElementById('update-avatar-error');
    const open_avatar_modal = document.getElementById('open-update-modal-button');
    const close_avatar_modal = document.getElementById('update-avatar-cancel');
    const input_avatar = document.getElementById('id_avatar');

    update_avatar_form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) {
        update_avatar_error.hidden = false;
        return;
      }
      close_avatar_modal.click();
      await reload();
    });

    open_avatar_modal.addEventListener('click', () => {
      update_avatar_error.hidden = true;
      input_avatar.value = '';
    });
  }
});
