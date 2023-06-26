import React from 'react';

export default function Timer({ time }) {
    return (
        <div className="timer">
            Reshuffle: {Math.floor(time / 60)}:{time % 60 < 10 ? '0' : ''}{time % 60}
        </div>
    );
}
