#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger()

leads = [
      {'id': 1, 'company': 'DoD Division 7', 'value': 250000, 'stage': 'PROPOSAL', 'industry': 'Government'},
      {'id': 2, 'company': 'CBP Procurement', 'value': 180000, 'stage': 'NEW', 'industry': 'Government'},
      {'id': 3, 'company': 'Price Capital Group', 'value': 35000, 'stage': 'CONTACTED', 'industry': 'Finance'},
      {'id': 4, 'company': 'Johnson Roofing LLC', 'value': 6000, 'stage': 'NEW', 'industry': 'Construction'},
      {'id': 5, 'company': 'Chen Tech Logistics', 'value': 25000, 'stage': 'PROPOSAL', 'industry': 'Tech'},
      {'id': 6, 'company': 'Thompson Industries', 'value': 8000, 'stage': 'WON', 'industry': 'Manufacturing'},
      {'id': 7, 'company': 'Walsh HVAC Solutions', 'value': 5000, 'stage': 'WON', 'industry': 'Services'},
      {'id': 8, 'company': 'Rivera Medical Supplies', 'value': 9000, 'stage': 'CONTACTED', 'industry': 'Healthcare'},
      {'id': 9, 'company': 'Williams Auto Group', 'value': 8000, 'stage': 'NEW', 'industry': 'Automotive'},
      {'id': 10, 'company': 'Guzman Electrical', 'value': 12000, 'stage': 'CONTACTED', 'industry': 'Construction'},
      {'id': 11, 'company': 'Park & Associates', 'value': 15000, 'stage': 'NEW', 'industry': 'Consulting'},
      {'id': 12, 'company': 'Tech Admin SBR', 'value': 17000, 'stage': 'PROPOSAL', 'industry': 'Tech'},
]

log.info('=' * 80)
log.info('AUTOMATED LEAD ASSIGNMENT ENGINE')
log.info('=' * 80)

assigned = []
total_value = 0
skipped = 0

for lead in leads:
      if lead['stage'] == 'WON':
                log.info(f'SKIP: {lead["company"]} (already WON)')
                skipped += 1
                continue
            if lead['value'] >= 250000:
                      agent = 'Noah'
elif 'government' in lead['industry'].lower():
        agent = 'Adam'
elif lead['value'] >= 50000:
        agent = 'Malik'
elif lead['stage'] == 'CONTACTED':
        agent = 'Sara'
elif lead['stage'] in ['PROPOSAL', 'NEGOTIATING']:
        agent = 'Malik'
elif lead['stage'] == 'NEW':
        agent = 'Zara'
else:
        agent = 'Samson'
      assigned.append({'lead': lead['company'], 'agent': agent, 'value': lead['value']})
    total_value += lead['value']
    log.info(f'ASSIGN: {lead["id"]:2d} | {lead["company"]:30s} | ${lead["value"]:>9,} -> {agent} | {lead["stage"]}')

log.info('')
  log.info('SUMMARY')
log.info('=' * 80)
log.info(f'Total Leads:       {len(leads)}')
log.info(f'Assigned:          {len(assigned)}')
log.info(f'Skipped (WON):     {skipped}')
log.info(f'Total Value:       ${total_value:,}')
agent_counts = {}
for a in assigned:
      agent_counts[a['agent']] = agent_counts.get(a['agent'], 0) + 1
log.info('')
log.info('AGENT DISTRIBUTION:')
for agent in sorted(agent_counts.keys()):
      log.info(f'  {agent:15s}: {agent_counts[agent]:2d} leads')
log.info('=' * 80)
log.info('COMPLETE: All leads automatically assigned!')
log.info('=' * 80)
