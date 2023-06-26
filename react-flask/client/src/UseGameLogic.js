import { useState, useCallback, useEffect, useRef } from 'react';
import { get_balance, get_reels, reshuffle } from './api.js';

const useGameLogic = () => {
  const [reels, set_reels] = useState([]);
  const [balance, set_balance] = useState(0);
  const [spin_count, set_spin_count] = useState(0);
  const [is_spinning, set_is_spinning] = useState(false);
  const [time, set_time] = useState(5 * 60)

  const intervalRef = useRef();

  const spin = useCallback(() => {
    if (!is_spinning) {
        set_is_spinning(true);
        set_spin_count(spin_count => spin_count + 1);
        get_reels(set_reels);
        setTimeout(() => {
            set_is_spinning(false);
            get_balance(set_balance);
        }, 5600);
    }
  }, [is_spinning]);

  useEffect(() => {
    if (time >= 0) {
      intervalRef.current = setInterval(() => {
        set_time(time => time - 1);
      }, 600);
    } else {
      clearInterval(intervalRef.current);
      reshuffle().then((success) => {
        if (success) {
            set_time(5 * 60);
        }
      });
    }
  
    return () => clearInterval(intervalRef.current);
  }, [time]);

  return { reels, balance, spin_count, is_spinning, time, spin };
};

export default useGameLogic;
