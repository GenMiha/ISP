// Get all the elements in a form
let cardNumberElement = document.getElementById('id_card_number');
let cardHolderNameElement = document.getElementById('id_card_holder_name');
let cardExpirationMonthElement = document.getElementById('id_expiration_month');
let cardExpirationYearElement = document.getElementById('id_expiration_year');
let cardCVVNumberElement = document.getElementById('id_cvv_number');

let cardNumberValid = true;
let cardHolderNameValid = true;
let cardExpirationMonthValid = true;
let cardExpirationYearValid = true;
let cardCVVNumberValid = true;

let submitBtn = document.getElementById('submit_btn');

function addValidationClass(element, cls) {
	if (cls === 'valid') {
		element.classList.remove('invalid');
		element.classList.add('valid');
	} else {
		element.classList.remove('valid');
		element.classList.add('invalid');
	}

	if (
		cardNumberValid &&
		cardHolderNameValid &&
		cardExpirationMonthValid &&
		cardExpirationYearValid &&
		cardCVVNumberValid
	) {
		submitBtn.classList.remove('disabled');
	} else {
		submitBtn.classList.add('disabled');
	}
}

function cardNumberValidation(event) {
	let data = event.target.value;
	let regExp = /\D/g;
	if (regExp.test(data)) {
		cardNumberValid = false;
		addValidationClass(cardNumberElement, 'invalid');
		return;
	}

	console.log(cardNumberElement.value);
	// Card number we accept is only 16 chars long
	if (data.length !== 16) {
		cardNumberValid = false;
		addValidationClass(cardNumberElement, 'invalid');
	} else {
		cardNumberValid = true;
		addValidationClass(cardNumberElement, 'valid');
	}
}

function cardExpirationMonthValidation(event) {
	let data = event.target.value;
	let regExp = /\D/g;
	if (regExp.test(data)) {
		cardExpirationMonthValid = false;
		addValidationClass(cardExpirationMonthElement, 'invalid');
		return;
	}

	if (data > 12 || data < 1) {
		cardExpirationMonthValid = false;
		addValidationClass(cardExpirationMonthElement, 'invalid');
	} else {
		cardExpirationMonthValid = true;
		addValidationClass(cardExpirationMonthElement, 'valid');
	}
}

function cardExpirationYearValidation(event) {
	let data = event.target.value;
	let regExp = /\D/g;
	if (regExp.test(data)) {
		cardExpirationYearValid = false;
		addValidationClass(cardExpirationYearElement, 'invalid');
		return;
	}

	if (data.length !== 2) {
		cardExpirationYearValid = false;
		addValidationClass(cardExpirationYearElement, 'invalid');

	} else {
		cardExpirationYearValid = true;
		addValidationClass(cardExpirationYearElement, 'valid');
	}
}

function cardCVVNumberValidation(event) {
	let data = event.target.value;
	let regExp = /\D/g;
	if (regExp.test(data)) {
		cardCVVNumberValid = false;
		addValidationClass(cardCVVNumberElement, 'invalid');
		return;
	}

	if (data.length !== 3) {
		cardCVVNumberValid = false;
		addValidationClass(cardCVVNumberElement, 'invalid');
	} else {
		cardCVVNumberValid = true;
		addValidationClass(cardCVVNumberElement, 'valid');
	}
}

function cardHolderNameValidation(event) {
	let data = event.target.value;
	let regExp = /^[a-zA-Z]+\s[a-zA-Z]+$/g;
	if (regExp.test(data)) {
		cardHolderNameValid = true;
		addValidationClass(cardHolderNameElement, 'valid');
	} else {
		cardHolderNameValid = false;
		addValidationClass(cardHolderNameElement, 'invalid');
	}
}

// Adding validation functions to corresponding DOM elements
cardNumberElement.addEventListener('input', cardNumberValidation);
cardExpirationMonthElement.addEventListener('input', cardExpirationMonthValidation);
cardExpirationYearElement.addEventListener('input', cardExpirationYearValidation);
cardCVVNumberElement.addEventListener('input', cardCVVNumberValidation);
cardHolderNameElement.addEventListener('input', cardHolderNameValidation);