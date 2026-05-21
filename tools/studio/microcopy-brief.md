# NEXOURA Studio — Microcopy Brief

**Owner:** brand-director
**Last updated:** 2026-05-21
**Audience:** PM (Omar) — all Studio UI strings
**Reading level:** 6th grade (every sentence in this brief is one Omar can ship)
**Open Decision ref:** #7 (brand-director owns the microcopy brief)

---

## 1. Voice Principles

Five rules. If a string breaks one, rewrite it before shipping.

**1. Calm = no exclamation points.**
Except in errors where urgency helps the user act fast. "Done!" is noise. "Saved." is enough.

**2. Premium = no marketing words.**
The UI is not an ad. Drop words that sell. Keep words that explain.

**3. Futuristic = short, clean, present tense.**
"Running." not "Your job is currently running." Trim every extra word.

**4. Intelligent = explain what matters.**
Tell the user what happened and what to do next. Never leave them guessing.

**5. Silence is a violation.**
A blank state, a missing label, a missing error message — each is a brand failure. Every surface must have copy.

---

## 2. Banned Words

Each word below is banned. The reason is listed so you know what to replace it with.

| Word | Why it is banned | Use instead |
|---|---|---|
| **leverage** | Business jargon. Means nothing. | "use" |
| **utilize** | Formal jargon for "use." Never clearer. | "use" |
| **cutting-edge** | Marketing claim. Users must judge that, not us. | describe the actual feature |
| **seamless** | Every product claims this. Means nothing. | describe what is smooth and why |
| **streamline** | Vague. Sounds like a sales pitch. | say what specifically got faster or simpler |
| **unlock** | Gamification language. Studio is not a game. | "enable," "turn on," or describe the action |
| **powerful** | Adjective that adds no information. | describe the specific capability |
| **revolutionary** | Superlative. Creates distrust, not belief. | describe what changed and why it matters |
| **solution** | Enterprise filler word. Means nothing alone. | name the specific tool or feature |
| **ecosystem** | Vague, overused in tech. | name the actual components |
| **synergy** | Meaningless in any context. | describe the actual connection |
| **next-generation** | Every product claims this. | describe what is new |
| **best-in-class** | Unverified claim. Do not assert it. | show metrics or let users decide |
| **world-class** | Same problem as above. | show the evidence |
| **innovative** | If you must say it, you lost. Innovation shows. | show the specific thing that is new |

---

## 3. Preferred Constructions

Short beats long. Active beats passive. Specific beats vague.

### Do / Don't pairs

**Labels and headings**

| Do | Don't |
|---|---|
| Dispatches | Active Dispatches |
| Last run | Most recent execution time |
| Add agent | Click here to add a new agent |
| 3 errors | There are 3 errors present |

**Actions**

| Do | Don't |
|---|---|
| Approve | Approve This Decision Now |
| Cancel | Cancel This Operation |
| Retry | Please Try Again |
| Save | Save Changes |
| Delete | Delete This Item Permanently |

**Status descriptions**

| Do | Don't |
|---|---|
| Running | Currently Running |
| Paused | This job has been paused |
| Done | Completed Successfully |
| Failed | An Error Has Occurred |

**General prose**

| Do | Don't |
|---|---|
| No dispatches yet. | There are currently no active dispatches running at this time. |
| Select a project to continue. | In order to continue, you must first select a project. |
| 2 agents need approval. | There are 2 agents that require your approval before proceeding. |

---

## 4. Empty State Copy

Use these patterns when a list, table, or section has no data.

**Pattern:** One short sentence. State the fact. If helpful, add one short action.

### Templates

**1. No items yet — simple**
> No dispatches yet.

**2. No items yet — with action**
> No agents added. [Add one]

**3. Filter returned nothing**
> No results for this filter.

**4. Waiting for an event**
> No activity in the last 24 hours.

**5. Feature not configured**
> Not set up. [Configure]

### Rules for empty states
- Do not say "currently" or "at this time." It adds nothing.
- Do not apologize. "Sorry, nothing here." is noise.
- Do not use passive voice. "No agents have been added" → "No agents added."
- One action link max. If the fix needs more than one step, link to docs.

---

## 5. Error Message Patterns

Two sentences max. Sentence 1: what broke. Sentence 2: what to do.

**Pattern:** `[What broke]. [What to do].`

### Templates

**1. Network error**
> Connection lost. Check your network and try again.

**2. Action failed**
> Could not save. Try again or reload the page.

**3. Permission denied**
> You do not have access to this. Ask your admin for permission.

**4. Timeout**
> This took too long. Reload and try again.

**5. Validation error (field)**
> This field is required. Enter a value to continue.

### Rules for errors
- Say what broke in plain terms. No error codes in the visible label (log them, do not show them).
- Do not blame the user. "You entered an invalid value." → "That value is not valid."
- Do not say "Oops" or "Uh oh." Studio is not playful in failure states.
- One exclamation point rule exception: urgent data-loss risk only. "Unsaved changes will be lost!" is allowed. "Error!" is not.

---

## 6. Button Label Patterns

Use a verb alone when the action is clear from context. Add a noun only when needed to avoid ambiguity.

### Do / Don't

| Do | Don't |
|---|---|
| Approve | Approve This Decision Now |
| Reject | Reject and Send Back |
| Run | Run This Agent |
| Stop | Stop Running |
| Export | Export Results |
| Delete | Delete This Item Permanently |
| Connect | Connect Your Account |
| Retry | Please Try Again |

### Rules
- No marketing language on buttons. "Get Started" → "Start." "Unlock Premium" → "Upgrade."
- No filler words: "Click to...", "Go to...", "Press..."
- Destructive actions must name the object: "Delete project" not just "Delete."
- Loading state: verb + "ing." "Saving..." not "Please wait..."

---

## 7. Time and Date Patterns

**Fresh (under 1 hour):** Use relative time.
> 2m ago · 45s ago · 59m ago

**Recent (1 hour to 48 hours):** Use relative time.
> 3h ago · 1d ago

**Older (over 48 hours):** Use absolute time in ISO format.
> 2026-05-21 18:16

**Rules**
- Never show both relative and absolute at the same time. Pick one.
- ISO 8601 only for absolute dates: `YYYY-MM-DD HH:MM`. No "May 21st" or "21/05/26."
- Timezone: show UTC unless the user has set a local timezone. Label it: `18:16 UTC`.
- Avoid vague terms: "recently," "just now," "a while ago." Use the actual number.

---

## 8. Acronym Policy

**Always define on first use in any document or long-form surface.**
**In UI labels, define in a tooltip or help text, not inline.**

### Safe to use without definition
These are known by the target audience (PM, product team):

- AI — Artificial Intelligence
- PM — Product Manager
- PR — Pull Request
- UI — User Interface
- API — Application Programming Interface

### Define on first use (everything else)

| Acronym | Define as |
|---|---|
| KPI | Key Performance Indicator |
| SLA | Service Level Agreement |
| CTA | Call to Action |
| ETA | Estimated Time of Arrival |
| RBAC | Role-Based Access Control |
| SSO | Single Sign-On |
| LLM | Large Language Model |
| NFR | Non-Functional Requirement |
| GTM | Go-to-Market |

### Rule
If you are not sure the reader knows it: define it. Short definitions are not a sign of weakness. They are a sign of respect.

---

*This brief is a living document. Open a PR against `tools/studio/microcopy-brief.md` to propose changes. Owner: brand-director.*
