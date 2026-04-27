// SVG Icons for Aurora Website
const svgIcons = {
    robot: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>',
    atom: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    cosmos: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/><path d="M12 2a14.5 14.5 0 0 1 0 20 14.5 14.5 0 0 1 0-20"/></svg>',
    lightbulb: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2v1"/><path d="M12 18v-2a4 4 0 0 0-4-4c0-1.5.5-2 2-2"/><path d="M12 14a4 4 0 0 0 4-4c0-1.5-.5-2-2-2"/><path d="M4.93 4.93l.7.7"/><path d="M17.66 17.66l.7.7"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-.7.7"/><path d="M19.07 4.93l-.7.7"/></svg>',
    chart: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    brain: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>',
    globe: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    scales: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
    microscope: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/></svg>',
    handshake: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m11 17 2 2a1 1 0 1 1-1.41 1.41L9.5 18.08"/><path d="m7.5 14.08 2 2a1 1 0 1 1-1.41 1.41L6 16.5"/><path d="m10.5 11.08 2 2a1 1 0 1 1-1.41 1.41L9 13.5"/><path d="M16.5 6.5a1 1 0 0 1 1.41 1.41l-8.5 8.5a1 1 0 0 1-1.41-1.41l8.5-8.5a1 1 0 0 1 1.41 0Z"/><path d="m19 3-1.5 1.5"/><path d="M22 22l-5-10-5 10"/><path d="M17 22V7"/><path d="M3 22h18"/></svg>',
    rocket: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
    masks: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12a5 5 0 0 0 5 5 8 8 0 0 1 5 2 8 8 0 0 1 5-2 5 5 0 0 0 5-5V7h-5a8 8 0 0 0-5-2 8 8 0 0 0-5 2H2z"/><path d="M6 11c1.5 0 3 .5 3 2-1.5 0-3-.5-3-2ZM18 11c-1.5 0-3 .5-3 2 1.5 0 3-.5 3-2Z"/></svg>',
    meditation: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10 10 10 0 0 0-10-10z"/><circle cx="12" cy="12" r="3"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>',
    computer: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>',
    cloud: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19c0-3.037-2.463-5.5-5.5-5.5S6.5 15.963 6.5 19"/><path d="M17.5 19c2.485 0 4.5-2.015 4.5-4.5S19.985 10 17.5 10c-.535 0-1.045.095-1.515.268A4.5 4.5 0 0 0 7.5 6c-2.485 0-4.5 2.015-4.5 4.5s2.015 4.5 4.5 4.5"/></svg>',
    refresh: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/></svg>',
    lock: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    target: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    gear: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M12 2v2"/><path d="M12 22v-2"/><path d="m17 20.66-1-1.73"/><path d="M11 10.27 7 3.34"/><path d="m20.66 17-1.73-1"/><path d="m3.34 7 1.73 1"/><path d="M14 12h8"/><path d="M2 12h2"/><path d="m20.66 7-1.73 1"/><path d="m3.34 17 1.73-1"/><path d="m17 3.34-1 1.73"/><path d="M11 13.73 7 20.66"/></svg>',
    network: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" x2="6" y1="6" y2="6"/><line x1="6" x2="6" y1="18" y2="18"/></svg>',
    heart: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    art: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>',
    barChart: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>',
    lineChart: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    alert: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    search: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    document: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>',
    lightning: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    wrench: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    check: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    shield: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>',
    folder: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    key: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="8.5" r="4.5"/><path d="m21 21-1-1"/><path d="M21 3l-1 1"/><path d="M3 21l1-1"/><path d="M3 3l1 1"/><path d="M9 12h6"/><path d="M12 9v6"/><path d="M15 12l-3-3"/><path d="M12 15l3-3"/></svg>',
    graduation: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
    muscle: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 11V4"/><path d="M13 11l-2.5 2.5"/><path d="M13 11l2.5 2.5"/><path d="M6 13h12"/><path d="M10 17h4"/><path d="M6 20a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2Z"/></svg>',
    chartDown: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/><polyline points="2 12 6 12 9 3 15 21 18 12 22 12"/></svg>',
    database: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    warning: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    unlock: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>',
    infinity: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Z"/><path d="M12 12c2-2.67 4-4 6-4a4 4 0 1 1 0 8c-2 0-4-1.33-6-4Z"/></svg>',
    sparkle: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>',
    music: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    star: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    save: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>',
    pin: '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="17" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>'
};

function replaceEmojisWithSVGs() {
    console.log('SVG icon replacement script loaded');
    
    const iconMappings = {
        '🤖': svgIcons.robot,
        '⚛️': svgIcons.atom,
        '🌌': svgIcons.cosmos,
        '💡': svgIcons.lightbulb,
        '📈': svgIcons.chart,
        '🧠': svgIcons.brain,
        '🌍': svgIcons.globe,
        '⚖️': svgIcons.scales,
        '🔬': svgIcons.microscope,
        '🤝': svgIcons.handshake,
        '🚀': svgIcons.rocket,
        '🎭': svgIcons.masks,
        '🧘': svgIcons.meditation,
        '💻': svgIcons.computer,
        '☁️': svgIcons.cloud,
        '🔄': svgIcons.refresh,
        '🔒': svgIcons.lock,
        '🎯': svgIcons.target,
        '⚙️': svgIcons.gear,
        '🌐': svgIcons.network,
        '💜': svgIcons.heart,
        '🎨': svgIcons.art,
        '📊': svgIcons.barChart,
        '📈': svgIcons.lineChart,
        '🚨': svgIcons.alert,
        '🔍': svgIcons.search,
        '📝': svgIcons.document,
        '⚡': svgIcons.lightning,
        '🔧': svgIcons.wrench,
        '✅': svgIcons.check,
        '🛡️': svgIcons.shield,
        '🗂️': svgIcons.folder,
        '🔐': svgIcons.key,
        '🎓': svgIcons.graduation,
        '💪': svgIcons.muscle,
        '📉': svgIcons.chartDown,
        '🗄️': svgIcons.database,
        '⚠️': svgIcons.warning,
        '🆓': svgIcons.unlock,
        '∞': svgIcons.infinity,
        '✨': svgIcons.sparkle,
        '🎵': svgIcons.music,
        '🌟': svgIcons.star,
        '💾': svgIcons.save,
        '📍': svgIcons.pin
    };

    let replacedCount = 0;
    
    document.querySelectorAll('.card-icon').forEach(icon => {
        const emoji = icon.textContent.trim();
        console.log('Found card-icon with content:', emoji);
        if (iconMappings[emoji]) {
            icon.innerHTML = iconMappings[emoji];
            icon.classList.add('svg-icon');
            replacedCount++;
            console.log('Replaced emoji:', emoji);
        }
    });

    document.querySelectorAll('.feature-visual').forEach(icon => {
        const emoji = icon.textContent.trim();
        console.log('Found feature-visual with content:', emoji);
        if (iconMappings[emoji]) {
            icon.innerHTML = iconMappings[emoji];
            icon.classList.add('svg-icon');
            replacedCount++;
            console.log('Replaced emoji:', emoji);
        }
    });
    
    console.log('Total emojis replaced:', replacedCount);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', replaceEmojisWithSVGs);
} else {
    replaceEmojisWithSVGs();
}

