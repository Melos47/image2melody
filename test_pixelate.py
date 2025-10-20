"""
测试像素化功能
"""
from image_processor import ImageProcessor
from PIL import Image

# 创建一个测试图像
def create_test_image():
    """创建一个简单的测试图像"""
    img = Image.new('RGB', (64, 64), color='white')
    pixels = img.load()
    
    # 创建一个彩色渐变
    for x in range(64):
        for y in range(64):
            r = int(255 * x / 64)
            g = int(255 * y / 64)
            b = 128
            pixels[x, y] = (r, g, b)
    
    img.save('test_image.png')
    print("✅ Created test image: test_image.png")
    return 'test_image.png'

# 测试像素化
def test_pixelate():
    print("\n🎨 Testing Pixelation Feature\n")
    print("=" * 50)
    
    # 创建测试图像
    test_img_path = create_test_image()
    
    # 初始化处理器
    processor = ImageProcessor(pixel_size=8)
    
    # 像素化图像
    print("\n🔧 Pixelating image with 8x8 blocks...")
    rgb_data, pixelated_img = processor.extract_rgb_from_pixelated(test_img_path, pixel_size=8)
    
    # 保存像素化图像
    pixelated_img.save('test_pixelated.png')
    print(f"✅ Saved pixelated image: test_pixelated.png")
    
    # 显示结果
    print(f"\n📊 Results:")
    print(f"   - Total pixel blocks: {len(rgb_data)}")
    print(f"   - Pixelated image size: {pixelated_img.size}")
    print(f"   - Grid dimensions: {pixelated_img.size[0] // 8} x {pixelated_img.size[1] // 8}")
    
    # 显示前10个像素块的RGB值
    print(f"\n🎨 First 10 pixel block colors:")
    for i, (r, g, b) in enumerate(rgb_data[:10], 1):
        print(f"   Block {i}: R={r:3d}, G={g:3d}, B={b:3d}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("\nYou can now:")
    print("1. Check test_image.png (original)")
    print("2. Check test_pixelated.png (pixelated with 8x8 blocks)")

if __name__ == "__main__":
    test_pixelate()
