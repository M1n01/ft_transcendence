//import { fetchAsFormByGet, fetchAsForm } from '../../spa/js/utility/fetch.js';
//import { navigateTo, updatePage } from '../../spa/js/routing/routing.js';
//import { reload } from '../../spa/js/utility/user.js';
export const NotificationEvent = new Event('NotificationEvent');
document.addEventListener('NotificationEvent', () => {
  console.log('notifiation test');
});
