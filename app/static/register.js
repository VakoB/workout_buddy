let loginBtn = document.getElementById('login-btn');

loginBtn.onclick = (event)=>{

    event.preventDefault();

    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    let url = 'http://127.0.0.1:5000/auth/register';
    fetch(url, {
        method: "POST",
        body: JSON.stringify(
            {
                username: username,
                email: email,
                password: password
            }
        ),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    }).then(response => {
        return response.json();
    })
    .then(result => {
        if (!result.success) {
            alert(result.message);
        }
        else{
            window.location.href = '/auth/login';
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}