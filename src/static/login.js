let cus = document.getElementById('cus_login');
let man = document.getElementById('man_login');

function cusfunc(){
    cus.style.display = "none";
    document.querySelector('#customer_login formarea').style.display = "flex";
    document.querySelector('#customer_login ').style.overflow = "auto";

    document.querySelector('.login-forms').style.gap = "0.5em";
}

function manfunc(){
    man.style.display = "none";
    console.log("drugs");
    document.querySelector('#manager_login formarea').style.display = "flex";
    document.querySelector('#manager_login ').style.overflow = "auto";
    document.querySelector('.login-forms').style.gap = "0.5em";

}
    cus.addEventListener('click', cusfunc);
    man.addEventListener('click', manfunc);
