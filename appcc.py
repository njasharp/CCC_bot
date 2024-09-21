import streamlit as st
import os
from groq import Groq

# Initialize Groq client with API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found in environment variables. Please set it and restart the app.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Supported models
SUPPORTED_MODELS = {
    "Llama 3 8B": "llama3-8b-8192",
    "Llama 3.1 70B": "llama-3.1-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
    "LLaVA 1.5 7B": "llava-v1.5-7b-4096-preview"  # New model added
}

# Initialize temperature in session state
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.7

# Function to query Groq with retry and temperature
def query_groq_with_retry(messages, model, temperature=None, retries=3):
    for attempt in range(retries):
        try:
            kwargs = {"messages": messages, "model": model}
            if temperature is not None:
                kwargs["temperature"] = temperature
            chat_completion = client.chat.completions.create(**kwargs)
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retries - 1:
                continue  # Retry if possible
            else:
                st.error(f"An error occurred after {retries} attempts: {e}")
                return ""

st.write("")  # Extra line space
st.write("")  # Extra line space
st.image("p1.png")

# Main app function
def main():
    st.write("This tool allows users to evaluate and optimize their business offers using Alex Hormozi's framework, providing actionable insights based on user inputs and selected analysis prompts.")

    # Sidebar input fields
    st.sidebar.header("Business Information")
    business_name = st.text_input("Business Name:")
    business_description = st.text_area("Business Description:")
    target_audience = st.text_input("Target Audience:")
    dream_outcome = st.text_input("Dream Outcome:")




    # Model selection and temperature adjustment
    st.sidebar.header("Model Settings")
    selected_model = st.sidebar.selectbox("Select a model", list(SUPPORTED_MODELS.keys()), index=0)
    model_id = SUPPORTED_MODELS[selected_model]

    st.sidebar.header("Temperature Settings")
    st.session_state["temperature"] = st.sidebar.slider(
        "Set Model Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["temperature"],
        step=0.1,
        key="temperature_slider"
    )

    
    # Prompt selection
    st.sidebar.header("Select Analysis Prompt")
    prompt_option = st.sidebar.selectbox("Choose a prompt", ["$100M Offer Validation", "Generic Offer Validation"])#  Slider inputs for scores
    dream_score = st.sidebar.slider("Dream Score (1-10) = (Desirability)", 1, 10, 5)
    success_score = st.sidebar.slider("Success Score (1-100) =  (Likelihood of Achievement)", 1, 100, 50)
    time_score = st.sidebar.slider("Time Score (1-100) = Time Score (Time Delay)", 1, 100, 50)
    effort_score = st.sidebar.slider("Effort Score (1-100) = (Effort and Sacrifice)", 1, 100, 50)

    if st.sidebar.button("Validate Business"):
        with st.spinner('Validating...'):
            # Prepare the prompt for LLM based on selection
            if prompt_option == "$100M Offer Validation":
                prompt = f"""Adopt the role of an expert business analyst specializing in offer evaluation and optimization. Your task is to evaluate the offer of a business using Alex Hormozi's offer value calculation formula.

Information about me:
My business: {business_name}
My offer: {business_description}
My target audience: {target_audience}
Dream outcome of my offer: {dream_outcome}
Perceived likelihood of achievement: {success_score}
Time delay to achieve outcome: {time_score}
Effort and sacrifice required: {effort_score}

You have to rate my offer based on Alex Hormozi's 4-part value equation framework:
How desirable is this offer's dream outcome on a scale of 1-10? This is called "Dream Score": {dream_score}.
How high is the offer's perceived likelihood of achievement on a scale of 1-100? This is called "Success Score": {success_score}.
How high is the offer's perceived time delay between purchasing the product and reaching the promised achievement on a scale from 1 to 100? This is called "Time Score": {time_score}.
How high is the offer's perceived effort and sacrifice on a scale of 1 to 100? This is the "Effort Score": {effort_score}.

After rating each of the 4 points mentioned above, calculate an 'offer score'. Provide actionable advice on how I can improve my offer.
"""

            elif prompt_option == "Generic Offer Validation":
                prompt = f"""Assume the role of an expert analyst tasked with evaluating any given offer using a generalized version of Alex Hormozi’s offer value calculation formula.

Information about me:
My business: {business_name}
My offer: {business_description}
My target audience: {target_audience}
Dream outcome of my offer: {dream_outcome}
Perceived likelihood of achievement: {success_score}
Time delay to achieve outcome: {time_score}
Effort and sacrifice required: {effort_score}

Your Task: Provide an analysis of this offer, detailing how it could be optimized based on the components below.
- Dream Outcome of the Offer: Rate the desirability on a scale of 1-10. This is your "Dream Score": {dream_score}.
- Likelihood of Achievement: Estimate on a scale from 1-100, your "Success Score": {success_score}.
- Time Delay: Assess on a scale from 1 to 100: {time_score}.
- Effort and Sacrifice: Evaluate on a scale from 1 to 100: {effort_score}.

Calculation of Offer Score:
Multiply the "Dream Score" by the "Success Score."
Multiply the "Time Score" by the "Effort Score."
Divide to derive the final "Offer Score."

Provide actionable advice on how to enhance each component of the offer to maximize the overall score.
"""

            # Query the LLM with the prepared prompt
            messages = [{"role": "user", "content": prompt}]
            response = query_groq_with_retry(messages, model=model_id, temperature=st.session_state["temperature"])
            
            st.success("Validation Result:")
            st.text_area("Recommendations:", value=response, height=800)
st.sidebar.info("built by dw 9-20-24")
if __name__ == "__main__":
    main()
