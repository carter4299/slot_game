import React, { useState } from 'react';
import './App.css';
import Reel from './Reel';
import Timer from './Timer';
import useGameLogic from './useGameLogic';
import Login from './login';

function App() {
  const { reels, balance, spin_count, is_spinning, time, spin } = useGameLogic();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div id="app" className="app_container">
      <div className="reel_container">
        {reels.map((reel, index) => (
          <Reel key={`${spin_count}-${index}`} numbers={reel} />
        ))}
      </div>
      <button 
        onClick={spin} 
        className={`spin_button ${is_spinning ? 'disabled' : ''}`}
        disabled={is_spinning}
      >
        Respin
      </button>
      <div className="balance">
        Balance: ${balance}
      </div>
      <div>
        <Timer time={time} />
      </div>
      <div className="spin_count">
        Spin Count: {spin_count}
      </div>
    </div>
  );
}

export default App;
