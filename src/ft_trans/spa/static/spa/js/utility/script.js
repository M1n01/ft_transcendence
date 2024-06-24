export function executeScriptTab(path) {
  const app = document.querySelector('#app');
  var newDiv = document.createElement('script');
  const id = 'script' + path;

  // すでに<script>タグがあれば削除する
  if (document.getElementById(id)) {
    document.getElementById(id).remove();
  }

  var script = app.getElementsByTagName('script');
  if (script !== undefined && script[0] !== undefined) {
    if (script[0].src !== '') {
      newDiv.src = path;
    } else if (script[0].innerHTML !== '') {
      newDiv.textContent = script[0].innerHTML;
    }
    newDiv.id = id;
    document.body.appendChild(newDiv);
  }
}
