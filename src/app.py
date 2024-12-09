from flask import Flask, jsonify, render_template, request

from src.llm import transform_content
from src.parser import extract_main_content
from src.scraper import scrape_url


app = Flask(__name__, static_folder="static", template_folder="static")


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/process", methods=["POST"])
async def process():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400

        url = data.get("url")
        output_format = data.get("format")
        prompt = data.get("prompt")
        custom_fields = data.get("customFields")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Scrape the webpage
        html_content = await scrape_url(url)

        # Extract main content
        main_content = extract_main_content(html_content)

        # Transform content using OpenLLaMA with custom prompt and fields
        result = await transform_content(
            content=main_content,
            output_format=output_format,
            prompt=prompt,
            custom_fields=custom_fields,
        )

        # Response enclosure ::[[response]]::
        if "::[[" in result and "]]::" in result:
            result = result.split("::[[")[1].split("]]::")[0]

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    """Entry point for the application."""
    app.run(debug=True)


if __name__ == "__main__":
    main()


# Export the Flask app for testing
def create_app():
    return app
