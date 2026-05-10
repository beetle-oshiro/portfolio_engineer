document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll("a");

  links.forEach(function (link) {
    link.addEventListener("click", function (event) {
      const url = link.getAttribute("href");

      // 新規タブはスキップ
      if (link.target === "_blank") {
        return;
      }

      // 外部リンク・javascript・空はスキップ
      if (!url || url.startsWith("#") || url.startsWith("javascript")) {
        return;
      }

      // 同一ページなら何もしない
      if (url === window.location.pathname) {
        return;
      }

      event.preventDefault();

      document.body.style.overflow = "hidden"; // スクロール止める

      const overlay = document.createElement("div");
      overlay.className = "page-transition";

      overlay.innerHTML = `
        <div class="door door-left"></div>
        <div class="door door-right"></div>
        <p>ACCESSING DATA...</p>
      `;

      document.body.appendChild(overlay);

      setTimeout(function () {
        window.location.href = url;
      }, 500);
    });
  });

  // 戻る・進む時に transition が残っていたら削除
  const oldOverlay = document.querySelector(".page-transition");

  if (oldOverlay) {
    oldOverlay.remove();
  }

  // スクロール制限も解除
  document.body.style.overflow = "auto";
});

// ブラウザの戻る・進む対応
window.addEventListener("pageshow", function () {
  const overlay = document.querySelector(".page-transition");

  if (overlay) {
    overlay.remove();
  }

  document.body.style.overflow = "auto";
});

// UFOメニューの開閉
const ufoButton = document.querySelector(".ufo-button");
const ufoMenu = document.querySelector(".ufo-menu");

if (ufoButton && ufoMenu) {
  ufoButton.addEventListener("click", function (event) {
    event.stopPropagation();
    ufoMenu.classList.toggle("active");
  });
}