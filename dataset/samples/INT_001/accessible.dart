import 'package:flutter/material.dart';

class TapTargetButton extends StatelessWidget {
  final VoidCallback onPressed;

  const TapTargetButton({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: 'Submit',
      child: SizedBox(
        width: 48,
        height: 48,
        child: IconButton(
          icon: const Icon(Icons.check),
          onPressed: onPressed,
          tooltip: 'Submit',
        ),
      ),
    );
  }
}
