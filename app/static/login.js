
let loginBtn = document.getElementById('login-btn');
let jwt_tokens;
const url_main = 'http://127.0.0.1:5000/main';
const url_login = 'http://127.0.0.1:5000/auth/login';
const url_refresh = 'http://127.0.0.1:5000/auth/refresh';


loginBtn.onclick = async function(event){

    await event.preventDefault();

    await login();
}

async function login(){
    console.log('Entered the login function where i try to POST username and password into /auth/login.');
    console.log('if result is successful, i save access and refresh token in local browser storage.');
    console.log('im calling fetchMainContent function')

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    try {
        let response = await fetch(url_login, {
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
    console.log('Im in fetchMainContent function.');
    console.log('getting access token from local storage, checking if it exists.');

    
    let accessItem = localStorage.getItem('access');
    if (!accessItem){
        console.error('No access token found');
    }
    try {
        console.log('attepting to GET /main endpoint with the eccess key.');
        console.log(`the access key im gonna send in headers: ${localStorage.getItem('access')}`)
        const token = `Bearer ${localStorage.getItem('access')}`;
        console.log(token);

        let fetchContent = await fetch(url_main, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": token,
            }
        });
    
        if (fetchContent.status == 401){

            console.log('fetchContent.status == 401 -its expired so ill attempt to use refresh token');
            console.log('calling refreshToken function...');
            await refreshToken();
            console.log('attepting to GET /main endpoint with the new eccess key.');
            
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
    console.log('Im in refreshToken function');
    console.log('Got refresh token from local storage');
    const refreshTokenVar = localStorage.getItem('refresh');

    if (!refreshTokenVar){
        console.error('Refresh token not found:', refreshTokenVar);
    }


    try {
        console.log('');
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
            console.log(`new access token: ${newAccessToken.get('access_token')}`);
        }
        else{ 
            console.error('failed to refresh access.');
        }
    }catch (error){
        console.error('There was a problem with fetch operation', error);
    }
    
}
