import 'package:flutter/material.dart';

class CarouselControls extends StatelessWidget {
  final VoidCallback onPrevious;
  final VoidCallback onNext;

  const CarouselControls({
    super.key,
    required this.onPrevious,
    required this.onNext,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          tooltip: 'Previous image',
          onPressed: onPrevious,
        ),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          tooltip: 'Next image',
          onPressed: onNext,
        ),
      ],
    );
  }
}
