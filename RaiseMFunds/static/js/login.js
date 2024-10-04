document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const isLoginMode = document.getElementById('submit-button').textContent.trim() === 'Login';
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
    const headers = document.getElementById('headers');
    const submitBtn = document.getElementById('submit-button');
    const toggleText = document.getElementById('toggle-text');

    if (submitBtn.textContent.trim() === 'Login') {
        headers.textContent = 'Sign Up';
        submitBtn.textContent = 'Sign Up';
        toggleText.innerHTML = 'Already have an account? <a href="#" id="toggleLink">Login</a>';
    } else {
        headers.textContent = 'Login';
        submitBtn.textContent = 'Login';
        toggleText.innerHTML = 'Don\'t have an account? <a href="#" id="toggleLink">Sign up</a>';
    }

    // Re-add event listener for the new toggle link after changing innerHTML
    document.getElementById('toggleLink').addEventListener('click', function (e) {
        e.preventDefault();
        toggleForm();
    });
}

// Add the initial event listener to the toggle link when the page loads
document.getElementById('toggleLink').addEventListener('click', function (e) {
    e.preventDefault();
    toggleForm();
});
