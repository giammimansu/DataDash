// src/components/AnimatedBackground.jsx

import React, { useMemo } from 'react';
import { styled, keyframes } from '@mui/material/styles';

// Keyframes per l’animazione del gradiente
const gradientAnim = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

// Keyframes per il movimento delle icone
const floatUp = keyframes`
  0% { transform: translateY(100vh) rotate(0deg); }
  100% { transform: translateY(-20vh) rotate(360deg); }
`;

// Styled component per il background a gradiente animato
const GradientBg = styled('div')({
  position: 'absolute',
  width: '200%',
  height: '200%',
  top: '-50%',
  left: '-50%',
  background: 'linear-gradient(45deg, #0A1F44, #002B5B, #0A1F44, #002B5B)',
  backgroundSize: '400% 400%',
  animation: `${gradientAnim} 20s ease infinite`,
});

// Styled component per ciascuna icona che “galleggia”
const IconDiv = styled('div')(({ left, size, dur, delay }) => ({
  position: 'absolute',
  left,
  fontSize: size,
  opacity: 0.15,
  animation: `${floatUp} ${dur}s linear infinite`,
  animationDelay: delay,
}));

export default function AnimatedBackground() {
  // Calcolo memoizzato delle icone
  const icons = useMemo(() => {
    const types = ['🍴', '📊', '📈'];
    const max = 20;
    return Array.from({ length: max }).map((_, idx) => {
      const type = types[Math.floor(Math.random() * types.length)];
      const left = `${Math.random() * 100}vw`;
      const size = `${Math.random() * 30 + 20}px`;
      const dur = Math.random() * 15 + 10;
      const delay = `${Math.random() * -dur}s`;
      return { id: idx, type, left, size, dur, delay };
    });
  }, []);

  return (
    <>
      <GradientBg />
      {icons.map(({ id, type, left, size, dur, delay }) => (
        <IconDiv
          key={id}
          left={left}
          size={size}
          dur={dur}
          delay={delay}
        >
          {type}
        </IconDiv>
      ))}
    </>
  );
}
