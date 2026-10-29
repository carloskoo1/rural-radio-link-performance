# Data-security and repository boundary

The article's public reproducibility archive is deliberately **derived-data only** for its later 3×2 campaign. No machine in the active monitoring campaign should be queried, reconfigured or restarted to maintain this publication package.

**Prohibited public uploads:** frozen or live SQLite RF databases; controller backups; device payloads; SSH keys; tokens; passwords; management IP addresses; internal hostnames; SNMP secrets; raw infrastructure topology/configurations; uncontrolled logs; any personally identifiable data not intended for article authorship; and future prospective records.

The archived database checksum is a public verification identifier, not a database download. Never convert a request for scientific verification into access to an operational endpoint. Use authorized immutable snapshot copies and run all analyses read-only and **outside** the acquisition system.

Pre-push checks: (1) inspect exact changed paths, (2) scan files for secrets/IPs, (3) compute SHA-256, (4) compare original experimental figures/code with their frozen V5 package, (5) confirm data-access text and author approvals, (6) review the final Git diff. The included `.gitignore` is only an additional safeguard.
