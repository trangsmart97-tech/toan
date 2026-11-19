/* Menu điện thoại. Tắt JavaScript thì menu vẫn hiện sẵn và dùng được. */
(function () {
  var nut = document.getElementById("nut-menu");
  var menu = document.getElementById("menu");
  if (!nut || !menu) return;
  var rong = window.matchMedia("(min-width: 1040px)");
  function dong() { menu.hidden = true; nut.setAttribute("aria-expanded", "false"); }
  function mo() { menu.hidden = false; nut.setAttribute("aria-expanded", "true"); }
  if (!rong.matches) dong();
  nut.addEventListener("click", function () { menu.hidden ? mo() : dong(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !menu.hidden && !rong.matches) { dong(); nut.focus(); } });
  rong.addEventListener("change", function (e) { if (e.matches) { menu.hidden = false; } else { dong(); } });
})();
