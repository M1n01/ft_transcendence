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
      moveTo('/users/profile');
    });
  }
  // パスワードの変更
  const change_password_form = document.getElementById('change-password-form');
  if (change_password_form != null) {
    change_password_form.addEventListener('submit', async (event) => {
      const response = await submitForm(event);
      if (response.error) {
        // console.log('Error: change-password-form');
        return;
      }
      moveTo('/users/changed-password');
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
