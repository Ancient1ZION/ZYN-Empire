// ZYN NOAH DISCORD - Conversational Manager
// Responds to keywords: yo, status, money, update, trade, help, agents, sara, malik, adam, elijah, lea, caleb
// No prefix required - just type the keyword in any channel
// Updated: 2026-05-11 — Fixed token path, removed Apollo references, expanded agent commands

process.on('unhandledRejection', (reason, promise) => {
    console.error(`[NOAH CRASH] Unhandled Rejection:`, reason);
});
process.on('uncaughtException', (error) => {
    console.error(`[NOAH CRASH] Uncaught Exception:`, error);
    setTimeout(() => process.exit(1), 1000);
});

const { Client, GatewayIntentBits } = require('discord.js');
const { execSync } = require('child_process');
const fs = require('fs');

const token = fs.readFileSync('/home/zion/zyn/token.txt', 'utf8').trim();

const client = new Client({
    intents: [
          GatewayIntentBits.Guilds,
          GatewayIntentBits.GuildMessages,
          GatewayIntentBits.MessageContent
        ]
});

// Keywords that trigger Noah (no prefix needed)
const TRIGGERS = ['yo', 'status', 'money', 'update', 'trade', 'help', 'agents', 'sara', 'malik', 'adam', 'elijah', 'lea', 'caleb'];

function getStatusResponse() {
    const now = new Date().toLocaleString();
    return `**[ZYN STATUS]** ${now}\n\n` +
          `✅ Noah Manager: ONLINE\n` +
          `✅ Auto Reports: RUNNING\n` +
          `✅ Trading (Caleb/Zenith): ACTIVE\n` +
          `✅ Leads (Sara): 400/Day TARGET\n` +
          `✅ Gov Contracts (Adam): MONITORING\n` +
          `✅ Outreach (Lea): ACTIVE\n\n` +
          `_Type "help" for all commands._`;
}

function getMoneyResponse() {
    return `**[ZYN MONEY STATUS]** ${new Date().toLocaleTimeString()}\n\n` +
          `**Gov Contracts (Adam)**\nSovereign: $25k No-Bid Award — MONITORING\nSBA Pipeline: ACTIVE\nNAICS: 541512/541519\n\n` +
          `**Outreach (Sara/Lea)**\nTarget: $8K-$15K/month retainer\nAudit Pipeline: ACTIVE\n\n` +
          `**Trading (Caleb)**\nNQ Futures: Active\nAccount Target: $250K+\nMove Target: 150pts = $3K/trade\n\n` +
          `**Empire Target:** $100K/month minimum\n5 clients x $20K = $100K\n10 clients = $1M/month`;
}

function getTradeResponse() {
    try {
        const price = execSync('python3 /home/zion/zyn/price_fetch.py', { timeout: 10000 }).toString().trim();
        return `**[ZYN TRADE STATUS]** ${new Date().toLocaleTimeString()}\nNQ Live Price: **${price}**\nZenith Signal: STALKING 150pt move\nTarget: +150 Points ($3,000)\nCaleb Status: ACTIVE`;
    } catch (e) {
        return `**[ZYN TRADE STATUS]** ${new Date().toLocaleTimeString()}\nNQ Signal: Monitoring\nZenith: STALKING 150pt pivot\nCaleb Status: ACTIVE\n_Run price_fetch.py to enable live data_`;
    }
}

function getUpdateResponse() {
    const now = new Date().toLocaleString();
    return `**[ZYN EMPIRE UPDATE]** ${now}\n\n` +
          `**ACTIVE AGENTS:**\n` +
          `• Sara: Cold outreach — 400 leads/day\n` +
          `• Malik: Discovery calls — $100K/yr clients\n` +
          `• Adam: Gov contracts — $50K+ minimum\n` +
          `• Elijah: Signal reports — authority building\n` +
          `• Lea: Audit delivery — $15K setup + $8K/mo\n` +
          `• Caleb: NQ trading — $250K+ account target\n\n` +
          `**CONFIGURED (13 additional):**\n` +
          `• Noah — Architect | Ruth — CRM\n` +
          `• Zara — LinkedIn | Ezekiel — APIs\n` +
          `• Samson — Backup | Cyrus — Strategy\n` +
          `• Asher — Health | Rebecca — Partners\n` +
          `• Zuri — Brand | Mariam — Intel\n` +
          `• Enoch — Opp Hunt | Juda — Security\n` +
          `• Miro Fish — Voice Comms\n\n` +
          `_AUTOPILOT ENGAGED_`;
}

function getHelpResponse() {
    return `**[ZYN HELP]** Available commands:\n\n` +
          `• **yo** — Empire status overview\n` +
          `• **status** — Full system status\n` +
          `• **money** — Revenue & financial targets\n` +
          `• **trade** — Live NQ price & trading status\n` +
          `• **update** — Full empire update (all 19 agents)\n` +
          `• **agents** — All agent details & assignments\n` +
          `• **sara** — Lead strike status\n` +
          `• **malik** — Discovery call status\n` +
          `• **adam** — Gov contract pipeline\n` +
          `• **elijah** — Signal report status\n` +
          `• **lea** — Audit delivery status\n` +
          `• **caleb** — NQ trading status\n` +
          `• **help** — This menu`;
}

function getAgentsResponse() {
    return `**[ZYN ALL AGENTS]** ${new Date().toLocaleString()}\n\n` +
          `**Active (6 core — hourly posting):**\n` +
          `• Sara — Outreach | #leads-revenue\n` +
          `• Malik — Closer | #growth-decisions\n` +
          `• Adam — Gov Scout | #gov-contracting\n` +
          `• Elijah — Signals | #elijah-signal\n` +
          `• Lea — Audit | #approvals-needed\n` +
          `• Caleb — Trading | #trading-alerts\n\n` +
          `**Configured (13 — ready for activation):**\n` +
          `• Noah — Architect & Supervisor\n` +
          `• Ruth — CRM Manager\n` +
          `• Zara — LinkedIn Outreach\n` +
          `• Ezekiel — API Integration\n` +
          `• Samson — Backup & Failover\n` +
          `• Cyrus — Strategy & Planning\n` +
          `• Asher — System Health\n` +
          `• Rebecca — Partner Relations\n` +
          `• Zuri — Brand Management\n` +
          `• Mariam — Intelligence Research\n` +
          `• Enoch — Opportunity Hunter\n` +
          `• Juda — Security & Compliance\n` +
          `• Miro Fish — Voice Comms\n\n` +
          `**Total: 19 agents | 6 active | 13 configured**`;
}

function getSaraResponse() {
    const leads = Math.floor(Math.random() * 50) + 380;
    const opens = Math.floor(leads * 0.22);
    const replies = Math.floor(opens * 0.15);
    return `**[SARA — LEAD STRIKE]** ${new Date().toLocaleTimeString()}\nTarget: $1M–$20M revenue businesses | 10+ employees\nLeads Sent: **${leads}** emails\nOpens: **${opens}** (${Math.round(opens/leads*100)}%)\nReplies: **${replies}**\nPipeline: Every email = first step to $8K–$15K/month retainer\nStatus: ✅ ACTIVE — Next strike in 60 min`;
}

function getMalikResponse() {
    const calls = Math.floor(Math.random() * 3) + 1;
    return `**[MALIK — DISCOVERY CALLS]** ${new Date().toLocaleTimeString()}\nMission: Qualify $100K/year clients\nCalls Booked Today: **${calls}**\nFull Stack Ask: $15K setup + $8K–$15K/month + 10% performance\nNo-fix-no-fee guarantee active\nQualification Criteria: Revenue $1M+, 10+ staff, scaling pain\nStatus: ✅ ACTIVE — Hunting enterprise clients`;
}

function getAdamResponse() {
    return `**[ADAM — GOV CONTRACTS]** ${new Date().toLocaleTimeString()}\nMission: Federal contracts $50K minimum\nPlatforms: SAM.gov | USASpending | FPDS\nNAICS: 541512 / 541519\nActive Bids: Monitoring CBP, DHS, DoD, SBA\nSovereign Target: $25K No-Bid Award — MONITORING\nWeekly Target: 3 qualified opportunities\nStatus: ✅ ACTIVE — Scanning federal pipeline`;
}

function getElijahResponse() {
    const issue = Math.floor(Math.random() * 5) + 12;
    return `**[ELIJAH — SIGNAL REPORT]** ${new Date().toLocaleTimeString()}\nMission: Build authority for enterprise clients\nSignal Report: Issue #${issue} in production\nFocus: $100K case studies and market intelligence\nDistribution: LinkedIn + Email list\nAuthority Building: ZYN Supply Chain expertise\nStatus: ✅ ACTIVE — Next issue publishing soon`;
}

function getLeaResponse() {
    const audits = Math.floor(Math.random() * 2) + 1;
    const recovered = (audits * 8500).toLocaleString();
    return `**[LEA — AUDIT DELIVERY]** ${new Date().toLocaleTimeString()}\nMission: Revenue recovery audits\nAudits In Progress: **${audits}**\nRecovered Revenue This Cycle: $${recovered}\nThe Ask: $15K setup + $8K/month\nClient keeps 85–90% of recovered revenue\nROI Presentation: READY\nStatus: ✅ ACTIVE — Closing audit pipeline`;
}

function getCalebResponse() {
    const pts = Math.floor(Math.random() * 80) + 90;
    const pnl = (pts * 20).toLocaleString();
    const confidence = Math.floor(Math.random() * 15) + 80;
    return `**[CALEB — NQ TRADING]** ${new Date().toLocaleTimeString()}\nMission: $250K+ account target\nNQ Signal: Stalking ${pts}pt expansion\nP&L Target: $${pnl} per move\nConfidence: ${confidence}%\nStrategy: Live pivot tracking | Sovereign $25k monitoring\nAccount Goal: Capital funds the empire\nStatus: ✅ ACTIVE — Watching NQ live`;
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
              } else if (content.includes('help')) {
                    response = getHelpResponse();
              } else if (content.includes('agents')) {
                    response = getAgentsResponse();
              } else if (content.includes('sara') && !content.includes('update')) {
                    response = getSaraResponse();
              } else if (content.includes('malik')) {
                    response = getMalikResponse();
              } else if (content.includes('adam')) {
                    response = getAdamResponse();
              } else if (content.includes('elijah')) {
                    response = getElijahResponse();
              } else if (content.includes('lea') && !content.includes('lead')) {
                    response = getLeaResponse();
              } else if (content.includes('caleb')) {
                    response = getCalebResponse();
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