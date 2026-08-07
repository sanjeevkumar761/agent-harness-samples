# Demo Video Plan — Copilot Studio × Microsoft Agent Framework

A complete, viral-optimized plan for a ~90-second LinkedIn demo. It's built
around what we actually shipped: the terminal chat, the Streamlit UI with the
live "API & backend call" panel, and the architecture story. Voiceover lines are
written short and clean for AI TTS.

---

## 🎬 Title & hook options (pick one)

- **"I connected Copilot Studio to code in 5 minutes. Here's how."**
- **"Your Copilot Studio agent doesn't have to live in a chat window."**
- **"Call any Copilot Studio agent from Python — with full auth. Live."**

**Format:** 9:16 vertical (or 1:1), 60–95s, captions burned in, upbeat low
background music. First 3 seconds decide everything.

---

## Scene-by-scene

### Scene 1 — Hook (0:00–0:06)

- **Visual:** Fast screen-cut of the Streamlit app answering a question, then freeze.
- **On-screen text:** `Copilot Studio × Microsoft Agent Framework`
- **Voiceover:** "What if your Copilot Studio agent could be called from *any* app you build? Watch this."

### Scene 2 — The problem (0:06–0:16)

- **Visual:** Split screen — Copilot Studio maker canvas on one side, a Python file on the other.
- **On-screen text:** `Built in Copilot Studio → Called from code`
- **Voiceover:** "You build a great agent in Copilot Studio. But it's stuck in a chat box. To use it in your own product, you need code — and secure auth. Let's do both."

### Scene 3 — The one-liner reveal (0:16–0:28)

- **Visual:** Zoom on `copilotstudio_basic.py` — highlight `agent = CopilotStudioAgent()` and `await agent.run(...)`.
- **On-screen text:** `3 lines. That's the integration.`
- **Voiceover:** "This is the whole integration. Create the agent. Call run. Get an answer. The Microsoft Agent Framework treats your Copilot Studio agent as a first-class agent."

### Scene 4 — Terminal chat live (0:28–0:42)

- **Visual:** Run `python copilotstudio_chat.py`, type "What is the capital of France?", answer streams in.
- **On-screen text:** `Real agent. Real tenant. Live.`
- **Voiceover:** "Here it is running. I ask a question… and that's a live call to my published Copilot Studio agent, over Microsoft's Direct-to-Engine API. No mock. No fake data."

### Scene 5 — The web app + WOW panel (0:42–1:02)

- **Visual:** Streamlit app. Click an example prompt → answer. Then **expand the "API & backend call" panel**; the URL and conversation ID snap to real values.
- **On-screen text:** `See exactly how the UI calls the backend`
- **Voiceover:** "Now the part engineers love. This panel shows the *exact* call path — the Agent Framework method, and the real HTTP request to Copilot Studio, with the live endpoint and conversation ID. Full transparency, no black box."

### Scene 6 — Enterprise-grade auth (1:02–1:16)

- **Visual:** Architecture diagram from `ARCHITECTURE.md`; highlight the Entra → PPAPI → agent path.
- **On-screen text:** `Entra ID auth · same-tenant · least privilege`
- **Voiceover:** "And it's secure by design. Sign-in is Microsoft Entra ID. The token is scoped to one permission. The platform enforces that the caller and the agent live in the same tenant. Enterprise-ready, out of the box."

### Scene 7 — Payoff + CTA (1:16–1:30)

- **Visual:** Quick montage: code → terminal → web app → GitHub repo page.
- **On-screen text:** `Code on GitHub 👇  Follow for more`
- **Voiceover:** "From a no-code agent to a production integration — in one afternoon. Code's in the repo below. Follow for more agent engineering."

---

## 🗣️ Clean voiceover script (paste into your AI TTS)

> What if your Copilot Studio agent could be called from any app you build? Watch this.
>
> You build a great agent in Copilot Studio. But it's stuck in a chat box. To use it in your own product, you need code — and secure auth. Let's do both.
>
> This is the whole integration. Create the agent. Call run. Get an answer. The Microsoft Agent Framework treats your Copilot Studio agent as a first-class agent.
>
> Here it is running. I ask a question, and that's a live call to my published Copilot Studio agent, over Microsoft's Direct-to-Engine API. No mock. No fake data.
>
> Now the part engineers love. This panel shows the exact call path — the Agent Framework method, and the real HTTP request to Copilot Studio, with the live endpoint and conversation ID. Full transparency, no black box.
>
> And it's secure by design. Sign-in is Microsoft Entra ID. The token is scoped to one permission. The platform enforces that the caller and the agent live in the same tenant. Enterprise ready, out of the box.
>
> From a no-code agent to a production integration, in one afternoon. Code's in the repo below. Follow for more agent engineering.

*(~150 words ≈ 80–90s at a natural TTS pace. For a tighter 60s cut, drop Scene 2 and Scene 6's last sentence.)*

---

## 🔥 Virality tips

- **Hook in 3s:** open on the *answer appearing*, not on your face or a title card. Motion first.
- **Burned-in captions:** 85% of LinkedIn plays on mute. Every line on screen.
- **Zoom & highlight:** use cursor zoom on `agent.run(...)` and the API panel URL — the "reveal" of real values is the shareable moment.
- **One idea per shot:** keep cuts ≤ 4s; match cuts to voiceover sentences.
- **Reveal the magic trick:** the "API & backend call" panel is your differentiator — linger 1 extra second there.
- **End card:** repo link + "Follow" + your handle for 3s.
- **Aspect ratio:** 9:16 for feed/Reels reach; 1:1 as a safe alternative.

---

## 📝 LinkedIn caption (ready to post)

> Copilot Studio is amazing for building agents — but they don't have to stay in a chat window. 🚀
>
> I wired a published Copilot Studio agent into Python using the **Microsoft Agent Framework** — with real Microsoft Entra ID auth and full Direct-to-Engine calls. Then I built a UI that shows the *exact* API call path, so there's zero black box.
>
> 3 lines of code for the integration. Enterprise-grade auth by design. Full code in the repo. 👇
>
> What would you build if your Copilot Studio agent had an API? 👇
>
> #CopilotStudio #AIAgents #MicrosoftAgentFramework #Azure #PowerPlatform #GenAI #DeveloperTools #Python

**Hashtags trimmed set:** `#CopilotStudio #AIAgents #Azure #GenAI #Python`

---

## Assets & references

- Cover image: [`assets/cover.png`](assets/cover.png) (1280×720) / [`assets/cover.svg`](assets/cover.svg)
- Terminal chat: [`copilotstudio_chat.py`](copilotstudio_chat.py)
- Web demo: [`app.py`](app.py)
- Architecture & auth story: [`ARCHITECTURE.md`](ARCHITECTURE.md)
