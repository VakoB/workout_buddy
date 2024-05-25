let loginBtn = document.getElementById('login-btn');

loginBtn.onclick = ()=>{
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    let url = '/auth/register';
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(
            {
                username: username,
                email: email,
                password: password
            }
        ),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('=======================================')
        console.log(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}