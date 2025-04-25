const form = document.getElementById("contactForm");
const username = document.getElementById("name");
const email = document.getElementById("email");
const subject = document.getElementById("subject");
const message = document.getElementById("message");

function validateInputs() {
    var es_valido = true;
    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const subjectValue = subject.value.trim();
    const messageValue = message.value.trim();

    if(usernameValue === "") {
        setError(username, "Necesitas ingresar un nombre.");
        es_valido = false;
    } else {
        setSuccess(username);
    }

    if(emailValue === "") {
        setError(email, "Necesitas ingresar un mail");
        es_valido = false;
    } else if (!isValidEmail(emailValue)) {
        setError(email, "Ese mail no es valido.");
        es_valido = false;
    } else {
        setSuccess(email);
    }

    if(subjectValue === "") {
        setError(subject, "Necesitas agregar un asunto.");
        es_valido = false;
    } else {
        setSuccess(subject)
    }

    if (messageValue === "") {
        setError(message, "Necesitas agregar un mensaje.");
        es_valido = false;
    } else {
        setSuccess(message)
    }

    return es_valido;
}

function setError(input, message){
    const formGroup = input.parentElement; 
    const small = formGroup.querySelector("small");
    small.innerText = message;
    formGroup.className = "form-group error";
}

function setSuccess(input) {
    const formGroup = input.parentElement;
    formGroup.className = "form-group success"
}

function isValidEmail(email){
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 4500);
});