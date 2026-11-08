import os
import sys
import json
import urllib.request
import urllib.error

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()

def generate_image(prompt, output_path, size="1024x1792", quality="standard"):
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env")
        sys.exit(1)

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality
    }

    print(f"Calling DALL-E 3 (size: {size}, quality: {quality})...")
    print(f"Prompt: {prompt[:100]}...")

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            image_url = data['data'][0]['url']
            revised_prompt = data['data'][0].get('revised_prompt', '')
            print("Image generated successfully!")
            print(f"Revised prompt: {revised_prompt[:120]}...")

            # Download image
            print(f"Downloading image to {output_path}...")
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            urllib.request.urlretrieve(image_url, output_path)
            print(f"Saved successfully: {output_path} (size: {os.path.getsize(output_path)} bytes)")
            return True
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Details: {err_body}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_prompt = (
        "Interior view of a majestic Vietnamese Buddhist temple sanctuary, Chùa Thiên Cảnh. "
        "A grand glowing golden statue of Buddha Amitabha sits serenely on an ornate pink lotus throne at the altar, "
        "radiating divine golden halos of light. In the foreground and middle ground, an elegant crimson carpet adorned "
        "with embroidered golden lotus flowers stretches straight down the center aisle towards the altar. "
        "Along both sides of the red carpet are glowing lotus floor lanterns. "
        "The polished dark mahogany floor on either side is wide, spacious, and completely empty of people, "
        "ready for meditation mats. Warm sacred atmospheric lighting, delicate incense smoke drifting, "
        "ornate golden lacquered wooden columns and classical Vietnamese Buddhist temple architecture. "
        "Vertical portrait orientation 9:16 ratio, hyper-detailed, spiritual, sacred, peaceful."
    )
    out_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "assets", "dalle_thien_canh_empty.png")
    generate_image(test_prompt, out_file)
