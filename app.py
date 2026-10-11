
import os
from datetime import date, timedelta

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="ZeroWaste Kitchen",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 ZeroWaste Kitchen")
st.caption("Plan smart. Cook fresh. Waste less.")

if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame(
        columns=["Ingredient", "Quantity", "Unit", "Expiry"]
    )

if "shopping" not in st.session_state:
    st.session_state.shopping = []

st.sidebar.header("Kitchen Dashboard")
page = st.sidebar.radio(
    "Choose a feature",
    ["Dashboard", "Add Ingredients", "AI Meal Planner", "Shopping List"]
)

inventory = st.session_state.inventory.copy()

if not inventory.empty:
    inventory["Expiry"] = pd.to_datetime(
        inventory["Expiry"]
    ).dt.date

if page == "Dashboard":
    st.subheader("Your Kitchen Overview")

    if inventory.empty:
        st.info("Your inventory is empty. Add ingredients to get started.")
    else:
        today = date.today()
        expiring = inventory[
            inventory["Expiry"] <= today + timedelta(days=3)
        ]

        col1, col2, col3 = st.columns(3)
        col1.metric("Ingredient Types", len(inventory))
        col2.metric("Expiring Soon", len(expiring))
        col3.metric("Shopping Items", len(st.session_state.shopping))

        st.subheader("Current Inventory")
        st.dataframe(inventory, use_container_width=True)

        if not expiring.empty:
            st.warning("Check these ingredients first:")
            st.dataframe(expiring, use_container_width=True)

elif page == "Add Ingredients":
    st.subheader("Add Kitchen Ingredients")

    with st.form("ingredient_form", clear_on_submit=True):
        name = st.text_input("Ingredient name")
        quantity = st.number_input("Quantity", min_value=0.1, value=1.0)
        unit = st.selectbox(
            "Unit", ["pieces", "kg", "g", "litres", "ml", "packets"]
        )
        expiry = st.date_input("Expiry date", value=date.today())

        submitted = st.form_submit_button("Add Ingredient")

    if submitted:
        if not name.strip():
            st.error("Please enter an ingredient name.")
        elif expiry < date.today():
            st.error("Check the expiry date before adding this item.")
        else:
            new_row = pd.DataFrame([{
                "Ingredient": name.strip(),
                "Quantity": quantity,
                "Unit": unit,
                "Expiry": expiry
            }])

            st.session_state.inventory = pd.concat(
                [st.session_state.inventory, new_row],
                ignore_index=True
            )
            st.success(f"{name} added to your kitchen!")
            st.rerun()

    if not inventory.empty:
        st.subheader("Manage Inventory")
        selected = st.selectbox(
            "Ingredient to remove",
            inventory["Ingredient"].tolist()
        )
        if st.button("Remove Selected Ingredient"):
            idx = st.session_state.inventory[
                st.session_state.inventory["Ingredient"] == selected
            ].index[0]
            st.session_state.inventory = (
                st.session_state.inventory.drop(idx).reset_index(drop=True)
            )
            st.rerun()

elif page == "AI Meal Planner":
    st.subheader("Smart Meal Planner")

    people = st.number_input(
        "Number of people", min_value=1, max_value=30, value=2
    )
    diet = st.selectbox(
        "Food preference",
        ["Vegetarian", "Vegan", "Eggitarian", "Non-vegetarian"]
    )
    meal = st.selectbox(
        "Meal type", ["Breakfast", "Lunch", "Dinner", "Full-day plan"]
    )

    ingredients = inventory["Ingredient"].tolist()

    if st.button("Generate Meal Plan", type="primary"):
        if not ingredients:
            st.warning("Add ingredients before generating a meal plan.")
        else:
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                st.warning(
                    "Gemini API key not found. Showing basic ingredient-based suggestions."
                )
                st.write(
                    "Available ingredients: " + ", ".join(ingredients)
                )
                st.write(
                    "Choose a recipe using these ingredients and check "
                    "expiry, freshness, and food safety before cooking."
                )
            else:
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are ZeroWaste Kitchen, a food planning AI agent.
                    Plan {meal} for {people} people.
                    Food preference: {diet}.
                    Available ingredients: {ingredients}.
                    Prioritize safe ingredients that expire soon.
                    Suggest practical Indian recipes, portions, ingredients,
                    preparation steps, and missing ingredients to buy.
                    Do not assume that an ingredient is safe merely because
                    its expiry date has not passed.
                    Respect the selected dietary preference.
                    """
                    with st.spinner("AI is planning your meals..."):
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                    st.markdown(response.text)
                except Exception as error:
                    st.error(
                        "AI request failed. Check your API key, model "
                        "availability, internet connection, and API quota."
                    )
                    st.caption(str(error))

elif page == "Shopping List":
    st.subheader("Smart Shopping List")

    item = st.text_input("Missing ingredient to buy")

    if st.button("Add to Shopping List"):
        if item.strip():
            st.session_state.shopping.append(item.strip())
            st.rerun()

    for i, product in enumerate(st.session_state.shopping):
        col1, col2 = st.columns([4, 1])
        col1.write(f"🛒 {product}")
        if col2.button("Remove", key=f"remove_{i}"):
            st.session_state.shopping.pop(i)
            st.rerun()

    if st.session_state.shopping:
        shopping_text = "\n".join(
            f"- {item}" for item in st.session_state.shopping
        )
        st.download_button(
            "Download Shopping List",
            data=shopping_text,
            file_name="shopping_list.txt",
            mime="text/plain"
        )
    else:
        st.info("Your shopping list is empty.")

st.divider()
st.caption("ZeroWaste Kitchen | AI-assisted food planning")