import { fetchAsForm } from './fetch.js';

export const submitForm = async (event) => {
  event.preventDefault();
  const form = event.target;
  if (form.disabled == true) {
    return;
  }

  form.disabled = true;
  const formData = new FormData(form);
  const response = await fetchAsForm(form, formData);
  form.disabled = false;
  return response;
};
