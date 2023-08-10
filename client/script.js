/* jshint esversion: 6 */
/* jshint node: true */
/* jshint browser: true */
/* jshint jquery: true */
'use strict';

const BASE_URL = "http://127.0.0.1:5000/api/v1/";
const chars_to_encode = {
    ':': '%3A',
    '/': '%2F',
    '?': '%3F',
    '#': '%23',
    '[': '%5B',
    ']': '%5D',
    '@': '%40',
    '!': '%21',
    '$': '%24',
    '&': '%26',
    "'": '%27',
    '(': '%28',
    ')': '%29',
    '*': '%2A',
    '+': '%2B',
    ',': '%2C',
    ';': '%3B',
    '=': '%3D',
    '%': '%25',
    ' ': '%20',
}

async function requestData(option) {

    let length = document.querySelector(`#length-${option}`).value;
    let amount = document.querySelector(`#amount-${option}`).value;
    let checkbox = document.querySelectorAll('[type="checkbox"]:checked')[0]
    let resultStatus = document.querySelector("#result-status");

    resultStatus.innerHTML = "";
    resultStatus.classList.remove("text-info");
    resultStatus.classList.add("text-warning");

    if (length === "") {
        resultStatus.innerHTML = "(Need length)";
    } else if (parseInt(length) < 1 || parseInt(length) > 30) {
        resultStatus.innerHTML = "(Need length between 1-30)";
    } else if (checkbox === undefined && option == "password") {
        resultStatus.innerHTML = "(Need checkbox)";
    } else if (amount !== "" && (parseInt(amount) < 1 || parseInt(amount) > 20)) {
        resultStatus.innerHTML = "(Need amount between 1-20)";
    } else {

        let cat = (option == "password" ? checkbox.value : "words");
        let param  = document.querySelector(`#param-${option}`).value;
        let param_name = (option == "password" ? "omit" : "separator");
        let param_tidy = [];
        for (var idx = 0; idx < param.length; idx++) {
            if (param[idx] in chars_to_encode) {
                param_tidy.push(chars_to_encode[param[idx]]);
            } else {
                param_tidy.push(param[idx]);
            }
        }
        return fetch(`${BASE_URL}${cat}/${length}/${amount}?${param_name}=${param_tidy.join("")}`)
            .then(response => response.json())
            .then(json => printData(json))
            .catch(error => console.log(error))
    }
}

function copyPwd(pwd) {
    navigator.clipboard.writeText(pwd);
    let resultStatus = document.querySelector("#result-status");
    resultStatus.innerHTML = "(Copied)";
    resultStatus.classList.remove("text-warning");
    resultStatus.classList.add("text-info");
    setTimeout(function(){
        resultStatus.innerHTML = "";
    }, 700);
}

function printData(result) {
    let resultStatus = document.querySelector("#result-status");
    resultStatus.innerHTML = "";
    let responseDiv = document.querySelector("#response")
    responseDiv.innerHTML = 
        result.map(r => `
            <div class="input-group">
                <input
                    type="text" 
                    class="form-control bg-dark bg-dark text-info" 
                    aria-describedby="basic-addon3"
                    value="${r.password}"
                    disabled
                />
                <span 
                    class="input-group-text bg-dark text-white" 
                >
                    ${
                        r.entropy >= 100 ? "Very strong" : (
                        r.entropy >= 80 ? "Strong" : (
                        r.entropy >= 60 ? "Weak" : (
                        r.entropy >= 40 ? "Very weak" : "Avoid"
                    )))}
                </span>
                <button 
                    class="input-group-text bg-dark text-white"
                    onclick="copyPwd('${r.password}')"
                >
                    Copy
                </button>
            </div>
        `
    ).join('')
}

function optionChecked(id) {
    for (var i = 1; i <= 7; i++) {
        document.getElementById("checkbox-" + i).checked = false;
    }
    document.getElementById(id).checked = true;
}
