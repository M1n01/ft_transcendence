# from django.urls import reverse
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from accounts.models import FtUser

# class EditProfileTestCase(TestCase):
#     def setUp(self):
#         # テスト用のユーザーを作成
#         # self.User = get_user_model()
#         self.test_user = FtUser.objects.create_user(
#             username="testA1",
#             password="AAdfBC3DfwFi49",
#             email="testA1@gmail.com",
#             email42="testA142@gmail.com",
#             first_name="test",
#             last_name="A1",
#             country_code="+81",
#             phone="9012345678",
#             language="jp",
#             birth_date="2024-01-01",
#             created_at="2024-01-01T00:00:00Z",
#             updated_at="2024-01-01T00:00:00Z",
#             is_ft=False,
#         )

#     def test_redirect_if_not_logged_in(self):
#         response = self.client.get(reverse('users:edit-profile'))
#         self.assertEqual(response.status_code, 302)  # リダイレクトが発生しているか確認
#         # self.assertRedirects(response, '/accounts/login/?next=/users/edit-profile')  # リダイレクト先を確認

#     def test_profile_edit_page_renders_correctly(self):
#         # ユーザーでログイン
#         login = self.client.login(username='testA1', password='AAdfBC3DfwFi49')
#         self.assertTrue(login)  # ログインが成功したかを確認
        
#         # edit-profileビューにアクセス
#         response = self.client.get(reverse('users:edit-profile'))
        
#         # ステータスコードが200であることを確認
#         self.assertEqual(response.status_code, 200)
        
#         # テンプレートが正しくレンダリングされているか確認
#         self.assertTemplateUsed(response, 'users/edit-profile.html')


# from django.test import TestCase

# # Create your tests here.
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from accounts.models import FtUser

# class EditProfileTestCase(TestCase):

#     def setUp(self):
#         # テスト用のユーザーを作成
#         self.user = FtUser.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpassword',
#             first_name='Test',
#             last_name='User',
#             phone='1234567890',
#             language='English',
#             birth_date='1990-01-01'
#         )
#         self.client.login(username='testuser', password='testpassword')

#     def test_profile_edit_page_renders_correctly(self):
#         # プロフィール編集ページが正しく表示されるか確認
#         response = self.client.get(reverse('users:edit-profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Edit Profile')
#         self.assertContains(response, self.user.username)
#         self.assertContains(response, self.user.email)

#     def test_profile_update_success(self):
#         # プロフィールのデータが更新されるか確認
#         response = self.client.post(reverse('edit-profile'), {
#             'username': 'newusername',
#             'email': 'newemail@example.com',
#             'first_name': 'NewFirst',
#             'last_name': 'NewLast',
#             'phone': '0987654321',
#             'language': 'Japanese',
#             'birth_date': '1995-05-05'
#         })
#         # 正常にリダイレクトされるか確認
#         self.assertRedirects(response, reverse('profile'))

#         # データが正しく更新されているか確認
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, 'newusername')
#         self.assertEqual(self.user.email, 'newemail@example.com')
#         self.assertEqual(self.user.first_name, 'NewFirst')
#         self.assertEqual(self.user.last_name, 'NewLast')
#         self.assertEqual(self.user.phone, '0987654321')
#         self.assertEqual(self.user.language, 'Japanese')
#         self.assertEqual(str(self.user.birth_date), '1995-05-05')

#     def test_profile_update_invalid_data(self):
#         # 不正なデータでの更新が失敗するか確認（例：無効なメールアドレス）
#         response = self.client.post(reverse('edit-profile'), {
#             'username': 'newusername',
#             'email': 'invalid-email',  # 不正なメールアドレス
#         })
#         # ページが再表示されるか確認
#         self.assertEqual(response.status_code, 200)
#         # フォームにエラーが含まれるか確認
#         self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
