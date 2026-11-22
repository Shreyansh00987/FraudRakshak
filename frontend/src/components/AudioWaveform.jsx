import React, { useEffect, useRef } from 'react';

export default function AudioWaveform({ isActive = false, color = 'blue' }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let phase = 0;

    const render = () => {
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      const numBars = 28;
      const barWidth = width / numBars - 3;
      const centerY = height / 2;

      let primaryColor = '#3B82F6'; // Blue
      if (color === 'crimson') primaryColor = '#EF4444';
      if (color === 'emerald') primaryColor = '#10B981';

      for (let i = 0; i < numBars; i++) {
        const x = i * (barWidth + 3);
        let barHeight = 4;

        if (isActive) {
          const wave = Math.sin(phase + i * 0.4) * 14;
          const wave2 = Math.cos(phase * 1.2 + i * 0.3) * 8;
          barHeight = Math.max(4, Math.abs(wave + wave2) + 4);
        } else {
          barHeight = 4;
        }

        const topY = centerY - barHeight / 2;

        ctx.fillStyle = primaryColor;
        ctx.beginPath();
        ctx.roundRect(x, topY, barWidth, barHeight, [2, 2, 2, 2]);
        ctx.fill();
      }

      phase += isActive ? 0.15 : 0;
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [isActive, color]);

  return (
    <div className="w-full flex items-center justify-center py-1">
      <canvas
        ref={canvasRef}
        width={280}
        height={36}
        className="w-full max-w-[280px] h-[36px]"
      />
    </div>
  );
}
