(function () {
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Números que contam até o valor final
  function animarNumeros() {
    if (reduzir) { return; }
    document.querySelectorAll("[data-alvo]").forEach(function (el) {
      var alvo = parseFloat(el.dataset.alvo);
      var casas = parseInt(el.dataset.casas || "0", 10);
      var inicio = null;

      function passo(t) {
        if (inicio === null) { inicio = t; }
        var p = Math.min((t - inicio) / 900, 1);
        el.textContent = (alvo * (1 - Math.pow(1 - p, 3))).toFixed(casas);
        if (p < 1) { requestAnimationFrame(passo); }
      }
      requestAnimationFrame(passo);
    });
  }

  // Botão mostra "Analisando…" ao enviar o formulário
  function estadoDoBotao() {
    var formulario = document.querySelector("form");
    if (!formulario) { return; }
    formulario.addEventListener("submit", function () {
      var botao = formulario.querySelector("button");
      botao.textContent = "Analisando…";
      botao.classList.add("carregando");
    });
  }

  animarNumeros();
  estadoDoBotao();
})();