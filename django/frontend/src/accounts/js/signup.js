import '../scss/signup.scss';
export const SignupEvent = new Event('SignupEvent');

function SetTime() {
  const Mytoday = new Date();
  const yyyy = Mytoday.getFullYear();
  const mm = String(Mytoday.getMonth() + 1).padStart(2, '0');
  const dd = String(Mytoday.getDate()).padStart(2, '0');
  const todayString = `${yyyy}-${mm}-${dd}`;
  document.getElementById('id_created_at').value = todayString;
  document.getElementById('id_birth_date').type = 'date';
}

document.addEventListener('SignupEvent', function () {
  SetTime();

  const signup_button = document.getElementById('signup-button');

  const auth_select = document.getElementById('id_auth');
  const phone_input = document.getElementById('id_phone');
  const phone_auth_error = document.getElementById('phone-auth-error');
  signup_button.addEventListener('click', function (e) {
    phone_auth_error.hidden = true;
    console.log('value=' + auth_select.value);
    if (auth_select.value == 'S' && phone_input.value == '') {
      phone_auth_error.hidden = false;
      console.log('Error');
      e.preventDefault();
    }
  });
  phone_input.addEventListener('input', function () {
    phone_auth_error.hidden = true;
  });
});
