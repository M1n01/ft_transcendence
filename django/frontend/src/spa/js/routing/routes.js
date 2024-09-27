import Dashboard from '../views/Dashboard.js';
import Posts from '../views/Posts.js';
import PostView from '../views/PostView.js';
import Settings from '../views/Settings.js';
import Signup from '../views/Signup.js';
//import SignupTwoFA from '../views/SignupTwoFA.js';
import Login from '../views/Login.js';
import Logout from '../views/Logout.js';
import Lang from '../views/Lang.js';
import Script from '../views/Script.js';
import Script2 from '../views/Script2.js';
import Index from '../views/Index.js';
import Pong from '../views/Pong.js';
import Admin from '../views/Admin.js';
import LoginSuccess from '../views/LoginSuccess.js';
import TwoFA from '../views/TwoFA.js';
import LoginSignup from '../views/LoginSignup.js';
import Profile from '../views/Profile.js';
import EditProfile from '../views/EditProfile.js';
import DeleteUser from '../views/DeleteUser.js';
import CookieBanner from '../views/CookieBanner.js';

export const Routes = [
  { path: '/', view: Dashboard },
  { path: '/home', view: Index },
  { path: '/pong', view: Pong },
  { path: '/sign', view: Index },
  { path: '/signup', view: Signup },
  { path: '/login', view: Login },
  { path: '/logout', view: Logout },
  { path: '/admin', view: Admin },
  { path: '/posts', view: Posts },
  { path: '/posts/:id', view: PostView },
  { path: '/settings', view: Settings },
  { path: '/ja/settings', view: Settings },
  { path: '/lang', view: Lang },
  { path: '/scriptt', view: Script2 },
  { path: '/script', view: Script },
  { path: '/success-login', view: LoginSuccess },
  //{ path: '/signup-two-fa', view: SignupTwoFA },
  { path: '/2fa', view: TwoFA },
  { path: '/login-signup', view: LoginSignup },
  { path: '/profile', view: Profile },
  { path: '/edit-profile', view: EditProfile },
  { path: '/delete-user', view: DeleteUser },
  { path: '/cookie-banner', view: CookieBanner },
];
