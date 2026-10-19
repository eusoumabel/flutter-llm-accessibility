import 'package:flutter/material.dart';

class RemovableFilter extends StatelessWidget {
  final String label;
  final VoidCallback onRemove;

  const RemovableFilter({super.key, required this.label, required this.onRemove});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.only(left: 12),
      decoration: BoxDecoration(
        color: Colors.blueGrey.shade50,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(label),
          IconButton(
            icon: const Icon(Icons.close),
            iconSize: 16,
            tooltip: 'Remove filter $label',
            onPressed: onRemove,
          ),
        ],
      ),
    );
  }
}
