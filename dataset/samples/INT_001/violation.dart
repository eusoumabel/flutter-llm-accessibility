import 'package:flutter/material.dart';

class TapTargetButton extends StatelessWidget {
  final VoidCallback onPressed;

  const TapTargetButton({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: SizedBox(width: 24, height: 24, child: Icon(Icons.check)),
    );
  }
}
