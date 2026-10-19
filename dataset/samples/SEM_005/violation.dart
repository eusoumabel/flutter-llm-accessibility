import 'package:flutter/material.dart';

class MuteButton extends StatelessWidget {
  final bool isMuted;
  final VoidCallback onToggle;

  const MuteButton({super.key, required this.isMuted, required this.onToggle});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(isMuted ? Icons.volume_off : Icons.volume_up),
      tooltip: 'Mute',
      onPressed: onToggle,
    );
  }
}
