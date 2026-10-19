import 'package:flutter/material.dart';

class VideoThumbnail extends StatelessWidget {
  final ImageProvider thumbnail;
  final String title;
  final VoidCallback onPlay;

  const VideoThumbnail({
    super.key,
    required this.thumbnail,
    required this.title,
    required this.onPlay,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: 'Play video: $title',
      child: GestureDetector(
        onTap: onPlay,
        child: Stack(
          alignment: Alignment.center,
          children: [
            Image(image: thumbnail, width: 320, height: 180, fit: BoxFit.cover),
            const Icon(Icons.play_circle_fill, size: 64, color: Colors.white),
          ],
        ),
      ),
    );
  }
}
