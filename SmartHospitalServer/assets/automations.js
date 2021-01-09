// Automating usernames and age to be filled in forms

const first_name_text = document.querySelector('input[name=first_name]');
const last_name_text = document.querySelector('input[name=last_name]');
const username_text = document.querySelector('input[name=username]');

const create_username_func = (first_name, last_name) => {
    return (first_name + ' ' + last_name).toString().toLowerCase().trim().replace(/[\s\W-]+/g, '-')
};

first_name_text.addEventListener('keyup', (e) => {
    username_text.setAttribute('value', create_username_func(first_name_text.value, last_name_text.value))
});

last_name_text.addEventListener('keyup', (e) => {
    username_text.setAttribute('value', create_username_func(first_name_text.value, last_name_text.value))
});

const date_text = document.querySelector('input[name=DOB]');
const age_text = document.querySelector('input[name=age]');

const find_age = (dateString) => {
    var today = new Date();
    var birthDate = new Date(dateString);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) 
    {
        age--;
    }
    return age;
};

date_text.addEventListener('keyup', (e) => {
    age_text.setAttribute('value', find_age(date_text.value))
});