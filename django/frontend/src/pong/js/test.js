console.log('test.js Replace Test ');
import { navigateTo } from '../../spa/js/routing/routing.js';

export const ScriptEvent = new Event('ScriptEvent');

document.addEventListener('ScriptEvent', function () {
  const test_button = document.getElementById('test-button');
  test_button.addEventListener('click', () => {
    let tmp_path = window.location.pathname;
    navigateTo(tmp_path);
  });
});
