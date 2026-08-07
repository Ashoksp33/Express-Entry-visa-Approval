/* 
   CYBER Matrix Rain & Particle Canvas Engine
*/

class CyberMatrixEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.mode = 'matrix'; // 'matrix', 'nodes', 'hybrid'
    
    this.chars = 'アカサタナハマヤラワ0123456789ABCDEFJAVA_SPRING_BOOT_REST_API_SQL_PYTHON';
    this.fontSize = 14;
    this.columns = 0;
    this.drops = [];
    
    // Mouse interactivity
    this.mouse = { x: null, y: null, radius: 120 };
    this.particles = [];

    this.init();
  }

  init() {
    this.resize();
    window.addEventListener('resize', () => this.resize());
    
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    });

    this.createNodes();
    this.animate();
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.columns = Math.floor(this.canvas.width / this.fontSize);
    
    this.drops = [];
    for (let i = 0; i < this.columns; i++) {
      this.drops[i] = Math.floor(Math.random() * -100);
    }
  }

  createNodes() {
    const nodeCount = Math.floor((this.canvas.width * this.canvas.height) / 18000);
    this.particles = [];
    for (let i = 0; i < nodeCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        size: Math.random() * 2 + 1
      });
    }
  }

  drawMatrix() {
    // Semi-transparent background fade for matrix trail effect
    this.ctx.fillStyle = 'rgba(5, 6, 11, 0.08)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.ctx.font = `${this.fontSize}px 'Share Tech Mono', monospace`;

    for (let i = 0; i < this.drops.length; i++) {
      const text = this.chars.charAt(Math.floor(Math.random() * this.chars.length));
      const x = i * this.fontSize;
      const y = this.drops[i] * this.fontSize;

      // Glow head character
      if (Math.random() > 0.9) {
        this.ctx.fillStyle = '#ffffff';
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = '#00f0ff';
      } else if (i % 3 === 0) {
        this.ctx.fillStyle = '#ff0055';
        this.ctx.shadowBlur = 4;
        this.ctx.shadowColor = '#ff0055';
      } else {
        this.ctx.fillStyle = '#00f0ff';
        this.ctx.shadowBlur = 2;
        this.ctx.shadowColor = '#00f0ff';
      }

      this.ctx.fillText(text, x, y);
      this.ctx.shadowBlur = 0;

      if (y > this.canvas.height && Math.random() > 0.975) {
        this.drops[i] = 0;
      }

      this.drops[i]++;
    }
  }

  drawNodes() {
    this.ctx.fillStyle = 'rgba(5, 6, 11, 0.2)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw nodes
    for (let i = 0; i < this.particles.length; i++) {
      let p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

      // Interactivity with mouse
      if (this.mouse.x !== null) {
        let dx = this.mouse.x - p.x;
        let dy = this.mouse.y - p.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < this.mouse.radius) {
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(255, 0, 85, ${1 - dist / this.mouse.radius})`;
          this.ctx.lineWidth = 1;
          this.ctx.moveTo(p.x, p.y);
          this.ctx.lineTo(this.mouse.x, this.mouse.y);
          this.ctx.stroke();
        }
      }

      // Draw particle
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fillStyle = '#00f0ff';
      this.ctx.fill();

      // Connect nearby particles
      for (let j = i + 1; j < this.particles.length; j++) {
        let p2 = this.particles[j];
        let dx = p.x - p2.x;
        let dy = p.y - p2.y;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 100) {
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(0, 240, 255, ${0.2 * (1 - dist / 100)})`;
          this.ctx.lineWidth = 0.6;
          this.ctx.moveTo(p.x, p.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
        }
      }
    }
  }

  switchMode(newMode) {
    this.mode = newMode;
  }

  animate() {
    if (this.mode === 'matrix') {
      this.drawMatrix();
    } else if (this.mode === 'nodes') {
      this.drawNodes();
    } else {
      this.drawMatrix();
      this.drawNodes();
    }

    requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.matrixEngine = new CyberMatrixEngine('bg-canvas');
});
