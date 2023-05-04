import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = "ChatGPT, you are a chief marketing officer for {}. You want to" \
                  " launch an influencer marketing campaign for your new product, {}. " \
                  "Your target demographic is {}. You have a budget of {}" \
                  " for paid amplification of the campaigns that you run. You want to launch these campaigns" \
                  " {}. " \
                  "You have a policy of no-affiliate based campaigns. The key performance indicators to measure" \
                  " success for the campaigns are click-through-rate and engagement rate. With these dimensions" \
                  " and constraints in mind, what are 5 campaign ideas that you have?"

prompt=PROMPT_TEMPLATE.format("a food and beverage company", "cherry pop",
                                "20 year old college students in metropolitan areas",
                                "$10000", "the week before memorial day")


PRE_TEXT_TO_REMOVE = "As an AI language model, I don't have personal preferences or an imaginative capacity. Nonetheless, given the criteria and information you provided, here are some possible campaign ideas:"

PROMPT_TEMPLATE_2 = "ChatGPT, you are a chief marketing officer for {}, a {}. You want to" \
                    " launch an influencer marketing campaign for {}. Your target demographic is {}. You" \
                    " have a budget of {} for paid amplification of the campaigns that you run. You " \
                    "want to launch these campaigns by {} {}. You have a policy of no-affiliate" \
                    " based campaigns. The key performance indicators to measure success for the campaigns are click-through-rate and " \
                    "engagement rate. With these dimensions and constraints in mind, what are 5 campaign ideas that you have? Please " \
                    "ensure that brand messaging for {} is incorporated in each idea, and with each idea provide an example" \
                    " of similar content currently on social media. Don't add any disclaimers at the start of your answer."

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        brand_name = request.form["brand_name"]
        brand_description = request.form["brand_description"]
        product_description = request.form["product_description"]
        target_demo = request.form["target_demo"]
        budget = request.form["budget"]
        campaign_launch_time = request.form["campaign_launch_time"]
        launch_date_reason = request.form["launch_date_reason"]

        print (get_prompt_2(brand_name, brand_description, product_description, target_demo, budget, campaign_launch_time, launch_date_reason))

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": get_prompt_2(brand_name, brand_description, product_description, target_demo, budget, campaign_launch_time, launch_date_reason)}
            ]
        )

        raw_response = completion.choices[0].message.content
        response = raw_response
        if PRE_TEXT_TO_REMOVE in raw_response:
            response = raw_response.replace(PRE_TEXT_TO_REMOVE, "")
        return redirect(url_for("index", results=format_response(response)))

    result = request.args.get("results")
    if result is None:
        result = []
    return render_template("index.html", results=result)

def format_response(result):
    output_result = []
    for line in result.split("\n"):
        output_result.append(line)
    return ", ".join(output_result)


def get_prompt_2(brand_name, brand_description, product_description, target_demo, budget, campaign_launch_time, launch_date_reason=None):
    return PROMPT_TEMPLATE_2.format(brand_name, brand_description, product_description,
                                  target_demo,
                                  budget, campaign_launch_time, launch_date_reason, brand_name)
def get_prompt(company_description, product_description, target_demo, budget, campaign_launch_time):
    return PROMPT_TEMPLATE.format(company_description, product_description,
                                  target_demo,
                                  budget, campaign_launch_time)