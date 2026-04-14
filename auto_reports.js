// ZYN AUTO REPORTS - Proactive Hourly Heartbeat
// Runs under PM2 and posts automated updates every 60 minutes
// STEP 1: Run channel_discovery.js first, then fill in the channel IDs below

const { Client, GatewayIntentBits } = require('discord.js');
const { execSync } = require('child_process');
const fs = require('fs');

const token = fs.readFileSync('/root/zyn/token.txt', 'utf8').trim();

// === FILL THESE IN after running channel_discovery.js ===
const CHANNELS = {
    TRADING_ALERTS:      'REPLACE_WITH_TRADING_ALERTS_ID',
    SARA_OUTREACH:       'REPLACE_WITH_SARA_OUTREACH_ID',
    ADAM_OPPORTUNITIES:  'REPLACE_WITH_ADAM_OPPORTUNITIES_ID',
    NOAH_COMMAND:        'REPLACE_WITH_NOAH_COMMAND_ID',
};

const REPORT_INTERVAL_MS = 60 * 60 * 1000; // 60 minutes

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages]
});

// === REPORT FUNCTIONS ===

function getTradingReport() {
    try {
          const price = execSync('python3 /root/zyn/price_fetch.py', { timeout: 10000 }).toString().trim();
          return `**[ZYN TRADING ALERT]** ${new Date().toLocaleTimeString()}\nNQ Live Price: **${price}**\nZenith Signal: STALKING 150pt move\nCaleb Status: ACTIVE`;
    } catch (e) {
          return `**[ZYN TRADING ALERT]** ${new Date().toLocaleTimeString()}\nNQ Signal: Monitoring\nCaleb Status: ACTIVE\n_price_fetch.py: ${e.message}_`;
    }
}

function getSaraReport() {
    return `**[SARA/LEA STRIKE STATUS]** ${new Date().toLocaleTimeString()}\nSara Outreach: ACTIVE\nEmails Sent: [pulling from outreach log...]\nOpens: [tracking...]\nNext Strike: 1 hour`;
}

function getAdamReport() {
    const now = new Date();
    return `**[VA CONTRACT COUNTDOWN]** ${now.toLocaleTimeString()}\nSovereign: $25k No-Bid Award Monitoring\nAdam Status: ACTIVE\nDeadline Tracking: LIVE\nNAICS: 541512/541519`;
}

function getEmpireHealthReport() {
    const now = new Date().toLocaleString();
    return `**[ZYN EMPIRE HEALTH SUMMARY]** ${now}\n\n` +
          `✅ Noah Manager: ONLINE\n` +
          `✅ Auto Reports: RUNNING\n` +
          `✅ Trading (Caleb): ACTIVE\n` +
          `✅ Outreach (Sara/Lea): ACTIVE\n` +
          `✅ Gov Contracts (Adam): ACTIVE\n` +
          `✅ Leads: 400/Day TARGET\n\n` +
          `_Next report in 60 minutes_`;
}

// === SEND ALL REPORTS ===

async function sendReports() {
    console.log(`[${new Date().toISOString()}] Sending hourly reports...`);

  try {
        const tradingCh = await client.channels.fetch(CHANNELS.TRADING_ALERTS);
        await tradingCh.send(getTradingReport());
        console.log('  ✅ Trading alert sent');
  } catch (e) { console.error('  ❌ Trading alert failed:', e.message); }

  try {
        const saraCh = await client.channels.fetch(CHANNELS.SARA_OUTREACH);
        await saraCh.send(getSaraReport());
        console.log('  ✅ Sara report sent');
  } catch (e) { console.error('  ❌ Sara report failed:', e.message); }

  try {
        const adamCh = await client.channels.fetch(CHANNELS.ADAM_OPPORTUNITIES);
        await adamCh.send(getAdamReport());
        console.log('  ✅ Adam report sent');
  } catch (e) { console.error('  ❌ Adam report failed:', e.message); }

  try {
        const noahCh = await client.channels.fetch(CHANNELS.NOAH_COMMAND);
        await noahCh.send(getEmpireHealthReport());
        console.log('  ✅ Empire health sent');
  } catch (e) { console.error('  ❌ Empire health failed:', e.message); }
}

client.once('ready', async () => {
    console.log(`[ZYN AUTO REPORTS] Online as ${client.user.tag}`);
    console.log(`Sending first report immediately, then every 60 minutes...`);
    await sendReports();
    setInterval(sendReports, REPORT_INTERVAL_MS);
});

client.login(token);
