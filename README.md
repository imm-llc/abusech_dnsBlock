# abusech_dnsBlock

This tool updates a WatchGuard alias containing IP addresses marked as "online" by https://ransomwaretracker.abuse.ch/feeds/csv/

The idea is that you'll have an up-to-date IP blacklist to prevent communication to C2 servers.

I wrote this to be as simple as I could while working around edge cases I've encountered.

Originally, I intended to use a DNS-based block, but that made less sense than IP. Hence the misleading repo name

## Setup

Install Python36 and pip3. Install the packages listed in `Pipfile`.

Setup MongoDB. You could run this in a container, even. It wouldn't be a bad idea to drop the database and clear the list every few weeks in order to avoid stale entries.

Copy `config.example.py` to `config.py`.

Configure your Mongo URL and WatchGuard SSH settings in `config.py`.

Send it.

## Advice

Set up the alias first but don't put it in the firewall rules. Give it a dry run first to make sure nothing breaking will occur. 