document.addEventListener('DOMContentLoaded', function() {
    const btnMedir = document.getElementById('btnMedir');
    const statusTxt = document.getElementById('status');

    if (btnMedir) {
        btnMedir.addEventListener('click', function() {
            btnMedir.disabled = true;
            statusTxt.innerText = "Solicitando leitura...";

            fetch('/medir', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    statusTxt.innerText = "Sucesso! Atualizando painel...";
                    setTimeout(() => window.location.reload(), 3000);
                })
                .catch(err => {
                    statusTxt.innerText = "Erro na solicitação.";
                    btnMedir.disabled = false;
                });
        });
    }

    const ctx = document.getElementById('meuGrafico');
    if (ctx) {
        const labels = JSON.parse(ctx.getAttribute('data-labels'));
        const dataTemp = JSON.parse(ctx.getAttribute('data-temp'));
        const dataUmid = JSON.parse(ctx.getAttribute('data-umid'));

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: dataTemp,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    fill: true,
                    tension: 0.3
                }, {
                    label: 'Umidade (%)',
                    data: dataUmid,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: false } }
            }
        });
    }
});