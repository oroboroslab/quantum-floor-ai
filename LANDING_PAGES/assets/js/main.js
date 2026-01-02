/**
 * Quantum-Floor AI - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initCopyButtons();
    initDemoTabs();
    initCounters();
    initSmoothScroll();
    initNavScroll();
    initDemos();
});

/**
 * Theme Toggle
 */
function initThemeToggle() {
    const toggle = document.getElementById('theme-toggle');
    const icon = toggle.querySelector('.theme-icon');

    // Check saved preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.setAttribute('data-theme', 'light');
        icon.textContent = '\u2600'; // Sun
    }

    toggle.addEventListener('click', () => {
        const isLight = document.body.getAttribute('data-theme') === 'light';

        if (isLight) {
            document.body.removeAttribute('data-theme');
            icon.textContent = '\u263E'; // Moon
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.setAttribute('data-theme', 'light');
            icon.textContent = '\u2600'; // Sun
            localStorage.setItem('theme', 'light');
        }
    });
}

/**
 * Copy to Clipboard Buttons
 */
function initCopyButtons() {
    const copyBtns = document.querySelectorAll('.copy-btn');

    copyBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const text = btn.dataset.copy;

            try {
                await navigator.clipboard.writeText(text);
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                btn.style.background = '#00ff88';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
}

/**
 * Demo Tabs
 */
function initDemoTabs() {
    const tabs = document.querySelectorAll('.demo-tab');
    const panels = document.querySelectorAll('.demo-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.demo;

            // Update tabs
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update panels
            panels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === `demo-${target}`) {
                    panel.classList.add('active');
                }
            });
        });
    });
}

/**
 * Animated Counters
 */
function initCounters() {
    const counters = document.querySelectorAll('.counter-value');

    const animateCounter = (counter) => {
        const target = parseInt(counter.dataset.target);
        const duration = 2000;
        const start = performance.now();

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(target * easeOutQuart);

            counter.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        };

        requestAnimationFrame(updateCounter);
    };

    // Use Intersection Observer to trigger animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

/**
 * Smooth Scrolling
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Navigation Scroll Effect
 */
function initNavScroll() {
    const nav = document.querySelector('.nav');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            nav.style.background = 'rgba(10, 10, 15, 0.95)';
        } else {
            nav.style.background = 'rgba(10, 10, 15, 0.8)';
        }

        lastScroll = currentScroll;
    });
}

/**
 * Initialize Demo Interactions
 */
function initDemos() {
    initRegisDemo();
    initAxisDemo();
    initCoreDemo();
}

/**
 * REGIS Demo
 */
function initRegisDemo() {
    const generateBtn = document.getElementById('regis-generate');
    const input = document.getElementById('regis-input');
    const output = document.getElementById('regis-output');
    const latencyDisplay = document.getElementById('regis-latency');

    if (!generateBtn) return;

    generateBtn.addEventListener('click', () => {
        const text = input.value.trim();
        if (!text) return;

        // Simulate loading
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        output.innerHTML = '<div class="audio-placeholder"><span>Generating audio...</span></div>';

        // Simulate API call with random latency
        const latency = Math.floor(Math.random() * 50 + 60); // 60-110ms

        setTimeout(() => {
            output.innerHTML = `
                <div style="text-align: center;">
                    <div style="background: linear-gradient(135deg, #00f0ff, #00b8d4); border-radius: 50%; width: 80px; height: 80px; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0a0a0f" stroke-width="2">
                            <polygon points="5 3 19 12 5 21 5 3"/>
                        </svg>
                    </div>
                    <p style="color: var(--text-secondary);">Audio generated successfully!</p>
                    <p style="color: var(--text-muted); font-size: 12px;">Duration: ${(text.length * 0.06).toFixed(1)}s | Size: ${(text.length * 0.5).toFixed(1)}KB</p>
                </div>
            `;
            latencyDisplay.textContent = `Latency: ${latency}ms`;
            latencyDisplay.style.color = latency < 100 ? '#00ff88' : '#ff6b35';

            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Speech';
        }, latency);
    });
}

/**
 * AXIS Demo
 */
function initAxisDemo() {
    const buttons = document.querySelectorAll('.instant-btn');
    const latencyDisplay = document.getElementById('axis-latency');

    if (!buttons.length) return;

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const text = btn.dataset.text;

            // Simulate ultra-fast response
            const startTime = performance.now();

            // Add active state
            btn.style.background = 'var(--primary)';
            btn.style.color = 'var(--bg-primary)';

            // Simulate instant response (8-25ms)
            const latency = Math.floor(Math.random() * 17 + 8);

            setTimeout(() => {
                const endTime = performance.now();
                const actualLatency = Math.round(endTime - startTime);

                latencyDisplay.textContent = `${latency} ms`;
                latencyDisplay.style.color = latency < 20 ? '#00ff88' : '#ff6b35';

                // Flash effect
                latencyDisplay.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    latencyDisplay.style.transform = 'scale(1)';
                }, 100);

                // Reset button
                setTimeout(() => {
                    btn.style.background = '';
                    btn.style.color = '';
                }, 200);
            }, latency);
        });
    });
}

/**
 * Connection-Core Demo
 */
function initCoreDemo() {
    const addBtn = document.getElementById('memory-add-btn');
    const searchBtn = document.getElementById('memory-search-btn');
    const addInput = document.getElementById('memory-input');
    const searchInput = document.getElementById('memory-search');
    const memoryList = document.getElementById('memory-list');
    const memoryCount = document.getElementById('memory-count');
    const memorySize = document.getElementById('memory-size');

    if (!addBtn) return;

    let memories = [
        { content: "User's name is Alice", importance: 0.8 },
        { content: "Prefers dark mode", importance: 0.7 },
        { content: "Python developer", importance: 0.6 }
    ];

    const renderMemories = (items) => {
        memoryList.innerHTML = items.map(m => `
            <div class="memory-item">
                <span class="memory-content">${m.content}</span>
                <span class="memory-importance">${m.importance.toFixed(1)}</span>
            </div>
        `).join('');
    };

    const updateStats = () => {
        memoryCount.textContent = memories.length;
        memorySize.textContent = `${(memories.length * 4)}KB`;
    };

    addBtn.addEventListener('click', () => {
        const content = addInput.value.trim();
        if (!content) return;

        const importance = Math.random() * 0.4 + 0.5; // 0.5-0.9
        memories.unshift({ content, importance });

        renderMemories(memories);
        updateStats();
        addInput.value = '';

        // Flash effect
        memoryList.firstElementChild.style.background = 'rgba(0, 240, 255, 0.2)';
        setTimeout(() => {
            memoryList.firstElementChild.style.background = '';
        }, 500);
    });

    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {
            renderMemories(memories);
            return;
        }

        // Simple search simulation
        const results = memories.filter(m =>
            m.content.toLowerCase().includes(query)
        ).sort((a, b) => b.importance - a.importance);

        renderMemories(results.length ? results : [{ content: 'No memories found', importance: 0 }]);
    });

    // Enter key support
    addInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addBtn.click();
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBtn.click();
    });
}

/**
 * Utility: Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
