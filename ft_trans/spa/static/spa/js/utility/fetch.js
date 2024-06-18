function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

//If you activate CSRF_USE_SESSIONS or CSRF_COOKIE_HTTPONLY
//const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

function makeRequest(method, url) {
  return fetch(url, {
    method: method,
    headers: { "X-CSRFToken": csrftoken },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(" Fetch() Error");
    }
    return response.text();
  });
}

function sendRequestAsForm(method, url) {
  return fetch(url, {
    method: method,
    headers: { "X-CSRFToken": csrftoken, SPA: "spa" },
    mode: "same-origin",
    body: {
      spa: "enable",
    },
  }).then((response) => {
    console.error("Fetch error status:" + response.status);
    if (300 <= response.status && response.status < 400) {
      console.log(response.headers);
    }

    if (!response.ok) {
      throw new Error(" Fetch() Error");
    }

    return response.text();
  });
}

export default async function fetchData(url) {
  try {
    console.log("No.1 fetch url:" + url);
    //url = "http://localhost:8000/ja/pong/script";
    //const response = await makeRequest("GET", url);
    const response = await sendRequestAsForm("POST", url);
    return response;
  } catch (error) {
    console.error(error);
  }
  return "";
}
