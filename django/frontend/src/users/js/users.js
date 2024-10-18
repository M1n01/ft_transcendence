import '../scss/users.scss';
import { submitForm } from '../../spa/js/utility/form.js';
import { moveTo } from '../../spa/js/routing/routing.js';
import { reload } from '../../spa/js//utility/user.js';

export const UserEvent = new Event('UserEvent');

document.addEventListener('UserEvent', function () {
  // フォームバリデーションのエラーメッセージの更新
  const updateErrorMessages = (tempDiv, errorFields) => {
    errorFields.forEach(({ selector, errorId }) => {
      const errors = tempDiv.querySelector(`${selector} ul.errorlist`);
      if (errors != null) {
        document.getElementById(errorId).innerHTML = errors.outerHTML;
      }
    });
  };

  // フォームバリデーションのエラーメッセージをクリアするリスナーを各フィールドに追加
  const addClearErrorListeners = (fields) => {
    fields.forEach(({ field, errorId }) => {
      if (field) {
        field.addEventListener('input', () => {
          document.getElementById(errorId).innerHTML = ''; // エラーメッセージをクリア
        });
      }
    });
  };

  // フォームの送信処理
  const handleFormSubmit = async (form, errorFields, successRedirect) => {
    form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) return;

      if (response.status != 200) {
        const html = await response.text();
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        updateErrorMessages(tempDiv, errorFields);
      } else {
        moveTo(successRedirect);
      }
    });
  };

  // プロフィール編集フォームの処理
  const editProfileForm = document.getElementById('edit-profile-form');
  if (editProfileForm != null) {
    const profileFields = [
      { selector: '#username-errors', errorId: 'username-errors' },
      { selector: '#email-errors', errorId: 'email-errors' },
      { selector: '#first-name-errors', errorId: 'first-name-errors' },
      { selector: '#last-name-errors', errorId: 'last-name-errors' },
      { selector: '#birth-date-errors', errorId: 'birth-date-errors' },
      { selector: '#country-code-errors', errorId: 'country-code-errors' },
      { selector: '#phone-errors', errorId: 'phone-errors' },
      { selector: '#language-errors', errorId: 'language-errors' },
    ];

    const profileFieldsWithElements = [
      {
        field: editProfileForm.querySelector('input[name="username"]'),
        errorId: 'username-errors',
      },
      { field: editProfileForm.querySelector('input[name="email"]'), errorId: 'email-errors' },
      {
        field: editProfileForm.querySelector('input[name="first_name"]'),
        errorId: 'first-name-errors',
      },
      {
        field: editProfileForm.querySelector('input[name="last_name"]'),
        errorId: 'last-name-errors',
      },
      {
        field: editProfileForm.querySelector('input[name="birth_date"]'),
        errorId: 'birth-date-errors',
      },
      {
        field: editProfileForm.querySelector('input[name="country_code"]'),
        errorId: 'country-code-errors',
      },
      { field: editProfileForm.querySelector('input[name="phone"]'), errorId: 'phone-errors' },
      {
        field: editProfileForm.querySelector('input[name="language"]'),
        errorId: 'language-errors',
      },
    ];

    handleFormSubmit(editProfileForm, profileFields, '/users/profile');
    addClearErrorListeners(profileFieldsWithElements);
  }

  // パスワード変更フォームの処理
  const changePasswordForm = document.getElementById('change-password-form');
  if (changePasswordForm != null) {
    const passwordFields = [
      { selector: '#old-password-errors', errorId: 'old-password-errors' },
      { selector: '#new-password1-errors', errorId: 'new-password1-errors' },
      { selector: '#new-password2-errors', errorId: 'new-password2-errors' },
    ];

    const passwordFieldsWithElements = [
      {
        field: changePasswordForm.querySelector('input[name="old_password"]'),
        errorId: 'old-password-errors',
      },
      {
        field: changePasswordForm.querySelector('input[name="new_password1"]'),
        errorId: 'new-password1-errors',
      },
      {
        field: changePasswordForm.querySelector('input[name="new_password2"]'),
        errorId: 'new-password2-errors',
      },
    ];

    handleFormSubmit(changePasswordForm, passwordFields, '/users/changed-password');
    addClearErrorListeners(passwordFieldsWithElements);
  }

  // ユーザ情報のCSVエクスポート
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
