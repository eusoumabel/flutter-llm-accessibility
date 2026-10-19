import 'package:flutter/material.dart';

class AdvancedDetailsButton extends StatelessWidget {
  const AdvancedDetailsButton({
    required this.advanced,
    required this.onToggle,
    super.key,
  });

  final bool advanced;
  final VoidCallback onToggle;

  @override
  Widget build(BuildContext context) {
    return TextButton.icon(
      style: TextButton.styleFrom(foregroundColor: Theme.of(context).colorScheme.onSurface),
      onPressed: onToggle,
      icon: const Icon(Icons.info),
      label: Text(advanced ? 'Hide' : 'Advanced'),
    );
  }
}
