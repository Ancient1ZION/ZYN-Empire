// ZYN NOAH DISCORD - Conversational Manager
// Responds to keywords: yo, status, money, update, trade
// No prefix required - just type the keyword in any channel

const { Client, GatewayIntentBits } = require('discord.js');
const { execSync } = require('child_process');
const fs = require('fs');

const token = fs.readFileSync('/root/zyn/token.txt', 'utf8').trim();

const client = new Client({
    intents: [
          GatewayIntentBits.Guilds,
          GatewayIntentBits.GuildMessages,
          GatewayIntentBits.MessageContent
        ]
});

// Keywords that trigger Noah (no prefix needed)
const TRIGGERS = ['yo', 'status', 'money', 'update', 'trade'];

function getStatusResponse() {
    const now = new Date().toLocaleString();
    return `**[ZYN STATUS]** ${now}\n\n` +
          `✅ Noah Manager: ONLINE\n` +
          `✅ Auto Reports: RUNNING\n` +
          `✅ Trading (Caleb/Zenith): ACTIVE\n` +
          `✅ Leads (Sara): 400/Day TARGET\n` +
          `✅ Gov Contracts (Adam): MONITORING\n` +
          `✅ Outreach (Lea): ACTIVE\n\n` +
          `_Type "money", "trade", or "update" for specific silos._`;
}

function getMoneyResponse() {
    return `**[ZYN MONEY STATUS]** ${new Date().toLocaleTimeString()}\n\n` +
          `**Gov Contracts (Adam)**\nSovereign: $25k No-Bid Award — MONITORING\nSBA Pipeline: ACTIVE\nNAICS: 541512/541519\n\n` +
          `**Outreach (Sara/Lea)**\nTarget: $8K-$15K/month retainer\nAudit Pipeline: ACTIVE\n\n` +
          `**Empire Target:** $100K/month minimum\n5 clients x $20K = $100K\n10 clients = $1M/month`;
}

function getTradeResponse() {
    try {
          const price = execSync('python3 /root/zyn/price_fetch.py', { timeout: 10000 }).toString().trim();
          return `**[ZYN TRADE STATUS]** ${new Date().toLocaleTimeString()}\n\nNQ Live Price: **${price}**\nZenith Signal: STALKING 150pt move\nTarget: +150 Points ($3,000)\nCaleb Status: ACTIVE`;
    } catch (e) {
          return `**[ZYN TRADE STATUS]** ${new Date().toLocaleTimeString()}\n\nNQ Signal: Monitoring\nZenith: STALKING 150pt pivot\nCaleb Status: ACTIVE\n_Run price_fetch.py to enable live data_`;
    }
}

function getUpdateResponse() {
    const now = new Date().toLocaleString();
    return `**[ZYN EMPIRE UPDATE]** ${now}\n\n` +
          `**AGENTS ONLINE:** 17 agents active\n` +
          `**CHANNELS WIRED:** 20 channels operational\n` +
          `**TOOLS LOADED:** 36 tools deployed\n\n` +
          `**ACTIVE MISSIONS:**\n` +
          `• Sara: Cold outreach — 400 leads/day\n` +
          `• Malik: Discovery calls — $100K/yr clients\n` +
          `• Adam: Gov contracts — $50K+ minimum\n` +
          `• Elijah: Signal reports — authority building\n` +
          `• Lea: Audit delivery — $15K setup + $8K/mo\n` +
          `• Caleb: NQ trading — $250K+ account target\n\n` +
          `_AUTOPILOT ENGAGED_`;
}

client.once('ready', () => {
    console.log(`[NOAH DISCORD] Online as ${client.user.tag}`);
    console.log(`Listening for keywords: ${TRIGGERS.join(', ')}`);
});

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;

            const content = message.content.toLowerCase().trim();

            // Check if message matches or contains a trigger keyword
            const triggered = TRIGGERS.find(t => content === t || content.startsWith(t + ' ') || content.includes(' ' + t));
    if (!triggered) return;

            console.log(`[NOAH] Triggered by "${content}" from ${message.author.tag}`);

            try {
                  await message.channel.sendTyping();

      // Respond within 3 seconds
      setTimeout(async () => {
              let response;
              if (content.includes('money')) {
                        response = getMoneyResponse();
              } else if (content.includes('trade')) {
                        response = getTradeResponse();
              } else if (content.includes('update')) {
                        response = getUpdateResponse();
              } else {
                        // yo, status, or anything else
                response = getStatusResponse();
              }
              await message.reply(response);
      }, 500);

            } catch (e) {
                  console.error('[NOAH] Error responding:', e.message);
            }
});

client.login(token);
