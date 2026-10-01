// SOCVision — Chart.js Visualizations

const COLORS = {
    critical: 'rgba(255, 0, 51, 0.85)',
    high:     'rgba(255, 145, 0, 0.85)',
    medium:   'rgba(255, 215, 64, 0.85)',
    low:      'rgba(0, 230, 118, 0.85)',
    blue:     'rgba(30, 144, 255, 0.85)',
    cyan:     'rgba(0, 212, 255, 0.85)',
};

const BORDER_COLORS = {
    critical: '#ff0033',
    high:     '#ff9100',
    medium:   '#ffd740',
    low:      '#00e676',
    blue:     '#1e90ff',
    cyan:     '#00d4ff',
};

Chart.defaults.color = '#8ea7cc';
Chart.defaults.borderColor = '#1e2d45';
Chart.defaults.font.family = "'Share Tech Mono', monospace";

function applyDarkPlugin() {
    return {
        id: 'darkBackground',
        beforeDraw(chart) {
            const ctx = chart.canvas.getContext('2d');
            ctx.save();
            ctx.globalCompositeOperation = 'destination-over';
            ctx.fillStyle = '#111827';
            ctx.fillRect(0, 0, chart.width, chart.height);
            ctx.restore();
        }
    };
}

// ===== Chart 1: Failed Logins Over Time =====
async function renderFailedLoginsChart() {
    const res = await fetch('/api/analytics/failed_logins');
    const data = await res.json();

    const ctx = document.getElementById('failedLoginsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        plugins: [applyDarkPlugin()],
        data: {
            labels: data.labels.length ? data.labels : ['No Data'],
            datasets: [{
                label: 'Failed Logins',
                data: data.data.length ? data.data : [0],
                borderColor: BORDER_COLORS.high,
                backgroundColor: 'rgba(255,145,0,0.08)',
                borderWidth: 2,
                pointBackgroundColor: BORDER_COLORS.high,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0d1320',
                    borderColor: '#1e2d45',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: '#1e2d45' },
                    ticks: { color: '#4a6080' }
                },
                y: {
                    grid: { color: '#1e2d45' },
                    ticks: { color: '#4a6080', stepSize: 1 },
                    beginAtZero: true
                }
            }
        }
    });
}

// ===== Chart 2: Alert Severity Distribution =====
async function renderSeverityChart() {
    const res = await fetch('/api/analytics/severity_distribution');
    const data = await res.json();

    const ctx = document.getElementById('severityChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        plugins: [applyDarkPlugin()],
        data: {
            labels: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
            datasets: [{
                data: [data.LOW, data.MEDIUM, data.HIGH, data.CRITICAL],
                backgroundColor: [
                    COLORS.low, COLORS.medium, COLORS.high, COLORS.critical
                ],
                borderColor: [
                    BORDER_COLORS.low, BORDER_COLORS.medium, BORDER_COLORS.high, BORDER_COLORS.critical
                ],
                borderWidth: 1.5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 16, font: { size: 11 } }
                },
                tooltip: {
                    backgroundColor: '#0d1320',
                    borderColor: '#1e2d45',
                    borderWidth: 1
                }
            }
        }
    });
}

// ===== Chart 3: Top Suspicious IPs =====
async function renderTopIpsChart() {
    const res = await fetch('/api/analytics/top_ips');
    const data = await res.json();

    const ctx = document.getElementById('topIpsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        plugins: [applyDarkPlugin()],
        data: {
            labels: data.labels.length ? data.labels : ['No Data'],
            datasets: [{
                label: 'Alert Count',
                data: data.data.length ? data.data : [0],
                backgroundColor: COLORS.blue,
                borderColor: BORDER_COLORS.blue,
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0d1320',
                    borderColor: '#1e2d45',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: '#1e2d45' },
                    ticks: { color: '#4a6080' }
                },
                y: {
                    grid: { color: '#1e2d45' },
                    ticks: { color: '#4a6080', stepSize: 1 },
                    beginAtZero: true
                }
            }
        }
    });
}

// ===== Chart 4: Event Type Distribution =====
async function renderEventTypeChart() {
    const res = await fetch('/api/analytics/event_types');
    const data = await res.json();

    const palette = [
        COLORS.blue, COLORS.cyan, COLORS.low, COLORS.medium,
        COLORS.high, COLORS.critical,
        'rgba(138,180,248,.8)', 'rgba(200,100,200,.8)'
    ];

    const ctx = document.getElementById('eventTypeChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        plugins: [applyDarkPlugin()],
        data: {
            labels: data.labels.length ? data.labels : ['No Data'],
            datasets: [{
                data: data.data.length ? data.data : [1],
                backgroundColor: palette.slice(0, data.labels.length),
                borderColor: '#111827',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 12, font: { size: 10 } }
                },
                tooltip: {
                    backgroundColor: '#0d1320',
                    borderColor: '#1e2d45',
                    borderWidth: 1
                }
            },
            cutout: '60%'
        }
    });
}

// ===== Init all charts =====
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('failedLoginsChart')) renderFailedLoginsChart();
    if (document.getElementById('severityChart'))     renderSeverityChart();
    if (document.getElementById('topIpsChart'))       renderTopIpsChart();
    if (document.getElementById('eventTypeChart'))    renderEventTypeChart();
});