import 'package:flutter/material.dart';

class OpenProfileButton extends StatelessWidget {
  const OpenProfileButton({required this.onOpenProfile, super.key});

  final VoidCallback onOpenProfile;

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.account_circle),
      iconSize: 24,
      padding: const EdgeInsets.symmetric(
        horizontal: 16,
        vertical: 8,
      ),
      onPressed: onOpenProfile,
      tooltip: 'Open profile',
    );
  }
}
