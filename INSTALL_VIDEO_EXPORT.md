# 安装视频导出功能

## 问题
视频导出功能需要额外的库才能工作。

## 解决方案

在终端中运行以下命令：

```bash
cd /Users/siqi/Documents/PolyU/Sem1/SD5913/image2melody
pip install imageio imageio-ffmpeg
```

## 或者安装所有依赖

```bash
pip install -r requirements.txt
```

## 验证安装

安装完成后，运行以下命令验证：

```bash
python -c "import imageio; print('✓ imageio installed:', imageio.__version__)"
python -c "import imageio_ffmpeg; print('✓ imageio-ffmpeg installed')"
```

## 如果遇到问题

### 方法1: 使用 pip3
```bash
pip3 install imageio imageio-ffmpeg
```

### 方法2: 使用 python -m pip
```bash
python -m pip install imageio imageio-ffmpeg
```

### 方法3: 使用 conda (如果你用 Anaconda)
```bash
conda install -c conda-forge imageio imageio-ffmpeg
```

## 安装后

重新运行程序：
```bash
./run.sh
```

然后尝试导出视频功能，应该就可以正常工作了！

## 需要的库

- **imageio**: 用于视频编码
- **imageio-ffmpeg**: FFmpeg 编解码器支持

这两个库总大小约 20-30 MB。
