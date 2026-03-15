from PIL import Image
import itertools

def analyze_webp(filename):
    with open('analysis_output.txt', 'w') as f:
        with Image.open(filename) as im:
            f.write(f"Format: {im.format}, Size: {im.size}, Mode: {im.mode}\n")
            frames = getattr(im, "n_frames", 1)
            f.write(f"Total frames: {frames}\n")
            
            means = []
            for i in range(frames):
                im.seek(i)
                frame = im.convert("RGB")
                stat = frame.resize((1, 1)).getpixel((0, 0))
                dur = im.info.get("duration", 100)
                means.append((i, stat, dur))
                
            f.write("Frame samples (every 20th frame):\n")
            for i, stat, dur in means[::20]:
                f.write(f"Frame {i:3d}: RGB={stat}, duration={dur}ms\n")
                
            changes = []
            for j in range(1, len(means)):
                prev = means[j-1][1]
                curr = means[j][1]
                dist = sum((p - c) ** 2 for p, c in zip(prev, curr)) ** 0.5
                if dist > 30:
                    changes.append((j, dist))
                    
            f.write("\nMajor changes detected at frames:\n")
            for frame_idx, dist in changes:
                f.write(f"Frame {frame_idx:3d}: Dist={dist:.1f}\n")

if __name__ == "__main__":
    analyze_webp("currency_converter_demo.webp")
