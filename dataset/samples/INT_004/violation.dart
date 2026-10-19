import 'package:flutter/material.dart';

class PhotoPost extends StatelessWidget {
  final ImageProvider photo;
  final String author;
  final bool liked;
  final int likeCount;
  final VoidCallback onToggleLike;

  const PhotoPost({
    super.key,
    required this.photo,
    required this.author,
    required this.liked,
    required this.likeCount,
    required this.onToggleLike,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        GestureDetector(
          onDoubleTap: onToggleLike,
          child: Image(
            image: photo,
            semanticLabel: 'Photo by $author',
            fit: BoxFit.cover,
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(8),
          child: Text('$likeCount likes'),
        ),
      ],
    );
  }
}
