# Example: How to use the Image to 8-bit Melody Converter

from image_processor import ImageProcessor
from melody_generator import MelodyGenerator

# Initialize modules
image_proc = ImageProcessor(sample_rate=32)
melody_gen = MelodyGenerator()

# Process an image
image_path = "your_image.jpg"
rgb_data = image_proc.extract_rgb_data(image_path)

# Generate melody from RGB data
notes, info = melody_gen.generate_melody(rgb_data)

# Save as MIDI file
melody_gen.save_midi("output.mid")

# Play the melody
melody_gen.play_melody()

print("Melody generated successfully!")
print(info)
