---
name: yandex-metrika
description: Use when working with Yandex Metrika (Yandex Metrica) analytics - retrieving traffic stats, managing counters and goals via API, setting up tracking code in web projects, building reports, analyzing conversions, or debugging counter issues. Triggers on mentions of Yandex Metrika, Metrica, web analytics counters, pageviews metrics, site traffic reports, conversion goals, or counter IDs. Always use this skill when the user mentions Yandex Metrika or wants analytics data from their site, even if they don't say "API" explicitly.
---

# Yandex Metrika

## Overview

Yandex Metrika (Metrica) provides three APIs:
- **Management API** — create/edit/delete counters, goals, filters, grants
- **Reporting API** — retrieve traffic stats, build reports with dimensions & metrics
- **Logs API** — access raw non-aggregated hit/visit data

Base URL: `https://api-metrika.yandex.net`

## Authentication

All API requests require an OAuth token in the header:

```
Authorization: OAuth <token>
```

### Getting a token

1. Create an app at https://oauth.yandex.com/?dialog=create-client-entry
2. Select "For API access or debugging"
3. Add scopes:
   - `metrika:read` — read stats and counter settings
   - `metrika:write` — create/modify counters, upload data
4. Generate auth URL: `https://oauth.yandex.com/authorize?response_type=token&client_id=<app_id>`
5. Copy the token from the redirect

### Using the token

```bash
curl -H 'Authorization: OAuth YOUR_TOKEN' \
  'https://api-metrika.yandex.net/management/v1/counters'
```

## Management API

### Counters

| Action | Method | Endpoint |
|--------|--------|----------|
| List all | GET | `/management/v1/counters` |
| Get one | GET | `/management/v1/counters/{id}` |
| Create | POST | `/management/v1/counters` |
| Update | PUT | `/management/v1/counters/{id}` |
| Delete | DELETE | `/management/v1/counters/{id}` |
| Restore | POST | `/management/v1/counters/{id}/undelete` |

**List counters with filters:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/management/v1/counters?status=Active&sort=Visits&per_page=50'
```

Query params: `status` (Active/Deleted), `sort` (Visits/Hits/Uniques/Name), `per_page`, `offset`, `search_string`, `permission` (own/view/edit), `favorite`.

### Goals

| Action | Method | Endpoint |
|--------|--------|----------|
| List | GET | `/management/v1/counter/{id}/goals` |
| Get one | GET | `/management/v1/counter/{id}/goal/{goalId}` |
| Create | POST | `/management/v1/counter/{id}/goals` |
| Update | PUT | `/management/v1/counter/{id}/goal/{goalId}` |
| Delete | DELETE | `/management/v1/counter/{id}/goal/{goalId}` |

**Goal types:** url, action, phone, email, messenger, chat, file, social_network, search, payment_system, visit_duration, depth, composite.

**Create a URL goal:**
```bash
curl -X POST \
  -H 'Authorization: OAuth TOKEN' \
  -H 'Content-Type: application/json' \
  'https://api-metrika.yandex.net/management/v1/counter/COUNTER_ID/goals' \
  -d '{
    "goal": {
      "name": "Thank you page",
      "type": "url",
      "conditions": [
        {"type": "contain", "url": "/thank-you"}
      ]
    }
  }'
```

URL condition types: `exact`, `contain`, `start`, `regexp`.

**Create a JavaScript event goal:**
```bash
curl -X POST \
  -H 'Authorization: OAuth TOKEN' \
  -H 'Content-Type: application/json' \
  'https://api-metrika.yandex.net/management/v1/counter/COUNTER_ID/goals' \
  -d '{
    "goal": {
      "name": "Form submitted",
      "type": "action",
      "conditions": [
        {"type": "exact", "url": "form_submit"}
      ]
    }
  }'
```

Then trigger from JS: `ym(COUNTER_ID, 'reachGoal', 'form_submit');`

## Reporting API

### Endpoints

| Endpoint | Purpose |
|----------|----------|
| `/stat/v1/data` | Table report |
| `/stat/v1/data/bytime` | Time-series data |
| `/stat/v1/data/comparison` | Compare two segments |
| `/stat/v1/data/drilldown` | Hierarchical drill-down |

### Core Parameters

| Param | Description | Example |
|-------|-------------|----------|
| `ids` | Counter ID(s) | `44147844` |
| `metrics` | What to measure (max 20) | `ym:s:visits,ym:s:users` |
| `dimensions` | How to group (max 10) | `ym:s:trafficSource` |
| `date1` | Start date | `2025-01-01` or `30daysAgo` |
| `date2` | End date | `today` |
| `filters` | Segment filter | `ym:s:isNewUser=='Yes'` |
| `sort` | Sort by (prefix `-` for desc) | `-ym:s:visits` |
| `limit` | Results per page (max 100000) | `100` |
| `accuracy` | Sampling (full/medium/low) | `full` |
| `lang` | Response language | `ru` |

### Common Metrics

| Metric | Description |
|--------|-------------|
| `ym:s:visits` | Sessions |
| `ym:s:users` | Unique visitors |
| `ym:s:hits` | Pageviews |
| `ym:s:bounceRate` | Bounce rate |
| `ym:s:pageDepth` | Pages per session |
| `ym:s:avgVisitDurationSeconds` | Avg session duration |
| `ym:s:goal<goal_id>visits` | Goal completions |
| `ym:s:goal<goal_id>conversionRate` | Goal conversion rate |
| `ym:s:goal<goal_id>users` | Users who reached goal |

### Common Dimensions

| Dimension | Description |
|-----------|-------------|
| `ym:s:date` | Date |
| `ym:s:trafficSource` | Traffic source |
| `ym:s:lastTrafficSource` | Last traffic source |
| `ym:s:searchEngine` | Search engine |
| `ym:s:browser` | Browser |
| `ym:s:operatingSystem` | OS |
| `ym:s:regionCountry` | Country |
| `ym:s:regionCity` | City |
| `ym:s:deviceCategory` | Device type |
| `ym:s:UTMSource` | UTM source |
| `ym:s:UTMMedium` | UTM medium |
| `ym:s:UTMCampaign` | UTM campaign |

### Report Presets

Instead of specifying dimensions/metrics manually, use presets: `sources_summary`, `sources_search_phrases`, `tech_platforms`, `publishers_sources`, `publishers_authors`, `publishers_rubrics`.

```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?preset=sources_summary&id=COUNTER_ID'
```

### Filter Syntax

```
# Equals
ym:s:trafficSource=='organic'

# Not equals
ym:s:trafficSource!='organic'

# Contains (for strings)
ym:s:startURL=@'blog'

# Greater than
ym:s:pageViews>5

# Multiple values
ym:s:lastTrafficSource=.('organic','direct','referral')

# AND
ym:s:trafficSource=='organic' AND ym:s:isNewUser=='Yes'

# Not null
ym:s:publisherArticle!n
```

### Examples

**Traffic overview (last 30 days):**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?id=COUNTER_ID&metrics=ym:s:visits,ym:s:users,ym:s:bounceRate&date1=30daysAgo&date2=today'
```

**Daily visits time series:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data/bytime?id=COUNTER_ID&metrics=ym:s:visits&date1=30daysAgo&date2=today&group=day'
```

**Traffic by source:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?id=COUNTER_ID&metrics=ym:s:visits,ym:s:users&dimensions=ym:s:lastTrafficSource&sort=-ym:s:visits'
```

**Goal conversions by traffic source:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?id=COUNTER_ID&dimensions=ym:s:trafficSource&metrics=ym:s:users,ym:s:goal<goal_id>conversionRate&goal_id=GOAL_ID'
```

**Mobile vs Desktop comparison:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data/comparison?id=COUNTER_ID&metrics=ym:s:users,ym:s:bounceRate&dimensions=ym:s:trafficSource&filters_a=ym:s:isMobile==%27Yes%27&filters_b=ym:s:isMobile==%27No%27'
```

**Geographic breakdown:**
```bash
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?id=COUNTER_ID&metrics=ym:s:visits,ym:s:users&dimensions=ym:s:regionCityName&sort=-ym:s:visits&limit=20&lang=ru'
```

## Setting Up a Counter in a Web Project

### Next.js / React

For detailed setup patterns, see `references/nextjs-setup.md`.

The key steps:
1. Load the Metrika `tag.js` script dynamically via `next/script` or a `useEffect`
2. Call `ym(COUNTER_ID, "init", { ... })` with your options
3. Track SPA page navigations with `ym(COUNTER_ID, 'hit', url)` on route change
4. Add a `<noscript>` pixel fallback

**Important:** Do NOT use `ssr: true` in the init options for static exports — it prevents the counter from initializing.

### Plain HTML

```html
<!-- Place before </head> or at end of <body> -->
<script type="text/javascript">
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
  m[i].l=1*new Date();
  for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
  k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
  (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
  ym(COUNTER_ID, "init", {
    clickmap: true,
    trackLinks: true,
    accurateTrackBounce: true,
    webvisor: true
  });
</script>
<noscript>
  <div><img src="https://mc.yandex.ru/watch/COUNTER_ID" style="position:absolute; left:-9999px;" alt="" /></div>
</noscript>
```

### Init Options

| Option | Default | Description |
|--------|---------|-------------|
| `clickmap` | false | Record click coordinates for heatmaps |
| `trackLinks` | false | Track outbound link clicks |
| `accurateTrackBounce` | false | Accurate bounce rate (true = 15s threshold) |
| `webvisor` | false | Enable session replay (Webvisor) |
| `trackHash` | false | Track hash changes as page views |
| `ecommerce` | false | Enable e-commerce data layer |
| `triggerEvent` | false | Fire `yacounter{ID}inited` when ready |

### JavaScript API (client-side)

```js
// Track a pageview (SPA navigation)
ym(COUNTER_ID, 'hit', '/new-page', { title: 'Page Title' });

// Reach a goal
ym(COUNTER_ID, 'reachGoal', 'goal_identifier');

// Reach a goal with callback
ym(COUNTER_ID, 'reachGoal', 'purchase', function() {
  window.location = '/thank-you';
});

// Set user parameters
ym(COUNTER_ID, 'userParams', { age: 25, gender: 'male' });

// Set visit parameters
ym(COUNTER_ID, 'params', { order_price: 1500, currency: 'RUB' });
```

## Quotas

- Reporting API: 10 requests per second per token
- Management API: varies by endpoint
- Logs API: limited concurrent requests
- Max 20 metrics and 10 dimensions per report request
- Max `limit` = 100,000 rows per request

## Troubleshooting

| Issue | Check |
|-------|-------|
| No data in reports | Counter status is Active, tracking code is on all pages |
| Goal not tracking | Goal ID matches, `reachGoal` event name matches condition exactly |
| Stats delayed | Data lag is normal (up to several hours); check `data_lag` in API response |
| 403 from API | Token has correct scopes (`metrika:read` / `metrika:write`) |
| Sampling applied | Set `accuracy=full` (slower but precise); check `sampled` in response |
| SPA pages not tracked | Add `ym(ID, 'hit', url)` on route change |
| Counter not initializing | Remove `ssr: true` from init options if using static export |
