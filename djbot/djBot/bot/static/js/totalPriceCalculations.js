let totalPriceElement = document.getElementById('totals');
let priceElement = document.getElementById('price');
let amountElement = document.getElementById('amount');

let rangeElement = document.getElementById('item-amount');

function calculatePriceTotal() {
    let amount = rangeElement.value;
    amountElement.innerHTML = amount;
    totalPriceElement.innerHTML = parseInt(priceElement.innerText) * amount;
}

rangeElement.addEventListener('change', calculatePriceTotal)