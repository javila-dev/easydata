const container = document.getElementById('container');
const registerBtn = document.getElementById('forgot-pwd');
const gologinBtn = document.getElementById('go-to-login');
const loginBtn = document.getElementById('login');
const formsignin = document.getElementById('form-signin');
const formreset = document.getElementById('form-reset-pwd');
const btnrstpwd = document.getElementById('bntrstpwd');
const resetresult = document.getElementById('reset-result')
const atlanticloader = document.getElementById('app-loader')

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

gologinBtn.addEventListener('click', () => {
    let email = document.getElementById('emailforreset')
    container.classList.remove("active");
    resetresult.innerText = ''
    resetresult.classList.remove("green").remove("red");
    email.value = ''
    btnrstpwd.innerText = 'Solicitar'
    btnrstpwd.classList.remove("loader");
});

formsignin.addEventListener('submit', (event) => {
    atlanticloader.classList.add('active')
})


formreset.addEventListener('submit', (event) => {
    event.preventDefault();
    btnrstpwd.innerText = ''
    btnrstpwd.classList.add("loader");
    let email = document.getElementById('emailforreset').value
    form = new FormData()
    form.append('email',email)
    form.append('todo','sendmail')
    form.append('csrfmiddlewaretoken',getCookie('csrftoken'))
    postData('/accounts/passwordreset/', form)
    .then(data => {
      if (data.status == 'ok'){
        resetresult.innerText = '¡Enviamos las instrucciones al correo indicado!'
        resetresult.classList.add("green");
        
      }
      else{
        resetresult.innerText = 'El correo ingresado no está asociado a ningun usuario'
        resetresult.classList.add("red");
      }
        btnrstpwd.innerText = 'Solicitar'
        btnrstpwd.classList.remove("loader");; // JSON data parsed by `data.json()` call
    });
})

async function postData(url = '', form) {
    
    // Opciones por defecto estan marcadas con un *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      body:  form// body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }
  


