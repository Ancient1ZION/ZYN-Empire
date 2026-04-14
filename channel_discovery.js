// ZYN Channel Discovery Script
// Run once to list all channel names and IDs in the server
// Usage: node channel_discovery.js

const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');

const token = fs.readFileSync('/root/zyn/token.txt', 'utf8').trim();

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.once('ready', () => {
    console.log(`\n=== ZYN EMPIRE CHANNEL DISCOVERY ===`);
  console.log(`Bot: ${client.user.tag}\n`);

  client.guilds.cache.forEach(guild => {
        console.log(`\nSERVER: ${guild.name} (${guild.id})`);
    console.log('--- CHANNELS ---');
    guild.channels.cache
            .filter(ch => ch.type === 0) // text channels only
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach(ch => {
              console.log(`  #${ch.name} => ${ch.id}`);
});
});

  console.log('\n=== COPY THE IDs ABOVE INTO auto_reports.js ===\n');
      process.exit(0);
});

client.login(token);
