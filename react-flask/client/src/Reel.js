import React from 'react';
import { animated, useSpring } from 'react-spring';

function Reel({ numbers }) {
  const props = useSpring({
    from: { transform: 'translateY(0%)' },
    to: { transform: `translateY(-${100 * ((numbers.length - 3) / numbers.length)}%)` },
    config: {
      duration: numbers.length * 100 // you can tweak this to adjust the speed of the animation
    },
    reset: false,
  });

  return (
    <div style={{ overflow: 'hidden', height: '550px', width: '100px', display: 'block', margin: '0px 25px', justifyContent: 'center', alignItems: 'center', padding: '25px'}}>
      <animated.div style={props}>
        {numbers.map((num, index) => (
          <div key={index} style={{ height: '175px', width: '100px', paddingBlock: '10px'}}>
            <img src={`card_imgs/im${num}.png`} alt={`img${num}`} style={{ height: '150px', width: '100px', border: '5px solid #921115' }} />
          </div>
        ))}
      </animated.div>
    </div>
  );
}

export default Reel;
