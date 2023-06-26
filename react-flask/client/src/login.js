import React, { useState } from 'react';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const sanitizedUsername = username.replace(/\s+/g, '');
    
    if (sanitizedUsername.length < 4 || sanitizedUsername.length > 24) {
      alert("Username must be between 4 and 24 characters without spaces.");
      return;
    }

    for (let i = 0; i < sanitizedUsername.length; i++) {
      const charCode = sanitizedUsername.charCodeAt(i);
      if (charCode < 33 || charCode > 126) {
        alert("Username must only contain ASCII characters.");
        return;
      }
    }

    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: sanitizedUsername })
    });

    const data = await response.json();

    if (data.success) {
      onLogin();
    } else {
      alert("Invalid username. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Login-Key:
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
      </label>
      <input type="submit" value="Login" />
    </form>
  );
};

export default Login;
