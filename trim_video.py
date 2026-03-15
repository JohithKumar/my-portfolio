from PIL import Image

def trim_webp(input_file, output_file, start_frame):
    with Image.open(input_file) as im:
        frames = []
        for i in range(start_frame, getattr(im, "n_frames", 1)):
            im.seek(i)
            # Make sure we preserve duration
            dur = im.info.get("duration", 100)
            frame = im.copy()
            frame.info["duration"] = dur
            frames.append(frame)
            
        if frames:
            # Save the trimmed frames as a new animated webp
            frames[0].save(
                output_file,
                save_all=True,
                append_images=frames[1:],
                duration=[f.info["duration"] for f in frames],
                loop=0,
                format="WEBP",
                method=4, # tradeoff between speed and size
                quality=80
            )

if __name__ == "__main__":
    trim_webp("currency_converter_demo.webp", "currency_converter_demo_trimmed.webp", 364)
