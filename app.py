import streamlit as st
import os
from dotenv import load_dotenv
from xai_sdk import Client

from xai_sdk.chat import user, system
from datetime import datetime
import pathlib

load_dotenv()
client = Client(api_key=os.getenv("XAI_API_KEY") or "")

st.set_page_config(page_title="Grok What-If Simulator", layout="wide")

st.title("Grok What-If Simulator")
st.markdown("Explore alternate histories, physics scenarios, tech divergences - all powered by Grok.")

# sidebar controls
with st.sidebar:
    st.header("Simulation Settings")
    model = st.selectbox("Grok Model", ['grok-beta', 'grok-4-0709'], index=0)
    steps = st.slider("Number of Steps", min_value=4, max_value=12, value=8, step=1)
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.68, 0.05)
    interactive = st.checkbox("Enable interactive follow-ups", value=False)


# main input
scenario = st.text_area(
    "What if...?",
    height=120,
    placeholder="What if penicillin was never discovered?\nWhat if the asteroid missed Earth?\nWhat if smartphones were invented in the 1800s",
    help="Be as specific or crazy as you can be!!",
)

if st.button("Run Simulation", type="primary", use_container_width=True):
    if not scenario.strip():
        st.error("Please enter a scenario first...")
    elif not os.getenv("XAI_API_KEY"):
        st.error("XAI_API_KEY. not found - check your .env file")
    else:
        with st.spinner("Grok is simulating alternate reality..."):
            SYSTEM_PROMPT = f"""
You are a maximally truth-seeking, first-principles world simulator.
Given this "What if" scenario, simulate realistic causal consequences step by step.

Rules:
- Number each major step (1., 2., ...)
- Show clear cause → effect reasoning
- Cover short-term (years), medium-term (decades), long-term (centuries) where relevant
- Be detailed but concise — clarity over fluff
- Add dry wit or irony only when it fits naturally

Simulate approximately {steps} steps.
"""
            
            messages = [
                system(SYSTEM_PROMPT),
                user(scenario),
            ]

            # run first simulation
            chat_session = client.chat.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2200,
            )
            result = chat_session.sample().content.strip()

            full_output = f"**Scenario:** {scenario}\n\n{result}"

            st.subheader("Simulation Output")
            st.markdown(result)

            # Interactive follow up (one extra turn for mvp)
            if interactive:
                tweak = st.text_input("Want to tweak the timeline or ask a follow up? (optional)")
                if tweak.strip():
                    messages.append(user(tweak))
                    with st.spinner("Continuing the simulation..."):
                        chat_session = client.chat.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=2200,
                        )
                        continuation = chat_session.sample().content.strip()
                    st.subheader("Follow-up / Branch")
                    st.markdown(continuation)
                    full_output += f"\n\n**Follow-up:** {tweak}\n\n{continuation}"

        # auto save
        out_dir = pathlib.Path("simulations")
        out_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in scenario[:50] if c.isalnum() or c in " -_").rstrip()
        file_path = out_dir / f"sim_{timestamp}_{safe_name}.txt"
        file_path.write_text(full_output)
        st.success(f"Saved to: {file_path}")

st.markdown("---")
st.caption("Grok powered What-if simulator - Built with xAi API key - More features coming soon")
