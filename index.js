// ZYN EMPIRE - Main Entry Point
// Run: npm start
// Starts all bots with crash recovery

process.on('unhandledRejection', (reason, promise) => {
    console.error(`[CRASH] Unhandled Rejection at: ${promise}`, reason);
    // Don't exit — let the bot recover
});

process.on('uncaughtException', (error) => {
    console.error(`[CRASH] Uncaught Exception:`, error);
    // Don't exit immediately — give time for logs
    setTimeout(() => process.exit(1), 1000);
});

const { execSync } = require('child_process');
const path = require('path');

// Start all agents via PM2
console.log('===============================================');
console.log('ZYN EMPIRE - Starting All Bots');
console.log('===============================================');

try {
    const dir = path.dirname(__filename);
    process.chdir(dir);

    console.log('Starting noah-manager...');
    execSync('npx pm2 start noah_discord.js --name noah-manager', { stdio: 'inherit' });

    console.log('Starting auto-reports...');
    execSync('npx pm2 start auto_reports.js --name auto-reports', { stdio: 'inherit' });

    console.log('Starting zyn-agents...');
    execSync('npx pm2 start agents.js --name zyn-agents', { stdio: 'inherit' });

    console.log('\nAll bots started!');
    console.log('Run "pm2 list" to see status.');
    console.log('Run "pm2 logs <name>" to view logs.');
} catch (e) {
    console.error('Failed to start bots:', e.message);
    process.exit(1);
}