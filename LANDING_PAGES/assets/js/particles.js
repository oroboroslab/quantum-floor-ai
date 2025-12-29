/**
 * Quantum Particles Animation
 * Creates an interactive particle system with quantum entanglement visualization
 */

class QuantumParticles {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.connections = [];
        this.mouse = { x: null, y: null, radius: 150 };
        this.config = {
            particleCount: 80,
            particleSize: 2,
            connectionDistance: 150,
            speed: 0.5,
            colors: {
                particle: '#00f0ff',
                connection: 'rgba(0, 240, 255, 0.15)',
                highlight: 'rgba(0, 240, 255, 0.4)'
            }
        };

        this.init();
    }

    init() {
        this.resize();
        this.createParticles();
        this.bindEvents();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        const count = this.getParticleCount();

        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * this.config.speed,
                vy: (Math.random() - 0.5) * this.config.speed,
                size: Math.random() * this.config.particleSize + 1,
                pulse: Math.random() * Math.PI * 2,
                entangled: Math.random() < 0.1 // 10% chance of being entangled
            });
        }
    }

    getParticleCount() {
        // Reduce particles on mobile for performance
        const isMobile = window.innerWidth < 768;
        return isMobile ? this.config.particleCount / 2 : this.config.particleCount;
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.createParticles();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        window.addEventListener('mouseout', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }

    update() {
        for (const p of this.particles) {
            // Update position
            p.x += p.vx;
            p.y += p.vy;

            // Pulse animation
            p.pulse += 0.02;

            // Boundary check with wrapping
            if (p.x < 0) p.x = this.canvas.width;
            if (p.x > this.canvas.width) p.x = 0;
            if (p.y < 0) p.y = this.canvas.height;
            if (p.y > this.canvas.height) p.y = 0;

            // Mouse interaction
            if (this.mouse.x !== null && this.mouse.y !== null) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.mouse.radius) {
                    const force = (this.mouse.radius - dist) / this.mouse.radius;
                    const angle = Math.atan2(dy, dx);
                    p.vx -= Math.cos(angle) * force * 0.02;
                    p.vy -= Math.sin(angle) * force * 0.02;
                }
            }

            // Speed limit
            const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
            if (speed > this.config.speed * 2) {
                p.vx = (p.vx / speed) * this.config.speed * 2;
                p.vy = (p.vy / speed) * this.config.speed * 2;
            }

            // Gradual velocity decay
            p.vx *= 0.99;
            p.vy *= 0.99;

            // Minimum velocity
            if (speed < this.config.speed * 0.5) {
                p.vx += (Math.random() - 0.5) * 0.1;
                p.vy += (Math.random() - 0.5) * 0.1;
            }
        }
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw connections first (behind particles)
        this.drawConnections();

        // Draw particles
        for (const p of this.particles) {
            this.drawParticle(p);
        }

        // Draw entanglement effects
        this.drawEntanglement();
    }

    drawParticle(p) {
        const pulseSize = p.size + Math.sin(p.pulse) * 0.5;

        // Glow effect
        const gradient = this.ctx.createRadialGradient(
            p.x, p.y, 0,
            p.x, p.y, pulseSize * 3
        );
        gradient.addColorStop(0, this.config.colors.particle);
        gradient.addColorStop(1, 'transparent');

        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, pulseSize * 3, 0, Math.PI * 2);
        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // Core
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, pulseSize, 0, Math.PI * 2);
        this.ctx.fillStyle = p.entangled ? '#a855f7' : this.config.colors.particle;
        this.ctx.fill();
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.config.connectionDistance) {
                    const opacity = 1 - (dist / this.config.connectionDistance);

                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = `rgba(0, 240, 255, ${opacity * 0.2})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }

        // Mouse connections
        if (this.mouse.x !== null && this.mouse.y !== null) {
            for (const p of this.particles) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.mouse.radius) {
                    const opacity = 1 - (dist / this.mouse.radius);

                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(this.mouse.x, this.mouse.y);
                    this.ctx.strokeStyle = `rgba(0, 240, 255, ${opacity * 0.4})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }

    drawEntanglement() {
        const entangled = this.particles.filter(p => p.entangled);

        if (entangled.length < 2) return;

        // Draw quantum entanglement lines between entangled particles
        for (let i = 0; i < entangled.length; i++) {
            for (let j = i + 1; j < entangled.length; j++) {
                const p1 = entangled[i];
                const p2 = entangled[j];

                // Animated dashed line
                this.ctx.beginPath();
                this.ctx.setLineDash([5, 10]);
                this.ctx.lineDashOffset = Date.now() / 50;
                this.ctx.moveTo(p1.x, p1.y);
                this.ctx.lineTo(p2.x, p2.y);
                this.ctx.strokeStyle = 'rgba(168, 85, 247, 0.3)';
                this.ctx.lineWidth = 1;
                this.ctx.stroke();
                this.ctx.setLineDash([]);
            }
        }
    }

    animate() {
        this.update();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new QuantumParticles('quantum-particles');
});
