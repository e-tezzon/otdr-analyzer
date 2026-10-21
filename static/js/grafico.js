(function () {
  var canvas = document.getElementById("grafico");
  var fonte = document.getElementById("dados-medicao");
  if (!canvas || !fonte || !window.Chart) { return; }

  var dados = JSON.parse(fonte.textContent);
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NOMES = { inicio: "Início", emenda: "Emenda", conector: "Conector", fim: "Fim" };

  function nome(tipo) { return NOMES[tipo] || tipo; }

  // Transforma os eventos nos pontos da curva (a linha desce a cada perda)
  function montarCurva(eventos, limites) {
    var linha = [{ x: 0, y: 0 }];
    var marcas = [];
    var nivel = 0;

    eventos.forEach(function (e) {
      var limite = limites[e.tipo];
      var ruim = limite !== undefined && e.perda_db > limite;
      var antes = nivel;
      nivel = Math.round((nivel - e.perda_db) * 1000) / 1000;
      linha.push({ x: e.distancia_km, y: antes });
      linha.push({ x: e.distancia_km, y: nivel, ruim: ruim });
      marcas.push({ x: e.distancia_km, y: nivel, ev: e, ruim: ruim, limite: limite });
    });

    return { linha: linha, marcas: marcas };
  }

  function textoDoTitulo(e) {
    var valor = e.perda_db > 0 ? "-" + e.perda_db.toFixed(2) : "0.00";
    return "Perda de " + valor + " dB | " + nome(e.tipo);
  }

  function textoDoDetalhe(m) {
    var linhas = ["Posição: " + m.ev.distancia_km + " km", "Reflectância: " + m.ev.reflectancia_db + " dB"];
    if (m.limite !== undefined) {
      var excesso = m.ev.perda_db - m.limite;
      linhas.push("Limite: " + m.limite + " dB");
      linhas.push(excesso > 0 ? "Excesso: +" + excesso.toFixed(2) + " dB" : "Dentro do limite");
    }
    return linhas;
  }

  function criarGrafico(curva) {
    var marcas = curva.marcas;
    var minimo = Math.min.apply(null, marcas.map(function (m) { return m.y; }));
    var maxKm = Math.max.apply(null, marcas.map(function (m) { return m.x; }));

    return new Chart(canvas, {
      type: "line",
      data: {
        datasets: [
          {
            label: "Sinal",
            data: curva.linha,
            borderColor: "#12263a",
            borderWidth: 3,
            tension: 0,
            pointRadius: 0,
            pointHoverRadius: 0,
            pointHitRadius: 0,
            segment: {
              borderColor: function (c) { return c.p1.raw.ruim ? "#c8382b" : "#12263a"; },
              borderWidth: function (c) { return c.p1.raw.ruim ? 5 : 3; }
            }
          },
          {
            label: "Eventos",
            data: marcas,
            showLine: false,
            pointRadius: function (c) { return c.raw && c.raw.ruim ? 8 : 5; },
            pointHoverRadius: function (c) { return c.raw && c.raw.ruim ? 15 : 11; },
            pointHitRadius: 14,
            pointBackgroundColor: function (c) { return c.raw && c.raw.ruim ? "#c8382b" : "#12263a"; },
            pointBorderColor: "#ffffff",
            pointBorderWidth: 2,
            pointHoverBorderWidth: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: reduzir ? false : { duration: 1200, easing: "easeOutQuart" },
        transitions: { active: { animation: { duration: 250 } } },
        interaction: { mode: "nearest", intersect: true },
        scales: {
          x: { type: "linear", min: 0, max: maxKm, title: { display: true, text: "Distância (km)" } },
          y: { max: 0.1, min: minimo - 0.2, title: { display: true, text: "Nível relativo do sinal (dB)" } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            filter: function (item) { return item.datasetIndex === 1; },
            displayColors: false,
            backgroundColor: "#12263a",
            padding: 12,
            titleFont: { size: 14, weight: "bold" },
            callbacks: {
              title: function (itens) { return textoDoTitulo(itens[0].raw.ev); },
              label: function (item) { return textoDoDetalhe(item.raw); }
            }
          }
        }
      }
    });
  }

  // Ao passar o mouse na tabela, o ponto da falha cresce no gráfico
  function ligarTabela(grafico, marcas) {
    document.querySelectorAll("tr[data-km]").forEach(function (linhaTabela) {
      var km = parseFloat(linhaTabela.dataset.km);
      var indice = marcas.findIndex(function (m) { return m.x === km && m.ruim; });

      linhaTabela.addEventListener("mouseenter", function () {
        if (indice < 0) { return; }
        var ativo = [{ datasetIndex: 1, index: indice }];
        grafico.setActiveElements(ativo);
        grafico.tooltip.setActiveElements(ativo, { x: 0, y: 0 });
        grafico.update();
      });
      linhaTabela.addEventListener("mouseleave", function () {
        grafico.setActiveElements([]);
        grafico.tooltip.setActiveElements([], { x: 0, y: 0 });
        grafico.update();
      });
    });
  }

  var curva = montarCurva(dados.eventos, dados.limites);
  var grafico = criarGrafico(curva);
  ligarTabela(grafico, curva.marcas);
})();