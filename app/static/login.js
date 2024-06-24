let loginBtn = document.getElementById('login-btn');
let jwt_tokens;
const url_main = 'http://127.0.0.1:5000/main';
let url = 'http://127.0.0.1:5000/auth/login';
const url_refresh = 'http://127.0.0.1:5000/auth/refresh';


loginBtn.onclick = async function(event){

    await event.preventDefault();

    await login();
}

async function login(){

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    let url = 'http://127.0.0.1:5000/auth/login';
    try {
        let response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(
                {
                    username: username,
                    password: password
                }
            ),
            headers: {
                "Content-Type": "application/json; charset=UTF-8"
            }
        });
        let result = await response.json();

        if (!result.success) {
            alert(result.message);
        }
        else if(result.success){
            jwt_tokens = await result.tokens;
            localStorage.setItem('access', jwt_tokens.access);
            localStorage.setItem('refresh', jwt_tokens.refresh);
            // window.location.href = '/main';
            await fetchMainContent();

        }
    }
    catch(e){
        console.error('There was an error with the fetch operation: ', e);
    };

}


// ===================== fetch main content =================

async function fetchMainContent(){
    let accessItem = localStorage.getItem('access');
    if (!accessItem){
        console.error('No access token found');
    }
    try {
        let fetchContent = await fetch(url_main, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": `Bearer ${accessItem}`
            }
        });
    
        if (fetchContent.status == 401){
            await refreshToken();
            fetchContent = await fetch(url_main, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": `Bearer ${localStorage.getItem('access')}`
                }
            });
        }
    
        if (fetchContent.ok){
            console.log(fetchContent);
            window.location.href = '/main';
        }
        else{
            console.error('Failed to fetch data', fetchContent.status);
        }

    }catch(e) {
        console.error('There was a problem with the fetch operation:', e);
    }
}



// ===================== refresh token if it timed out =========================

async function refreshToken(){
    const refreshTokenVar = localStorage.getItem('refresh');

    if (!refreshTokenVar){
        console.error('Refresh token not found:', refreshTokenVar);
    }


    try {
        getNewToken = await fetch(url_refresh, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": `Bearer ${refreshTokenVar}`
            }
        });
    
        let newAccessToken = await getNewToken.json();
    
        if (newAccessToken.success){
            localStorage.setItem('access', newAccessToken.get('access_token'));
        }
        else{ 
            console.error('failed to refresh access.');
        }
    }catch (error){
        console.error('There was a problem with fetch operation', error);
    }
    
}
