import requests
import json
import os

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual API URL
EMBED_URL = f"{BASE_URL}/api/v1/embed"
EXTRACT_URL = f"{BASE_URL}/api/v1/extract"
DOWNLOAD_URL = f"{BASE_URL}/api/v1/download"

# --- Helper Functions ---


def create_dummy_file(filename="dummy_image.png"):
    """Creates a small, black PNG image for testing."""
    from PIL import Image

    img = Image.new("RGB", (60, 30), color="black")
    img.save(filename)
    return filename


def embed_message(
    file_path: str,
    message: str,
    password: str,
    encryption_algos: list,
    hash_function: str,
    stenographic_technique: str,
):
    """
    Sends a request to the /embed endpoint to hide a message in a file.
    """
    print("--- Sending Embed Request ---")
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "image/png")}
        data = {
            "message": message,
            "password": password,
            "encryption_algos": ",".join(encryption_algos),
            "hash_function": hash_function,
            "stenographic_technique": stenographic_technique,
        }

        try:
            response = requests.post(EMBED_URL, files=files, data=data)
            response.raise_for_status()  # Raise an exception for bad status codes

            print("Embed Request Successful!")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Embed Request Failed: {e}")
            if e.response:
                print(f"Response Content: {e.response.text}")
            return None


def extract_message(
    file_path: str,
    password: str,
    stenographic_technique: str,
    codebook: dict = None,
    encryption_algos: list = None,
    hash_function: str = None,
):
    """
    Sends a request to the /extract endpoint to retrieve a hidden message from a file.
    """
    print("\n--- Sending Extract Request ---")
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "image/png")}
        data = {
            "password": password,
            "stenographic_technique": stenographic_technique,
        }

        # The codebook must be sent as a JSON string
        if codebook:
            data["codebook"] = json.dumps(codebook)

        # These are only required if the codebook is not provided
        if encryption_algos:
            data["encryption_algos"] = ",".join(encryption_algos)
        if hash_function:
            data["hash_function"] = hash_function

        try:
            response = requests.post(EXTRACT_URL, files=files, data=data)
            response.raise_for_status()

            print("Extract Request Successful!")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Extract Request Failed: {e}")
            print(f"Response Content: {e.response.text} ")
            if e.response:
                print(f"Response Content: {e.response.text}")
            return None


def download_file(file_name: str, destination_filename: str):
    """Downloads the processed file from the API."""
    print(f"\n--- Downloading Processed File ---")
    url = f"{DOWNLOAD_URL}/{file_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(destination_filename, "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully as {destination_filename}")
        return destination_filename
    except requests.exceptions.RequestException as e:
        print(f"Download Failed: {e}")
        if e.response:
            print(f"Response Content: {e.response.text}")
        return None


# --- Main Execution ---

if __name__ == "__main__":
    # 1. Create a dummy file to work with
    dummy_file = create_dummy_file()
    print(f"Created dummy file: {dummy_file}")

    # 2. Define the parameters for embedding
    secret_message = "This is a secret message!"
    secret_password = "mysecretpassword"
    algos = ["AES", "AES"]
    h_function = "SHA256"
    tech = "LSB"

    # 3. Embed the message into the file
    embed_result = embed_message(
        file_path=dummy_file,
        message=secret_message,
        password=secret_password,
        encryption_algos=algos,
        hash_function=h_function,
        stenographic_technique=tech,
    )

    if embed_result:
        print("Embed Result:", json.dumps(embed_result, indent=2))

        # 4. Download the file with the embedded message
        output_file_path = embed_result.get("output_path")
        codebook_data = embed_result.get("codebook")

        if output_file_path and codebook_data:
            embedded_file = download_file(output_file_path, "embedded_image.png")

            if embedded_file:
                # 5. Extract the message from the new file using the codebook
                # --- 5a. Try extraction WITHOUT the codebook -------------------------
                extract_result_no_cb = extract_message(
                    file_path=embedded_file,
                    password=secret_password,
                    stenographic_technique=tech,
                    encryption_algos=algos,  # same list you used for embed
                    hash_function=h_function,  # same hash you used for embed
                )

                # --- 5b. Fallback extraction WITH the codebook (optional) ------------
                extract_result_cb = extract_message(
                    file_path=embedded_file,
                    password=secret_password,
                    stenographic_technique=tech,
                    codebook=codebook_data,
                )

                if extract_result_cb:
                    print(
                        "Extract Result for Codebook:",
                        json.dumps(extract_result_cb, indent=2),
                    )

                    # 6. Verify the result
                    if extract_result_cb.get("message") == secret_message:
                        print(
                            "\n✅ Success! The extracted message matches the original secret."
                        )
                    else:
                        print(
                            "\n❌ Failure! The extracted message does not match the original."
                        )
                if extract_result_no_cb:
                    print(
                        "Extract Result for No Codebook:",
                        json.dumps(extract_result_no_cb, indent=2),
                    )

                    # 6. Verify the result
                    if extract_result_no_cb.get("message") == secret_message:
                        print(
                            "\n✅ Success! The extracted message matches the original secret.(No Codebook)"
                        )
                    else:
                        print(
                            "\n❌ Failure! The extracted message does not match the original."
                        )

    # Clean up the created files
    if os.path.exists(dummy_file):
        os.remove(dummy_file)
    if os.path.exists("embedded_image.png"):
        os.remove("embedded_image.png")
