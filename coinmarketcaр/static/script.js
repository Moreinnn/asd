document.getElementById('cryptoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const symbol = document.getElementById('symbol').value;
    const currency = document.getElementById('currency').value;

    fetch('/get_crypto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `symbol=${symbol}&currency=${currency}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('response').textContent = data.error;
        } else {
            let result = `Цена ${data.symbol}: ${data.price.toFixed(2)} ${currency.toUpperCase()}\n`;
            result += `Рыночная капитализация: ${data.market_cap.toFixed(2)} ${currency.toUpperCase()}\n`;
            result += `Объем торгов за 24 часа: ${data.volume_24h.toFixed(2)} ${currency.toUpperCase()}\n`;
            result += `Изменение цены за 1 час: ${data.percent_change_1h.toFixed(2)}%\n`;
            result += `Изменение цены за 24 часа: ${data.percent_change_24h.toFixed(2)}%\n`;
            result += `Изменение цены за 7 дней: ${data.percent_change_7d.toFixed(2)}%\n`;
            result += `Доступное предложение: ${data.circulating_supply}\n`;
            result += `Общее предложение: ${data.total_supply}\n`;
            result += `Максимальное предложение: ${data.max_supply || 'Неизвестно'}`;

            document.getElementById('response').textContent = result;
        }
    })
    .catch(error => {
        document.getElementById('response').textContent = 'Ошибка при получении данных';
    });
});