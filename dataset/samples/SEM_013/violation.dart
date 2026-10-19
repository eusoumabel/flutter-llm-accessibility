import 'package:flutter/material.dart';

class StarRating extends StatelessWidget {
  final int rating;
  final ValueChanged<int> onRatingChanged;

  const StarRating({
    super.key,
    required this.rating,
    required this.onRatingChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        for (var star = 1; star <= 5; star++)
          GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: () => onRatingChanged(star),
            child: SizedBox(
              width: 48,
              height: 48,
              child: Icon(
                star <= rating ? Icons.star : Icons.star_border,
                color: Colors.amber,
              ),
            ),
          ),
      ],
    );
  }
}
