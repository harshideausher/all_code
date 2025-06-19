from transformers import AutoProcessor, AutoModelForVision2Seq, BitsAndBytesConfig
import torch
from PIL import Image
import time


device = "cuda" if torch.cuda.is_available() else 'cpu'
device = 'cuda'

# Load the instruction-tuned, quantized model
def load_model():
    model = AutoModelForVision2Seq.from_pretrained(
        "HuggingFaceTB/SmolVLM-500M-Instruct",
        # quantization_config=BitsAndBytesConfig(load_in_8bit=True),
        device_map="auto",
        torch_dtype="auto"
    )

    model.to(device)

    processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct")
    return processor, model


def summarize_image(processor, model, img: Image.Image) -> str:

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": (
                    "Look at this image and describe everything in detail. "
                    "Include all visible objects, people, animals, actions, clothing, facial expressions, "
                    "text or signs, colors, background elements, layout, and anything else that stands out. "
                    "If you recognize any famous places or famous persons in the image, "
                    "identify and name them accurately. "
                    "Be specific and thorough. Imagine you're explaining this image to someone who cannot see it."
                )}
            ]
        }
    ]
    # Prepare
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[img], return_tensors="pt")
    inputs = {k: v.to(model.device) for k,v in inputs.items()}

    # Generate full sequence
    outputs = model.generate(**inputs, max_new_tokens=1000)

    new_tokens = outputs[:, inputs["input_ids"].shape[1]:]
    description = processor.batch_decode(new_tokens, skip_special_tokens=True)[0]

    return description


def comment_from_summary(processor, model, summary: str, caption: str = None) -> str:
    """
    Generate a natural, human-like social media comment based on the image summary and optional user-provided caption.
    """
    # Build system instructions for style
    system = (
        "You are SocialMediaCommentBot – a friendly, enthusiastic commenter who writes in a casual social-media style. "
        "Your comments should:\n"
        "- Be 1–2 short sentences\n"
        "- Mention something specific you “see” or “feel” from the image or caption\n"
        "- Use 1–3 emojis to add warmth\n"
        "- Sound like a real person leaving a quick, positive note under a post\n\n"
        "Use up to 15 words and feel free to add emojis like someone commenting on a post."
    )

    # Build user content including caption if provided
    user_content = []
    if caption:
        user_content.append({"type": "text", "text": f"Caption: {caption}"})
    user_content.append({"type": "text", "text": f"Summary: {summary} , Leave a genuine, upbeat one-sentence reaction to this image for someone commenting on the post:"})

    # Compose messages
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content}
    ]

    # Prepare prompt
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)

    inputs = processor(text=prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=True,
        temperature=0.9,
        top_p=0.9,
        num_beams=1,
        no_repeat_ngram_size=2,
        eos_token_id=processor.tokenizer.eos_token_id
    )
    gen = outputs[:, inputs["input_ids"].shape[1]:]
    comment = processor.batch_decode(gen, skip_special_tokens=True)[0].strip()
    # Return only the first sentence
    return comment.split('\n')[0]


def commnet_genrater(image_path: str , caption: str = None) -> None:

    processor, model = load_model()
    img = Image.open(image_path).convert("RGB")
    summary = summarize_image(processor, model, img) 
    comment = comment_from_summary(processor, model, summary , caption)
    print("💬 Generated Comment:\n", comment)


    return comment





