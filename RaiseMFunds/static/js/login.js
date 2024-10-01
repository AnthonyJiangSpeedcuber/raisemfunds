document.getElementById('BOBBY').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('passsord').value;

    const isLoginMode = document.getElementById('submit-button').textContent === 'Login';
    const url = isLoginMode ? '/checkLogin' : '/registerUser';

    const payload = { email, password };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('debug').textContent = isLoginMode ? 'Login successful!' : 'Registration successful!';
            document.getElementById('debug').style.color = 'green';
        } else {
            document.getElementById('debug').textContent = data.error || (isLoginMode ? 'Login failed. Please try again.' : 'Registration failed. Please try again.');
            document.getElementById('debug').style.color = 'red';
        }
    })
    .catch(error => {
        document.getElementById('debug').textContent = 'An error occurred. Please try again.';
        document.getElementById('debug').style.color = 'red';
    });
});

function toggleForm() {
    const Dude = document.getElementById('Dude');
    const submitBtn = document.getElementById('submit-button');
    const toggleText = document.getElementById('toggle-text');

    if (submitBtn.textContent === 'Login') {
        Dude.textContent = 'Sign Up';
        submitBtn.textContent = 'Sign Up';
        toggleText.innerHTML = 'Already have an account? <a href="#" id="toggleLink">Login</a>';
    } else {
        Dude.textContent = 'Login';
        submitBtn.textContent = 'Login';
        toggleText.innerHTML = 'Don\'t have an account? <a href="#" id="toggleLink">Sign up</a>';
    }

    document.getElementById('toggleLink').addEventListener('click', function (e) {
        e.preventDefault();
        toggleForm();
    });
}

document.getElementById('toggleLink').addEventListener('click', function (e) {
    e.preventDefault();
    toggleForm();
});
