// ZYN EMPIRE - Discord Diagnostics Tool
// Run: node diagnose_discord.js
// Prints all channel info, bot status, and connectivity

const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');

const token = fs.readFileSync('/home/zion/zyn/token.txt', 'utf8').trim();

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

client.once('ready', async () => {
    console.log(`\n========== ZYN EMPIRE DIAGNOSTICS ==========`);
    console.log(`Bot: ${client.user.tag}`);
    console.log(`ID: ${client.user.id}`);
    console.log(`Ping: ${client.ws.ping}ms`);
    console.log(`Uptime: ${Math.floor(client.uptime / 1000)}s`);
    console.log(`=============================================\n`);

    // Get all guilds
    const guilds = client.guilds.cache;
    console.log(`Guilds: ${guilds.size}`);

    for (const [guildId, guild] of guilds) {
        console.log(`\n--- Guild: ${guild.name} (ID: ${guildId}) ---`);
        console.log(`  Members: ${guild.memberCount}`);
        console.log(`  Channels: ${guild.channels.cache.size}`);
        console.log(`  Roles: ${guild.roles.cache.size}`);

        // List all channels
        console.log(`\n  CHANNELS:`);
        const channels = guild.channels.cache
            .filter(c => c.isTextBased())
            .sort((a, b) => a.rawPosition - b.rawPosition);

        for (const channel of channels.values()) {
            console.log(`    #${channel.name.padEnd(30)} | ID: ${channel.id}`);
        }

        // Bot permissions
        const botMember = guild.members.me;
        console.log(`\n  Bot Permissions: ${botMember.permissions.toArray().join(', ')}`);
    }

    console.log(`\n=============================================`);
    console.log(`DIAGNOSTICS COMPLETE`);
    console.log(`=============================================\n`);

    process.exit(0);
});

client.on('error', (error) => {
    console.error(`[DIAGNOSTIC ERROR] ${error.message}`);
});

client.login(token);