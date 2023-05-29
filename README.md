# Cloudflare Sampled Firewall Log Puller

So in order to use the Cloudflare Log Pull API, you need to [enable retention](https://developers.cloudflare.com/logs/logpull/enabling-log-retention/), which is awkward when you didn't realise it works that way, and now you don't have a means to pull historical data when needed.

The Cloudflare Dashboard shows [_some logs_](https://developers.cloudflare.com/analytics/graphql-api/sampling#adaptive-sampling), however they're sampled (like maybe around 5% of the actual traffic). Whilst it's not everything, getting hold of this data is the next best thing if we want _some_ statistical visibility of events that happened (even if not complete).

This script contacts the Cloudflare Analytics API to grab the sampled firewall events

> Requirements: Cloudflare email address, Cloudflare API key, Cloudflare zone ID

---

